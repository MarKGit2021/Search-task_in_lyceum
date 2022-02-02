import sys
from io import BytesIO

import requests
from PIL import Image


def func(address, key="40d1649f-0493-4b70-98ba-98533de7710b"):
    server = "http://geocode-maps.yandex.ru/1.x/"

    params = {
        "apikey": key,
        "geocode": address,
        "format": "json"}

    res = requests.get(server, params=params)

    json_res = res.json()
    toponym = json_res["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    bounded_by = toponym['boundedBy']['Envelope']
    size1 = [float(i) for i in bounded_by['lowerCorner'].split()]
    size2 = [float(i) for i in bounded_by['upperCorner'].split()]
    size = [str(max(size2[0], size1[0]) - min(size2[0], size1[0])),
            str(max(size2[1], size1[1]) - min(size2[1], size1[1]))]
    return size


if __name__ == '__main__':
    toponym_to_find = " ".join(sys.argv[1:])

    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)
    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    toponym_coodrinates = toponym["Point"]["pos"]
    toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")

    map_params = {
        "ll": ",".join([toponym_longitude, toponym_lattitude]),
        "spn": ",".join(func(toponym_to_find)),
        "l": "map",
        "pt": f"{toponym_longitude},{toponym_lattitude},pm2dgm1"
        }
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)
    Image.open(BytesIO(
        response.content)).show()
