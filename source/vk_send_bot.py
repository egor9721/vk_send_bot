import vk_api
from vk_api.longpoll import VkLongPoll
import random 
import re
import urllib.request as req


def acc_check(id):
    address = 'https://vk.com/' + id

    try:
        req.urlopen(address).getcode()
        result = True
    except:
        result = False
    return result


def error_stats(dont_send, dont_exist):
    print('----------------------------------------------------')
    print('         Статистика по ошибкам отправления')
    print('----------------------------------------------------')
    print('\nНедоставленных сообщений:    {}'.format(len(dont_send)))
    print('Несуществующих аккаунтов:    {}'.format(len(dont_exist)))
    print('\n----------------------------------------------------')
    print('Список пользователей, которым не было отправлено сообщение:\n')
    for user in dont_send:
        print(user)
    print('\n----------------------------------------------------')
    print('Список несуществующих аккаунтов:\n')
    for user in dont_exist:
        print(user)
    print('\n----------------------------------------------------')
    pass


class send_bot(object):

    def __init__(self, token, users, message):
        vk_session = vk_api.VkApi(token=token)
        self.longpoll = VkLongPoll(vk_session) # штука для реакции на действия в сообществе
        self.vk = vk_session.get_api()
        self.users = users
        self.message = message

    def list_generator(self):
        print('\nСоздается список пользователей для отправки рассылки')
        users_list = []
        users_id = []
        new_data = []
        error_data = []
        with open(self.users, 'r') as f:
            for line in f:
                users_list.append(line)

        for user in users_list:
            try:
                user = re.sub('\n', '', re.split('com/', user)[1])
            except IndexError:
                pass
            if acc_check(user):
                users_id.append(user)
            else:
                error_data.append('https://vk.com/{}'.format(user))

        for item in users_id:
            if item.startswith(r'id[0-9]'):
                new_data.append(int(re.sub('id', '', item)))
            else:
                new_data.append(self.vk.utils.resolveScreenName(screen_name=item)['object_id'])

        print('\nСписок пользователей для отправки составлен')
        return new_data, error_data
        
    def create_message(self):
        with open(self.message, 'r', encoding='utf-8') as f:
            message_start = f.readlines()

        formatted_mess =''
        for line in message_start:
            formatted_mess = formatted_mess  + line
        return formatted_mess

    def send_message(self):
        recipients, error_data = self.list_generator()
        mess = self.create_message()

        print("\nИдет отправка сообщений")
        count = 0
        dont_send_message = []
        for user in recipients:
            try:
                self.vk.messages.send(user_id=user, message=mess, random_id=random.randint(1, 9999999999))
                count += 1
            except vk_api.exceptions.ApiError:
                dont_send_message.append('vk.com/id{}'.format(user))
        print('Сообщение было доставлено {} пользователь из {}\n'.format(count, len(recipients)))
        
        error_stats(dont_send_message, error_data)
