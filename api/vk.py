from api.basic import ApiBasic
from config import TOKEN_VK
from pprint import pprint
import time
from datetime import datetime


class VkApi(ApiBasic):
    host = 'https://api.vk.com'

    def __init__(self, user_id, age_from, age_to, city):
        self.age_from = age_from
        self.age_to = age_to
        self.city = city
        self.ids = user_id
        self.param_vk = {
            'access_token': TOKEN_VK,
            'v': '5.131'
        }

    def get_user(self):
        """Получаем пользователя, используя унаследованный метод _send_request"""

        return self._send_request(
            http_method='GET',
            uri_path='method/users.get',
            params={
                'user_id': self.ids,
                'fields': 'bdate, sex, city',
                **self.param_vk
            },
            response_type='json'
        )['response'][0]

    def user_id(self):
        return self._send_request(
            http_method='GET',
            uri_path='method/users.get',
            params={
                'user_ids': self.ids,
                **self.param_vk
            },
            response_type='json'
        )['response'][0]

    def get_hometown(self):
        return self._send_request(
            http_method='GET',
            uri_path='method/database.getCities',
            params={
                'q': self.city,
                'country_id': 1,
                'count': 1,
                **self.param_vk
            },
            response_type='json'
        )['response']['items']

    def search_users(self):
        return self._send_request(
            http_method='GET',
            uri_path='method/users.search',
            params={
                'count': 5,
                'city': self.get_hometown()[0]['id'],
                'sex': 1,
                'age_from': self.age_from,
                'age_to': self.age_to,
                'fields': 'city',
                **self.param_vk
            },
            response_type='json'
        )['response']['items']

    def photos_albums(self):
        return self._send_request(
            http_method='GET',
            uri_path='method/photos.getAlbums',
            params={
                'owner_id': self.user_id()['response'][0]['id'],
                'photo_sizes': '1',
                **self.param_vk
            },
            response_type='json'
        )

    def get_photo_list(self, search_id):
        return self._send_request(
            http_method='GET',
            uri_path='method/photos.get',
            params={
                **self.param_vk,
                'owner_id': search_id,
                'album_id': 'profile',
                'extended': '1',
                'photo_sizes': '1',
                'count': 10
            },
            response_type='json'
        )


if __name__ == '__main__':
    user_1 = VkApi('mashunya793', 25, 33, 'Нижний Новгород')
    user_2 = VkApi('haritonova_love', 35, 37, 'Волгоград')
    pprint(user_2.get_user())
    pprint(user_1.get_hometown())
    print('--------------------------')
    pprint(user_1.search_users())
