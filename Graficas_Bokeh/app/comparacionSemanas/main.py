import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Div, HoverTool, FactorRange
from bokeh.transform import dodge
from bokeh.layouts import column
from bokeh.io import curdoc
from os.path import dirname, join

# 📌 Cargar descripción del HTML
desc = Div(text=open(join(dirname(__file__), "grafico.html")).read(), sizing_mode="stretch_width")

# 📌 Cargar datos desde CSV
csv_one_path = r"../../../CSVs/UTPL_CREAA1_2024_2_grade_report_2024-11-08-2038.csv"
csv_two_path = r"../../../CSVs/UTPL_CREAA1_2024_2_grade_report_2024-12-02-1435.csv"
csv_three_path = r"../../../CSVs/UTPL_CREAA1_2024_2_grade_report_2025-02-12-2116.csv"

data1 = pd.read_csv(csv_one_path, delimiter=',')
data2 = pd.read_csv(csv_two_path, delimiter=',')
data3 = pd.read_csv(csv_three_path, delimiter=',')

# 📌 Definir puntaje mínimo
puntaje_minimo = 0.7  

# 📌 Función para contar aprobados y reprobados
def contar_aprobados_reprobados(data):
    aprobados = data[data["EvalSemanal Avg"] >= puntaje_minimo].shape[0]
    reprobados = data[data["EvalSemanal Avg"] < puntaje_minimo].shape[0]
    return aprobados, reprobados

# 📌 Crear estructura de datos para el gráfico
csv_names = ["CSV 1", "CSV 2", "CSV 3"]
aprobados_list = []
reprobados_list = []

for data in [data1, data2, data3]:
    aprobados, reprobados = contar_aprobados_reprobados(data)
    aprobados_list.append(aprobados)
    reprobados_list.append(reprobados)

# 📌 Crear `ColumnDataSource` con **una sola entrada por CSV**
source = ColumnDataSource(data=dict(
    CSV=csv_names,
    Aprobados=aprobados_list,
    Reprobados=reprobados_list
))

# 📊 **Gráfico de Barras Agrupadas**
p = figure(
    x_range=FactorRange(*csv_names),  # Solo CSVs en el eje X
    title="Cantidad de Estudiantes Aprobados y No Aprobados por CSV",
    x_axis_label="Archivo CSV",
    y_axis_label="Cantidad",
    width=700,
    height=500
)

# 📌 Graficar barras con desplazamiento `dodge`
barra_aprobados = p.vbar(
    x=dodge("CSV", -0.2, range=p.x_range),  
    top="Aprobados",
    width=0.35, 
    source=source,
    color="#2ca02c",  # Verde
    legend_label="Aprobados"
)

barra_reprobados = p.vbar(
    x=dodge("CSV", 0.2, range=p.x_range),  
    top="Reprobados",
    width=0.35, 
    source=source,
    color="#d62728",  # Rojo
    legend_label="Reprobados"
)

# 📌 Agregar herramientas de hover
hover_aprobados = HoverTool(
    renderers=[barra_aprobados],
    tooltips=[("Estado", "Aprobados"), ("Cantidad", "@Aprobados"), ("CSV", "@CSV")]
)

hover_reprobados = HoverTool(
    renderers=[barra_reprobados],
    tooltips=[("Estado", "Reprobados"), ("Cantidad", "@Reprobados"), ("CSV", "@CSV")]
)

p.add_tools(hover_aprobados, hover_reprobados)

# 📌 Configurar leyenda y formato del eje X
p.legend.title = "Estado"
p.legend.location = "top_right"
p.xgrid.grid_line_color = None
p.xaxis.major_label_orientation = 1.2  # Inclinar etiquetas

# 📌 Agregar al documento
curdoc().add_root(column(desc, p))
