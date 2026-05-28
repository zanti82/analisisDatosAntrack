import pandas as pd
import ast




# Cargar un archivo CSV
df = pd.read_csv('data/raw/datos_gasto.csv')

print(f"\n✅ Dataset cargado: {df.shape[0]} filas × {df.shape[1]} columnas")
print("\n📋 Primeras 5 filas:")
print(df.head().to_string(index=False))
print("\n📊 Tipos de datos:")
print(df.dtypes)
print("\n🔍 Valores nulos por columna:")
print(df.isnull().sum())
print(f"Duplicados totales: {df.duplicated().sum()}")

# ─────────────────────────────────────────────────────────────
# 2. LIMPIEZA Y TRANSFORMACIÓN
# ─────────────────────────────────────────────────────────────
print("\n🧹 PASO 2: Limpiando y transformando datos...")

#columanas nuevas convietiendo datos string a diccinoarios

# ast convierte
df['categoria'] = df['categoria'].apply(ast.literal_eval)
df['metodoPago'] = df['metodoPago'].apply(ast.literal_eval)
df['comercio'] = df['comercio'].apply(ast.literal_eval)
df['usuario'] = df['usuario'].apply(ast.literal_eval)

# nuevas columnas el lamba ayuda  a relaizr operaciones rapidas
df['categoria_nombre'] = df['categoria'].apply(lambda x: x['nombre'])
df['forma_pago'] = df['metodoPago'].apply(lambda x: x['formaPago'])
df['comercio_nombre'] = df['comercio'].apply(lambda x: x['nombreComercio'])
df['usuario_nombre'] = df['usuario'].apply(lambda x: x['nombre'])

# fechas con mixed, por error de datos, venian mexcladas sin milisegindos
df['fecha'] = pd.to_datetime(df['fecha'], format='mixed')

df['mes'] = df['fecha'].dt.month_name()
df['dia'] = df['fecha'].dt.day_name()

#revisamos las 10 priemras entradas
print(df.head(10))


df.to_csv('data/processed/datos_GastoFinal.csv', index=False)
print("¡Archivo depurado guardado con éxito en la carpeta processed!")



#organizamos los datos de mayor a menor por valor de gasto

df_final = df.sort_values(by='valor', ascending=False)

print(df_final.head(10))

#y mirmaos la suam de cada ususario por nombre

gastos_por_usuario = df_final.groupby(
    ['usuario_nombre']
)['valor'].sum().sort_values(ascending=False)

print("\n📊 gastos totales por usuarios:")
print(gastos_por_usuario)





