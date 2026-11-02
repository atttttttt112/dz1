import json
import xml.etree.ElementTree as ET

weather = {
    "city": "Москва",
    "temp": -5,
    "humidity": 80,
    "is_snowing": True
}

# JSON
json_data = json.dumps(weather, ensure_ascii=False)
print("JSON:", json_data)
print("Размер JSON:", len(json_data.encode("utf-8")), "байт")

# XML
root = ET.Element("weather")
for key, value in weather.items():
    child = ET.SubElement(root, key)
    child.text = str(value)
xml_data = ET.tostring(root, encoding="unicode")
print("XML:", xml_data)
print("Размер XML:", len(xml_data.encode("utf-8")), "байт")

# Проверка восстановления данных
restored_json = json.loads(json_data)
restored_xml = {child.tag: child.text for child in root}
print("\nВосстановлено из JSON:", restored_json)
print("Восстановлено из XML:", restored_xml)
print("JSON совпадает с исходными данными:", restored_json == weather)
