import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Select, HoverTool, FactorRange
from bokeh.layouts import column
from bokeh.io import curdoc
from bokeh.palettes import Category10
from bokeh.transform import factor_cmap, dodge, factor_mark
from bokeh.models import Div
from math import pi
from bokeh.transform import cumsum
from os.path import dirname, join
from bokeh.plotting import figure, curdoc
from bokeh.layouts import column


# Direccionar al html
from os.path import dirname, join
from bokeh.models import Div

desc0 = Div(text=open(join(dirname(__file__), "TituloACCS1.html")).read(), sizing_mode="stretch_width")
desc1 = Div(text=open(join(dirname(__file__), "grafica1.html")).read(), sizing_mode="stretch_width")
desc2 = Div(text=open(join(dirname(__file__), "grafica2.html")).read(), sizing_mode="stretch_width")
desc22 = Div(text=open(join(dirname(__file__), "grafica2v2.html")).read(), sizing_mode="stretch_width")
desc3 = Div(text=open(join(dirname(__file__), "grafica3.html")).read(), sizing_mode="stretch_width")
desc32 = Div(text=open(join(dirname(__file__), "grafica3v2.html")).read(), sizing_mode="stretch_width")
desc4 = Div(text=open(join(dirname(__file__), "grafica4.html")).read(), sizing_mode="stretch_width")
desc42 = Div(text=open(join(dirname(__file__), "grafica4v2.html")).read(), sizing_mode="stretch_width")
desc5 = Div(text=open(join(dirname(__file__), "grafica5.html")).read(), sizing_mode="stretch_width")
desc52 = Div(text=open(join(dirname(__file__), "grafica5v2.html")).read(), sizing_mode="stretch_width")

# Cargar el archivo CSV
# csv_path = r"D:/Users/LENOVO/Desktop/Codigo-OpenCampus/CSVs/Unificacar_CSVs/xd.csv"
csv_path = r"../../../CSVs/Unificar Oct-Nov24/xd.csv"
data = pd.read_csv(csv_path, delimiter=',')

curdoc().add_root(column(desc0))

# Contar total de estudiantes
total_estudiantes = len(data)

# Contar aprobados y reprobados según la columna "grade"
total_aprobados = len(data[data["grade"] >= 0.7])
total_reprobados = len(data[data["grade"] < 0.7])

# Crear un DataFrame con los valores
df_estudiantes = pd.DataFrame({
    "Categoría": ["Total Estudiantes", "Aprobados", "Reprobados"],
    "Cantidad": [total_estudiantes, total_aprobados, total_reprobados]
})

df_estudiantes["Color"] = ["grey", "green", "crimson"]

# Actualizar la fuente de datos
source_estudiantes = ColumnDataSource(df_estudiantes)

''' 
GRAFICA 1: Total de estudiantes, aprobados y reprobados 
'''
# Crear la figura
p_estudiantes = figure(
    x_range=FactorRange(*df_estudiantes["Categoría"].astype(str)),  
    title="Cantidad de Estudiantes: Totales, Aprobados y Reprobados",
    x_axis_label="Categoría",
    y_axis_label="Cantidad",
    width=800,
    height=400
)

p_estudiantes.add_tools(
    HoverTool(tooltips=[("Cantidad", "@Cantidad")], 
            show_arrow=False,
            point_policy='follow_mouse'))

# Agregar las barras correctamente
p_estudiantes.vbar(
    x="Categoría", 
    top="Cantidad",  
    source=source_estudiantes, 
    width=0.6, 
    color="Color",
    alpha=0.8  # Esto controla la opacidad; 1 = sin transparencia, 0 = totalmente transparente
)

# Agregar al documento
curdoc().add_root(column(desc1, p_estudiantes))

''' 
GRAFICA 5: Pastel con el porcentaje de particioantes aprobados y reprobados
'''
# Crear el DataFrame con Aprobados y Reprobados
data_pie = pd.DataFrame({"Estado": ["Aprobado", "Reprobado"],
                         "Cantidad": [total_aprobados, total_reprobados]})

# Calcular Porcentaje y Ángulos para el Gráfico de Pastel
data_pie["Porcentaje"] = data_pie["Cantidad"] / data_pie["Cantidad"].sum()
data_pie["angle"] = data_pie["Porcentaje"] * 2 * pi
data_pie["color"] = ["green", "crimson"]

source_pie = ColumnDataSource(data_pie)

# Crear la Figura
p_pastel = figure(
    title="Distribución Aprobados vs Reprobados",
    width=400,
    height=400
)

# Agregar herramienta de Hover mostrando cantidad y porcentaje
p_pastel.add_tools(
    HoverTool(tooltips=[("Estado", "@Estado"),
                        ("Cantidad", "@Cantidad"),
                        ("Porcentaje", "@Porcentaje{0.0%}")],
              show_arrow=False,
              point_policy='follow_mouse')
)

# Graficar el Pastel
p_pastel.wedge(
    x=0, y=0, radius=0.8,
    start_angle=cumsum('angle', include_zero=True),
    end_angle=cumsum('angle'),
    line_color='white',
    fill_color='color',
    source=source_pie,
    legend_field='Estado',
    alpha=0.8  # Esto controla la opacidad; 1 = sin transparencia, 0 = totalmente transparente
)

p_pastel.axis.axis_label = None
p_pastel.axis.visible = False
p_pastel.grid.grid_line_color = None

# Finalmente, añadir a la aplicación
curdoc().add_root(column(desc5, p_pastel))

''' 
GRAFICA 2: Promedios por Evaluacion Semanal
'''
# Columnas de evaluación semanal
eval_columns = ["EvalSemanal 01", "EvalSemanal 02", "EvalSemanal 03", "EvalSemanal 04"]

# Calcular promedio por semana
promedios_semanales = data[eval_columns].mean()

# Crear DataFrame con los valores
hist_data = pd.DataFrame({
    "Semana": eval_columns,
    "Promedio": promedios_semanales
})

# Fuente de datos para Bokeh
source_hist = ColumnDataSource(hist_data)

# Crear la figura para el histograma
p_hist = figure(
    x_range=FactorRange(*hist_data["Semana"].astype(str)),  
    title="Promedio de Notas por Semana",
    x_axis_label="Semana",
    y_axis_label="Promedio",
    width=800,
    height=400
)

p_hist.add_tools(
    HoverTool(tooltips=[("Promedio:", "@Promedio")], 
            show_arrow=False,
            point_policy='follow_mouse'))

# Agregar barras al histograma
p_hist.vbar(
    x="Semana", 
    top="Promedio",  
    source=source_hist, 
    width=0.6, 
    color="dodgerblue",
    alpha=0.8  # Esto controla la opacidad; 1 = sin transparencia, 0 = totalmente transparente
)

# Agregar línea de tendencia
p_hist.line(
    x=hist_data["Semana"], 
    y=hist_data["Promedio"], 
    line_width=2, 
    color="red"
)

# Agregar las gráficas al documento
curdoc().add_root(column(desc2, p_hist))

''' 
GRAFICA 2.2: Promedios por Evaluacion Semanal (Excluyendo estudiantes con solo 0s)
'''
# eval_columns = ["EvalSemanal 01", "EvalSemanal 02", "EvalSemanal 03", "EvalSemanal 04"]

# Filtrar estudiantes que no tengan 0 en todas las evaluaciones
filtered_data = data[(data[eval_columns] != 0).any(axis=1)]

# Calcular promedios por semana
data_avg_filtered = filtered_data[eval_columns].mean()

# Crear DataFrame con los valores
hist_data_filtered = pd.DataFrame({
    "Semana": eval_columns,
    "Promedio": data_avg_filtered
})

# Fuente de datos para Bokeh
source_hist_filtered = ColumnDataSource(hist_data_filtered)

# Crear la figura para el histograma
p_hist_filtered = figure(
    x_range=FactorRange(*hist_data_filtered["Semana"].astype(str)),  
    title="Promedio de Notas por Semana (Excluyendo Solo 0s Totales)",
    x_axis_label="Semana",
    y_axis_label="Promedio",
    width=800,
    height=400
)

p_hist_filtered.add_tools(
    HoverTool(tooltips=[("Promedio:", "@Promedio")], 
            show_arrow=False,
            point_policy='follow_mouse'))

# Agregar barras al histograma
p_hist_filtered.vbar(
    x="Semana", 
    top="Promedio",  
    source=source_hist_filtered, 
    width=0.6, 
    color="orange",
    alpha=0.8  # Esto controla la opacidad; 1 = sin transparencia, 0 = totalmente transparente
)

# Agregar línea de tendencia
p_hist_filtered.line(
    x=hist_data_filtered["Semana"], 
    y=hist_data_filtered["Promedio"], 
    line_width=2, 
    color="red"
)

curdoc().add_root(column(desc22, p_hist_filtered))

''' 
GRAFICA 3: Cantidad de personas que tienen una nota menor y mayor a 7
'''
# Calcular cantidad de aprobados y reprobados por semana
aprobados = [len(data[data[col] >= 0.7]) for col in eval_columns]
reprobados = [len(data[data[col] < 0.7]) for col in eval_columns]

# Crear DataFrame con los valores
df_estudiantes = pd.DataFrame({
    "Semana": eval_columns,
    "Aprobados": aprobados,
    "Reprobados": reprobados
})

# Fuente de datos para Bokeh
source_aprepo = ColumnDataSource(df_estudiantes)

# Crear la figura
p_aprepo = figure(
    x_range=FactorRange(*df_estudiantes["Semana"].astype(str)),  
    title="Cantidad de Estudiantes Aprobados y Reprobados por Semana",
    x_axis_label="Semana",
    y_axis_label="Cantidad",
    width=800,
    height=400
)

# Apilar las barras correctamente
barraApro = p_aprepo.vbar(
    x=dodge("Semana", -0.15, range=p_aprepo.x_range), 
    top="Aprobados",  
    source=source_aprepo, 
    width=0.3, 
    color="green",
    legend_label="Aprobados",
    alpha=0.8  # Esto controla la opacidad; 1 = sin transparencia, 0 = totalmente transparente
)

barraRepro = p_aprepo.vbar(
    x=dodge("Semana", 0.15, range=p_aprepo.x_range), 
    top="Reprobados",  
    source=source_aprepo, 
    width=0.3, 
    color="crimson",
    legend_label="Reprobados",
    alpha=0.8  # Esto controla la opacidad; 1 = sin transparencia, 0 = totalmente transparente
)


# Agregar `HoverTool` a cada barra individualmente
hover_Apro = HoverTool(
    renderers=[barraApro],
    tooltips=[("Estado", "Aprobados"), ("Cantidad", "@Aprobados")]
)

# Agregar `HoverTool` a cada barra individualmente
hover_Repro = HoverTool(
    renderers=[barraRepro],
    tooltips=[("Estado", "Reprobados"), ("Cantidad", "@Reprobados")]
)

# Configurar leyenda
p_aprepo.legend.location = "top_right"

# Agregar los `HoverTool` a la gráfica
p_aprepo.add_tools(hover_Apro, hover_Repro)

# Mejoras visuales
p_aprepo.x_range.range_padding = 0.1
p_aprepo.xgrid.grid_line_color = None
p_aprepo.legend.location = "top_left"
p_aprepo.legend.orientation = "horizontal"

# Agregar al documento
curdoc().add_root(column(desc3, p_aprepo))

''' 
GRAFICA 3.2: Cantidad de personas que tienen una nota menor y mayor a 7 (Excluyendo estudiantes con solo 0s)
'''
# Filtrar estudiantes que no tengan 0 en todas las evaluaciones
filtered_data_aprepo = data[(data[eval_columns] != 0).any(axis=1)]

# Calcular cantidad de aprobados y reprobados por semana después del filtro
aprobados_filtered = [len(filtered_data_aprepo[filtered_data_aprepo[col] >= 0.7]) for col in eval_columns]
reprobados_filtered = [len(filtered_data_aprepo[filtered_data_aprepo[col] < 0.7]) for col in eval_columns]

# Crear DataFrame con los valores filtrados
df_aprepo_filtered = pd.DataFrame({
    "Semana": eval_columns,
    "Aprobados": aprobados_filtered,
    "Reprobados": reprobados_filtered
})

# Fuente de datos para Bokeh
source_aprepo_filtered = ColumnDataSource(df_aprepo_filtered)

# Crear la figura
p_aprepo_filtered = figure(
    x_range=FactorRange(*df_aprepo_filtered["Semana"].astype(str)),  
    title="Cantidad de Estudiantes Aprobados y Reprobados por Semana (Excluyendo Solo 0s Totales)",
    x_axis_label="Semana",
    y_axis_label="Cantidad",
    width=800,
    height=400
)

# Apilar las barras correctamente
barra_Apro_filtered = p_aprepo_filtered.vbar(
    x=dodge("Semana", -0.15, range=p_aprepo_filtered.x_range), 
    top="Aprobados",  
    source=source_aprepo_filtered, 
    width=0.3, 
    color="green",
    legend_label="Aprobados",
    alpha=0.8  # Esto controla la opacidad; 1 = sin transparencia, 0 = totalmente transparente
)

barra_Repro_filtered = p_aprepo_filtered.vbar(
    x=dodge("Semana", 0.15, range=p_aprepo_filtered.x_range), 
    top="Reprobados",  
    source=source_aprepo_filtered, 
    width=0.3, 
    color="crimson",
    legend_label="Reprobados",
    alpha=0.8  # Esto controla la opacidad; 1 = sin transparencia, 0 = totalmente transparente
)

# Agregar `HoverTool` a cada barra individualmente
hover_Apro_filtered = HoverTool(
    renderers=[barra_Apro_filtered],
    tooltips=[("Estado", "Aprobados"), ("Cantidad", "@Aprobados")]
)

# Agregar `HoverTool` a cada barra individualmente
hover_Repro_filtered  = HoverTool(
    renderers=[barra_Repro_filtered],
    tooltips=[("Estado", "Reprobados"), ("Cantidad", "@Reprobados")]
)

# Agregar los `HoverTool` a la gráfica
p_aprepo_filtered.add_tools(hover_Apro_filtered, hover_Repro_filtered)

# Mejoras visuales
p_aprepo_filtered.x_range.range_padding = 0.1
p_aprepo_filtered.xgrid.grid_line_color = None
p_aprepo_filtered.legend.location = "top_left"
p_aprepo_filtered.legend.orientation = "horizontal"

# Agregar la gráfica al documento
curdoc().add_root(column(desc32, p_aprepo_filtered))

''' 
GRAFICA 4: Promedios obtenidos por Genero en las Evaluaciones Semanales
'''
# Calcular promedios por género
data_avg = data.groupby("gender")[eval_columns].mean().reset_index()

# Convertir DataFrame a formato compatible con Bokeh
data_melted = data_avg.melt(id_vars=["gender"], var_name="Evaluación", value_name="Promedio")
# print(data_melted)

# Crear la fuente de datos inicial con un solo género seleccionado
initial_gender = data_melted["gender"].unique()[0]  # Primer género disponible
filtered_data = data_melted[data_melted["gender"] == initial_gender]
source = ColumnDataSource(filtered_data)


# Crear la figura
p = figure(
    x_range=eval_columns,  # Las evaluaciones en el eje X
    title="Promedio de Evaluaciones Semanales por Género",
    x_axis_label="Evaluaciones",
    y_axis_label="Promedio",
    width=800,
    height=400,
)

p.add_tools(
    HoverTool(tooltips=[("Promedio", "@Promedio")], 
            show_arrow=False,
            point_policy='follow_mouse'))

# Dibujar las barras (Inicialmente con un solo género)
p.vbar(
    x="Evaluación", 
    top="Promedio",  
    source=source, 
    width=0.6, 
    color="pink",
    alpha=0.9  # Esto controla la opacidad; 1 = sin transparencia, 0 = totalmente transparente
)

# Crear Select para cambiar el género
gender_list = data_melted["gender"].unique().tolist()
select = Select(title="Selecciona un Género:", value=initial_gender, options=gender_list)

# Función para actualizar la gráfica
def update_plot(attr, old, new):
    selected_gender = select.value
    new_data = data_melted[data_melted["gender"] == selected_gender]
    source.data = dict(ColumnDataSource(new_data).data)  # 🔹 SOLUCIÓN: Convertir a dict

select.on_change("value", update_plot)

# Agregar la gráfica al documento
curdoc().add_root(column(desc4, select, p))

''' 
GRAFICA 4.2: Promedios obtenidos por Genero en las Evaluaciones Semanales (Excluyendo estudiantes con solo 0s)
'''
# Filtrar datos: excluir participantes que tengan solo ceros en todas las semanas
filtered_data = data[(data[eval_columns] != 0).any(axis=1)]

# Calcular promedios por género excluyendo solo participantes con ceros en todas las semanas
def mean_exclude_all_zeros(series):
    return series.mean()

data_avg_filtered = filtered_data.groupby("gender")[eval_columns].agg(mean_exclude_all_zeros).reset_index()

data_melted_filtered = data_avg_filtered.melt(id_vars=["gender"], var_name="Evaluación", value_name="Promedio")

# Fuente de datos inicial
initial_gender_filtered = data_melted_filtered["gender"].unique()[0]
filtered_data_filtered = data_melted_filtered[data_melted_filtered["gender"] == initial_gender_filtered]
source_filtered = ColumnDataSource(filtered_data_filtered)

# Crear la nueva figura
p_filteredd = figure(
    x_range=eval_columns,
    title="Promedio de Evaluaciones Semanales por Género (Excluyendo Solo 0s Totales)",
    x_axis_label="Evaluaciones",
    y_axis_label="Promedio",
    width=800,
    height=400,
)

p_filteredd.add_tools(
    HoverTool(tooltips=[("Promedio", "@Promedio")], 
            show_arrow=False,
            point_policy='follow_mouse'))

p_filteredd.vbar(
    x="Evaluación", 
    top="Promedio",  
    source=source_filtered, 
    width=0.6, 
    color="purple",
    alpha=0.8  # Esto controla la opacidad; 1 = sin transparencia, 0 = totalmente transparente
)

# Crear Select para cambiar el género
gender_list_filtered = data_melted_filtered["gender"].unique().tolist()
select_filteredd = Select(title="Selecciona un Género:", value=initial_gender_filtered, options=gender_list_filtered)

def update_plot_filtered(attr, old, new):
    selected_gender_filtered = select_filteredd.value
    new_data_filtered = data_melted_filtered[data_melted_filtered["gender"] == selected_gender_filtered]
    source_filtered.data = dict(ColumnDataSource(new_data_filtered).data)

select_filteredd.on_change("value", update_plot_filtered)

curdoc().add_root(column(desc42, select_filteredd, p_filteredd))