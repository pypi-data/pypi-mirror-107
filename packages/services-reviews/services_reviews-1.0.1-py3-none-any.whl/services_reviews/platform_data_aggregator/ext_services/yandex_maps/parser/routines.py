import urllib.parse

def generate_s(local_url):
    """ функция, которая определяет параметр s """
    const_first = 5381
    const_second = 33
    n = const_first
    for char in local_url:
        n = const_second * n ^ ord(char)
    return rshift(n, 0)


def rshift(val, n):
    return (val % 0x100000000) >> n


def generate_s_by_params(params: dict):
    """ определяет параметр s на основе переданных query параметров """
    sorted_params = sorted(params.items())  # важен порядок параметров
    local_url = urllib.parse.urlencode(sorted_params)   # включает в себя кодирование символов
    return generate_s(local_url)
