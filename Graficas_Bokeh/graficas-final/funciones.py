import pandas as pd
import json
from collections import defaultdict
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.plotting import figure
from bokeh.layouts import column, row
from bokeh.palettes import Spectral4

def cargar_json(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return pd.DataFrame(data)


def contar_usuarios_unicos_por_video(df_json, interaccion="play_video"):
    usuarios_por_video = defaultdict(set)

    for _, row in df_json.iterrows():
        if row.get("name") == interaccion:
            try:
                evento = json.loads(row.get("event", "{}"))
                codigo = evento.get("code")
                usuario = row.get("username")
                if codigo and usuario:
                    usuarios_por_video[codigo].add(usuario)
            except json.JSONDecodeError:
                continue

    # Contar únicos
    return {codigo: len(usuarios) for codigo, usuarios in usuarios_por_video.items()}


def calcular_estado_aprobacion(data, columnas_promedio, umbral=0.7):
    data["promedio"] = data[columnas_promedio].mean(axis=1)
    aprobados = data[data["promedio"] >= umbral].shape[0]
    reprobados = data[data["promedio"] < umbral].shape[0]
    return aprobados, reprobados


def generar_pie_data(aprobados, reprobados):
    total = aprobados + reprobados
    if total == 0:
        return pd.DataFrame(columns=["Estado", "Cantidad", "Porcentaje", "angle", "color"])

    data = pd.DataFrame({
        "Estado": ["Aprobado", "Reprobado"],
        "Cantidad": [aprobados, reprobados]
    })
    data["Porcentaje"] = data["Cantidad"] / total
    data["angle"] = data["Porcentaje"] * 2 * 3.1416
    data["color"] = ["#66c2a5", "#fc8d62"]  # Verde y coral
    return data


def mapear_codigos_a_nombres(diccionario_codigos):
    return {v: k for k, v in diccionario_codigos.items()}


def preparar_datos_linea(ed1, ed2, codigo_a_nombre):
    codigos = set(ed1.keys()).union(set(ed2.keys()))
    nombres = [codigo_a_nombre.get(codigo, codigo) for codigo in codigos]
    valores_ed1 = [ed1.get(codigo, 0) for codigo in codigos]
    valores_ed2 = [ed2.get(codigo, 0) for codigo in codigos]

    return pd.DataFrame({
        "Video": nombres,
        "Edición 1": valores_ed1,
        "Edición 2": valores_ed2
    })


def calcular_promedios(df, columnas):
    return [df[col].mean() * 10 for col in columnas]


def preparar_dataframe_conjunto(df1, df2, excluir_ceros=False):
    if excluir_ceros:
        df1 = df1[df1["grade"] > 0]
        df2 = df2[df2["grade"] > 0]

    # Columnas por semana
    eval_cols_ed1 = [f"EvalSemanal 0{i}" for i in range(1, 5)]
    auto_cols_ed1 = [f"FormAutoevaluacion 0{i}" for i in range(1, 5)]

    eval_cols_ed2 = [f"EvalSemanal 0{i}" for i in range(1, 5)]
    auto_cols_ed2 = [f"FormAutoevaluacion 0{i}" for i in range(1, 5)]
    lud_cols_ed2 = [f"EvalLud 0{i}" for i in range(1, 3)]  # Solo hay dos lúdicas

    # Calcular promedios
    evaluaciones_ed1 = calcular_promedios(df1, eval_cols_ed1)
    autoeval_ed1 = calcular_promedios(df1, auto_cols_ed1)

    evaluaciones_ed2 = calcular_promedios(df2, eval_cols_ed2)
    autoeval_ed2 = calcular_promedios(df2, auto_cols_ed2)
    ludicas_ed2 = calcular_promedios(df2, lud_cols_ed2)

    semanas = ['Semana 1', 'Semana 2', 'Semana 3', 'Semana 4']
    ediciones = ['Edición 1', 'Edición 2']

    data = {
        'Semana': semanas * 2,
        'Edición': ['Edición 1'] * 4 + ['Edición 2'] * 4,
        'Evaluaciones': evaluaciones_ed1 + evaluaciones_ed2,
        'Autoevaluaciones': autoeval_ed1 + autoeval_ed2,
        'Lúdicas': [0, 0, 0, 0] + ludicas_ed2 + [0, 0]  # solo hay dos semanales lúdicas
    }

    return pd.DataFrame(data)


# ---------------------- GRAFICAR CON Y SIN  ----------------------

def generar_graficas(actividad_df, titulo_sufijo=""):
    semanas = ['Semana 1', 'Semana 2', 'Semana 3', 'Semana 4']
    ediciones = ['Edición 1', 'Edición 2']
    colors = Spectral4
    
    # 📈 Gráfico de líneas
    p_line = figure(title=f"Promedio semanal por tipo de actividad {titulo_sufijo}", x_range=semanas, height=400, width=600)

    for i, tipo in enumerate(['Evaluaciones', 'Autoevaluaciones', 'Lúdicas']):
        for edicion in ediciones:
            if tipo == 'Lúdicas' and edicion == 'Edición 1':
                continue
            subset = actividad_df[actividad_df['Edición'] == edicion]
            source = ColumnDataSource(subset)
            p_line.line(x='Semana', y=tipo, source=source, legend_label=f"{tipo} ({edicion})", color=colors[i], line_width=2)
            p_line.circle(x='Semana', y=tipo, source=source, color=colors[i], size=6)

    # print(source.data)
    
    p_line.yaxis.axis_label = "Promedio sobre 10"
    p_line.legend.location = "bottom_left"
    p_line.legend.click_policy="mute"
    p_line.add_tools(HoverTool(tooltips=[("Semana", "@Semana"), ("Promedio Evaluacion", "@Evaluaciones{0.00}"), ("Promedio Autoevaluacion", "@Autoevaluaciones{0.00}"), ("Promedio Act. Lúdica", "@Lúdicas{0.00}")], mode='mouse', point_policy='follow_mouse', show_arrow=False,))

    # 📊 Barras apiladas
    from bokeh.transform import dodge

    semana_labels = [f"{semana} ({edicion})" for edicion in ediciones for semana in semanas]
    actividad_stacked = pd.DataFrame({
        'Semana': semana_labels,
        'Evaluaciones': actividad_df['Evaluaciones'],
        'Autoevaluaciones': actividad_df['Autoevaluaciones'],
        'Lúdicas': actividad_df['Lúdicas']
    })

    source_stacked = ColumnDataSource(actividad_stacked)

    p_stack = figure(x_range=semana_labels, title=f"Promedio por tipo de actividad y semana {titulo_sufijo}", height=500, width=1000, toolbar_location=None)

    renderers = p_stack.vbar_stack(
        ['Evaluaciones', 'Autoevaluaciones', 'Lúdicas'],
        x='Semana', width=0.9, color=colors[:3], source=source_stacked,
        legend_label=['Evaluaciones', 'Autoevaluaciones', 'Lúdicas']
    )

    p_stack.add_tools(HoverTool(tooltips=[("Tipo", "$name"), ("Promedio", "@$name{0.0}")], renderers=renderers))

    p_stack.y_range.start = 0
    p_stack.yaxis.axis_label = "Promedio sobre 10"
    p_stack.xaxis.major_label_orientation = 1
    p_stack.legend.location = "top_right"
    p_stack.legend.click_policy="mute"

    return column(row(p_line, p_stack))
