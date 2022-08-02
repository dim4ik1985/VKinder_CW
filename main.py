from api.vk import VkApi
from database.db_class_version import DbSession
from pprint import pprint

if __name__ == '__main__':
    q = input("Начнем?(д/н): ").lower()               # проверка если человек будет жать на другой раскладке
    user_1 = VkApi('dim4ik0985', 35, 37, 'Иваново')   # Тестовые данные
    session = DbSession()                             # Создаем сессию sqlalchemy
    session.get_session_start()
    session.create_table()                            # Строим таблицы из models.py
    user_db_1 = session.adding_users(user_1)          # Создаем экземпляр пользователя в БД
    session.add_search_users(user_1, user_db_1)       # Поиск по парметрам и занесение в БД кандидатов и их фото
    dict_users = {'url': []}                          # Словарь для времнного хранения информации по кандидатам (для кнопок NEXT)
    counter = session.get_count(user_1)               # Счетчик количества кандидатов в БД
    step = 0                                          # Шаг смещения
    while counter > 0 and (q in 'lyynдн'):            # Цикл для выбора кандидатов
        for item in session.get_requests_db(user_1, step):
            if item[2] in dict_users.values():
                dict_users['url'].append(item[3])
            else:
                dict_users['f_name'] = item[0]
                dict_users['l_name'] = item[1]
                dict_users['id'] = item[2]
                dict_users['url'].append(item[3])
        step += 3                    # Смещение поиска
        counter -= 1                 # Счетчик запросов
        pprint(dict_users)           # Выдает инфу для message.search
        dict_users = {'url': []}     # Обнуляет словарь для след запроса
    #     # q_favorites = True
    #     button_next = True
    #     button_stop = True
    #     pprint(dict_users)
    #     if q_favorites:
    #         add_favorites_user()
    #         dict_users = {'url': []}
    #     else:
    #         dict_users = {'url': []}
    #     if button_next:
    #         continue
    #     elif button_stop:
    #         break
    # else:
    #     print('Bay')
    session.get_session_end()
