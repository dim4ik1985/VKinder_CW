import requests


class HttpException(Exception):
    """Класс исключения, выбрасываем, когда API возвращает ошибку"""

    def __init__(self, status, message=''):
        self.status = status
        self.message = message

    def __str__(self):
        return f'http error: {self.status}\n{self.message}'


class ApiBasic:
    """Базовый класс API от него унаследуются Клиент VK и Yandex"""
    host = ''

    def _send_request(self, http_method, uri_path, params=None, headers=None, json=None, response_type=None):
        """
        Через этот метод будут отправляться все запросы ко всем API.
        Здесь мы можем обрабатывать любые исключения, логировать запросы и т.п.

        :param http_method: GET/POST/PUT/PATCH/DELETE
        :param uri_path: uri API, например method/users.get
        :param params:
        :param json:
        :param response_type: тип ответа, например json
        :return:
        """
        response = requests.request(http_method, f'{self.host}/{uri_path}', params=params, headers=headers,
                                    json=json)  # отправляем запрос
        if response.status_code >= 400:
            # если с сервера приходит ошибка выбрасываем исключение
            raise HttpException(response.status_code, response.text)
        if response_type == 'json':
            response = response.json()
        if response_type == 'status_code':
            response = response.status_code
        return response
