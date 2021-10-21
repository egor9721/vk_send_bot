import vk_api
from vk_api.longpoll import VkLongPoll
import random
import re
import urllib.request as req
import time


def write_log_file(log_file_name, sent_message, dont_sent_message, dont_exist_message):
    print("Запись в лог: " + str(log_file_name))
    log_file = open(log_file_name, 'w')
    log_file.write("Сообщения отправлены: \n")
    log_file.write("\n".join(sent_message))
    log_file.write("\nСообщения не получилось доставить: \n")
    log_file.write("\n".join(dont_sent_message))
    log_file.write("\nНе удалось найти аккаунт: \n")
    log_file.write("\n".join(dont_exist_message))
    log_file.close()


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
        # штука для реакции на действия в сообществе
        self.longpoll = VkLongPoll(vk_session)
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
                try:
                    user = re.sub('\n', '', re.split('@', user)[1])
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
                try:
                    new_data.append(self.vk.utils.resolveScreenName(
                        screen_name=item)['object_id'])
                except:
                    error_data.append(
                        'https://vk.com/{} - плохая ссылка'.format(item))

        print('\nСписок пользователей для отправки составлен')
        return new_data, error_data

    def create_message(self):
        with open(self.message, 'r', encoding='utf-8') as f:
            message_start = f.readlines()

        formatted_mess = ''
        for line in message_start:
            formatted_mess = formatted_mess + line
        return formatted_mess

    def send_message(self):
        recipients, error_data = self.list_generator()
        mess = self.create_message()

        print("\nИдет отправка сообщений")
        count = 0
        dont_send_message = []
        sent_messages = []
        for user in recipients:
            try:
                self.vk.messages.send(
                    user_id=user, message=mess, random_id=random.randint(1, 9999999999))
                count += 1
                sent_messages.append('vk.com/id{}'.format(user))
            except vk_api.exceptions.ApiError:
                dont_send_message.append('vk.com/id{}'.format(user))
        print('Сообщение было доставлено {} пользователь из {}\n'.format(
            count, len(recipients)))

        error_stats(dont_send_message, error_data)
        write_log_file(self.message + "-" + str(time.time()) + ".log", sent_messages,
                       dont_send_message, error_data)
