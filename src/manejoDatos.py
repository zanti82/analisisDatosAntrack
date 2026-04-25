import pandas as pd
import ast




# Cargar un archivo CSV
df_gastos = pd.read_csv('data/raw/datos_Gastos.csv')

#Muestra el tipo de datos de cada columna y si hay valores nulos
print(df_gastos.info())

#df.describe(): #Estadisticos descriptivos (media, max, min) para columnas numéricas
print(f'\n Los datos estadisticos son {df_gastos.describe()}')

#Detección de nulos
# Contar cuántos nulos hay por columna
print(f'Nulos por columnas: {df_gastos.isna().sum()}')

# Verificar si hay filas idénticas
print(f"Duplicados totales: {df_gastos.duplicated().sum()}")

#traemos usuarios y comercio
df_usuarios = pd.read_csv('data/raw/datos_Usuarios.csv')
df_categorias = pd.read_csv('data/raw/datos_Categorias.csv')

#Buscamos columans id
print(df_gastos.columns)
print(df_usuarios.columns)
print(df_categorias.columns)

#cambaiamos nobres de columnas para merger

print(df_gastos.columns)

##mereg gastos con ususarios y categorias

df = df_gastos.merge(
    df_usuarios[['id', 'nombre', 'documento']],
    left_on='id',
    right_on='id',
    how='left'
)

df = df.merge(
    df_categorias[['id', 'nombre']],
    left_on='id',
    right_on='id',
    how='left'
)

print(df.columns)

# dejamos la base de datos final y la guardamos
df_final = df[[
    'id', 
    'descripcion',
    'categoria',
    'usuario',           
    'documento',        
    'valor', 
    'fecha'
]]



df.to_csv('data/processed/datos_GastoFinal.csv', index=False)
print("¡Archivo depurado guardado con éxito en la carpeta processed!")

print(df_final)

#organizamos los datos de mayor a meno por avlor de gasto

df_final = df_final.sort_values(by='valor', ascending=False)

print(df_final.head(10))

#y mirmaos la suam de cada ususario por docuemnto poerque por nombre nos trae un dicc.

gastos_por_usuario = df_final.groupby(
    ['documento']
)['valor'].sum().sort_values(ascending=False)

print(gastos_por_usuario)



