import json

# Rutas de los archivos
input_file = "Open-Campus-Bokeh\Jsonl\course-creaaa1\course-creaaa1.txt" 
output_file = "Open-Campus-Bokeh\Jsonl\course-creaaa1\course-creaaa1-limpio.json"

# Leer el archivo JSONL
with open(input_file, "r", encoding="utf-8") as infile:
    data = [json.loads(line) for line in infile]

# Guardar como JSON
with open(output_file, "w", encoding="utf-8") as outfile:
    json.dump(data, outfile, indent=4, ensure_ascii=False)

print(f"Archivo convertido exitosamente a {output_file}")
