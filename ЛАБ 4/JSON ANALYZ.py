import json

# Файлды оқу
with open('/Users/ramazan/Desktop/лаба/ЛАБ 4/sample-data.json', 'r') as file:
    data = json.load(file)

#Тақырыбын қоямыз
header = "Interface Status\n" + "=" * 86
column_names = "DN                                                 Description           Speed    MTU  "
separator = "-" * 86

# ОБРАБОТКА ДАННЫХ
interface_data = []
for item in data["imdata"]:
    attributes = item["l1PhysIf"]["attributes"]
    dn = attributes["dn"]
    descr = attributes.get("descr", "")
    speed = attributes.get("speed", "")
    mtu = attributes.get("mtu", "")
    interface_data.append(f"{dn:<50} {descr:<20} {speed:<7} {mtu:<5}")

print(header)
print(column_names)
print(separator)
for line in interface_data:
    print(line)
