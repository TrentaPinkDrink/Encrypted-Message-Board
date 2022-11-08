from tkinter import *
from tkinter.messagebox import *
import pymongo
from pymongo import MongoClient
import time

# client = pymongo.MongoClient("")
# copy the mongoDB link here in MongoClient""
db = client['Encryption']
user_collection = db['Users']
message_collection = db['Messages']


class LoginPage(object):
	global user_collection

	def __init__(self, master): #master=None?
		self.root = master
		self.root.geometry("300x150")
		self.user_name = StringVar()
		self.username = self.user_name.get()
		self.user_password = StringVar()
		self.createPage()

	def createPage(self):
		self.page = Frame(self.root)
		self.page.pack()
		Label(self.page).grid(row=0, stick=W)

		Label(self.page, text='Account Name:').grid(row=1, stick=W, pady=10)
		Entry(self.page, textvariable=self.user_name).grid(row=1, column=1, stick=E)
		Label(self.page, text='Password:').grid(row=2, stick=W)
		Entry(self.page, textvariable=self.user_password, show='*').grid(row=2, column=1, stick=E)

		Button(self.page, text='Log in', command=self.loginCheck).grid(row=3, stick=W, pady=10)
		Button(self.page, text='Create Account', command=self.createAccount).grid(row=3, column=1, stick=W)

	def loginCheck(self):
		name = self.user_name.get()
		pw = self.user_password.get()

		found_user = user_collection.find_one({'user_name': name})

		if found_user != None:
			if name == found_user['user_name'] and pw == found_user['user_password']:
				self.page.destroy()
				self.username = self.user_name.get()
				MainPage(self.root, self.username)
			else:
				showinfo(title='Error', message='Incorrect Account Password')
		else:
			showinfo(title='Error', message='Account not found')

	def createAccount(self):
		def subCreate():
			np = new_pwd.get()
			nn = new_name.get()
			if user_collection.find_one({'user_name': nn}) != None:
				showinfo(title='Error', message='Account already exist')
			else:
				showinfo(title='Success', message='Successfully created')
				user_collection.insert_one({'user_name': nn, 'user_password': np})
				window_sign_up.destroy()
		window_sign_up = Toplevel(self.root)
		window_sign_up.geometry('300x200')


		new_name = StringVar()
		Label(window_sign_up).grid(row=0, stick=W, padx=10, pady=10)
		Label(window_sign_up, text='New Account Name：').grid(row=1, stick=W, pady=10, padx=10)
		entry_new_name = Entry(window_sign_up, textvariable=new_name)
		entry_new_name.grid(row=1, column=1, stick=E)

		new_pwd = StringVar()
		Label(window_sign_up, text='Password：').grid(row=2, padx=10, stick=W)
		entry_usr_pwd = Entry(window_sign_up, textvariable=new_pwd, show='*')
		entry_usr_pwd.grid(row=2, column=1, stick=E)

		Button(window_sign_up, text='注册', command=subCreate).grid(row=3, column=1, stick=W)


class MainPage(object):
	global user_collection

	def __init__(self, master, username):
		self.root = master
		self.root.geometry("250x300")
		self.createPage()
		self.username = username

	def createPage(self):
		# self.leaveNotesPage = LeaveNotesPageFrame(self.root)
		# self.checkNotesPage = CheckNotesPageFrame(self.root)
		# self.changePasswordPage = ChangePasswordPageFrame(self.root)
		self.page = Frame(self.root)
		self.page.pack()
		Label(self.page).grid(row=0, stick=W)

		Button(self.page,command=self.enterLeaveMsgPage, text='Check your messages',height= 1, width=20, justify=CENTER).grid(row=1, stick=W, pady=10) # leave notes
		Button(self.page,command=self.enterCheckMsgPage, text="Check others' messages", height= 1, width=20, justify=CENTER).grid(row=2, stick=W, pady=10) # check notes
		Button(self.page,command=self.enterChangePasswordPage, text='Change password', height= 1, width=20, justify=CENTER).grid(row=3, stick=W, pady=10) # change password
		Button(self.page,command=self.enterDeleteUserPage, text='Delete account', height= 1, width=20, justify=CENTER).grid(row=4, stick=W, pady=10) # delete user
		Button(self.page,command=self.enterLogOutPage, text='Log out', height= 1, width=20, justify=CENTER).grid(row=5, stick=W, pady=10) # log out 

	def enterLeaveMsgPage(self):
		self.page.destroy()
		SelfMessagePage(self.root, self.username)

	def enterCheckMsgPage(self):
		self.page.destroy()
		OthersMessagePage(self.root, self.username)

	def enterChangePasswordPage(self):
		changePwWindow = Toplevel(self.root)
		changePwWindow.geometry("300x200")
		Label(changePwWindow, text='Enter new password').grid(row=1)
		changedPwEntry = StringVar()
		Entry(changePwWindow, textvariable=changedPwEntry, show='*').grid(row=1, column=1)
		def change():
			nonlocal changedPwEntry, changePwWindow
			changedPw = changedPwEntry.get()
			user_collection.update_one({'user_name': self.username}, {'$set': {'user_password': changedPw}})
			changePwWindow.destroy()
		Button(changePwWindow, text='Confirm', command=change).grid(row=2)
		

	def enterDeleteUserPage(self):
		deleteUserWindow = Toplevel(self.root)
		deleteUserWindow.geometry("200x100")
		deleteFrame = Frame(deleteUserWindow)
		deleteFrame.pack()
		Label(deleteFrame).grid(row=0)
		Label(deleteFrame, text='Are you sure? All of your current messages will be deleted.').grid(row=1, columnspan=3)
		def yes():
			user_collection.delete_one({'user_name': self.username})
			self.root.destroy()
			LoginPage(Tk())
		def no():
			deleteUserWindow.destroy()
		Button(deleteFrame, text='Yes', command=yes, width=6, height=1).grid(row=2)
		Button(deleteFrame, text='No', command=no, width=6, height=1).grid(row=2, column=2)

	def enterLogOutPage(self):
		self.page.destroy()
		LoginPage(self.root)



class OthersMessagePage(object):
	global message_collection

	def __init__(self, master, username):
		self.root = master
		self.root.geometry("300x200")
		self.others_user_name = StringVar()
		self.current_page_idx = 0
		self.username = username


		self.createPage()

	def createPage(self):
		self.page = Frame(self.root)
		self.page.pack()

		Button(self.page, text='Back', command=self.goBack).grid(row=0, stick=W)
		Label(self.page).grid(row=1, stick=W)
		Label(self.page, text='Whose messages do you want to check?').grid(row=1, column=1, pady=10)

		Label(self.page, text='Enter his account name').grid(row=3, stick=W)
		Entry(self.page, textvariable=self.others_user_name).grid(row=3, column=1, stick=E, pady=10)

		Button(self.page, text='Check', command=self.getMessagesFromOthers).grid(row=4, column=1)


	def goBack(self):
		self.page.destroy()
		MainPage(self.root, self.username)

	def getMessagesFromOthers(self):
		others_name = self.others_user_name.get()
		messages = list(message_collection.find({'user_name': others_name}))

		
		if len(messages) != 0:
			others_message_window = Toplevel(self.root)
			others_message_window.geometry('500x400')
			page_numbers = int(len(messages)/3)
			if len(messages) % 3 == 0 and len(messages) != 0:
				page_numbers -= 1

			def change_text_button(): # message is a list
				nonlocal messages, m1, m1_button, m2, m2_button, m3, m3_button
				msg0 = messages[self.current_page_idx * 3]
				m1['text'] = msg0['time']
				m1_button['state'] = 'active'
				
				try:
					msg1 = messages[self.current_page_idx * 3 + 1]
					m2['text'] = ['time']
					m2_button['state'] = 'active'
				except IndexError:
					m2['text'] = 'There is no other message'
					m2_button['state'] = 'disabled'
				try:
					msg2 = messages[self.current_page_idx * 3 + 2]
					m3['text'] = msg2['time']
					m3_button['state'] = 'active'
				except IndexError:
					m3['text'] = 'There is no other message'
					m3_button['state'] = 'disabled'
				

			def forward():
				if self.current_page_idx < page_numbers:
					self.current_page_idx += 1
					if self.current_page_idx == page_numbers:
						nonlocal forward_button
						forward_button['state'] = 'disabled'
					nonlocal m1, m2, m3, backward_button
					backward_button['state'] = 'active'
					change_text_button()
					


			def backward():
				if self.current_page_idx != 0:
					self.current_page_idx -= 1
					if self.current_page_idx == 0:
						nonlocal backward_button
						backward_button['state'] = 'disabled'
					nonlocal m1, m2, m3, forward_button
					forward_button['state'] = 'active'
					change_text_button()

			def showKeyWindow(msg_idx):
				needKeyWindow = Toplevel(others_message_window)
				needKeyWindow.geometry('200x150')
				needKeyWindowFrame = Frame(needKeyWindow)
				needKeyWindowFrame.pack()
				key = StringVar()
				Label(needKeyWindowFrame, text='Enter the key for this message', justify=CENTER).grid(row=0, stick=W, padx=15, pady=15)
				Entry(needKeyWindowFrame, textvariable=key, justify=CENTER, show='*').grid(row=1, stick=W, padx=15, pady=15)
				Button(needKeyWindowFrame, text='Confirm', justify=CENTER, command=lambda: get_msg(msg_idx)).grid(row=2, stick=W, padx=15, pady=15)

				def dec(message):
					localKey = key.get()
					key_length = len(localKey)
					result_list = []
					for counter, char in enumerate(message):
						loc = counter % key_length
						char_ascii_decoded = chr(ord(char) - ord(localKey[loc]))
						result_list.append(char_ascii_decoded)
					result = ''.join(result_list)
					return result

				def read(msg1):
					if self.username not in msg1['readBy']:
						message_collection.update_one(msg1, {'$push': {'readBy': self.username}})
					nonlocal needKeyWindow
					needKeyWindow.destroy()


				def get_msg(msg_idx):
					nonlocal messages
					needKeyWindowFrame.destroy()
					needKeyWindow.geometry('400x300')
					otherMsgFrame = Frame(needKeyWindow)
					otherMsgFrame.pack()
					msg = messages[msg_idx]
					Label(otherMsgFrame, text=msg['time'], justify=CENTER).grid(row=0)
					Label(otherMsgFrame, text=dec(msg['message']), justify=CENTER, width=50, height=10, bg='#bbd8f2').grid(row=1, columnspan=2)
					Button(otherMsgFrame, text='Mark as read', command=lambda: read(msg)).grid(row=2)
					Label(otherMsgFrame, text=self.username).grid(row=2, column=1)
				

			Label(others_message_window, text=others_name+"'s Message").grid(row=0, column=1)
			backward_button = Button(others_message_window, text='<<', command=backward, state=DISABLED)
			backward_button.grid(row=2)
			forward_button = Button(others_message_window, text='>>', command=forward)
			if page_numbers == 0:
				forward_button['state'] = 'disabled'
			forward_button.grid(row=2, column=4)


			msg0 = messages[0]
			m1 = Label(others_message_window, text=msg0['time'], bg='white', width=40, height=5)
			m1.grid(row=1, column=1)
			m1_button = Button(others_message_window, text='Check', command=lambda: showKeyWindow(0))
			m1_button.grid(row=1, column=2, stick=E)

			try:
				msg1 = messages[1]
				m2 = Label(others_message_window, text=msg1['time'], bg='white', width=40, height=5)
				m2.grid(row=2, column=1)
				m2_button = Button(others_message_window, text='Check', command=lambda: showKeyWindow(1))
				m2_button.grid(row=2, column=2, stick=E)
			except IndexError:
				m2 = Label(others_message_window, text='There is no other message', bg='white', width=40, height=5)
				m2.grid(row=2, column=1)
				m2_button = Button(others_message_window, text='Check', state=DISABLED, command=lambda: showKeyWindow(1))
				m2_button.grid(row=2, column=2, stick=E)
			try:
				msg2 = messages[2]
				m3 = Label(others_message_window, text=msg2['time'], bg='white', width=40, height=5)
				m3.grid(row=3, column=1)
				m3_button = Button(others_message_window, text='Check', command=lambda: showKeyWindow(2))
				m3_button.grid(row=3, column=2, stick=E)
			except:
				m3 = Label(others_message_window, text='There is no other message', bg='white', width=40, height=5)
				m3.grid(row=3, column=1)
				m3_button = Button(others_message_window, text='Check', state=DISABLED, command=lambda: showKeyWindow(2))
				m3_button.grid(row=3, column=2, stick=E)



		else:
			showinfo(title='Error', message='This user does not have any message')


class SelfMessagePage(object):
	def __init__(self, master, username):
		self.root = master
		self.root.geometry("500x400")
		self.username = username
		self.messages = list(message_collection.find({'user_name': username}))
		self.page_numbers = int(len(self.messages) / 3)
		if len(self.messages) % 3 == 0 and len(self.messages) != 0:
			self.page_numbers -= 1
		self.current_page_idx = 0
		self.createPage()



	def createPage(self):
		self.page = Frame(self.root)
		self.page.pack()

		def leaveMessageWindow():
			createMsg = Toplevel(self.page)
			createMsg.geometry('500x400')
			createMsgFrame = Frame(createMsg)
			createMsgFrame.pack()

			Label(createMsgFrame).grid(row=0)

			msgContentEntry = Text(createMsgFrame, height=20, width=60)
			msgContentEntry.grid(columnspan=2, row=1)
			

			Label(createMsgFrame, text='Key').grid(row=2)
			encKeyEntry=StringVar()
			Entry(createMsgFrame, textvariable=encKeyEntry).grid(row=2, column=1)
			

			def enc(message, key1):
				key_length = len(key1)
				result_list = []
				for counter, char in enumerate(message):
					loc = counter % key_length
					char_ascii_encoded = chr(ord(char) + ord(key1[loc]))
					result_list.append(char_ascii_encoded)
				result = ''.join(result_list)
				return result


			def leaveMessage():
				nonlocal msgContentEntry, encKeyEntry
				message_before_encoding = msgContentEntry.get(1.0, 'end-1c')
				encKey=encKeyEntry.get()
				message_after_encoding = enc(message_before_encoding, encKey)
				now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
				print(now)
				message_collection.insert_one({'user_name':self.username, 'message':message_after_encoding, 'time':now, 'readBy': []})
				self.page.destroy()
				SelfMessagePage(self.root, self.username)
				

			Button(createMsgFrame, text='Confrim', command=leaveMessage).grid(row=4, column=1)



		Button(self.page, text='Back', command=self.goBack).grid(row=0, stick=W)
		Button(self.page, text='Create new message', command=leaveMessageWindow).grid(row=4)

		if len(self.messages) != 0:

			def clear():
				confirmClearWindow = Toplevel(self.page)
				confirmClearWindow.geometry('200x150')
				confirmFrame = Frame(confirmClearWindow)
				confirmFrame.pack()
				Label(confirmFrame, text='Are you sure?').grid(row=0, columnspan=3)

				def no():
					nonlocal confirmClearWindow
					confirmClearWindow.destroy()

				def yes():
					message_collection.delete_many({'user_name':self.username})
					self.page.destroy()
					SelfMessagePage(self.root, self.username)

				Button(confirmFrame, text='Yes', command=yes, width=6).grid(row=1)
				Button(confirmFrame, text='No', command=no, width=6).grid(row=1, column=2)


			Label(self.page, text=self.username + "'s message").grid(row=0, column=1, pady=10)
			Button(self.page, text='Clear All', command=clear).grid(row=4, column=4)
			def showKeyWindow(msg_idx):
				needKeyWindow = Toplevel(self.page)
				needKeyWindow.geometry('200x150')
				needKeyWindowFrame = Frame(needKeyWindow)
				needKeyWindowFrame.pack()
				key = StringVar()
				Label(needKeyWindowFrame, text='Enter the key for this message', justify=CENTER).grid(row=0, stick=W, padx=15, pady=15)
				Entry(needKeyWindowFrame, textvariable=key, justify=CENTER, show='*').grid(row=1, stick=W, padx=15, pady=15)
				Button(needKeyWindowFrame, text='Confirm', justify=CENTER, command=lambda: get_msg(msg_idx)).grid(row=2, stick=W, padx=15, pady=15)


				def dec(message, key1):
					key_length = len(key1)
					result_list = []
					for counter, char in enumerate(message):
						loc = counter % key_length
						char_ascii_decoded = chr(ord(char) - ord(key1[loc]))
						result_list.append(char_ascii_decoded)
					result = ''.join(result_list)
					return result

				def delete(msg1):
					nonlocal needKeyWindowFrame
					message_collection.delete_one(msg1)
					self.page.destroy()
					SelfMessagePage(self.root, self.username)

				def get_msg(msg_idx):
					nonlocal needKeyWindowFrame
					needKeyWindowFrame.destroy()
					needKeyWindow.geometry('400x300')
					myMsgFrame = Frame(needKeyWindow)
					myMsgFrame.pack()
					decKey = key.get()
					msg = self.messages[msg_idx]
					Label(myMsgFrame, text=msg['time'], justify=CENTER).grid(row=0)
					Label(myMsgFrame, text=dec(msg['message'], decKey), bg='#abedd6', justify=CENTER, width=40, height=10).grid(row=1, columnspan=3)
					Button(myMsgFrame, text='Delete this one', command=lambda: delete(msg)).grid(row=2)
					Label(myMsgFrame, text=self.username).grid(row=2, column=1)
					readers = ', '.join([reader for reader in msg['readBy']])
					if len(readers) != 0:
						Label(myMsgFrame, text=readers + '  had read this message').grid(row=3)
					else:
						Label(myMsgFrame, text='No one had read this message').grid(row=3)

			def change_text_button(): # message is a list
				nonlocal m1, m1_button, m2, m2_button, m3, m3_button
				msg0 = self.messages[self.current_page_idx * 3]
				m1['text'] = msg0['time']
				m1_button['state'] = 'active'
				
				try:
					msg1 = self.messages[self.current_page_idx * 3 + 1]
					m2['text'] = msg1['time']
					m2_button['state'] = 'active'
				except IndexError:
					m2['text'] = 'There is no other message'
					m2_button['state'] = 'disabled'
				try:
					msg2 = self.messages[self.current_page_idx * 3 + 2]
					m3['text'] = msg2['time']
					m3_button['state'] = 'active'
				except IndexError:
					m3['text'] = 'There is no other message'
					m3_button['state'] = 'disabled'

			def forward():
				if self.current_page_idx < self.page_numbers:
					self.current_page_idx += 1
					if self.current_page_idx == self.page_numbers:
						nonlocal forward_button
						forward_button['state'] = 'disabled'
					nonlocal m1, m2, m3, backward_button
					backward_button['state'] = 'active'
					change_text_button()
					


			def backward():
				if self.current_page_idx != 0:
					self.current_page_idx -= 1
					if self.current_page_idx == 0:
						nonlocal backward_button
						backward_button['state'] = 'disabled'
					nonlocal m1, m2, m3, forward_button
					forward_button['state'] = 'active'
					change_text_button()

			message_frame = Frame(self.root)
			message_frame.pack()
			backward_button = Button(self.page, text='<<', command=backward, state=DISABLED)
			backward_button.grid(row=2)
			forward_button = Button(self.page, text='>>', command=forward)
			if self.page_numbers == 0:
				forward_button['state'] = 'disabled'
			forward_button.grid(row=2, column=4)

			msg0 = self.messages[0]
			m1 = Label(self.page, text=msg0['time'], bg='white', width=40, height=5)
			m1.grid(row=1, column=1)
			m1_button = Button(self.page, text='Check', command=lambda: showKeyWindow(0))
			m1_button.grid(row=1, column=2, stick=E)

			try:
				msg1 = self.messages[1]
				m2 = Label(self.page, text=msg1['time'], bg='white', width=40, height=5)
				m2.grid(row=2, column=1)
				m2_button = Button(self.page, text='Check', command=lambda: showKeyWindow(1))
				m2_button.grid(row=2, column=2, stick=E)
			except IndexError:
				m2 = Label(self.page, text='There is no other message', bg='white', width=40, height=5)
				m2.grid(row=2, column=1)
				m2_button = Button(self.page, text='Check', state=DISABLED, command=lambda: showKeyWindow(1))
				m2_button.grid(row=2, column=2, stick=E)
			try:
				msg2 = self.messages[2]
				m3 = Label(self.page, text=msg2['time'], bg='white', width=40, height=5)
				m3.grid(row=3, column=1)
				m3_button = Button(self.page, text='Check', command=lambda: showKeyWindow(2))
				m3_button.grid(row=3, column=2, stick=E)
			except:
				m3 = Label(self.page, text='There is no other message', bg='white', width=40, height=5)
				m3.grid(row=3, column=1)
				m3_button = Button(self.page, text='Check', state=DISABLED, command=lambda: showKeyWindow(2))
				m3_button.grid(row=3, column=2, stick=E)




		else:
			Label(self.page, text='You do not have any message yet').grid(row=0, column=1)


	def goBack(self):
		self.page.destroy()
		MainPage(self.root, self.username)


if __name__ == "__main__":
	root = Tk()
	root.title('Secrets')
	LoginPage(root)
	root.mainloop()
