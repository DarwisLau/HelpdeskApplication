from kivy.lang import Builder
from kivymd.app import MDApp
from validate_email import validate_email
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.properties import ObjectProperty
import random
from LoginAndRegister import registerUser

user_email = None
user_password = None
user_reenter_password = None
user_captcha = None

user_login_email = None
user_login_password = None

current_user_email = None
current_user_role = None

text = 'abcdefghijklmnopqrstuvxyz0123456789'


class MainApp(MDApp):
	
	def build(self):
		self.theme_cls.theme_style = "Dark"
		self.theme_cls.primary_palette = "DeepPurple"
		return Builder.load_file("MultScreen.kv")

	def verify_login_email(self):

		LoginWindow_instance = self.root.get_screen("Login")

		global user_login_email

		if len(LoginWindow_instance.ids.login_email.text) > 150:
                        LoginWindow_instance.ids.login_email_error.text = "The character limit for email address is 150."
                        user_login_email = 0
                elif len(LoginWindow_instance.ids.login_email.text) == 0:
                        LoginWindow_instance.ids.login_email_error.text = "Please enter your email address"
                        user_login_email = 0

		if validate_email(LoginWindow_instance.ids.login_email.text) == True:
			self.root.ids.login_email_error.text = " "
			user_login_email = 1
		elif validate_email(LoginWindow_instance.ids.login_email.text) == False:
			self.root.ids.login_email_error.text = "Please use a valid email address"
			user_login_email = 0

	def verify_login_password(self):

                LoginWindow_instance = self.root.get_screen("Login")

                global user_login_password

                if len(LoginWindow_instance.ids.login_password.text) < 8 or len(LoginWindow_instance.ids.login_password.text) > 20:
                        LoginWindow_instance.ids.login_password_error.text = "Password length should be 8-20 characters"
                        user_login_password = 0
                else:
                        LoginWindow_instance.ids.login_password_error.text = " "
                        user_login_password = 1

	def login(self):

                LoginWindow_instance = self.root.get_screen("Login")

                if user_login_email == 1 and userlogin_password == 1:
                        email = LoginWindow_instance.ids.login_email.text
                        password = LoginWindow_instance.ids.login_password.text
                        

	def verify_email(self):
    #Number of characters

		registrationwindow_instance = self.root.get_screen("Registration")

		global user_email

		if len(registrationwindow_instance.ids.email.text) > 150:
                                registrationwindow_instance.ids.email_error.text= "The character limit for user's email address is 150."
                                user_email=0
		elif len(registrationwindow_instance.ids.email.text) == 0:
				registrationwindow_instance.ids.email_error.text= "Please enter your email address"
				user_email=0
    #Syntax
		else:
			if validate_email(registrationwindow_instance.ids.email.text) == False:
				registrationwindow_instance.ids.email_error.text= "Please use a valid email address"
				user_email=0
			elif validate_email(registrationwindow_instance.ids.email.text) == True:
				registrationwindow_instance.ids.email_error.text= " "
				user_email=1

	def create_captcha(self):

		registrationwindow_instance = self.root.get_screen("Registration")

		captcha_code =  ''.join(random.choices(text, k = 6))
		registrationwindow_instance.ids.captcha.text = (captcha_code)

	#Function to verify the text-based captcha upon pressing the verify button
	def verify_captcha(self):

		registrationwindow_instance = self.root.get_screen("Registration")

		global user_captcha

		if registrationwindow_instance.ids.captcha_answer.text == registrationwindow_instance.ids.captcha.text:
			registrationwindow_instance.ids.captcha_error.text = " "
			registrationwindow_instance.ids.captcha_validated.text = "Captcha validated."
			user_captcha=1
		elif registrationwindow_instance.ids.captcha_answer.text != registrationwindow_instance.ids.captcha.text:
			registrationwindow_instance.ids.captcha_error.text = "Invalid captcha, please try again"
			registrationwindow_instance.ids.captcha_validated.text = " "
			user_captcha=0


	#Function to verify the password input box to be either more than 8 characters but less than 20 characters upon pressing the register button
	def verify_password(self):

		registrationwindow_instance = self.root.get_screen("Registration")
		
		global user_password

		if len(registrationwindow_instance.ids.password.text)<8 or len(registrationwindow_instance.ids.password.text)>20:
			registrationwindow_instance.ids.password_error.text= "Password length should be 8-20 characters"
			user_password=0
		else:
			registrationwindow_instance.ids.password_error.text=" "
			user_password=1

	#Function to verify the Re-enter password input box upon pressing the register button
	def verify_re_enter_password(self):

		registrationwindow_instance = self.root.get_screen("Registration")

		global user_reenter_password

		if registrationwindow_instance.ids.password.text == registrationwindow_instance.ids.re_enter_password.text:
			registrationwindow_instance.ids.re_enter_password_error.text=" "
			user_reenter_password=1
		else:
			registrationwindow_instance.ids.re_enter_password_error.text= "Passwords do not match."
			user_reenter_password=0

	def register(self):

		registrationwindow_instance = self.root.get_screen("Registration")

		if user_email==1 and user_password==1 and user_reenter_password==1 and user_captcha==1:
                        registrationwindow_instance.ids.registration_complete.text = " "
                        email = registrationwindow_instance.ids.email.text
                        password = registrationwindow_instance.ids.password.text
                        password = password.encode("utf-8")
                        password = base64.b64encode(password)
                        registrationMessage = registerUser(email, password)
                        if registrationMessage == "Registration was successful.":
                                registrationwindow_instance.ids.registration_complete.text = "Registration complete"
                        else:
                                registrationwindow_instance.ids.registration_complete.text = str(registrationMessage)
		else:
			registrationwindow_instance.ids.registration_complete.text = " "

	def selected(self, filename):

		helpdeskform_instance = self.root.get_screen("Helpdesk form")

		try:
			helpdeskform_instance.ids.file_directory.text = (filename[0])
		except:
			pass

class LoginWindow(Screen):
	pass

class registrationwindow(Screen):
	pass

class mainmenu(Screen):
	pass

class helpdeskform(Screen):
	pass

class chooserpage(Screen):
	pass

class WindowManager(ScreenManager):
	pass

if __name__ == '__main__':
	MainApp().run()
