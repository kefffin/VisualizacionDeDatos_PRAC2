import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from wordcloud import WordCloud  # Para crear las nubes de palabras
import squarify  # Para diagramas de árbol
import plotly.express as px
import plotly.graph_objects as go
from ipywidgets import interact, Dropdown

data = pd.read_csv("data/NYPD_Hate_Crimes.csv", sep=",")

data['Record Create Date'] = pd.to_datetime(data['Record Create Date'])
data['Arrest Date'] = pd.to_datetime(data['Arrest Date'])
print(data['Record Create Date'].dtype)
print(data['Arrest Date'].dtype)

# Se añade la columna Boroughs (distrito) al dataframe para posteriores visualizaciones
data.loc[data['County'] == 'BRONX', 'Boroughs'] = 'BRONX'
data.loc[data['County'] == 'KINGS', 'Boroughs'] = 'BROOKLYN'
data.loc[data['County'] == 'NEW YORK', 'Boroughs'] = 'MANHATTAN'
data.loc[data['County'] == 'QUEENS', 'Boroughs'] = 'QUEENS'
data.loc[data['County'] == 'RICHMOND', 'Boroughs'] = 'STATEN ISLAND'

# Se añade la columna Month Year (Mes-Año) al dataframe
data['Month Year'] = data.apply(lambda row: str(row['Month Number']) + '-' + str(row['Complaint Year Number']), axis=1)

# Se añade la columna Year Month (Año-Mes) al dataframe
data['Year Month'] = data.apply(lambda row: str(row['Complaint Year Number']) + '-' + str(row['Month Number']).zfill(2),
                                axis=1)

# Se ordena el dataframe en un nuevo dataframe por las columnas 'Complaint Year Number' y 'Month Number'
data_ordenado = data.sort_values(by=['Complaint Year Number', 'Month Number'])

# Dataframe que muestra la frecuencia de denuncias por crímenes de odio a lo largo de los meses y los años
# Se subdivide el dataframe original en nuevos dataframes por Categoría de Ofensa para posteriores visualizaciones
# También se agrupan por Mes y año
data_religion = data.loc[data['Offense Category'] == 'Religion/Religious Practice']
data_etnia = data.loc[data['Offense Category'] == 'Ethnicity/National Origin/Ancestry']
data_raza = data.loc[data['Offense Category'] == 'Race/Color']
data_genero = data.loc[data['Offense Category'] == 'Gender']
data_orientacions = data.loc[data['Offense Category'] == 'Sexual Orientation']

data_religion_grouped = data_religion.groupby(
    ['Complaint Year Number', 'Month Number', 'Year Month']).size().reset_index(name='count')
data_etnia_grouped = data_etnia.groupby(['Complaint Year Number', 'Month Number', 'Year Month']).size().reset_index(
    name='count')
data_raza_grouped = data_raza.groupby(['Complaint Year Number', 'Month Number', 'Year Month']).size().reset_index(
    name='count')
data_genero_grouped = data_genero.groupby(['Complaint Year Number', 'Month Number', 'Year Month']).size().reset_index(
    name='count')
data_orientacions_grouped = data_orientacions.groupby(
    ['Complaint Year Number', 'Month Number', 'Year Month']).size().reset_index(name='count')

df_unido_anio_ofensa = pd.merge(data_religion_grouped, data_etnia_grouped,
                                on=['Complaint Year Number', 'Month Number', 'Year Month'], how='outer',
                                suffixes=('_df1', '_df2'))
df_unido_anio_ofensa = pd.merge(df_unido_anio_ofensa, data_raza_grouped,
                                on=['Complaint Year Number', 'Month Number', 'Year Month'], how='outer',
                                suffixes=('_df12', '_df3'))
df_unido_anio_ofensa = pd.merge(df_unido_anio_ofensa, data_genero_grouped,
                                on=['Complaint Year Number', 'Month Number', 'Year Month'], how='outer',
                                suffixes=('_df123', '_df4'))
df_unido_anio_ofensa = pd.merge(df_unido_anio_ofensa, data_orientacions_grouped,
                                on=['Complaint Year Number', 'Month Number', 'Year Month'], how='outer',
                                suffixes=('_df1234', '_df5'))

df_unido_anio_ofensa.columns = ['Complaint Year Number', 'Month Number', 'Year Month', 'Religion/Religious Practice',
                                'Ethnicity/National Origin/Ancestry', 'Race/Color', 'Gender', 'Sexual Orientation']

# Se ordena el dataframe en un nuevo dataframe por las columnas 'Complaint Year Number' y 'Month Number'
df_unido_anio_ofensa = df_unido_anio_ofensa.sort_values(by=['Complaint Year Number', 'Month Number'])

# Se transforman los nulos a 0 y se muestra el resultado
df_unido_anio_ofensa.fillna(0, inplace=True)

# Se obtiene una pequeña muestra para su visualización
print(df_unido_anio_ofensa.head(5))

# Se subdivide por Distrito y se agrupa de acuerdo a la Categoría de Ofensa

data_bronx = data.loc[data['Boroughs'] == 'BRONX']
data_kings = data.loc[data['Boroughs'] == 'BROOKLYN']
data_newyork = data.loc[data['Boroughs'] == 'MANHATTAN']
data_queens = data.loc[data['Boroughs'] == 'QUEENS']
data_richmond = data.loc[data['Boroughs'] == 'STATEN ISLAND']

data_bronx_grouped = data_bronx.groupby(['Month Year', 'Offense Category']).size().reset_index(name='count')
data_kings_grouped = data_kings.groupby(['Month Year', 'Offense Category']).size().reset_index(name='count')
data_newyork_grouped = data_newyork.groupby(['Month Year', 'Offense Category']).size().reset_index(name='count')
data_queens_grouped = data_queens.groupby(['Month Year', 'Offense Category']).size().reset_index(name='count')
data_richmond_grouped = data_richmond.groupby(['Month Year', 'Offense Category']).size().reset_index(name='count')

df_unido_ofensa_distrito = pd.merge(data_bronx_grouped, data_kings_grouped, on=['Month Year', 'Offense Category'],
                                    how='outer', suffixes=('_df1', '_df2'))
df_unido_ofensa_distrito = pd.merge(df_unido_ofensa_distrito, data_newyork_grouped,
                                    on=['Month Year', 'Offense Category'], how='outer', suffixes=('_df12', '_df3'))
df_unido_ofensa_distrito = pd.merge(df_unido_ofensa_distrito, data_queens_grouped,
                                    on=['Month Year', 'Offense Category'], how='outer', suffixes=('_df123', '_df4'))
df_unido_ofensa_distrito = pd.merge(df_unido_ofensa_distrito, data_richmond_grouped,
                                    on=['Month Year', 'Offense Category'], how='outer', suffixes=('_df1234', '_df5'))

df_unido_ofensa_distrito.columns = ['Month Year', 'Offense Category', 'Bronx', 'Brooklyn', 'Manhattan', 'Queens',
                                    'Staten Island']

# Se transforman los nulos a 0 y se muestra el resultado
df_unido_ofensa_distrito.fillna(0, inplace=True)
print(df_unido_ofensa_distrito)

# ANALISIS

# Obtener los datos de la columna "Offense Category"
offense_category = data['Offense Category'].value_counts()

# Obtener los dos primeros valores y la suma del resto de valores
top_categories = offense_category[:4]
other_categories = offense_category[4:].sum()

# Crear un diccionario con los datos
data_dict = {
    "Top Categories": top_categories.values.tolist() + [other_categories],
    "Category": top_categories.index.tolist() + ["Others"]
}

# Establecer la paleta de colores
sns.set_palette('pastel')

# Crear el gráfico de pastel
plt.figure(figsize=(8, 8))
plt.pie(data_dict["Top Categories"], labels=data_dict["Category"], autopct='%1.1f%%', startangle=90,
        colors=sns.color_palette())

# Mostrar leyenda fuera del gráfico
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

# Mostrar el gráfico
#plt.show()

zz = pd.DataFrame.from_dict(data_dict)
zz.to_csv("data_queso_1.csv", index=False)


# ¿Cómo ha evolucionado la frecuencia de los crímenes de odio a lo largo de los años?

data_count = data.groupby(['Complaint Year Number', 'Month Number', 'Month Year'])['County'].count().reset_index(name='Contador')
data_count = data_count.sort_values(['Complaint Year Number', 'Month Number', 'Month Year'])
plt.figure(figsize=(28,12))
my_palette = sns.color_palette('pastel', 7)
sns.histplot(x='Month Year', data=data_ordenado, hue='Offense Category', multiple='stack', palette=my_palette)

sns.lineplot(x='Month Year', y='Contador', data=data_count)
plt.xticks(rotation=-45)  # Rotamos las etiquetas para que no se solapen
plt.show()

data_count.to_csv("data_count.csv", index=False)

religion_crimes = data_ordenado.loc[data_ordenado['Offense Category'] == 'Religion/Religious Practice']
count_religion = religion_crimes.groupby(['Complaint Year Number', 'Month Number', 'Month Year'])['Offense Category'].count().reset_index(name='Contador')
count_religion = count_religion.sort_values(by=['Complaint Year Number', 'Month Number'])

religion_crimes.to_csv("religion_crimes.csv", index=False)

race_color_crimes = data_ordenado.loc[data_ordenado['Offense Category'] == 'Race/Color']
count_race_color = race_color_crimes.groupby(['Complaint Year Number', 'Month Number', 'Month Year'])['Offense Category'].count().reset_index(name='Contador')
count_race_color = count_race_color.sort_values(by=['Complaint Year Number', 'Month Number'])

race_color_crimes.to_csv("race_color_crimes.csv", index=False)

sexual_orientation_crimes = data_ordenado.loc[data_ordenado['Offense Category'] == 'Sexual Orientation']
count_sexual_orientation = sexual_orientation_crimes.groupby(['Complaint Year Number', 'Month Number', 'Month Year'])['Offense Category'].count().reset_index(name='Contador')
count_sexual_orientation = count_sexual_orientation.sort_values(by=['Complaint Year Number', 'Month Number'])


sexual_orientation_crimes.to_csv("sexual_orientation_crimes.csv", index=False)

ethnicity_crimes = data_ordenado.loc[data_ordenado['Offense Category'] == 'Ethnicity/National Origin/Ancestry']
count_ethnicity = ethnicity_crimes.groupby(['Complaint Year Number', 'Month Number', 'Month Year'])['Offense Category'].count().reset_index(name='Contador')
count_ethnicity = count_ethnicity.sort_values(by=['Complaint Year Number', 'Month Number'])

ethnicity_crimes.to_csv("ethnicity_crimes.csv", index=False)

gender_crimes = data_ordenado.loc[data_ordenado['Offense Category'] == 'Gender']
count_gender = gender_crimes.groupby(['Complaint Year Number', 'Month Number', 'Month Year'])['Offense Category'].count().reset_index(name='Contador')
count_gender = count_gender.sort_values(by=['Complaint Year Number', 'Month Number'])

gender_crimes.to_csv("gender_crimes.csv", index=False)
data_ordenado.to_csv("data_ordenado.csv", index=False)

df_crimenes_odio = df_unido_anio_ofensa[['Year Month', 'Religion/Religious Practice', 'Ethnicity/National Origin/Ancestry', 'Race/Color', 'Gender', 'Sexual Orientation']].groupby(by='Year Month').sum()
df_crimenes_odio.to_csv("df_crimenes_odio.csv", index=False)

df_subcategories = data.groupby(['Offense Category', 'Bias Motive Description']).size().reset_index(name='counts')
df_subcategories.to_csv("df_subcategories.csv", index=False)

data_offense_year = pd.DataFrame(columns=data['Offense Description'].unique())
for column in data_offense_year:
  data_offense_year[column] = data[data['Offense Description'] == column].groupby(by=['Complaint Year Number']).count()['Offense Category']
data_offense_year

data_offense_year.to_csv("data_offense_year.csv", index=False)

crime_county = data['Boroughs'].value_counts()
crime_county.to_csv("crime_county.csv", index=False)
offense_county = data['Offense Description'].value_counts()[:10]
offense_county.to_csv("offense_county.csv", index=False)