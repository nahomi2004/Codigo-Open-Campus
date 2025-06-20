import json

input_file = r"Jsonl/course-v1_/course-v1_UTPL_CREAA2_2025_1.txt" 
output_file = r"Jsonl/course-v1_/course-v1_UTPL_CREAA2limpio.json"

with open(input_file, "r", encoding="utf-8") as infile:
    data = []
    for line in infile:
        idx = line.find('{')
        if idx != -1:
            json_str = line[idx:]
            try:
                json_obj = json.loads(json_str)
                data.append(json_obj)
            except json.JSONDecodeError as e:
                print(f"Error parseando línea: {e}")
                continue

with open(output_file, "w", encoding="utf-8") as outfile:
    json.dump(data, outfile, indent=4, ensure_ascii=False)

print(f"Archivo convertido exitosamente a {output_file}")

