import json
import os

with open(os.path.join("maps", "level1", "level1.json"), "r", encoding="UTF-8") as fp:
    json_data = fp.read()

a = json.loads(json_data)
print(a)