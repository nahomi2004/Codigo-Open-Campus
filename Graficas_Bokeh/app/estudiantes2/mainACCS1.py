import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Div, HoverTool
from bokeh.palettes import Pastel1, Bokeh
from bokeh.transform import factor_cmap, cumsum, dodge
from bokeh.layouts import column, row
from bokeh.io import output_file, show, curdoc
from math import pi

# Para la dirección del HTML
from os.path import dirname, join

desc0 = Div(text=open(join(dirname(__file__), "TituloACCS1.html")).read(), sizing_mode="stretch_width")
desc = Div(text=open(join(dirname(__file__), "graficoBarras.html")).read(), sizing_mode="stretch_width")
desc2 = Div(text=open(join(dirname(__file__), "graficoPastel.html")).read(), sizing_mode="stretch_width")
desc3 = Div(text=open(join(dirname(__file__), "graficaGeneral.html")).read(), sizing_mode="stretch_width")
desc4 = Div(text=open(join(dirname(__file__), "graficoPastelPorcentaje.html")).read(), sizing_mode="stretch_width")

# herramientas = "hover,pan,wheel_zoom,box_zoom,reset,save"

# Cargar los archivos CSV
csv_profile_path = r"../../../CSVs/Unificar Oct-Nov24/UTPL_CREAA1_2024_2_student_profile_info_2025-02-12-2117.csv"
csv_grade_path = r"../../../CSVs/Unificar Oct-Nov24/UTPL_CREAA1_2024_2_grade_report_2025-02-12-2116.csv"

dataProfile = pd.read_csv(csv_profile_path, delimiter=',')
dataGrade = pd.read_csv(csv_grade_path, delimiter=',')

curdoc().add_root(column(desc0))

# Unir los CSVs por "username"
data = pd.merge(dataProfile, dataGrade, on="username")
data["gender"] = data["gender"].fillna("Desconocido")
data["gender"] = data["gender"].replace("f", "Femenino")
data["gender"] = data["gender"].replace("m", "Masculino")
data["gender"] = data["gender"].replace("o", "Otro")

# Definir el puntaje mínimo requerido
puntaje_minimo = 0.7  

eval_columns = ["EvalSemanal 01", "EvalSemanal 02", "EvalSemanal 03", "EvalSemanal 04", "EvalSemanal Avg"]

data_no_filtrada = data

conteo_genero_0 = data_no_filtrada["gender"].value_counts().reset_index()

conteo_genero_0.columns = ["Género", "Cantidad"]

# Filtrar los estudiantes que no alcanzaron el puntaje mínimo en "EvalSemanal Avg"
data_filtrada = data[data["EvalSemanal Avg"] < puntaje_minimo]
data_filtrada_apro = data[data["EvalSemanal Avg"] >= puntaje_minimo]

# Contar cantidad de estudiantes por género
conteo_genero = data_filtrada["gender"].value_counts().reset_index()
conteo_genero_apro = data_filtrada_apro["gender"].value_counts().reset_index()

conteo_genero.columns = ["Género", "Cantidad"]
conteo_genero_apro.columns = ["Género", "Cantidad"]

# Crear la fuente de datos para Bokeh
source_bar = ColumnDataSource(conteo_genero)
source_bar_apro = ColumnDataSource(conteo_genero_apro)
source_bar_total = ColumnDataSource(conteo_genero_0)

print(source_bar_total)

# Paleta de colores
colores0 = Bokeh[len(conteo_genero_0)]

# 📊 **Gráfico de Barras**
p_barras_0 = figure(
    x_range=conteo_genero_0["Género"],
    title="Cantidad de Estudiantes Total",
    x_axis_label="Género",
    y_axis_label="Cantidad",
    width=500,
    height=400
)
p_barras_0.add_tools(
    HoverTool(tooltips=[("Cantidad", "@Cantidad"), ("Genero:", "@Género")], 
            show_arrow=False,
            point_policy='follow_mouse'))

p_barras_0.vbar(
    x="Género",
    top="Cantidad",
    source=source_bar_total,
    width=0.6,
    color=factor_cmap("Género", palette=colores0, factors=conteo_genero_0["Género"])
)

# Paleta de colores
colores = Pastel1[len(conteo_genero)]

# 📊 **Gráfico de Barras**
p_barras = figure(
    x_range=conteo_genero["Género"],
    title="Cantidad de Estudiantes que NO Alcanzaron el Puntaje Mínimo en las Evaluaciones",
    x_axis_label="Género",
    y_axis_label="Cantidad",
    width=500,
    height=400
)

p_barras.add_tools(
    HoverTool(tooltips=[("Cantidad", "@Cantidad"), ("Genero:", "@Género")], 
            show_arrow=False,
            point_policy='follow_mouse'))

p_barras.vbar(
    x="Género",
    top="Cantidad",
    source=source_bar,
    width=0.6,
    color=factor_cmap("Género", palette=colores, factors=conteo_genero["Género"])
)

# 📊 **Gráfico de Barras**
p_barras2 = figure(
    x_range=conteo_genero_apro["Género"],
    title="Cantidad de Estudiantes que SI Alcanzaron el Puntaje Mínimo en las Evaluaciones",
    x_axis_label="Género",
    y_axis_label="Cantidad",
    width=500,
    height=400
)

p_barras2.add_tools(
    HoverTool(tooltips=[("Cantidad", "@Cantidad"), ("Genero:", "@Género")], 
            show_arrow=False,
            point_policy='follow_mouse'))

p_barras2.vbar(
    x="Género",
    top="Cantidad",
    source=source_bar_apro,
    width=0.6,
    color=factor_cmap("Género", palette=colores, factors=conteo_genero_apro["Género"])
)

curdoc().add_root(column(desc, p_barras_0, p_barras, p_barras2))

'''
# 📊 **Gráfico de Dispersión**
source_dispersion = ColumnDataSource(data_no_filtrada)

p_dispersion = figure(
    title="Distribución de Puntajes de Estudiantes que No Alcanzaron el Mínimo",
    x_range=eval_columns,
    y_range=(0, 1),
    x_axis_label="Evaluación",
    y_axis_label="Puntaje",
    width=500,
    height=400
)

p_dispersion.scatter(
    x=eval_columns,
    y="EvalSemanal Avg",
    source=source_dispersion,
    color=factor_cmap("gender", palette=colores, factors=conteo_genero["Género"]),
    size=10,
    fill_alpha=0.6
)

curdoc().add_root(column(desc, p_dispersion))
'''

# 📊 **Gráfico de Pastel**
data_pie = conteo_genero.copy()
data_pie["angle"] = data_pie["Cantidad"] / data_pie["Cantidad"].sum() * 2 * pi
data_pie["color"] = colores[:len(data_pie)]

source_pie = ColumnDataSource(data_pie)

p_pastel = figure(
    title="Distribución de Género en los que NO Alcanzaron el Puntaje Mínimo",
    width=500
)

p_pastel.add_tools(
    HoverTool(tooltips=[("Cantidad", "@Cantidad"), ("Genero:", "@Género")], 
            show_arrow=False,
            point_policy='follow_mouse'))

p_pastel.wedge(
    x=0,
    y=0,
    radius=0.8,
    start_angle=cumsum('angle', include_zero=True), 
    end_angle=cumsum('angle'),
    line_color="white", 
    fill_color='color',
    source=source_pie,
    legend_field="Género"
)

p_pastel.axis.axis_label = None
p_pastel.axis.visible = False
p_pastel.grid.grid_line_color = None

data_pie2 = conteo_genero_apro.copy()
data_pie2["angle"] = data_pie2["Cantidad"] / data_pie2["Cantidad"].sum() * 2 * pi
data_pie2["color"] = colores[:len(data_pie2)]

source_pie2 = ColumnDataSource(data_pie2)

p_pastel2 = figure(
    title="Distribución de Género en los que SI Alcanzaron el Puntaje Mínimo",
    width=500
)

p_pastel2.add_tools(
    HoverTool(tooltips=[("Cantidad", "@Cantidad"), ("Genero:", "@Género")], 
            show_arrow=False,
            point_policy='follow_mouse'))

p_pastel2.wedge(
    x=0,
    y=0,
    radius=0.8,
    start_angle=cumsum('angle', include_zero=True), 
    end_angle=cumsum('angle'),
    line_color="white", 
    fill_color='color',
    source=source_pie2,
    legend_field="Género"
)

p_pastel2.axis.axis_label = None
p_pastel2.axis.visible = False
p_pastel2.grid.grid_line_color = None

curdoc().add_root(column(desc2, p_pastel, p_pastel2))

# 📌 Datos iniciales
data_general = {
    'Estado': ["total", "aprobado", "reprobado"],
    'Femenino':    [conteo_genero_0["Cantidad"][0], conteo_genero_apro["Cantidad"][0], conteo_genero["Cantidad"][0]],
    'Masculino':   [conteo_genero_0["Cantidad"][1], conteo_genero_apro["Cantidad"][1], conteo_genero["Cantidad"][1]],
    'Otro':        [conteo_genero_0["Cantidad"][2], 0, conteo_genero["Cantidad"][2]],
    'Desconocido': [conteo_genero_0["Cantidad"][3], 0, conteo_genero["Cantidad"][3]],
}

# 📌 Convertir a `ColumnDataSource`
source_general = ColumnDataSource(data_general)

# 📌 Definir colores
colores = ["#c9d9d3", "#718dbf", "#e84d60", "#f6a000"]

# 📌 Crear la figura
p_general = figure(
    x_range=["total", "aprobado", "reprobado"],
    y_axis_label="Cantidad",
    title="Conteo General por Género",
    height=400,
    width=600
)

# 📌 Agregar barras separadas para cada género
barra_femenino = p_general.vbar(
    x=dodge('Estado', -0.3, range=p_general.x_range), top='Femenino', source=source_general,
    width=0.2, color=colores[0], legend_label="Femenino"
)

barra_masculino = p_general.vbar(
    x=dodge('Estado', -0.1, range=p_general.x_range), top='Masculino', source=source_general,
    width=0.2, color=colores[1], legend_label="Masculino"
)

barra_otro = p_general.vbar(
    x=dodge('Estado', 0.1, range=p_general.x_range), top='Otro', source=source_general,
    width=0.2, color=colores[2], legend_label="Otro"
)

barra_desconocido = p_general.vbar(
    x=dodge('Estado', 0.3, range=p_general.x_range), top='Desconocido', source=source_general,
    width=0.2, color=colores[3], legend_label="Desconocido"
)

# 📌 Agregar `HoverTool` a cada barra individualmente
hover_femenino = HoverTool(
    renderers=[barra_femenino],
    tooltips=[("Género", "Femenino"), ("Cantidad", "@Femenino")]
)

hover_masculino = HoverTool(
    renderers=[barra_masculino],
    tooltips=[("Género", "Masculino"), ("Cantidad", "@Masculino")]
)

hover_otro = HoverTool(
    renderers=[barra_otro],
    tooltips=[("Género", "Otro"), ("Cantidad", "@Otro")]
)

hover_desconocido = HoverTool(
    renderers=[barra_desconocido],
    tooltips=[("Género", "Desconocido"), ("Cantidad", "@Desconocido")]
)

# 📌 Agregar los `HoverTool` a la gráfica
p_general.add_tools(hover_femenino, hover_masculino, hover_otro, hover_desconocido)

# 📌 Mejoras visuales
p_general.x_range.range_padding = 0.1
p_general.xgrid.grid_line_color = None
p_general.legend.location = "top_left"
p_general.legend.orientation = "horizontal"

# 📌 Agregar a la interfaz de Bokeh
curdoc().add_root(column(desc, p_general))

data_pie_general = {
    "Género": ["Femenino", "Masculino", "Otro", "Desconocido"],
    "Total": [conteo_genero_0["Cantidad"][0], conteo_genero_0["Cantidad"][1], 
              conteo_genero_0["Cantidad"][2], conteo_genero_0["Cantidad"][3]],
    "Aprobado": [conteo_genero_apro["Cantidad"][0], conteo_genero_apro["Cantidad"][1], 
                 0, 0],
    "Reprobado": [conteo_genero["Cantidad"][0], conteo_genero["Cantidad"][1], 
                  conteo_genero["Cantidad"][2], conteo_genero["Cantidad"][3]]
}

colores_pastel = ["#AAB99A", "#E5989B"]  # Verde (Aprobado) - Marrón (Reprobado)
graficos_pastel = []

# 📌 Crear gráficos de pastel para cada género
for i, genero in enumerate(data_pie_general["Género"]):
    total = data_pie_general["Total"][i]
    aprobados = data_pie_general["Aprobado"][i]
    reprobados = data_pie_general["Reprobado"][i]

    # Si no hay datos, saltar ese género
    if total == 0:
        continue

    # 📌 Calcular porcentajes
    data_pie = pd.DataFrame({
        "Estado": ["Aprobado", "Reprobado"],
        "Cantidad": [aprobados, reprobados],
    })
    data_pie["Porcentaje"] = data_pie["Cantidad"] / total
    data_pie["angle"] = data_pie["Porcentaje"] * 2 * pi
    data_pie["color"] = colores_pastel

    source_pie = ColumnDataSource(data_pie)

    # 📌 Crear figura
    p_pastel = figure(
        title=f"Distribución de {genero}",
        width=300, height=300
    )

    p_pastel.add_tools(
        HoverTool(tooltips=[("Estado", "@Estado"), ("Cantidad", "@Cantidad"), ("Porcentaje", "@Porcentaje{0.0%}")], 
                  show_arrow=False,
                  point_policy='follow_mouse')
    )

    p_pastel.wedge(
        x=0, y=0, radius=0.8,
        start_angle=cumsum('angle', include_zero=True), 
        end_angle=cumsum('angle'),
        line_color="white", 
        fill_color='color',
        source=source_pie,
        legend_field="Estado"
    )

    p_pastel.axis.axis_label = None
    p_pastel.axis.visible = False
    p_pastel.grid.grid_line_color = None

    graficos_pastel.append(p_pastel)

curdoc().add_root(column(desc4, *graficos_pastel))