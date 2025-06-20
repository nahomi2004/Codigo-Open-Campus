import json
import pandas as pd
from collections import defaultdict
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Select
from bokeh.layouts import column
from bokeh.io import curdoc
from bokeh.palettes import Category10
from bokeh.transform import factor_cmap, dodge

# Direccionar al html
from os.path import dirname, join
from bokeh.models import Div
desc = Div(text=open(join(dirname(__file__), "TituloIntACCS1.html")).read(), sizing_mode="stretch_width")

# Ejemplo de uso:
codigo_a_nombre = {
    "video_intro": "vKq2NotGPJQ",
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
    "LR_2_Video1_Semana1": "leg7NPlfNf0",
    "LR_2_Video2_Semana1": "avTMbQWrFgM",
    "LR_2_Video3_Semana1": "cNoUwGM1DQs",
    "LR_2_Video4_Semana1": "6Mst559v-Uc",
    "LR_2_Video5_Semana1": "CNQpefXv5DY",
    "LR_2_Video_Semana1": "6W1_fBZFqns",
    "LR_1_Video1_Semana2": "o5VwDVJ7N3Q",
    "LR_1_Video2_Semana2": "LluqYlh2xg4",
    "LR_1_Video3_Semana2": "eE658thjDj8",
    "LR_1_Video4_Semana2": "QbEpClHzTeM",
    "LR_1_Video5_Semana2": "MCG0or2ULB4",
    "LR_1_Video6_Semana2": "ol-vGTdHBNU",
    "LR_1_Video7_Semana2": "WTXS0IMQ3Ss",
    "LR_1_Video8_Semana2": "9kqXmM3b3wc",
    "VS1_Video1_Semana2": "_zQHV3vCGpA",
    "VS2_Video2_Semana2": "RropOrUc2AE",
    "Video1_Semana3": "VGHSSIUyFhI",
    "Video1_Semana4": "kyGRuJXaboU",
}

# Lista de interacciones relacionadas con videos
interacciones_video = ["play_video", "pause_video", "seek_video", "stop_video"]

# Cargar datos JSON
json_path = "../../../Jsonl/course-creaaa1/course-creaaa1-limpio.json"
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)
    
# Convertir a DataFrame
data = pd.DataFrame(data)

# Función para contar interacciones
def contar_interacciones(data, interacciones):
    conteos = defaultdict(lambda: defaultdict(int))
    for _, row in data.iterrows():
        if row.get("name") in interacciones:
            try:
                evento_json = json.loads(row.get("event", '{}'))
                codigo_video = evento_json.get("code", "")
                if codigo_video:
                    conteos[row.get("name")][codigo_video] += 1
            except json.JSONDecodeError as e:
                print(f"Error al decodificar línea: {e}")
    return conteos

# Convertir los códigos de video a nombres
def convertir_codigos_a_nombres(datos_eventos, mapeo_codigos):
    codigo_a_nombre = {codigo: nombre for nombre, codigo in mapeo_codigos.items()}
    
    datos_con_nombres = {
        evento: {
            codigo_a_nombre.get(codigo, f"Desconocido ({codigo})"): conteo
            for codigo, conteo in conteos.items()
        } for evento, conteos in datos_eventos.items()
    }
    return datos_con_nombres

# Obtener los conteos y convertir los códigos
conteos = contar_interacciones(data, interacciones_video)
conteos_con_nombres = convertir_codigos_a_nombres(conteos, codigo_a_nombre)

# Fuente de datos para Bokeh
df_conteos = pd.DataFrame(conteos_con_nombres).fillna(0)

# Fuente de datos inicial para Bokeh
source = ColumnDataSource(data=dict(videos=[], interacciones=[]))

# Crear gráfico
p = figure(
    x_range=list(codigo_a_nombre.keys()),
    title="Interacciones por Video",
    x_axis_label="Videos",
    y_axis_label="Reproducciones",
    width=800,
    height=400,
    tools="pan,box_zoom,wheel_zoom,save,reset",
    toolbar_location="right",
)
p.xaxis.major_label_orientation = 1.0
p.vbar(x="videos", top="interacciones", source=source, width=0.6, color="dodgerblue")

# Función para actualizar gráfica
def actualizar_grafica(attr, old, new):
    accion = select.value  # Obtener acción seleccionada
    if accion in conteos_con_nombres:
        videos = list(conteos_con_nombres[accion].keys())
        interacciones = list(conteos_con_nombres[accion].values())
    else:
        videos, interacciones = [], []

    source.data = dict(videos=videos, interacciones=interacciones)
    p.x_range.factors = videos  # Actualizar rango del eje X
    
# Dropdown para seleccionar interacción
select = Select(title="Selecciona una interacción:", value=interacciones_video[0], options=interacciones_video)
select.on_change("value", actualizar_grafica)
    
'''
GRAFICA 2
'''
# Obtener la lista de videos y tipos de interacciones
videos = list(codigo_a_nombre.keys())
interacciones = list(conteos_con_nombres.keys())

# Construir datos en formato adecuado
data2 = {"videos": videos}
for interaccion in interacciones:
    data2[interaccion] = [
        conteos_con_nombres[interaccion].get(video, 0) for video in videos
    ]

# Crear una nueva fuente de datos
source2 = ColumnDataSource(data=data2)

# Crear la nueva figura para interacciones agrupadas
p1 = figure(
    x_range=videos, 
    title="Interacciones totales por Video",
    x_axis_label="Videos",
    y_axis_label="Cantidad de Interacciones",
    width=1700,
    height=800,
    tools="pan,box_zoom,wheel_zoom,save,reset",
    toolbar_location="right",
)

p1.xaxis.major_label_orientation = 1.0

# Usar colores para cada interacción
colors = Category10[len(interacciones)]

# Ancho y desplazamiento para que las barras no se sobrepongan
width = 0.2  
offsets = [dodge("videos", (i + 0.3) * width - (width * len(interacciones) / 2), range=p1.x_range) for i in range(len(interacciones))]

# Agregar barras agrupadas
for i, interaccion in enumerate(interacciones):
    p1.vbar(
        x=offsets[i], 
        top=interaccion, 
        source=source2, 
        width=width, 
        color=colors[i], 
        legend_label=interaccion
    )

p1.legend.title = "Tipos de Interacción"
p1.legend.location = "top_right"

# Diseño y actualización inicial
layout = column(desc, select, p, p1)
curdoc().add_root(layout)
curdoc().title = "Interacciones Video"

# Llamar la función de actualización para que la gráfica tenga datos al inicio
actualizar_grafica(None, None, interacciones_video[0])