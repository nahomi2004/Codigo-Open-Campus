import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Select, HoverTool, FactorRange
from bokeh.layouts import column
from bokeh.io import curdoc
from bokeh.palettes import Category10
from bokeh.transform import factor_cmap, dodge, factor_mark
from bokeh.models import CDSView, GroupFilter
from bokeh.models import Div
from math import pi
from bokeh.transform import cumsum
import numpy as np
from os.path import dirname, join
from bokeh.models import LabelSet, ColumnDataSource
from bokeh.plotting import figure, curdoc
from bokeh.layouts import column


# Direccionar al html
from os.path import dirname, join
from bokeh.models import Div

desc0 = Div(text=open(join(dirname(__file__), "title.html")).read(), sizing_mode="stretch_width")
desc = Div(text=open(join(dirname(__file__), "graficaBarrasFiltro.html")).read(), sizing_mode="stretch_width")
desc2 = Div(text=open(join(dirname(__file__), "graficaBarrasFiltro1.html")).read(), sizing_mode="stretch_width")
desc3 = Div(text=open(join(dirname(__file__), "graficaBarrasFiltro2.html")).read(), sizing_mode="stretch_width")
desc4 = Div(text=open(join(dirname(__file__), "graficaBarrasSimple.html")).read(), sizing_mode="stretch_width")
desc5 = Div(text=open(join(dirname(__file__), "graficaCircular.html")).read(), sizing_mode="stretch_width")


# Cargar los archivos CSV
csv_profile_path = r"../../../CSVs/UTPL_CREAA1_2024_2_student_profile_info_2025-02-12-2117.csv"
csv_grade_path = r"../../../CSVs/UTPL_CREAA1_2024_2_grade_report_2025-02-12-2116.csv"

dataProfile = pd.read_csv(csv_profile_path, delimiter=',')
dataGrade = pd.read_csv(csv_grade_path, delimiter=',')

# Unir los CSVs por "username"
data = pd.merge(dataProfile, dataGrade, on="username")

# Columnas de evaluación semanal
eval_columns = ["EvalSemanal 01", "EvalSemanal 02", "EvalSemanal 03", "EvalSemanal 04"]

curdoc().add_root(column(desc0))

'''
GRAFICA 1
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

# Dibujar las barras (Inicialmente con un solo género)
p.vbar(
    x="Evaluación", 
    top="Promedio",  
    source=source, 
    width=0.6, 
    color="dodgerblue"
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

'''
GRAFICA 2
'''
# Crear la nueva figura para promedios agrupados
p1 = figure(
    x_range=eval_columns, 
    title="Promedio por género",
    x_axis_label="Evaluación",
    y_axis_label="Promedio",
    width=1600,
    height=800,
    tools="pan,box_zoom,wheel_zoom,save,reset",
    toolbar_location="right",
)

p1.xaxis.major_label_orientation = 1.0

# Usar colores para cada género
colors = Category10[len(gender_list)]

# Ancho y desplazamiento para que las barras no se sobrepongan
width = 0.2  
offsets = [dodge("Evaluación", (i + 0.3) * width - (width * len(gender_list) / 2), range=p1.x_range) for i in range(len(gender_list))]

# Agregar barras agrupadas por género
for i, gender in enumerate(gender_list):
    # Filtrar datos manualmente para cada género
    filtered_data = data_melted[data_melted["gender"] == gender]
    source_gender = ColumnDataSource(filtered_data)
    
    p1.vbar(
        x=offsets[i], 
        top="Promedio",  # Ahora toma el promedio correcto
        source=source_gender, 
        width=width, 
        color=colors[i], 
        legend_label=gender
    )

p1.legend.title = "Género"
p1.legend.location = "top_right"

# Agregar todo al layout

curdoc().add_root(column(desc, select, p, p1))


''' 
GRAFICA 1 SIN 0's
'''
# Calcular promedios por género excluyendo valores de 0
def mean_exclude_zeros(series):
    return series[series != 0].mean()

data_avg_filtered = data.groupby("gender")[eval_columns].agg(mean_exclude_zeros).reset_index()

data_melted_filtered = data_avg_filtered.melt(id_vars=["gender"], var_name="Evaluación", value_name="Promedio")

# Fuente de datos inicial
initial_gender_filtered = data_melted_filtered["gender"].unique()[0]
filtered_data_filtered = data_melted_filtered[data_melted_filtered["gender"] == initial_gender_filtered]
source_filtered = ColumnDataSource(filtered_data_filtered)

# Crear la nueva figura
p_filtered = figure(
    x_range=eval_columns,
    title="Promedio de Evaluaciones Semanales por Género (Sin 0s)",
    x_axis_label="Evaluaciones",
    y_axis_label="Promedio",
    width=800,
    height=400,
)

p_filtered.vbar(
    x="Evaluación", 
    top="Promedio",  
    source=source_filtered, 
    width=0.6, 
    color="green"
)

# Crear Select para cambiar el género
gender_list_filtered = data_melted_filtered["gender"].unique().tolist()
select_filtered = Select(title="Selecciona un Género:", value=initial_gender_filtered, options=gender_list_filtered)

def update_plot_filtered(attr, old, new):
    selected_gender_filtered = select_filtered.value
    new_data_filtered = data_melted_filtered[data_melted_filtered["gender"] == selected_gender_filtered]
    source_filtered.data = dict(ColumnDataSource(new_data_filtered).data)

select_filtered.on_change("value", update_plot_filtered)

#bcurdoc().add_root(column(select_filtered, p_filtered))


''' 
GRAFICA 2 SIN 0's
'''
# Calcular promedios por género excluyendo valores de 0
def mean_exclude_zeros(series):
    return series[series != 0].mean()

data_avg_filtered = data.groupby("gender")[eval_columns].agg(mean_exclude_zeros).reset_index()

data_melted_filtered = data_avg_filtered.melt(id_vars=["gender"], var_name="Evaluación", value_name="Promedio")

# Crear la nueva figura para promedios agrupados sin considerar valores 0
p2_filtered = figure(
    x_range=eval_columns, 
    title="Promedio por Género (Sin considerar valores 0)",
    x_axis_label="Evaluación",
    y_axis_label="Promedio",
    width=1600,
    height=800,
    tools="pan,box_zoom,wheel_zoom,save,reset",
    toolbar_location="right",
)

p2_filtered.xaxis.major_label_orientation = 1.0

# Usar los mismos colores para cada género
colors = Category10[len(gender_list_filtered)]

# Ancho y desplazamiento para que las barras no se sobrepongan
width = 0.2  
offsets = [dodge("Evaluación", (i + 0.3) * width - (width * len(gender_list_filtered) / 2), range=p2_filtered.x_range) for i in range(len(gender_list_filtered))]

# Agregar barras agrupadas por género excluyendo valores 0
for i, gender in enumerate(gender_list_filtered):
    # Filtrar datos para cada género, excluyendo valores donde el promedio es 0
    filtered_data_filtered = data_melted_filtered[(data_melted_filtered["gender"] == gender) & (data_melted_filtered["Promedio"] > 0)]
    source_gender_filtered = ColumnDataSource(filtered_data_filtered)
    
    p2_filtered.vbar(
        x=offsets[i], 
        top="Promedio",  
        source=source_gender_filtered, 
        width=width, 
        color=colors[i], 
        legend_label=gender
    )

p2_filtered.legend.title = "Género"
p2_filtered.legend.location = "top_right"

# Agregar todo al layout
curdoc().add_root(column(desc2, select_filtered, p_filtered, p2_filtered))

def count_zeros(series):
    return (series == 0).sum()

'''
"GRAFICA 1.2 SIN PARTICIPANTES CON TODAS LAS EVALUACIONES CON 0's"
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

p_filteredd.vbar(
    x="Evaluación", 
    top="Promedio",  
    source=source_filtered, 
    width=0.6, 
    color="orange"
)

# Crear Select para cambiar el género
gender_list_filtered = data_melted_filtered["gender"].unique().tolist()
select_filteredd = Select(title="Selecciona un Género:", value=initial_gender_filtered, options=gender_list_filtered)

def update_plot_filtered(attr, old, new):
    selected_gender_filtered = select_filtered.value
    new_data_filtered = data_melted_filtered[data_melted_filtered["gender"] == selected_gender_filtered]
    source_filtered.data = dict(ColumnDataSource(new_data_filtered).data)

select_filteredd.on_change("value", update_plot_filtered)

# curdoc().add_root(column(select_filteredd, p_filteredd))

'''
GRAFICA 2.2 SIN PARTICIPANTES CON TODAS LAS EVALUACIONES CON 0's
'''
# Filtrar datos: excluir participantes que tengan solo ceros en todas las semanas
filtered_data = data[(data[eval_columns] != 0).any(axis=1)]

# Calcular promedios por género excluyendo solo participantes con ceros en todas las semanas
data_avg_filtered = filtered_data.groupby("gender")[eval_columns].mean().reset_index()

data_melted_filtered = data_avg_filtered.melt(id_vars=["gender"], var_name="Evaluación", value_name="Promedio")

# Crear la nueva figura para promedios agrupados sin participantes con todas las evaluaciones en 0
p2_filtered = figure(
    x_range=eval_columns, 
    title="Promedio por Género (Excluyendo Solo 0s Totales)",
    x_axis_label="Evaluación",
    y_axis_label="Promedio",
    width=1600,
    height=800,
    tools="pan,box_zoom,wheel_zoom,save,reset",
    toolbar_location="right",
)

p2_filtered.xaxis.major_label_orientation = 1.0

# Obtener lista de géneros presentes en los datos filtrados
gender_list_filtered = data_melted_filtered["gender"].unique().tolist()

# Usar colores distintos para cada género
colors = Category10[len(gender_list_filtered)]

# Ancho y desplazamiento para que las barras no se sobrepongan
width = 0.2  
offsets = [dodge("Evaluación", (i + 0.3) * width - (width * len(gender_list_filtered) / 2), range=p2_filtered.x_range) for i in range(len(gender_list_filtered))]

# Agregar barras agrupadas por género, excluyendo participantes con todas las evaluaciones en 0
for i, gender in enumerate(gender_list_filtered):
    # Filtrar datos para cada género
    filtered_data_filtered = data_melted_filtered[data_melted_filtered["gender"] == gender]
    source_gender_filtered = ColumnDataSource(filtered_data_filtered)
    
    p2_filtered.vbar(
        x=offsets[i], 
        top="Promedio",  
        source=source_gender_filtered, 
        width=width, 
        color=colors[i], 
        legend_label=gender
    )

p2_filtered.legend.title = "Género"
p2_filtered.legend.location = "top_right"

# Agregar todo al layout
curdoc().add_root(column(desc3, select_filteredd, p_filteredd, p2_filtered))
# curdoc().add_root(column(desc, select_filteredd, p_filteredd, p2_filteredd))

''' 
GRAFICA 3: Cantidad de ceros por evaluación 
'''
data_zeros = data[eval_columns].apply(count_zeros).reset_index()
data_zeros.columns = ["Evaluación", "Cantidad de Ceros"]
source_zeros = ColumnDataSource(data_zeros)

p_zeros = figure(
    x_range=eval_columns,
    title="Cantidad de Ceros por Evaluación Semanal",
    x_axis_label="Evaluaciones",
    y_axis_label="Cantidad de Ceros",
    width=800,
    height=400,
)

p_zeros.vbar(
    x="Evaluación", 
    top="Cantidad de Ceros",  
    source=source_zeros, 
    width=0.6, 
    color="red"
)

curdoc().add_root(column(desc4, p_zeros))

''' 
GRAFICA 4: Distribución de ceros por género 
'''
# Contar ceros por género y evaluación
data_zeros = data.melt(id_vars=["gender"], value_vars=eval_columns, var_name="Evaluación", value_name="Nota")
data_zeros["Cero"] = (data_zeros["Nota"] == 0).astype(int)
zeros_count = data_zeros.groupby(["Evaluación", "gender"])["Cero"].sum().reset_index()

# Crear gráficos de pastel para cada evaluación
graphs = []
colors = Category10[10]

for i, eval_name in enumerate(eval_columns):
    df_eval = zeros_count[zeros_count["Evaluación"] == eval_name].copy()
    
    if df_eval["Cero"].sum() == 0:
        continue  # Si no hay ceros, saltar la evaluación
    
    df_eval["angle"] = df_eval["Cero"] / df_eval["Cero"].sum() * 2 * pi
    df_eval["color"] = colors[:len(df_eval)]
    
    source_pie = ColumnDataSource(df_eval)
    
    p_pie = figure(
        title=f"Distribución de Ceros - {eval_name}",
        toolbar_location=None,
        tools="",
        x_range=(-1, 1),
        width=400,
        height=400,
    )
    
    p_pie.wedge(
        x=0, y=0, radius=0.8,
        start_angle=cumsum("angle", include_zero=True),
        end_angle=cumsum("angle"),
        line_color="white",
        fill_color="color",
        source=source_pie,
        legend_field="gender",
    )
    
    # Agregar HoverTool para mostrar cantidad de ceros
    hover = HoverTool(
        tooltips=[("Género", "@gender"), ("Ceros", "@Cero")],
        mode="mouse"
    )
    p_pie.add_tools(hover)
    
    p_pie.axis.axis_label = None
    p_pie.axis.visible = False
    p_pie.grid.grid_line_color = None
    
    graphs.append(p_pie)

# Agregar todo al layout
curdoc().add_root(column(desc5, *graphs))



'''
GRAFICA 3
'''
# Obtener los géneros únicos
generos = data["gender"].unique()

# Convertir DataFrame a formato compatible con Bokeh (manteniendo todos los puntajes individuales)
data_melted_2 = data.melt(
    id_vars=["username", "gender"], 
    value_vars=eval_columns,  # 🔹 Solo derretir las evaluaciones
    var_name="Evaluación", 
    value_name="Puntaje"
)

# Asegurar que la columna 'gender' sea de tipo string
data_melted_2["gender"] = data_melted_2["gender"].astype(str)
print(data_melted_2)

# Definir colores y marcadores para cada género
marcadores = ["hex", "circle_x", "triangle", "square"]
colores = Category10[len(gender_list)]

# Crear fuente de datos
source_2 = ColumnDataSource(data_melted_2)

# Crear figura
p3 = figure(
    title="Distribución de Puntajes por Género",
    x_range=eval_columns,  # Usar las evaluaciones como categorías en X
    y_range=(0.0, 1.0),
    x_axis_label="Evaluación",
    y_axis_label="Puntaje",
    width=900,
    height=600,
    tools="pan,box_zoom,wheel_zoom,save,reset",
)

# Agregar puntos de dispersión con colores y marcadores por género
p3.scatter(
    x="Evaluación",
    y="Puntaje",
    source=source_2,
    legend_group="gender",  # Usar "gender" porque así está en el DataFrame
    size=10,
    fill_alpha=0.5,
    marker=factor_mark("gender", markers=marcadores[:len(gender_list)], factors=gender_list),
    color=factor_cmap("gender", palette=colores, factors=gender_list)
)

# Configurar leyenda
p3.legend.title = "Género"
p3.legend.location = "top_right"

# Agregar la gráfica al documento sin afectar otras gráficas
# curdoc().add_root(column(desc, p3))