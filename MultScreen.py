from kivy.lang import Builder
from kivymd.app import MDApp
from validate_email import validate_email
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
import random
from LoginAndRegister import registerUser, loginAndGetRole, logoutUserAndAdministrator
from HelpdeskForm import userSubmitForm, listFormsSubmitted, listAllForms, viewForm, viewImage, setFormAsSolved
from kivymd.uix.list import OneLineListItem, TwoLineListItem
import kivymd.uix.label
import math

user_email = None
user_password = None
user_reenter_password = None
user_captcha = None

user_login_email = None
user_login_password = None



text = 'abcdefghijklmnopqrstuvxyz0123456789'


class MainApp(MDApp):
	
	def build(self):
		self.theme_cls.theme_style = "Dark"
		self.theme_cls.primary_palette = "DeepPurple"
		return Builder.load_file("MultScreen.kv")

	def verify_login_email(self):

		LoginWindow_instance = self.root.get_screen("login")

		global user_login_email

		LoginWindow_instance.ids.login_email.text = LoginWindow_instance.ids.login_email.text.strip()

		if len(LoginWindow_instance.ids.login_email.text) > 150:
                        LoginWindow_instance.ids.login_email_error.text = "The character limit for email address is 150."
                        user_login_email = 0
		elif len(LoginWindow_instance.ids.login_email.text) == 0:
                        LoginWindow_instance.ids.login_email_error.text = "Please enter your email address"
                        user_login_email = 0
		if validate_email(LoginWindow_instance.ids.login_email.text) == True:
                        LoginWindow_instance.ids.login_email_error.text = " "
                        user_login_email = 1
		elif validate_email(LoginWindow_instance.ids.login_email.text) == False:
                        LoginWindow_instance.ids.login_email_error.text = "Please use a valid email address"
                        user_login_email = 0

	def verify_login_password(self):

                LoginWindow_instance = self.root.get_screen("login")

                global user_login_password

                if len(LoginWindow_instance.ids.login_password.text) < 8 or len(LoginWindow_instance.ids.login_password.text) > 20:
                        LoginWindow_instance.ids.login_password_error.text = "Password length should be 8-20 characters"
                        user_login_password = 0
                else:
                        LoginWindow_instance.ids.login_password_error.text = " "
                        user_login_password = 1

	def login(self):

                LoginWindow_instance = self.root.get_screen("login")

                global current_user_email
                global current_user_role

                if user_login_email == 1 and user_login_password == 1:
                        LoginWindow_instance.ids.login_button_message.text = "Please wait while verifying the login credentials."
                        email = LoginWindow_instance.ids.login_email.text.strip()
                        password = LoginWindow_instance.ids.login_password.text
                        loginMessage = loginAndGetRole(email, password)
                        if loginMessage in ["user", "administrator"]:
                                current_user_email = email
                                current_user_role = loginMessage
                                LoginWindow_instance.ids.login_button_message.text = "Welcome..."
                        else:
                                LoginWindow_instance.ids.login_button_message.text = loginMessage

	def verify_email(self):
    #Number of characters

		registrationwindow_instance = self.root.get_screen("Registration")

		global user_email

		registrationwindow_instance.ids.email.text = registrationwindow_instance.ids.email.text.strip()

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
                        registrationwindow_instance.ids.registration_complete.text = "Registering..."
                        email = registrationwindow_instance.ids.email.text.strip()
                        password = registrationwindow_instance.ids.password.text
                        registrationMessage = registerUser(email, password)
                        if registrationMessage == "Registration was successful.":
                                registrationwindow_instance.ids.registration_complete.text = "Registration complete"
                        else:
                                registrationwindow_instance.ids.registration_complete.text = str(registrationMessage)
		else:
			registrationwindow_instance.ids.registration_complete.text = " "

	def logout(self):

                mainmenu_instance = self.root.get_screen("Main Menu")

                global current_user_email
                global current_user_role

                mainmenu_instance.ids.logout_button_message.text = "Logging out..."
                mainmenu_instance.ids.logout_button_message.text = current_user_role
                logoutMessage = logoutUserAndAdministrator(current_user_email, current_user_role)
                mainmenu_instance.ids.logout_button_message.text = logoutMessage
                if logoutMessage == "You have logged out.":
                        current_user_email = ""
                        current_user_role = ""

	def checkRole(self):

                return current_user_role
        
	def loadSelectedForm(self, num):

                viewhelpdeskform_instance = self.root.get_screen("ViewHelpdeskForm")
                
                global formList, currentLastNumber, formDetails

                if currentLastNumber < 0:
                        return
                elif currentLastNumber == len(formList) - 1:
                        remainder = (currentLastNumber + 1)%5
                        if remainder == 4:
                                num = num - 1
                        elif remainder == 3:
                                num = num - 2
                        elif remainder == 2:
                                num = num - 3
                        elif remainder == 1:
                                num = num - 4
                formIndex = currentLastNumber - num
                if formIndex < len(formList):
                        formNumber = formList[formIndex][0]
                if formNumber > 0:
                        viewhelpdeskform_instance.ids.form_description.text = "Obtaining Helpdesk Form details..."
                        formDetails = viewForm(current_user_role, current_user_email, formNumber)
                        if type(formDetails) == str:
                                viewhelpdeskform_instance.ids.form_description.text = formDetails
                        else:
                                formList = None
                                currentLastNumber = None
                                viewhelpdeskform_instance.ids.form_description.text = "Loading Helpdesk Form..."
                                if formDetails[1] == 0:
                                        formStatus = " (Pending)"
                                else:
                                        formStatus = " (Solved)"
                                helpdeskform_title = "Helpdesk Form Number: " + str(formDetails[1]) + formStatus + "\n"
                                if len(formDetails) == 6:
                                        helpdeskform_linebelowtitle = "Admin: " + formDetails[5] + "\n\n"
                                else:
                                        helpdeskform_linebelowtitle = "\n\n"
                                if formDetails[2] != "":
                                        helpdeskform_email = "User email address: " + formDetails[3] + "\n\n\n"
                                else:
                                        helpdeskform_email = "User email address: " + formDetails[2] + "; " + formDetails[3] + "\n\n\n"
                                helpdeskform_description = formDetails[4]
                                viewhelpdeskform_instance.form_description.text = helpdeskform_title + helpdeskform_linebelowtitle + helpdeskform_email + helpdeskform_description
                                if formDetails[6] == 1:
                                        viewhelpdeskform_instance.opacity = 100
                                        viewhelpdeskform_instance.form_image.source = formDetails[5]

	def loadFormList(self, previous_or_next):

                helpdeskformlist_instance = self.root.get_screen("HelpdeskFormList")

                global currentLastNumber

                currentList = [["",""],["",""],["",""],["",""],["",""]]
                
                if previous_or_next == "previous" and currentLastNumber < 5:
                        return
                elif previous_or_next == "next" and currentLastNumber == len(formList) - 1:
                        return

                if previous_or_next == "previous":
                        remainder = (currentLastNumber + 1) % 5
                        if remainder == 0:
                                currentLastNumber = currentLastNumber - 9
                        elif remainder == 4:
                                currentLastNumber = currentLastNumber - 8
                        elif remainder == 3:
                                currentLastNumber = currentLastNumber - 7
                        elif remainder == 2:
                                currentLastNumber = currentLastNumber - 6
                        else:
                                currentLastNumber = currentLastNumber - 5
                else:
                        currentLastNumber += 1

                num = 0
                for currentLastNumber in range(currentLastNumber, len(formList), 1):
                        form = formList[currentLastNumber]
                        if form[1] == 0:
                                formStatus = " (Pending)"
                        else:
                                formStatus = " (Solved)"
                        currentList[num][0] = "Helpdesk Form Number: " + str(form[0]) + formStatus
                        currentList[num][1] = form[2]
                        if num < 4:
                                num += 1
                        else:
                                break
                        if currentLastNumber == len(formList) - 1:
                                break

                helpdeskformlist_instance.ids.helpdeskformlistitem1.text = currentList[0][0]
                helpdeskformlist_instance.ids.helpdeskformlistitem1.secondary_text = currentList[0][1]
                helpdeskformlist_instance.ids.helpdeskformlistitem2.text = currentList[1][0]
                helpdeskformlist_instance.ids.helpdeskformlistitem2.secondary_text = currentList[1][1]
                helpdeskformlist_instance.ids.helpdeskformlistitem3.text = currentList[2][0]
                helpdeskformlist_instance.ids.helpdeskformlistitem3.secondary_text = currentList[2][1]
                helpdeskformlist_instance.ids.helpdeskformlistitem4.text = currentList[3][0]
                helpdeskformlist_instance.ids.helpdeskformlistitem4.secondary_text = currentList[3][1]
                helpdeskformlist_instance.ids.helpdeskformlistitem5.text = currentList[4][0]
                helpdeskformlist_instance.ids.helpdeskformlistitem5.secondary_text = currentList[4][1]

                currentPage = math.ceil((currentLastNumber + 1) / 5)
                lastPage = math.ceil(len(formList) / 5)
                if lastPage > 1:
                        helpdeskformlist_instance.ids.helpdeskformlist_previous_page_button.disabled = False
                        helpdeskformlist_instance.ids.helpdeskformlist_previous_page_button.opacity = 100
                        helpdeskformlist_instance.ids.helpdeskformlist_next_page_button.disabled = False
                        helpdeskformlist_instance.ids.helpdeskformlist_next_page_button.opacity = 100
                        helpdeskformlist_instance.ids.helpdeskformlist_page_number_label.text = str(currentPage) + " of " + str(lastPage)

	def loadHelpdeskForms(self, instruction):

                if instruction == "do nothing":
                        return

                helpdeskformlist_instance = self.root.get_screen("HelpdeskFormList")
                
                global formList, currentLastNumber

                if current_user_role == "user":
                        formList = listFormsSubmitted(current_user_email)
                else:
                        formList = listAllForms(current_user_email)

                if type(formList) == str:
                        helpdeskformlist_instance.ids.view_form_message.text = formList
                elif len(formList) == 0:
                        if current_user_role == "user":
                                helpdeskformlist_instance.ids.view_form_message.text = "You have not submitted any Helpdesk Forms. Submit a Helpdesk Form to tell us your issue."
                        else:
                                helpdeskformlist_instance.ids.view_form_message.text = "No Helpdesk Form."
                else:
                        currentLastNumber = -1
                        MainApp.loadFormList(self, "next")

	def clearHelpdeskFormList(self):

                helpdeskformlist_instance = self.root.get_screen("HelpdeskFormList")

                global formList, currentLastNumber, formDetails

                try:
                        formList = None
                        currentLastNumber = None
                        formDetails = None
                except:
                        pass

                helpdeskformlist_instance.ids.helpdeskformlistitem1.text = ""
                helpdeskformlist_instance.ids.helpdeskformlistitem1.secondary_text = ""
                helpdeskformlist_instance.ids.helpdeskformlistitem2.text = ""
                helpdeskformlist_instance.ids.helpdeskformlistitem2.secondary_text = ""
                helpdeskformlist_instance.ids.helpdeskformlistitem3.text = ""
                helpdeskformlist_instance.ids.helpdeskformlistitem3.secondary_text = ""
                helpdeskformlist_instance.ids.helpdeskformlistitem4.text = ""
                helpdeskformlist_instance.ids.helpdeskformlistitem4.secondary_text = ""
                helpdeskformlist_instance.ids.helpdeskformlistitem5.text = ""
                helpdeskformlist_instance.ids.helpdeskformlistitem5.secondary_text = ""
                helpdeskformlist_instance.ids.helpdeskformlist_previous_page_button.disabled = True
                helpdeskformlist_instance.ids.helpdeskformlist_previous_page_button.opacity = 0
                helpdeskformlist_instance.ids.helpdeskformlist_next_page_button.disabled = True
                helpdeskformlist_instance.ids.helpdeskformlist_next_page_button.opacity = 0
                helpdeskformlist_instance.ids.helpdeskformlist_page_number_label.text = ""
                helpdeskformlist_instance.ids.view_form_message.text = ""

	def setSolved(self):

                viewhelpdeskform_instance = self.root.get_screen("ViewHelpdeskForm")

                if current_user_role == "administrator":
                        solvedMessage = setFormAsSolved(current_user_email, formDetails[0])
                        viewhelpdeskform_instance.solved_message.text = solvedMessage
                        if solvedMessage == "Status is updated.":
                                formDetails[1] = 1
                                viewhelpdeskform_instance.form_description.text = viewhelpdeskform_instance.form_description.text.replace("Pending", "Solved", 1)

	def selected(self, filename):

		helpdeskform_instance = self.root.get_screen("Helpdesk form")

		try:
			helpdeskform_instance.ids.file_directory.text = (filename[0])
		except:
			pass

	def submitForm(self):

                helpdeskform_instance = self.root.get_screen("Helpdesk form")

                formEmail = helpdeskform_instance.ids.user_email_address.text.strip()
                description = helpdeskform_instance.ids.issue.text.strip()

                if len(formEmail) > 150:
                        helpdeskform_instance.ids.user_email_error.text= "The character limit for user's email address is 150."
                elif len(formEmail) > 0 and validate_email(formEmail) == False:
                        helpdeskform_instance.ids.user_email_error.text= "Please use a valid email address"
                else:
                        helpdeskform_instance.ids.user_email_error.text = ""
                        if len(description) > 0 and current_user_role == "user":
                                fileDirectory = helpdeskform_instance.ids.file_directory.text.strip()
                                helpdeskform_instance.ids.file_directory.text = "Submitting Helpdesk Form..."
                                formMessage = userSubmitForm(current_user_email, formEmail, description, fileDirectory)
                                helpdeskform_instance.ids.file_directory.text = formMessage

class LoginWindow(Screen):
	pass

class registrationwindow(Screen):
	pass

class mainmenu(Screen):
	pass

class helpdeskformlist(Screen):
        pass

class viewhelpdeskform(Screen):
        pass

class helpdeskform(Screen):
	pass

class chooserpage(Screen):
	pass

class WindowManager(ScreenManager):
	pass

if __name__ == '__main__':
	MainApp().run()

