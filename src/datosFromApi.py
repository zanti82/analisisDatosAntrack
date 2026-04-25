import pandas as pd
import requests
from datetime import datetime



#petición a la API
url = "http://localhost:8080/anttrackapi/v1/gastos"  
response = requests.get(url)

# Verificamos que la petición fue exitosa
if response.status_code == 200:
    datos = response.json()  
    print(f"Se obtuvieron {len(datos)} registros")
else:
    print(f"Error: {response.status_code}")
    datos = []

# 3. Convertir a DataFrame
df = pd.DataFrame(datos)

# 4. Mostrar las primeras filas
print(df.head())


carpeta_raw = 'data/raw'
#cambiamos el nombre y la direcion api para guardar datos
df.to_csv(f'{carpeta_raw}/datos_Gastos.csv', index=False)

