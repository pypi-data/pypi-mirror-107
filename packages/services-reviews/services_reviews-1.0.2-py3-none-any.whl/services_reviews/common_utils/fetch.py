import requests


def get(url, params={}):
    """отправка гет запроса по урлу"""
    response = requests.get(url, params)
    return response.text
