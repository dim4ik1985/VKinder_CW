import sqlalchemy as sq
import time
from sqlalchemy.orm import sessionmaker
from config import DB_USER_NAME, DB_PASS, DB_NAME
from database.models import create_table, BotUsers, UserSearch, PhotoUsers, FavoritesUsers
from api.vk import VkApi
from pprint import pprint


class DbSession:
    def __init__(self):
        self.db = DB_NAME
        self.user = DB_USER_NAME
        self.password = DB_PASS
        self.driver = 'postgresql'

    def __engine(self):
        DSN = f'{self.driver}://{self.user}:{self.password}@localhost:5432/{self.db}'
        return sq.create_engine(DSN)

    def create_table(self):
        create_table(self.__engine())

    def get_session_start(self):
        Session = sessionmaker(bind=self.__engine())
        self.session = Session()

    def get_session_end(self):
        return self.session.close()

    # Добавление пользователя в БД
    def adding_users(self, vk_user):
        info_user = vk_user.get_user()
        # проверка на дубликат
        res = self.session.query(BotUsers).filter(BotUsers.name == info_user['id']).all()
        if not res:
            if info_user.get('city'):
                user = BotUsers(
                    name=info_user['id'],
                    age=info_user['bdate'],
                    sex=info_user['sex'],
                    hometown=info_user['city']['title']
                )
            else:
                user = BotUsers(
                    name=info_user['id'],
                    age=info_user['bdate'],
                    sex=info_user['sex']
                )
            self.session.add(user)
            self.session.commit()
            return user
        else:  # если пользователь есть в базе
            user = self.session.query(BotUsers).get(self.session.query(BotUsers.id).all()[0][0])
            return user

    # Поиск и запись в БД по параматрам пользователя
    def add_search_users(self, user_vk, user):
        """
        Функция поиска кандидатов по параметрам и занесение в БД
        :param user_vk: Пользователь
        :param user: связь таблиц пользователя и найденных по параметрам
        :return: Данные для связи с таблицей FavoriteUsers
        """
        for item in user_vk.search_users():
            likes_photo = {}
            info_photo = user_vk.get_photo_list(item['id'])
            res = self.session.query(UserSearch).filter(
                UserSearch.url_profile == 'https://vk.com/id' + str(item['id'])).all()
            if not res:
                if item.get('is_closed'):
                    continue
                elif info_photo['response']['count'] >= 3:
                    search_user = UserSearch(
                        f_name=item['first_name'],
                        l_name=item['last_name'],
                        url_profile='https://vk.com/id' + str(item['id']),
                        relations_user=user
                    )
                    self.session.add(search_user)
                    self.session.commit()
                    for item_info in info_photo['response']['items']:
                        likes_photo[item_info['likes']['count']] = item_info['sizes'][-1]['url']
                    sort_dict_photo = dict(sorted(likes_photo.items(), reverse=True)[:3])
                    for url in sort_dict_photo.values():
                        photo_users = PhotoUsers(
                            url_photo=url,
                            relations_user_search=search_user
                        )
                        self.session.add(photo_users)
                        self.session.commit()
                    time.sleep(0.5)
        else:
            search_user = self.session.query(UserSearch).get(self.session.query(UserSearch.id).all()[0][0])
            return search_user

    # Функция добавления в избранное
    def add_favorites_user(self, user_vk, search_user):
        favorite_user = FavoritesUsers(
            users_relat_id=search_user
        )
        return favorite_user

    # Запросы в базу данных
    def get_requests_db(self, user_vk, step=0):
        """
        Запрос в БД для извлечения данных для выборке в приложении
        :param user_vk: пользователь VK
        :param step: смещение шага выбора след кандидата
        :return: отсортированные данные для вывода в Message.search
        """
        return self.session.query(
            UserSearch.f_name,
            UserSearch.l_name,
            UserSearch.url_profile,
            PhotoUsers.url_photo
        ).join(PhotoUsers).join(BotUsers).filter(
            BotUsers.name == user_vk.user_id()['id']
        ).limit(3).offset(step).all()

    # Расчет количества записей
    def get_count(self, user_vk) -> int:
        """
        Подсчет количества выбранных данных для последующего использования.
        :param user_vk: User VK
        :return:
        """
        return self.session.query(UserSearch).join(BotUsers).filter(
            BotUsers.name == user_vk.user_id()['id']).count()


if __name__ == '__main__':
    user_1 = VkApi('dim4ik0985', 30, 35, 'Иваново')
    # user_2 = VkApi('haritonova_love', 30, 35, 'Краснодар')
    # user_3 = VkApi('id688491342', 18, 25, 'Хабаровск')
    # session = DbSession()
    # session.get_session_start()
    # session.create_table()
    # user_db_1 = session.adding_users(user_1)
    # session.add_search_users(user_1, user_db_1)
    # user_db_2 = session.adding_users(user_2)
    # session.add_search_users(user_2, user_db_2)
    # user_db_3 = session.adding_users(user_3)
    # session.add_search_users(user_3, user_db_3)
    # session.add_favorites_user(us)
    # session.get_session_end()
