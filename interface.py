import PySimpleGUI as sg
layout = [
    [sg.Text('Адресаты'), sg.InputText(), sg.FileBrowse('Поиск')
     ],
    [sg.Text('Сообщение'), sg.InputText(), sg.FileBrowse('Поиск')
     ],
    [sg.Output(size=(88, 20))],
    [sg.Submit('Начать рассылку'), sg.Cancel('Выходы')]
]
window = sg.Window('File Compare', layout)
while True:                             # The Event Loop
    event, values = window.read()
    # print(event, values) #debug
    if event in (None, 'Exit', 'Cancel'):
        break