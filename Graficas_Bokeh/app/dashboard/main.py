import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, Div
from bokeh.palettes import Bright6
from bokeh.transform import factor_cmap
from bokeh.layouts import column
from bokeh.io import curdoc
from math import pi

# Para la dirección del HTML
from os.path import dirname, join

desc = Div(text=open(join(dirname(__file__), "dashboard.html")).read(), sizing_mode="stretch_width")

csv = "../../../CSVs/Unificacar_CSVs/UTPL_CREAA1_2024_2_profile&grade_totalreport_2025.csv"

data = pd.read_csv(csv, delimiter=',')

# Definir el puntaje mínimo requerido
puntaje_minimo = 0.7  

data_filtrada = data[data["EvalSemanal Avg"] < puntaje_minimo]
data_filtrada_apro = data[data["EvalSemanal Avg"] >= puntaje_minimo]

print(data_filtrada.size)

# Definir estados
estados = ["Total", "Aprobado", "Reprobado"]
counts = [data.size, data_filtrada_apro.size, data_filtrada.size]

# Crear la fuente de datos para Bokeh
source = ColumnDataSource(data=dict(estados=estados, counts=counts))

p = figure(x_range=estados, height=350, toolbar_location="right", title="Estudiantes aprobados y reprobados",
        tooltips=[("Estado", "@estados"), ("Cantidas", "@counts")])

p.vbar(x='estados', top='counts', width=0.9, source=source, legend_field="estados",
    line_color='white', fill_color=factor_cmap('estados', palette=Bright6, factors=estados))

p.xgrid.grid_line_color = None
p.legend.orientation = "horizontal"
p.legend.location = "top_center"

curdoc().add_root(column(desc, p))