import pandas as pd
import os

# Solamente cambiar las rutas relativas para poder acceder al documento alojado en cada carpeta.
# Rutas de los archivos CSV
csv_profile_path = r"CSVs/Unificar Abr-Jun25 Nuevo/UTPL_CREAA2_2025_1_student_profile_info_2025-06-16-0027.csv"
csv_grade_path = r"CSVs/Unificar Abr-Jun25 Nuevo/UTPL_CREAA2_2025_1_grade_report_2025-06-16-0027.csv"
csv_niu = r"CSVs/Unificar Abr-Jun25 Nuevo/Reporte CursoAccesActual.csv"


# Verificar si los archivos existen
if not os.path.exists(csv_profile_path) or not os.path.exists(csv_grade_path):
    print("⚠️ Error: Uno o ambos archivos no existen.")
    exit()

try:
    # Cargar ambos CSVs
    df1 = pd.read_csv(csv_profile_path)
    df2 = pd.read_csv(csv_grade_path)

    # Definir claves comunes para unir los archivos
    claves_comunes = ["id", "username", "email"]

    # Fusionar 
    df_combined = pd.merge(df1, df2, on=claves_comunes, how="outer")  # Usa "outer" para no perder datos

    # Reemplazar celdas vacías
    df_combined.fillna("N/A", inplace=True)

    # Lista de usuarios a eliminar
    usuarios_excluir = ["VeronicaLuna", "NahomiCabrera", "opencampus", "reroes3100", "ElizabethCadme"]

    # Filtrar para eliminar esos usuarios
    df_combined = df_combined[~df_combined["username"].isin(usuarios_excluir)]

    # Guardar el CSV unificado
    df_combined.to_csv(csv_niu, index=False)

    print(f"CSV nuevo guardado!")

except Exception as e:
    print(f" Error al procesar los archivos: {e}")