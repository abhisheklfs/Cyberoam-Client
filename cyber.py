#!/usr/bin/python2
# Cyberoam Client main page

#######################################################
# Developed by: abhisheklfs ###########################
# Special Thanks to: Siddhartha Sahu ##################
# idea Given: hari_om #################################
#######################################################
#######################################################
import sys,os,inspect
from PyQt4 import QtGui, QtCore
from PyQt4.uic import loadUi
import urllib , urllib2
import time



class Cyberoam(QtGui.QWidget):
	def __init__(self):
		super(Cyberoam,self).__init__()
		self.initializeWindow()

	def initializeWindow(self):
		##GENERAL VARIALBLES
		self.initSysTray()
		self.xv = 0
		self.status = 0
		self.xyzflag = 0
		self.proffFlag = 0
		self.studentIndex = 0
		self.studentMode = 0
		self.proffMode = 0
		self.proffIndex = 0
		self.proffNumber = []
		self.studentNumber = []
		self.users = []
		self.passwords = []
		self.ntd = 0
		self.userNumber = 0
		self.toDoAction = ['Login','Logout']
		self.path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
		self.x = self.path + '/main1.ui'
		loadUi(self.x,self)
		self.x = self.path + '/setting1.ui'
		self.ui = loadUi(self.x)
		self.timer = QtCore.QTimer(self)
		self.proffTimer = QtCore.QTimer(self)
		self.nonProffTimer = QtCore.QTimer(self)

		##%INITIALIZE MAIN WINDOW(elements)
		self.lineEdit_2.setEchoMode(QtGui.QLineEdit.Password)
		self.lineEdit_2.setPlaceholderText('Password')
		self.lineEdit.setPlaceholderText('Username')
		self.pushButton.setText(self.toDoAction[self.status])
		self.label_4.setText('Client is Idle')
		self.ui.setWindowFlags(self.ui.windowFlags() | QtCore.Qt.CustomizeWindowHint)
		self.ui.setWindowFlags(self.ui.windowFlags() & ~(QtCore.Qt.WindowCloseButtonHint))


		##ACTION HANDLER
		self.pushButton.clicked.connect(self.takeAction)
		self.pushButton_2.clicked.connect(self.addUser)
		self.pushButton_3.clicked.connect(self.closeAction)
		self.pushButton_4.clicked.connect(self.clearDatabase)
		self.pushButton_6.clicked.connect(self.nextUserChange)
		self.pushButton_5.clicked.connect(self.preUserChange)
		self.pushButton_5.setEnabled(False)
		#self.lineEdit_2.returnPressed.connect(self.takeAction)
		#self.lineEdit.returnPressed.connect(self.takeAction)
		self.timer.timeout.connect(self.relogin)
		self.proffTimer.timeout.connect(self.switchToProff)
		self.nonProffTimer.timeout.connect(self.switchToStudent)
		self.checkBox_3.stateChanged.connect(self.modeModify)


		##MAKEVIEW_WINDOW
		self.move(QtGui.QApplication.desktop().screen().rect().center()-self.rect().center())
		self.show()

		##Sync to dataBase
		self.syncData()


	def modeModify(self):
		if len(self.users)==0:
			return
		if self.checkBox_3.isChecked():
			self.tyme = int(time.strftime("%H"))
			if (self.tyme>=0 and self.tyme<7) or (self.tyme<24 and self.tyme >=19):
				self.switchToProff()
				if self.proffFlag == 0:
					self.switchToStudent()
			else:
				self.switchToStudent()

		else:
			self.studentMode = 0
			self.proffMode = 0
		self.setnextpre()

	def setnextpre(self):
		if self.studentMode == 1:
			if self.studentIndex == 0:
				self.pushButton_5.setEnabled(False)
			else:
				self.pushButton_5.setEnabled(True)
			if self.studentIndex == len(self.studentNumber) - 1 or len(self.studentNumber)==0:
				self.pushButton_6.setEnabled(False)
			else:
				self.pushButton_6.setEnabled(True)
		elif self.proffMode == 1:
			if self.proffIndex == 0:
				self.pushButton_5.setEnabled(False)
			else:
				self.pushButton_5.setEnabled(True)
			if self.proffIndex == len(self.proffNumber) - 1 or len(self.proffNumber)==0:
				self.pushButton_6.setEnabled(False)
			else:
				self.pushButton_6.setEnabled(True)
		else:
			if self.userNumber == 0:
				self.pushButton_5.setEnabled(False)
			else:
				self.pushButton_5.setEnabled(True)
			if self.userNumber == len(self.users) - 1 or len(self.users)==0:
				self.pushButton_6.setEnabled(False)
			else:
				self.pushButton_6.setEnabled(True)

	def switchToStudent(self):
		if self.status==1:
			self.logout()
		self.studentMode = 1
		self.proffMode = 0
		self.takeAction()
		self.nonProffTimer.stop()
		self.tyme = self.calTime()
		self.proffTimer.start(self.tyme)

	##switching to proff
	def switchToProff(self):
		if self.proffFlag ==0:
			return
		if self.status==1:
			self.logout()
		self.userNumber = self.proffNumber[self.proffIndex]
		self.proffMode = 1
		self.studentMode = 0
		self.takeAction()
		self.proffTimer.stop()
		self.tyme = self.calTime()
		self.nonProffTimer.start(self.tyme)

	def calTime(self):
		self.secu = int(time.strftime("%S"))
		self.minu = int(time.strftime("%M"))
		self.Hour = int(time.strftime('%H'))
		self.span = 60 - self.secu
		self.span = (60 - self.minu -1)*60 + self.span
		if self.Hour <19 and self.Hour >7:
			self.span = self.span + (19 - self.Hour)*60*60
		else:
			if self.Hour >=19:
				self.span = self.span + (24 - self.Hour + 6)*3600
			else:
				self.span = self.span + (6 - self.Hour)*3600
		return self.span*1000


	##USER Change	
	def nextUserChange(self):
		sender = self.sender()
		if self.status==1:
			self.logout()
		if self.studentMode == 1:
			self.studentIndex = self.studentIndex + 1
		elif self.proffMode == 1:
			self.proffIndex = self.proffIndex + 1
		else:
			self.userNumber = self.userNumber + 1
		self.setnextpre()
		self.xv = 1
		self.takeAction()
		self.xv = 0

	def preUserChange(self):
		if(self.status==1):
			self.logout()
		if self.studentMode == 1:
			self.studentIndex = self.studentIndex - 1
		elif self.proffMode == 1:
			self.proffIndex = self.proffIndex - 1
		else:
			self.userNumber = self.userNumber - 1
		self.setnextpre()
		self.xv = 1
		self.takeAction()
		self.xv = 0

	##defininge event when Enter Key is Pressed	
	def keyPressEvent(self,e):
		if e.key() == 16777220:
			self.takeAction()
		return

	def syncData(self):
		self.savedData = QtCore.QSettings('cyberoam-client','cyber')

		if(self.savedData.contains('n')):
			for i in xrange(int(self.savedData.value('n').toString())):
				self.users.append(str(self.savedData.value('user%d'%i).toString()))
				if len(self.users[i])==5:
					self.proffFlag = 1
					self.proffNumber.append(i)
				else:
					self.studentNumber.append(i)
				self.passwords.append(str(self.savedData.value('password%d'%i).toString()))
			if int(self.savedData.value('n').toString())>0:
				self.lineEdit.setText(self.users[0])
				self.lineEdit_2.setText(self.passwords[0])
				self.xyzflag=1
		if self.savedData.contains('switchProff'):
			if int(self.savedData.value('switchProff').toString())==1:
				self.checkBox_3.setChecked(True)
				self.tyme = int(time.strftime("%H"))
				if(self.tyme<24 and self.tyme > 19) or (self.tyme >=0 and self.tyme<7):
					if self.proffFlag ==1:
						self.userNumber = self.proffNumber[0]
						self.proffMode = 1
						self.studentMode = 0
				else:
					self.studentMode = 1
					self.proffMode = 0
					self.span = 0
					self.secu = int(time.strftime("%S"))
					self.minu = int(time.strftime("%M"))
					self.Hour = int(time.strftime('%H'))
					self.span = self.span + (60 - self.secu)
					self.span = self.span + (60 - self.minu - 1)*60
					self.span = self.span + (19 - self.Hour - 1)*3600
					self.span = self.span * 1000
					self.proffTimer.start(self.span)
		if self.savedData.contains('autoLogin'):
			if int(self.savedData.value('autoLogin').toString())==1:
				self.checkBox.setChecked(True)
		if self.savedData.contains('rememberme'):
			if int(self.savedData.value('rememberme').toString())==1:
				self.checkBox_2.setChecked(True)
		self.setnextpre()

		if self.savedData.contains('autoLogin'):
			if self.savedData.value('autoLogin')==1:
				if len(self.users)==0:
					return
				if self.status == 0:
					return
				self.hide()
				self.tray.show()
			else:
				if self.status==1:
					self.logout()
				self.label_4.setText('Client is Idle')

	##clearing Database
	def clearDatabase(self):
		reply = QtGui.QMessageBox.question(self, "Clear Database", "Are you sure you want to clear all Data?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
		if reply != QtGui.QMessageBox.Yes:
			return
		self.savedData.clear()
		self.savedData.sync()
		if self.status == 1:
			self.logout()
		self.lineEdit.clear()
		self.lineEdit_2.clear()
		self.users = []
		self.passwords = []
		self.studentNumber = []
		self.proffNumber = []
		self.proffIndex = 0
		self.studentIndex = 0
		self.xyzflag = 0
		self.userNumber = 0
		self.ntd = 0
		self.proffFlag = 0
		self.studentMode = 0
		self.proffMode = 0
		self.modeModify()
		self.setnextpre()





	##SystemTray
	def initSysTray(self):
		self.path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
		self.x = self.path + '/cyberoam.png'
		self.tray = QtGui.QSystemTrayIcon(QtGui.QIcon(self.x),self)
		self.options = QtGui.QMenu(self)
		self.x = self.path + '/res.png'
		self.windowAppear = self.options.addAction(QtGui.QIcon(self.x),'Restore')
		self.windowAppear.triggered.connect(self.showWindows)
		self.x = self.path + '/exit.png'
		self.exitEvent = self.options.addAction(QtGui.QIcon(self.x),'Exit')
		self.exitEvent.triggered.connect(self.closeAction)
		self.tray.setContextMenu(self.options)
		self.tray.activated.connect(self.showWindow)

	def showWindow(self, reason ):
		if reason != QtGui.QSystemTrayIcon.DoubleClick:
			return
		self.tray.hide()
		self.showNormal()
		#self.setWindowState(QtCore.Qt.WindowMaximized)

	def showWindows(self):
		self.tray.hide()
		self.showNormal()

	##Closing Event
	def closeEvent(self,event):
		event.ignore()
		self.closeAction()

	##Minimize-Event
	def changeEvent(self, event):
		if event.type() == QtCore.QEvent.WindowStateChange:
			if self.windowState() == QtCore.Qt.WindowMinimized:
				self.hide()
				event.ignore()
				self.tray.show()
				#self.tray.showMessage('Check','Done Checking',1,100000)


	##TakeAction Activity;
	def takeAction(self):
		if self.status == 1:
			self.logout()
			return
		if self.check() == 0:
			return
		if self.xyzflag == 0:
			self.ans = self.preCheck()
			if self.ans == 0:
				return
			self.xyzflag = 1
			self.users.append(str(self.lineEdit.text()))
			self.passwords.append(str(self.lineEdit_2.text()))
			if len(self.users[len(self.users)-1]) == 5:
				self.proffFlag = 1
				self.proffNumber.append(len(self.users)-1)
			else:
				self.studentNumber.append(len(self.users)-1)
			self.setnextpre()
		if self.studentMode == 1:
			self.userNumber = self.studentNumber[self.studentIndex]
		if self.proffMode == 1:
			self.userNumber = self.proffNumber[self.proffIndex]
		if (len(self.users) <= self.userNumber):
			self.label_4.setText('Out of Users')
			self.userNumber = 0
			return
		if(self.userNumber == 0 and self.xv == 0 and (self.users[self.userNumber] != self.lineEdit.text() or self.passwords[self.userNumber] != self.lineEdit_2.text())):
			self.users[self.userNumber] = self.lineEdit.text()
			self.passwords[self.userNumber] = self.lineEdit_2.text()

		self.uid = self.users[self.userNumber]
		self.pid = self.passwords[self.userNumber]
		self.url = 'https://172.16.1.1:8090/httpclient.html'
		self.data = {'mode':'191' , 'username':self.uid , 'password':self.pid }
		self.dataToSend = urllib.urlencode(self.data)
		try:
			self.dataReceived = urllib2.urlopen(self.url , self.dataToSend , timeout = 3).read()
			if 'You have successfully logged in'  in  self.dataReceived:
				self.label_4.setText('Connected')
				self.status = 1
				self.lineEdit.setText(self.users[self.userNumber])
				self.lineEdit_2.setText(self.passwords[self.userNumber])
				self.lineEdit.setReadOnly(True)
				self.lineEdit_2.setReadOnly(True)
				self.pushButton.setText(self.toDoAction[self.status])
			elif 'Your data transfer has been exceeded' in self.dataReceived or 'You have reached Maximum Login Limit' in self.dataReceived:
				if (self.studentMode == 1):
					self.studentIndex = self.studentIndex + 1
					self.userNumber = self.studentNumber[self.studentIndex]
				elif (self.proffMode == 1):
					self.userNumber = self.proffNumber[self.proffIndex]
				else:
					self.userNumber = self.userNumber + 1
				self.setnextpre()
				self.takeAction()
				return
			if self.isHidden() and self.ntd == 1:
				self.tray.showMessage('Reconnected!','Reconnection was done successfully.',1,5000)
				self.ntd = 0
		except IOError:
			self.label_4.setText('Connection Lost')
			self.logout()
			self.timer.start(5000)
			return
		self.timer.start(300000)

	##Re-Login Event
	def relogin(self):
		if self.status==0:
			self.takeAction()
			return

		self.url = 'https://172.16.1.1:8090'
		self.data = {'mode':'192','username':self.users[self.userNumber],'a':(str)((int)(time.time() * 1000))}
		try:
			self.dataReceived = urllib2.urlopen(self.url+'/live?'+urllib.urlencode(self.data)).read()
			if 'Your data transfer has been exceeded' in self.dataReceived or 'You have reached Maximum Login Limit' in self.dataReceived:
				self.logout()
				if (self.studentMode == 1):
					self.studentIndex = self.studentIndex + 1
					self.userNumber = self.studentNumber[self.studentIndex]
				elif (self.proffMode == 1):
					self.userNumber = self.proffNumber[self.proffIndex]
				else:
					self.userNumber = self.userNumber + 1
				self.setnextpre()
				self.takeAction()
				if self.isHidden() == True:
					self.tray.showMessage('Data Limit Exceeded','Urs %s Data Limit has been Exceeded.\n Changing to next User.'%self.users[self.userNumber-1],1,5000 )
				return
			if self.isHidden() and self.ntd == 1:
				self.tray.showMessage('Reconnected!','Reconnection was done successfully.',1,5000)
				self.ntd = 0
		except IOError:
			self.logout()
			self.label_4.setText('Connection Lost')
			if self.isHidden():
				self.tray.showMessage('Connection Lost','Data Connection lost. Will reconnect in 5s.',1,5000)
			self.timer.start(5000)
			self.ntd = 1
			return

	def preCheck(self):
		self.uid = self.lineEdit.text()
		self.pid = self.lineEdit_2.text()
		self.data = {'mode':'191','username':self.uid,'password':self.pid}
		self.dataToSend = urllib.urlencode(self.data)
		self.url = 'https://172.16.1.1:8090/httpclient.html'
		try:
			self.dataReceived = urllib2.urlopen(self.url,self.dataToSend,timeout = 3).read()
			if('You have successfully logged in' in self.dataReceived or 'Your data transfer has been exceeded' in self.dataReceived or 'You have reached Maximum Login Limit' in self.dataReceived):
				self.data = {'mode':'193','username':self.uid}
				self.dataToSend = urllib.urlencode(self.data)
				self.dataReceived = urllib2.urlopen(self.url, self.dataToSend , timeout = 3).read()
				return 1
			else:
				self.label_4.setText("Wrong Main User's Password")
				return 0
		except IOError:
			self.label_4.setText('Connection Lost')
			self.timer.start(100000)
			return 0
	##LOGOUT Event
	def logout(self):
		if self.status == 0:
			return

		self.lineEdit.setReadOnly(False)
		self.lineEdit_2.setReadOnly(False)
		self.status = 0
		self.pushButton.setText(self.toDoAction[self.status])
		self.data = {'mode':'193', 'username':self.users[self.userNumber]}
		self.url = 'https://172.16.1.1:8090/httpclient.html'
		try:
			self.dataReceived = urllib2.urlopen(self.url , urllib.urlencode(self.data) , timeout = 3 ).read()
			if 'You have successfully logged off' in self.dataReceived:
				self.label_4.setText('Logged Out successfully')
		except IOError:
			self.label_4.setText('Connection Lost')
			self.timer.start(100000)
			return
		self.timer.stop()



	##EVENT ON EXIT BUTTON PRESSED
	def closeAction(self):
		reply = QtGui.QMessageBox.question(self, "Exit Cyberoam", "Are you sure you want to quit?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)
		if reply != QtGui.QMessageBox.Yes:
			return
		if(self.status == 1):
			self.logout()
		##Saving settings
		if self.checkBox.isChecked():
			self.savedData.setValue('autoLogin','1')
		else: self.savedData.setValue('autoLogin','0')
		if self.checkBox_3.isChecked():
			self.savedData.setValue('switchProff','1')
		else: self.savedData.setValue('switchProff','0')
		if self.checkBox_2.isChecked():
			n = len(self.users)
			for x in xrange(n):
				self.savedData.setValue('user%d'%x,self.users[x])
				self.savedData.setValue('password%d'%x,self.passwords[x])
			self.savedData.setValue('rememberme','1')
			self.savedData.setValue('n',n)
		else:
			self.savedData.setValue('rememberme','0')
			self.savedData.setValue('n','0')
		self.savedData.sync()

		QtCore.QCoreApplication.instance().quit()

	def check(self):
		if self.lineEdit.text() == "" or self.lineEdit.text() == None:
			self.label_4.setText('Enter Username')
			return 0
		if self.lineEdit_2.text() == "" or self.lineEdit_2.text() == None:
			self.label_4.setText('Enter Password')
			return 0
		return 1

	def addUser(self):
		self.ans=self.check()
		if(self.ans==0):
			return
		if self.xyzflag == 0:
			if (self.preCheck() == 0):
				return
		self.hide()
		self.uiActionMessage = ['Verify','Add']
		self.verificationStatus = 0
		self.ui.pushButton.setText(self.uiActionMessage[self.verificationStatus])
		self.ui.lineEdit_2.setEchoMode(QtGui.QLineEdit.Password)
		self.ui.lineEdit.setPlaceholderText('Username')
		self.ui.lineEdit_2.setPlaceholderText('Password')
		self.ui.move(QtGui.QApplication.desktop().screen().rect().center()-self.rect().center())
		self.ui.show()
		self.ui.pushButton_2.clicked.connect(self.goBack)
		self.ui.pushButton_3.clicked.connect(self.makeNewView)
		self.ui.pushButton.clicked.connect(self.addActions)
		self.ui.label_3.setText("")

	def goBack(self):
		self.show()
		self.ui.hide()
		return

	def makeNewView(self):
		self.ui.lineEdit.clear()
		self.ui.lineEdit_2.clear()
		self.ui.lineEdit_2.setReadOnly(False)
		self.ui.lineEdit.setReadOnly(False)
		self.verificationStatus = 1
		self.ui.label_3.setText("")
		self.ui.pushButton.setText(self.uiActionMessage[self.verificationStatus])
		return

	def uiVerify(self):
		if(self.ui.lineEdit=="" or self.ui.lineEdit==None):
			self.ui.label_3.setText('Enter Username')
			return 0
		elif(self.ui.lineEdit_2=="" or self.ui.lineEdit_2==None):
			self.ui.label_3.setText('Enter Password')
			return 0
		self.ui_username=self.ui.lineEdit.text()
		self.ui_password=self.ui.lineEdit_2.text()
		self.url = 'https://172.16.1.1:8090/httpclient.html'
		self.data = {'mode':'191','username':self.ui_username,'password':self.ui_password}
		self.dataToSend = urllib.urlencode(self.data)
		self.logout()
		try:
			self.dataReceived = urllib2.urlopen(self.url,self.dataToSend, timeout = 3).read()
			if 'You have successfully logged in'  in  self.dataReceived:
				self.data = {'mode':'193','username':self.ui_username }
				self.dataToSend = urllib.urlencode(self.data)
				self.dataReceived = urllib2.urlopen(self.url,self.dataToSend, timeout=3 ).read()
				self.takeAction()
				return 1
			elif 'Make sure your password is correct' in self.dataReceived:
				self.ui.label_3.setText('Verification Status: Failed')
				return 0
		except IOError:
			self.ui.label_3.setText('Connection Lost')
			return 0



	def addActions(self):
		if self.verificationStatus == 0:
			self.ans = self.uiVerify()
			if(self.ans == 1):
				self.verificationStatus = 1
				self.ui.lineEdit.setReadOnly(True)
				self.ui.lineEdit_2.setReadOnly(True)
				self.ui.pushButton.setText(self.uiActionMessage[self.verificationStatus])
				self.ui.label_3.setText('Verification Status: Passed')
		elif self.verificationStatus == 1:
			self.ui_username = self.ui.lineEdit.text()
			self.ui_password = self.ui.lineEdit_2.text()
			if(self.xyzflag==0):
				self.users.append(self.lineEdit.text())
				self.passwords.append(self.lineEdit_2.text())
				self.xyzflag = 1
			if self.ui_username in self.users:
				self.ui.label_3.setText('Already Added')
				self.ui.lineEdit.clear()
				self.ui.lineEdit_2.clear()
				self.ui.lineEdit.setReadOnly(False)
				self.ui.lineEdit_2.setReadOnly(False)
				self.verificationStatus = 0
				self.ui.pushButton.setText(self.uiActionMessage[self.verificationStatus])
				return
			self.users.append(str(self.ui_username))
			self.passwords.append(str(self.ui_password))
			if len(str(self.ui_username)) == 5:
				self.proffFlag = 1
				self.proffNumber.append(len(self.users)-1)
				self.modeModify()
			else:
				self.studentNumber.append(len(self.users)-1)
			self.setnextpre()
			self.verificationStatus = 0
			self.ui.lineEdit.clear()
			self.ui.lineEdit_2.clear()
			self.ui.lineEdit.setReadOnly(False)
			self.ui.lineEdit_2.setReadOnly(False)
			self.ui.pushButton.setText(self.uiActionMessage[self.verificationStatus])
			self.ui.label_3.setText('New User Added')
		return



def main():
	app = QtGui.QApplication(sys.argv)
	system = Cyberoam()
	sys.exit(app.exec_())

if __name__=='__main__':
	main()
