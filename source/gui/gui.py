from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import QtCore
from gui.mainWindow import Ui_MainWindow
from gui.addCommunity import Ui_Add_community
import sys
import main
from vk_send_bot import send_bot


class Main(QMainWindow,Ui_MainWindow):
	def __init__(self):
		super(Main, self).__init__()
		self.setupUi(self)
		self.add_comm = Community()
		self.btn_close.clicked.connect(self.close)
		self.btn_edit_comm.clicked.connect(self.add_comm.show)
		self.add_comm.windowClose.connect(self.update_comm)

		comms = main.read_config()

		for comm, token in comms.items():
			self.combo_comm.addItem(comm, token)
		self.btn_start.clicked.connect(lambda: self.send_mess(self.textEdit_addr.toPlainText(),
															  self.textEdit_mess.toPlainText(),
															  self.combo_comm.currentData()))

	def send_mess(self, addr, mess, token):
		if not addr or not mess or not token:
			self.text_log.appendPlainText('Заполнены не все поля для отправки')
		else:
			send_msg = send_bot(token=token, users=addr, message=mess)
			if send_msg.error is True:
				self.text_log.appendPlainText('Некорректный токен сообщества! \n'
											  'Рассылка невозможна')
			else:
				result = send_msg.send_message()
				self.text_log.appendPlainText('----------    СТАТИСТИКА    ----------\n')
				self.text_log.appendPlainText('Количество пользователей, которым отправлено сообщение:'
											  ' {} ({})'.format(result[0], result[0]+len(result[3])))
				self.text_log.appendPlainText('Количество доставленных сообщений: {}'.format(result[1]))
				self.text_log.appendPlainText('Количество недоставленных сообщений: {}\n'.format(len(result[2])))
				if len(result[2]) != 0:
					self.text_log.appendPlainText('---------------------------------------')
					self.text_log.appendPlainText('Список пользователей, которым недоставлены сообщения:\n')
					for user in result[2]:
						self.text_log.appendPlainText(user)
					self.text_log.appendPlainText('---------------------------------------')
				if result[3]:
					self.text_log.appendPlainText('---------------------------------------')
					self.text_log.appendPlainText('Список проблемных ссылок:\n')
					for user in result[3]:
						self.text_log.appendPlainText(user)
					self.text_log.appendPlainText('---------------------------------------')

	def update_comm(self):
		self.combo_comm.clear()
		comms = main.read_config()
		for comm, token in comms.items():
			self.combo_comm.addItem(comm, token)


class Community(QMainWindow,Ui_Add_community):
	def __init__(self, ):
		super(Community, self).__init__()
		self.setupUi(self)
		self.is_close = False
		self.is_close = self.btn_close.clicked.connect(self.close)
		self.btn_add.clicked.connect(lambda: main.write_config(self.comm_name.text(), self.comm_token.text()))
		self.btn_add.clicked.connect(self.close)
		self.btn_add.clicked.connect(self.comm_name.clear)
		self.btn_add.clicked.connect(self.comm_token.clear)

	windowClose = QtCore.pyqtSignal()

	def closeEvent(self, event):
		self.windowClose.emit()
		return super(Community, self).closeEvent(event)



def start_gui():
	app = QApplication(sys.argv)
	main = Main()
	main.show()
	sys.exit(app.exec_())

if __name__ =="__main__":
	app = QApplication(sys.argv)
	main = Main()
	comm = Community()
	main.show()
	main.btn_edit_comm.clicked.connect(comm.OPEN)
	sys.exit(app.exec_())