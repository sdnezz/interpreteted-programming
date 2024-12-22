import xml.etree.ElementTree as ET

# Загрузка OSM-файла
osm_file = "supermarkets.osm"  # Путь к вашему файлу OSM

# Словарь для подсчета супермаркетов по сетям
supermarkets_by_network = {}

# Чтение и обработка файла
try:
    tree = ET.parse(osm_file)
    root = tree.getroot()

    # Итерация по узлам для поиска супермаркетов
    for element in root.findall(".//node"):
        tags = {tag.attrib['k']: tag.attrib['v'] for tag in element.findall("tag")}

        # Проверяем, является ли объект супермаркетом
        if tags.get("amenity") == "supermarket":
            network = tags.get("network", "Unknown Network")

            # Увеличиваем счетчик для этой сети
            supermarkets_by_network[network] = supermarkets_by_network.get(network, 0) + 1

    # Вывод результатов
    print("Количество супермаркетов по сетям:")
    for network, count in supermarkets_by_network.items():
        print(f"{network}: {count}")

except Exception as e:
    print(f"Ошибка обработки OSM-файла: {e}")
