import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool, Div
from bokeh.layouts import column, row
from bokeh.io import curdoc
from bokeh.palettes import Spectral4
from funciones import *
from math import pi
from bokeh.transform import cumsum

# Para la dirección del HTML
from os.path import dirname, join

# 📁 Rutas a los archivos
json_ed1 = "../../Jsonl/course-creaaa1/course-creaaa1-limpio.json"
json_ed2 = "../../Jsonl/course-v1_/course-v1_UTPL_CREAA2limpio.json"
csv_ed1 = "../../CSVs/Unificar Oct-Nov24/UTPL_CREAA1_2024_2_grade_report_2025-02-12-2116.csv"
csv_ed2 = "../../CSVs/Unificar Abr-Jun25/Curso accesibilidad/UTPL_CREAA2_2025_1_grade_report_2025-05-19-2109.csv"

# HTMLs
desc = Div(text=open(join(dirname(__file__), "html/primeraP.html")).read(), sizing_mode="stretch_width")
desc2 = Div(text=open(join(dirname(__file__), "html/segundaP.html")).read(), sizing_mode="stretch_width")

# 📺 Mapeo código a nombre para los videos
codigo_a_nombre = {
    "LR_1_Video1_Semana1": "U3cK1QMIIEQ",
    "LR_1_Video2_Semana1": "9aNQZ9dKXRY",
    "LR_1_Video3_Semana1": "lsNxh-lSpCY",
    "LR_1_Video4_Semana1": "C3LnEvN0qZ0",
    "LR_1_Video5_Semana1": "vbpbkQE5K_Q",
    "LR_1_Video6_Semana1": "zCFa0xjGXGQ",
    "LR_1_Video7_Semana1": "qlS7ShZfb-c",
    "LR_1_Video8_Semana1": "8cKRb9CKtxk",
    "LR_1_Video9_Semana1": "WyrfIZ6VBcM",
    "LR_1_Video10_Semana1": "NgUhK3rw1IE",
    "LR_1_Video11_Semana1": "ttP0EyzSbbo",
    "LR_1_Video12_Semana1": "Vy4FWDyjZo4",
    "LR_1_Video1_Semana2": "o5VwDVJ7N3Q",
    "LR_1_Video2_Semana2": "LluqYlh2xg4",
    "LR_1_Video3_Semana2": "eE658thjDj8",
    "LR_1_Video4_Semana2": "QbEpClHzTeM",
    "LR_1_Video5_Semana2": "MCG0or2ULB4",
    "LR_1_Video6_Semana2": "ol-vGTdHBNU",
    "LR_1_Video7_Semana2": "WTXS0IMQ3Ss",
    "LR_1_Video8_Semana2": "9kqXmM3b3wc"
}
nombre_a_codigo = {v: k for k, v in codigo_a_nombre.items()}

# 📊 Cargar datos de JSON y CSV
json1_df = cargar_json(json_ed1)
json2_df = cargar_json(json_ed2)
df_ed1 = pd.read_csv(csv_ed1)
df_ed2 = pd.read_csv(csv_ed2)

# 📈 Calcular usuarios únicos por video (play_video)
ed1_usuarios = contar_usuarios_unicos_por_video(json1_df)
ed2_usuarios = contar_usuarios_unicos_por_video(json2_df)

# 📈 Datos para gráfico de líneas
df_linea = preparar_datos_linea(ed1_usuarios, ed2_usuarios, nombre_a_codigo)
source_linea = ColumnDataSource(df_linea)

# print(source_linea.data)

# 🎯 Crear gráfico de líneas
p_lineas = figure(
    x_range=df_linea["Video"],
    title="Usuarios únicos por Video (Comparación Ediciones)",
    x_axis_label="Video",
    y_axis_label="Usuarios Únicos",
    width=1100,
    height=400,
    toolbar_location="above",
    tools="pan,wheel_zoom,box_zoom,reset,save"
)

p_lineas.add_tools(
    HoverTool(tooltips=[("Video", "@Video"), ("Edición 1", "@{Edición 1}"), ("Edición 2", "@{Edición 2}")], 
            show_arrow=False,
            point_policy='follow_mouse'))

p_lineas.line(x="Video", y="Edición 1", source=source_linea, line_width=2, color=Spectral4[0], legend_label="Edición 1")
p_lineas.line(x="Video", y="Edición 2", source=source_linea, line_width=2, color=Spectral4[1], legend_label="Edición 2")

p_lineas.circle(x="Video", y="Edición 1", source=source_linea, size=6, color=Spectral4[0])
p_lineas.circle(x="Video", y="Edición 2", source=source_linea, size=6, color=Spectral4[1])

p_lineas.xaxis.major_label_orientation = pi / 2
p_lineas.legend.location = "top_left"
p_lineas.legend.click_policy="mute"


# 🎯 Datos de pastel para Edición 1 (EvalSemanal Avg + FormAutoevaluacion Avg)
ap1, rep1 = calcular_estado_aprobacion(df_ed1, ["EvalSemanal Avg", "FormAutoevaluacion Avg"])
data_pie1 = generar_pie_data(ap1, rep1)
source_pie1 = ColumnDataSource(data_pie1)

p_pastel1 = figure(title="Edición 1 - Aprobados vs Reprobados", width=400, height=400)

p_pastel1.add_tools(
    HoverTool(tooltips=[("Porcentaje", "@Porcentaje{0.0%}"), ("Estado:", "@Estado"), ("Cantidad", "@Cantidad"),], 
            show_arrow=False,
            point_policy='follow_mouse'))

p_pastel1.wedge(x=0, y=0, radius=0.8,
    start_angle=cumsum("angle", include_zero=True), end_angle=cumsum("angle"),
    line_color="white", fill_color="color", legend_field="Estado", source=source_pie1)
p_pastel1.axis.visible = False
p_pastel1.grid.grid_line_color = None

# 🎯 Datos de pastel para Edición 2 (promedio de 3 columnas)
ap2, rep2 = calcular_estado_aprobacion(df_ed2, ["EvalSemanal 01", "EvalSemanal 02", "EvalSemanal 03"])
data_pie2 = generar_pie_data(ap2, rep2)
source_pie2 = ColumnDataSource(data_pie2)

p_pastel2 = figure(title="Edición 2 - Aprobados vs Reprobados", width=400, height=400)

p_pastel2.add_tools(
    HoverTool(tooltips=[("Porcentaje", "@Porcentaje{0.0%}"), ("Estado:", "@Estado"), ("Cantidad", "@Cantidad"),], 
            show_arrow=False,
            point_policy='follow_mouse'
            ))

p_pastel2.wedge(x=0, y=0, radius=0.8,
    start_angle=cumsum("angle", include_zero=True), end_angle=cumsum("angle"),
    line_color="white", fill_color="color", legend_field="Estado", source=source_pie2)
p_pastel2.axis.visible = False
p_pastel2.grid.grid_line_color = None

'''
#################################
    OTRAS GRAFICAS
#################################
'''

# Cargar CSVs
df_ed1 = pd.read_csv(csv_ed1)
df_ed2 = pd.read_csv(csv_ed2)

actividad_df_completo = preparar_dataframe_conjunto(df_ed1, df_ed2, excluir_ceros=False)
actividad_df_sin_ceros = preparar_dataframe_conjunto(df_ed1, df_ed2, excluir_ceros=True)

# 🧩 Layout final
layout = column(desc,
    row(p_pastel1, p_pastel2),
    p_lineas,
    desc2,
    generar_graficas(actividad_df_completo, "(incluyendo estudiantes con nota 0)"),
    generar_graficas(actividad_df_sin_ceros, "(excluyendo estudiantes con nota 0)")
)

curdoc().add_root(layout)
curdoc().title = "Comparación Ediciones"
