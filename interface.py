import PySimpleGUI as sg
from vk_send_bot import send_bot
import main


sg.theme('Reddit')


def main_window():
    layout = [
        [sg.Text('Адресаты', size=(15, 1)), sg.InputText(key='destination'), sg.FileBrowse('Поиск')
         ],
        [sg.Text('Сообщение', size=(15, 1)), sg.InputText(key='message.txt'), sg.FileBrowse('Поиск')
         ],
        [sg.Text('Выбор сообщества', size=(20, 1)), sg.Combo(list(main.read_config()), key='community', size=(15, 1)), sg.Button('add')],
        [sg.Output(size=(88, 20))],
        [sg.Submit(), sg.Cancel()]
    ]

    window = sg.Window('VK message.txt bot', layout)
    while True:
        event, values = window.read()
        if event in (None, 'Exit', 'Cancel'):
            break
        if event in 'add':
            add_com()
            window.Element('community').Update(values=list(main.read_config()))
        if event in 'Submit':
            address = values['destination']
            message = values['message.txt']
            comm = values['community']
            if address and message and comm:
                communities = main.read_config()
                token = communities[comm]
                send_msg = send_bot(token=token, users=address, message=message)
                send_msg.send_message()
            else:
                print('не заполнены данные для отправки')

    window.close()


def add_com():
    layout = [
        [sg.Text('Name'), sg.InputText(key='new_com_name')],
        [sg.Text('Token'), sg.InputText(key='new_token')],
        [sg.Submit('Add'), sg.Cancel()]
    ]

    window = sg.Window('Add new community', layout)

    while True:  # The Event Loop
        event, values = window.read()
        if event in (None, 'Exit', 'Cancel'):
            break
        if event == 'Add':
            if values['new_com_name'] and values['new_token']:
                main.write_config(values['new_com_name'], values['new_token'])
                break
            elif not values['new_com_name'] and not values['new_token']:
                print('community name and token is not define')
            elif not values['new_com_name']:
                print('community name is not define')
            elif not values['new_token']:
                print('community token is not define')
    window.close()



