import os
from bs4 import BeautifulSoup
import requests
import time
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns

#paso2
header = {'User-Agent': 'my-app/0.0.1'}
resource_url = "https://en.wikipedia.org/wiki/List_of_Spotify_streaming_records"
response = requests.get(resource_url, time.sleep(3), headers= header)
response

#paso3
if response:
    soup = BeautifulSoup(response.text, 'html.parser')
    tables = pd.read_html(str(soup))
df = tables[0]
df.head()

#paso4
df['Streams (billions)'] = pd.to_numeric(df['Streams (billions)'], errors='coerce')
df['Release date'] = pd.to_datetime(df['Release date'], errors ='coerce')
df = df.dropna(subset=['Streams (billions)', 'Release date'])
df['Release date'] = df['Release date'].dt.strftime('%d/%m/%Y')
df = df.drop(columns=['Ref.'])
df

#Paso 5
dfsql = sqlite3.connect('spotify_top_canciones.db')
df.to_sql('mas_sonados', dfsql, if_exists = 'replace', index= False)
cursor = dfsql.cursor()
dfsql.commit()
#dfsql.close()

#Paso 6. Mostrar los resultados
cursor.execute("SELECT * FROM mas_sonados")
result = cursor.fetchall()
for row in result:
    print(row)

#Preparar los datos para la visualización
df_top10 = df.sort_values(by='Streams (billions)', ascending=False).head(10)
df_top10['Streams (billions)'].dtype
df_top10

#Paso 6. Gráfico de barras con Matplotlip i Seaborn
plt.figure(figsize=(8,5))
sns.barplot(x='Song', y='Streams (billions)', data= df_top10, palette='viridis')
plt.title('Top 10 songs with more streams')
plt.xlabel('Songs')
plt.ylabel('Streams(billions)')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

#Paso 6. Gráfico de líneas para ver como evolucionan los streams según las fechas de lanzamiento.
df['Streams (billions)'] = df['Streams (billions)'].astype(float)

df['Release date'] = pd.to_datetime(df['Release date'], dayfirst=True)
df_time_sorted = df.sort_values(by='Release date', ascending=False).head(10)

plt.figure(figsize=(10,6))
plt.plot(df_time_sorted['Release date'], df_time_sorted['Streams (billions)'], marker='o', linestyle='-')
plt.title('Streams over release year')
plt.xlabel('Release date')
plt.ylabel('Streams (billions)')
plt.grid(True)
plt.xticks(rotation=45)

for i, song in enumerate(df_time_sorted['Song']):
    plt.annotate(song, (df_time_sorted['Release date'].iloc[i], df_time_sorted['Streams (billions)'].iloc[i]), fontsize=8, rotation= 45)

plt.margins(x=0.1, y=0.13)
plt.tight_layout()
plt.show()