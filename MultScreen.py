rom kivy.lang import Builder
from kivymd.app import MDApp
from validate_email import validate_email
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
import random
from LoginAndRegister import registerUser, registerAdministrator, loginAndGetRole, logoutUserAndAdministrator
from HelpdeskForm import userSubmitForm, listFormsSubmitted, listAllForms, viewForm, setFormAsSolved
from kivymd.uix.list import TwoLineListItem, ThreeLineListItem
import kivymd.uix.label
import math
from kivy.uix.image import Image, CoreImage
import io
from kivy.uix.dropdown import DropDown
from FrequentlyAskedQuestions import addFAQ, editFAQ, deleteFAQ, getAllFAQs, searchFAQByWord, viewFAQ, rateFAQ
import urllib

user_email = None
user_password = None
user_reenter_password = None
user_captcha = None

user_login_email = None
user_login_password = None

CURRENT_USER_EMAIL = ""
CURRENT_USER_ROLE = ""



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
                        LoginWindow_instance.ids.login_email_error.text = "The character limit for email address is 150"
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

                global CURRENT_USER_EMAIL
                global CURRENT_USER_ROLE

                if user_login_email == 1 and user_login_password == 1:
                        LoginWindow_instance.ids.login_button_message.text = "Please wait while verifying the login credentials."
                        email = LoginWindow_instance.ids.login_email.text.strip()
                        password = LoginWindow_instance.ids.login_password.text
                        loginMessage = loginAndGetRole(email, password)
                        if loginMessage in ["user", "administrator"]:
                                CURRENT_USER_EMAIL = email
                                CURRENT_USER_ROLE = loginMessage
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
                        registrationMessage = registerUser(email, password) #Comment this line when registering an administrator
                        #registrationMessage = registerAdministrator(email, password) #This line should always be commented except when registering an administrator
                        if registrationMessage == "Registration was successful.":
                                registrationwindow_instance.ids.registration_complete.text = "Registration complete"
                        else:
                                registrationwindow_instance.ids.registration_complete.text = str(registrationMessage)
                else:
                        registrationwindow_instance.ids.registration_complete.text = " "

        def logout(self):

                mainmenu_instance = self.root.get_screen("Main Menu")

                global CURRENT_USER_EMAIL
                global CURRENT_USER_ROLE

                mainmenu_instance.ids.logout_button_message.text = "Logging out..."
                logoutMessage = logoutUserAndAdministrator(CURRENT_USER_EMAIL, CURRENT_USER_ROLE)
                mainmenu_instance.ids.logout_button_message.text = logoutMessage
                if logoutMessage == "You have logged out.":
                        CURRENT_USER_EMAIL = ""
                        CURRENT_USER_ROLE = ""

        def checkRole(self):

                return CURRENT_USER_ROLE
        
        def loadSelectedForm(self, num):

                if num == 0:
                        return

                viewhelpdeskform_instance = self.root.get_screen("ViewHelpdeskForm")
                
                global formList, currentLastNumber, formDetails

                try:
                        if currentLastNumber < 0:
                                return
                except NameError:
                        return

                if CURRENT_USER_ROLE == "user":
                        viewhelpdeskform_instance.ids.set_as_solved_button.disabled = True
                        viewhelpdeskform_instance.ids.set_as_solved_button.opacity = 0
                if currentLastNumber == len(formList) - 1 and num < 5:
                        remainder = (currentLastNumber + 1)%5
                        if remainder > 0:
                                diff = remainder - num
                        else:
                                diff = 0
                else:
                        diff = 5 - num
                formIndex = currentLastNumber - diff
                formNumber = formList[formIndex][0]
                viewhelpdeskform_instance.ids.form_description.text = "Obtaining Helpdesk Form details..."
                formDetails = viewForm(CURRENT_USER_ROLE, CURRENT_USER_EMAIL, formNumber)
                if type(formDetails) != list:
                        viewhelpdeskform_instance.ids.solved_message.text = str(formDetails)
                else:
                        viewhelpdeskform_instance.ids.form_description.text = "Loading Helpdesk Form.."
                        if formDetails[1] == 0:
                                formStatus = " (Pending)"
                        else:
                                formStatus = " (Solved)"
                                viewhelpdeskform_instance.ids.set_as_solved_button.disabled = True
                                viewhelpdeskform_instance.ids.set_as_solved_button.opacity = 0
                        helpdeskform_title = "Helpdesk Form Number: " + str(formDetails[0]) + formStatus + "\n"
                        if len(formDetails) == 8:
                                helpdeskform_linebelowtitle = "Admin: " + formDetails[7] + "\n\n"
                        else:
                                helpdeskform_linebelowtitle = "\n\n"
                        if len(formDetails[2]) == 0:
                                helpdeskform_email = "User email address: " + formDetails[3] + "\n\n\n"
                        else:
                                helpdeskform_email = "User email address: " + formDetails[2] + "; " + formDetails[3] + "\n\n\n"
                        helpdeskform_description = formDetails[4]
                        viewhelpdeskform_instance.ids.form_description.text = helpdeskform_title + helpdeskform_linebelowtitle + helpdeskform_email + helpdeskform_description
                        if formDetails[6] == 0:
                                viewhelpdeskform_instance.ids.view_image_button.disabled = True
                                viewhelpdeskform_instance.ids.view_image_button.opacity = 0

        def checkHasImage(self):
                try:
                        return formDetails[6]
                except NameError:
                        return

        def loadImage(self):
                viewimage_instance = self.root.get_screen("ViewImage")
                imageData = io.BytesIO(formDetails[5])
                viewimage_instance.ids.form_image.texture = CoreImage(imageData, ext = 'jpg').texture

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
                elif previous_or_next == "reload":
                        remainder = (currentLastNumber + 1) % 5
                        if remainder == 0:
                                currentLastNumber = currentLastNumber - 4
                        elif remainder == 4:
                                currentLastNumber = currentLastNumber - 3
                        elif remainder == 3:
                                currentLastNumber = currentLastNumber - 2
                        elif remainder == 2:
                                currentLastNumber = currentLastNumber - 1
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
                        helpdeskformlist_instance.ids.helpdeskformlist_previous_page_button.opacity = 1
                        helpdeskformlist_instance.ids.helpdeskformlist_next_page_button.disabled = False
                        helpdeskformlist_instance.ids.helpdeskformlist_next_page_button.opacity = 1
                        helpdeskformlist_instance.ids.helpdeskformlist_page_number_label.text = "Page " + str(currentPage) + " of " + str(lastPage)

        def rearrangeForm(self):

                global formList, currentLastNumber

                if FORM_SORT_PREFERENCE == "ascending":
                        formList.sort(key = lambda form : form[0])
                elif FORM_SORT_PREFERENCE == "descending":
                        formList.sort(key = lambda form : form[0], reverse = True)
                elif FORM_SORT_PREFERENCE == "solved":
                        formList.sort(key = lambda form : form[1], reverse = True)
                else:
                        formList.sort(key = lambda form : form[1])

                currentLastNumber = -1
                MainApp.loadFormList(self, "next")

        def loadHelpdeskForms(self):

                helpdeskformlist_instance = self.root.get_screen("HelpdeskFormList")
                
                global formList, FORM_SORT_PREFERENCE

                if CURRENT_USER_ROLE == "user":
                        formList = listFormsSubmitted(CURRENT_USER_EMAIL)
                else:
                        formList = listAllForms(CURRENT_USER_EMAIL)

                if type(formList) != list:
                        helpdeskformlist_instance.ids.view_form_message.text = str(formList)
                elif len(formList) == 0:
                        if CURRENT_USER_ROLE == "user":
                                helpdeskformlist_instance.ids.helpdeskformlistitem1.text = "You have not submitted any Helpdesk Forms. Submit a Helpdesk Form to tell us your issue."
                        else:
                                helpdeskformlist_instance.ids.helpdeskformlistitem1.text = "No Helpdesk Form."
                else:
                        try:
                                MainApp.rearrangeForm(self)
                        except:
                                if CURRENT_USER_ROLE == "user":
                                        FORM_SORT_PREFERENCE = "descending"
                                else:
                                        FORM_SORT_PREFERENCE = "unsolved"
                                MainApp.rearrangeForm(self)

        def setFormSortPreference(self, preference):

                global FORM_SORT_PREFERENCE

                FORM_SORT_PREFERENCE = preference

        def clearHelpdeskFormList(self, clear):

                if clear == "formDetailsOnly":
                        viewhelpdeskform_instance = self.root.get_screen("ViewHelpdeskForm")
                        viewhelpdeskform_instance.ids.form_description.text = "" 
                        viewhelpdeskform_instance.ids.set_as_solved_button.disabled = False
                        viewhelpdeskform_instance.ids.set_as_solved_button.opacity = 1
                        viewhelpdeskform_instance.ids.view_image_button.disabled = False
                        viewhelpdeskform_instance.ids.view_image_button.opacity = 1
                        viewhelpdeskform_instance.ids.solved_message.text = ""
                        try:
                                global formDetails
                                del formDetails
                        except NameError:
                                pass
                        finally:
                                return

                helpdeskformlist_instance = self.root.get_screen("HelpdeskFormList")

                try:
                        global formList, currentLastNumber
                        del formList
                        del currentLastNumber
                except NameError:
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

                global formDetails, formList
                if CURRENT_USER_ROLE == "administrator":
                        solvedMessage = setFormAsSolved(CURRENT_USER_EMAIL, formDetails[0])
                        if solvedMessage == "Status is updated.":
                                formDetails[1] = 1
                                formDetails.append(CURRENT_USER_EMAIL)
                                for form in formList:
                                        if form[0] == formDetails[0]:
                                                form_L = list(form)
                                                form_L[1] = 1
                                                form = tuple(form_L)
                                                break
                                viewhelpdeskform_instance.ids.form_description.text = viewhelpdeskform_instance.ids.form_description.text.replace("Pending)\n", "Solved)\nAdmin :" + formDetails[7], 1)
                                viewhelpdeskform_instance.ids.set_as_solved_button.disabled = True
                                viewhelpdeskform_instance.ids.set_as_solved_button.opacity = 0
                        else:
                                viewhelpdeskform_instance.ids.solved_message.text = str(solvedMessage)
        def formOpenSort(self):

                global helpdeskformlist_sort_dropdown
                helpdeskformlist_sort_dropdown = Helpdeskformlist_sort_dropdown()
                helpdeskformlist_instance = self.root.get_screen("HelpdeskFormList")
                helpdeskformlist_sort_dropdown.open(helpdeskformlist_instance.ids.helpdeskformlist_sort_button)

        def dismissFormDropDown(self):

                global helpdeskformlist_sort_dropdown
                helpdeskformlist_sort_dropdown.dismiss()
                del helpdeskformlist_sort_dropdown

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
                        if len(description) > 0 and CURRENT_USER_ROLE == "user":
                                fileDirectory = helpdeskform_instance.ids.file_directory.text.strip()
                                helpdeskform_instance.ids.file_directory.text = "Submitting Helpdesk Form..."
                                formMessage = userSubmitForm(CURRENT_USER_EMAIL, formEmail, description, fileDirectory)
                                helpdeskform_instance.ids.file_directory.text = formMessage

        def openChooseCategory(self):

                global faq_category_dropdown
                faq_category_dropdown = FAQ_category_dropdown()
                addeditdeletefaqpage1_instance = self.root.get_screen("AddEditDeleteFAQPage1")
                faq_category_dropdown.open(addeditdeletefaqpage1_instance.ids.faq_category_button)

        def dismissCategoryDropDown(self, category):

                global faq_category_dropdown
                faq_category_dropdown.dismiss()
                del faq_category_dropdown
                addeditdeletefaqpage1_instance = self.root.get_screen("AddEditDeleteFAQPage1")
                addeditdeletefaqpage1_instance.ids.faq_category_button.text = category

        def checkFAQ(self, page):

                addeditdeletefaqpage1_instance = self.root.get_screen("AddEditDeleteFAQPage1")

                hasError = 0

                if len(addeditdeletefaqpage1_instance.ids.faq_title.text.strip()) > 300:
                        addeditdeletefaqpage1_instance.ids.faq_title_error.text = "Title cannot exceed 300 characters."
                        hasError = 1
                elif len(addeditdeletefaqpage1_instance.ids.faq_title.text.strip()) == 0:
                        addeditdeletefaqpage1_instance.ids.faq_title_error.text = "Please fill in the title."
                        hasError = 1
                else:
                        addeditdeletefaqpage1_instance.ids.faq_title_error.text = ""

                if addeditdeletefaqpage1_instance.ids.computer_togglebutton.state == "normal" and addeditdeletefaqpage1_instance.ids.smartphone_togglebutton.state == "normal":
                        addeditdeletefaqpage1_instance.ids.faq_computer_smartphone_error.text = "Please select at least one type of device."
                        hasError = 1
                else:
                        addeditdeletefaqpage1_instance.ids.faq_computer_smartphone_error.text = ""

                if addeditdeletefaqpage1_instance.ids.faq_category_button.text == "Choose Category":
                        addeditdeletefaqpage1_instance.ids.faq_category_subcategory_error.text = "Please select one category."
                        hasError = 1
                elif len(addeditdeletefaqpage1_instance.ids.faq_subcategory.text.strip()) > 100:
                        addeditdeletefaqpage1_instance.ids.faq_category_subcategory_error.text = "Subcategory cannot exceeds 100 characters."
                        hasError = 1
                elif (addeditdeletefaqpage1_instance.ids.faq_subcategory.text.strip()).lower() in ["computer", "smartphone", "hardware", "security", "architecture", "connections"]:
                        addeditdeletefaqpage1_instance.ids.faq_category_subcategory_error.text = "Subcategory should be different from any category."
                        hasError = 1
                else:
                        addeditdeletefaqpage1_instance.ids.faq_category_subcategory_error.text = ""

                if len(addeditdeletefaqpage1_instance.ids.faq_keywords.text.strip()) > 300:
                        addeditdeletefaqpage1_instance.ids.faq_keywords_error.text = "The total length of keywords cannot exceeds 300 characters."
                        hasError = 1
                else:
                        addeditdeletefaqpage1_instance.ids.faq_keywords_error.text = ""

                if page == "firstonly":
                        return hasError
                
                addeditdeletefaqpage2_instance = self.root.get_screen("AddEditDeleteFAQPage2")

                if len(addeditdeletefaqpage2_instance.ids.faq_partname.text.strip()) > 0 and len(addeditdeletefaqpage2_instance.ids.faq_url.text.strip()) == 0:
                        addeditdeletefaqpage2_instance.ids.faq_url_error.text = "Please fill in the URL."
                        hasError = 1
                elif len(addeditdeletefaqpage2_instance.ids.faq_partname.text.strip()) == 0 and len(addeditdeletefaqpage2_instance.ids.faq_url.text.strip()) > 0:
                       addeditdeletefaqpage2_instance.ids.faq_partname_error.text = "Please fill in part name."
                       hasError = 1
                elif len(addeditdeletefaqpage2_instance.ids.faq_partname.text.strip()) > 0 and len(addeditdeletefaqpage2_instance.ids.faq_partname.text.strip()) > 0:
                        if len(addeditdeletefaqpage2_instance.ids.faq_partname.text.strip()) > 200:
                                addeditdeletefaqpage2_instance.ids.faq_partname_error.text = "Part name cannot exceed 200 characters."
                                hasError = 1
                        else:
                                addeditdeletefaqpage2_instance.ids.faq_partname_error.text = ""
                        url = urllib.parse.urlparse(addeditdeletefaqpage2_instance.ids.faq_url.text.strip()) #break the URL (scheme://netloc/path;parameters?query#fragment) into 6 parts, if the URL has scheme and netloc, its syntax is correct
                        if url.scheme == '' or url.netloc == '':
                                addeditdeletefaqpage2_instance.ids.faq_url_error.text = "The syntax of the URL of the link is not correct."
                                hasError = 1
                        else:
                                addeditdeletefaqpage2_instance.ids.faq_url_error.text = ""
                else:
                        addeditdeletefaqpage2_instance.ids.faq_partname_error.text = ""
                        addeditdeletefaqpage2_instance.ids.faq_url_error.text = ""

                if len(addeditdeletefaqpage2_instance.ids.faq_content.text.strip()) == 0:
                        addeditdeletefaqpage2_instance.ids.faq_content_error.text = "Please fill in the content."
                        hasError = 1
                else:
                        addeditdeletefaqpage2_instance.ids.faq_content_error.text = ""

                return hasError

        def loadSelectedFAQ(self, num):

                if num == 0:
                        return

                viewfaq_instance = self.root.get_screen("ViewFAQ")
                
                global faqList, faqcurrentLastNumber, faqDetails

                try:
                        if faqcurrentLastNumber < 0:
                                return
                except NameError:
                        return

                if CURRENT_USER_ROLE == "administrator":
                        viewfaq_instance.ids.helpful_button.text = "Edit"
                if faqcurrentLastNumber == len(faqList) - 1 and num < 4:
                        remainder = (faqcurrentLastNumber + 1)%4
                        if remainder > 0:
                                diff = remainder - num
                        else:
                                diff = 0
                else:
                        diff = 4 - num
                faqIndex = faqcurrentLastNumber - diff
                faqNumber = faqList[faqIndex][0]
                viewfaq_instance.ids.faq_description.text = "Obtaining FAQ details..."
                faqDetails = viewFAQ(CURRENT_USER_ROLE, CURRENT_USER_EMAIL, faqNumber)
                if type(faqDetails) != tuple:
                        viewfaq_instance.ids.helpful_message.text = str(faqDetails)
                else:
                        viewfaq_instance.ids.faq_description.text = "Loading FAQ..."
                        faqTitle = "Title: " + faqDetails[4] + "\n"
                        faqEd = "Last edited: " + faqDetails[11] + ", " + str(faqDetails[10]) + "\n\n"
                        faqCat = faqDetails[3][0].upper() + faqDetails[3][1:]
                        faqCategory = "Category: " + faqCat + "\n"
                        if faqDetails[2] == 0:
                                faqDevice = "For: computer\n"
                        elif faqDetails[1] == 0:
                                faqDevice = "For: smartphone\n"
                        else:
                                faqDevice = "For: computer, smartphone\n"
                        if len(faqDetails[5]) == 0 and len(faqDetails[6]) == 0:
                                faqKeywordsSubcategory = "\n"
                        elif len(faqDetails[6]) == 0:
                                faqKeyWordsSubcategory = "Keywords: " + faqDetails[5] + "\n\n"
                        elif len(faqDetails[5]) == 0:
                                faqKeywordsSubcategory = "Subcategory: " + faqDetails[6] + "\n\n"
                        else:
                                faqKeywordsSubcategory = "Keywords: " + faqDetails[5] + "\nSubcategory: " + faqDetails[6] + "\n\n"
                        faqContent = faqDetails[7]
                        if len(faqDetails[8]) != 0:
                                faqPart = "\n\nPart name: " + formDetails[8] + "\nURL: " + formDetails[9]
                        else:
                                faqPart = ""
                        if CURRENT_USER_ROLE == "user":
                                if faqDetails[10] == 1:
                                        viewfaq_instance.ids.helpful_button.text = "Not Helpful"
                                else:
                                        viewfaq_instance.ids.helpful_button.text = "Helpful"
                        viewfaq_instance.ids.faq_description.text = faqTitle + faqEd + faqCategory + faqDevice + faqKeywordsSubcategory + faqContent + faqPart

        def loadFAQList(self, previous_or_next):

                faqlist_instance = self.root.get_screen("FAQList")

                global faqcurrentLastNumber

                faqcurrentList = [["","",""],["","",""],["","",""],["","",""]]
                
                if previous_or_next == "previous" and faqcurrentLastNumber < 4:
                        return
                elif previous_or_next == "next" and faqcurrentLastNumber == len(faqList) - 1:
                        return

                if previous_or_next == "previous":
                        remainder = (faqcurrentLastNumber + 1) % 4
                        if remainder == 0:
                                faqcurrentLastNumber = faqcurrentLastNumber - 7
                        elif remainder == 3:
                                faqcurrentLastNumber = faqcurrentLastNumber - 6
                        elif remainder == 2:
                                faqcurrentLastNumber = faqcurrentLastNumber - 5
                        else:
                                faqcurrentLastNumber = faqcurrentLastNumber - 4
                elif previous_or_next == "reload":
                        remainder = (faqcurrentLastNumber + 1) % 4
                        if remainder == 0:
                                faqcurrentLastNumber = faqcurrentLastNumber - 3
                        elif remainder == 3:
                                faqcurrentLastNumber = faqcurrentLastNumber - 2
                        elif remainder == 2:
                                faqcurrentLastNumber = faqcurrentLastNumber - 1
                else:
                        faqcurrentLastNumber += 1

                num = 0
                for faqcurrentLastNumber in range(faqcurrentLastNumber, len(faqList), 1):
                        faq = faqList[faqcurrentLastNumber]
                        faqcurrentList[num][0] = "Title: " + faq[4]
                        faqCategory = faq[3][0].upper() + faq[3][1:]
                        if faq[1] == 1 and faq[2] == 1:
                                faqcomsma = "Computer, Smartphone"
                        elif faq[2] == 1:
                                faqcomsma = "Smartphone"
                        else:
                                faqcomsma = "Computer"
                        faqcurrentList[num][1] = "Category: " + faqCategory + "; Device: " + faqcomsma
                        faqcurrentList[num][2] = "Last edited: " + str(faq[5]) + "; Rating: " + str(faq[6])
                        if num < 3:
                                num += 1
                        else:
                                break
                        if faqcurrentLastNumber == len(faqList) - 1:
                                break

                faqlist_instance.ids.faqlistitem1.text = faqcurrentList[0][0]
                faqlist_instance.ids.faqlistitem1.secondary_text = faqcurrentList[0][1]
                faqlist_instance.ids.faqlistitem1.tertiary_text = faqcurrentList[0][2]
                faqlist_instance.ids.faqlistitem2.text = faqcurrentList[1][0]
                faqlist_instance.ids.faqlistitem2.secondary_text = faqcurrentList[1][1]
                faqlist_instance.ids.faqlistitem2.tertiary_text = faqcurrentList[1][2]
                faqlist_instance.ids.faqlistitem3.text = faqcurrentList[2][0]
                faqlist_instance.ids.faqlistitem3.secondary_text = faqcurrentList[2][1]
                faqlist_instance.ids.faqlistitem3.tertiary_text = faqcurrentList[2][2]
                faqlist_instance.ids.faqlistitem4.text = faqcurrentList[3][0]
                faqlist_instance.ids.faqlistitem4.secondary_text = faqcurrentList[3][1]
                faqlist_instance.ids.faqlistitem4.tertiary_text = faqcurrentList[3][2]

                faqcurrentPage = math.ceil((faqcurrentLastNumber + 1) / 4)
                faqlastPage = math.ceil(len(faqList) / 4)
                if faqlastPage > 1:
                        faqlist_instance.ids.faqlist_previous_page_button.disabled = False
                        faqlist_instance.ids.faqlist_previous_page_button.opacity = 1
                        faqlist_instance.ids.faqlist_next_page_button.disabled = False
                        faqlist_instance.ids.faqlist_next_page_button.opacity = 1
                        faqlist_instance.ids.faqlist_page_number_label.text = "Page " + str(faqcurrentPage) + " of " + str(faqlastPage)

        def isInCat(faq):

                if faq[3] == FAQ_CATDEV:
                        return 1
                return 0

        def rearrangeFAQ(self):

                global faqList, faqcurrentLastNumber

                if FAQ_SORT_PREFERENCE == "ascending":
                        faqList.sort(key = lambda faq : faq[4])
                elif FAQ_SORT_PREFERENCE == "descending":
                        faqList.sort(key = lambda faq : faq[4], reverse = True)
                elif FAQ_SORT_PREFERENCE == "date":
                        faqList.sort(key = lambda faq : faq[5], reverse = True)
                else:
                        faqList.sort(key = lambda faq : faq[6], reverse = True)

                if FAQ_CATDEV == "computer":
                        faqList.sort(key = lambda faq : faq[1], reverse = True)
                elif FAQ_CATDEV == "smartphone":
                        faqList.sort(key = lambda faq : faq[2], reverse = True)
                elif FAQ_CATDEV == "all":
                        pass
                else:
                        faqList.sort(key = MainApp.isInCat, reverse = True)

                faqcurrentLastNumber = -1
                MainApp.loadFAQList(self, "next")

        def loadFAQs(self):

                faqlist_instance = self.root.get_screen("FAQList")
                
                global faqList, FAQ_SORT_PREFERENCE,FAQ_CATDEV

                faqList = getAllFAQs(CURRENT_USER_ROLE, CURRENT_USER_EMAIL)

                if type(faqList) != list:
                        faqlist_instance.ids.view_faq_message.text = str(faqList)
                elif len(faqList) == 0:
                        faqlist_instance.ids.faqlistitem1.text = "There is no FAQ available."
                else:
                        try:
                                MainApp.rearrangeFAQ(self)
                        except:
                                FAQ_SORT_PREFERENCE = "ascending"
                                try:
                                        MainApp.rearrangeFAQ(self)
                                except:
                                        FAQ_CATDEV = "all"
                                        MainApp.rearrangeFAQ(self)

        def searchFAQs(self):

                faqlist_instance = self.root.get_screen("FAQList")

                global faqList

                if faqlist_instance.ids.faqlistitem1.text == "There is no FAQ available.":
                        return

                searchWord = faqlist_instance.ids.faq_search_word.text
                if len(searchWord) > 100:
                        faqlist_instance.ids.view_faq_message.text = "The words in the search box cannot exceed 100 characters."
                        return
                elif len(searchWord) == 0:
                        return

                faqList = searchFAQByWord(CURRENT_USER_ROLE, CURRENT_USER_EMAIL, searchWord)

                if type(faqList) != list:
                        faqlist_instance.ids.view_faq_message.text = str(faqList)
                elif len(faqList) == 0:
                        faqlist_instance.ids.faqlistitem1.text = "There is no FAQ which matches the words. Try other words and see?"
                else:
                        try:
                                MainApp.rearrangeFAQ(self)
                        except:
                                FAQ_SORT_PREFERENCE = "ascending"
                                try:
                                        MainApp.rearrangeFAQ(self)
                                except:
                                        FAQ_CATDEV = "all"
                                        MainApp.rearrangeFAQ(self)

        def setFAQSortPreference(self, preference):

                global FAQ_SORT_PREFERENCE

                FAQ_SORT_PREFERENCE = preference

        def faqOpenSort(self):

                global faq_sort_dropdown
                faq_sort_dropdown = FAQlist_sort_dropdown()
                faqlist_instance = self.root.get_screen("FAQList")
                faq_sort_dropdown.open(faqlist_instance.ids.faqlist_sort_button)

        def dismissfaqsortDropDown(self):

                global faq_sort_dropdown
                faq_sort_dropdown.dismiss()
                del faq_sort_dropdown

        def faqOpencategorydevice(self):

                global faq_catdev_dropdown
                faq_catdev_dropdown = FAQlist_catdev_dropdown()
                faqlist_instance = self.root.get_screen("FAQList")
                faq_catdev_dropdown.open(faqlist_instance.ids.faqlist_catdev_button)

        def dismissfaqcatdevDropDown(self):

                global faq_catdev_dropdown
                faq_catdev_dropdown.dismiss()
                del faq_catdev_dropdown

        def setFAQcatdev(self, catdev):

                global FAQ_CATDEV
                FAQ_CATDEV = catdev

        def clearFAQList(self, clear):

                if clear == "faqDetailsOnly":
                        viewfaq_instance = self.root.get_screen("ViewFAQ")
                        viewfaq_instance.ids.faq_description.text = "" 
                        viewfaq_instance.ids.helpful_message.text = ""
                        try:
                                global faqDetails
                                del faqDetails
                        except NameError:
                                pass
                        finally:
                                return

                faqlist_instance = self.root.get_screen("FAQList")

                try:
                        global faqList, faqcurrentLastNumber
                        del faqList
                        del faqcurrentLastNumber
                except NameError:
                        pass

                faqlist_instance.ids.faqlistitem1.text = ""
                faqlist_instance.ids.faqlistitem1.secondary_text = ""
                faqlist_instance.ids.faqlistitem1.tertiary_text = ""
                faqlist_instance.ids.faqlistitem2.text = ""
                faqlist_instance.ids.faqlistitem2.secondary_text = ""
                faqlist_instance.ids.faqlistitem2.tertiary_text = ""
                faqlist_instance.ids.faqlistitem3.text = ""
                faqlist_instance.ids.faqlistitem3.secondary_text = ""
                faqlist_instance.ids.faqlistitem3.tertiary_text = ""
                faqlist_instance.ids.faqlistitem4.text = ""
                faqlist_instance.ids.faqlistitem4.secondary_text = ""
                faqlist_instance.ids.faqlistitem4.tertiary_text = ""
                faqlist_instance.ids.faqlist_previous_page_button.disabled = True
                faqlist_instance.ids.faqlist_previous_page_button.opacity = 0
                faqlist_instance.ids.faqlist_next_page_button.disabled = True
                faqlist_instance.ids.faqlist_next_page_button.opacity = 0
                faqlist_instance.ids.faqlist_page_number_label.text = ""
                faqlist_instance.ids.view_faq_message.text = ""
                if clear == "notsearch":
                        return
                faqlist_instance.ids.faq_search_word.text = ""

        def setAddFAQ(self):

                addeditdeletefaqpage1_instance = self.root.get_screen("AddEditDeleteFAQPage1")
                addeditdeletefaqpage2_instance = self.root.get_screen("AddEditDeleteFAQPage2")

                addeditdeletefaqpage1_instance.ids.addeditdeletefaqpage1_title.text = "Add FAQ (Page 1)"
                addeditdeletefaqpage1_instance.ids.faq1_menu_button.text = "FAQs"
                addeditdeletefaqpage1_instance.ids.faq1_delete_button.disabled = True
                addeditdeletefaqpage1_instance.ids.faq1_delete_button.opacity = 0

                addeditdeletefaqpage2_instance.ids.addeditdeletefaqpage2_title.text = "Add FAQ (Page 2)"
                addeditdeletefaqpage2_instance.ids.faq2_menu_button.text = "FAQs"
                addeditdeletefaqpage2_instance.ids.faq2_delete_button.disabled = True
                addeditdeletefaqpage2_instance.ids.faq2_delete_button.opacity = 0

        def setEditFAQ(self):

                addeditdeletefaqpage1_instance = self.root.get_screen("AddEditDeleteFAQPage1")
                addeditdeletefaqpage2_instance = self.root.get_screen("AddEditDeleteFAQPage2")

                addeditdeletefaqpage1_instance.ids.addeditdeletefaqpage1_title.text = "Edit FAQ (Page 1)"
                addeditdeletefaqpage1_instance.ids.faq1_menu_button.text = "Menu"
                addeditdeletefaqpage1_instance.ids.faq1_delete_button.disabled = False
                addeditdeletefaqpage1_instance.ids.faq1_delete_button.opacity = 1
                addeditdeletefaqpage1_instance.ids.faq_title.text = faqDetails[4]
                if faqDetails[1] == 1:
                        addeditdeletefaqpage1_instance.ids.computer_togglebutton.state = "down"
                else:
                        addeditdeletefaqpage1_instance.ids.computer_togglebutton.state = "normal"
                if faqDetails[2] == 1:
                        addeditdeletefaqpage1_instance.ids.smartphone_togglebutton.state = "down"
                else:
                        addeditdeletefaqpage1_instance.ids.smartphone_togglebutton.state = "normal"
                addeditdeletefaqpage1_instance.ids.faq_category_button.text = faqDetails[3][0].upper() + faqDetails[3][1:]
                addeditdeletefaqpage1_instance.ids.faq_subcategory.text = faqDetails[6]
                addeditdeletefaqpage1_instance.ids.faq_keywords.text = faqDetails[5]

                addeditdeletefaqpage2_instance.ids.addeditdeletefaqpage2_title.text = "Edit FAQ (Page 2)"
                addeditdeletefaqpage2_instance.ids.faq2_menu_button.text = "Menu"
                addeditdeletefaqpage2_instance.ids.faq2_delete_button.disabled = False
                addeditdeletefaqpage2_instance.ids.faq2_delete_button.opacity = 1
                addeditdeletefaqpage2_instance.ids.faq_partname.text = faqDetails[8]
                addeditdeletefaqpage2_instance.ids.faq_url.text = faqDetails[9]
                addeditdeletefaqpage2_instance.ids.faq_content.text = faqDetails[7]

        def setHelpful(self):

                viewfaq_instance = self.root.get_screen("ViewFAQ")

                global faqDetails

                if faqDetails[12] == 1:
                        helpful = 0
                else:
                        helpful = 1
                if CURRENT_USER_ROLE == "user":
                        rateMessage = rateFAQ(CURRENT_USER_EMAIL, faqDetails[0], helpful)
                        if rateMessage == "Rating is updated.":
                                faqDetails = list(faqDetails)
                                faqDetails[12] = helpful
                                faqDetails = tuple(faqDetails)
                                if helpful == 1:
                                        viewfaq_instance.ids.helpful_button.text = "Not Helpful"
                                else:
                                        viewfaq_instance.ids.helpful_button.text = "Helpful"
                        else:
                                viewfaq_instance.ids.helpful_message.text = str(rateMessage)

        def clearFAQ(self):

                addeditdeletefaqpage1_instance = self.root.get_screen("AddEditDeleteFAQPage1")
                addeditdeletefaqpage2_instance = self.root.get_screen("AddEditDeleteFAQPage2")

                addeditdeletefaqpage1_instance.ids.faq_title.text = ""
                addeditdeletefaqpage1_instance.ids.faq_title_error.text = ""
                addeditdeletefaqpage1_instance.ids.computer_togglebutton.state = "normal"
                addeditdeletefaqpage1_instance.ids.smartphone_togglebutton.state = "normal"
                addeditdeletefaqpage1_instance.ids.faq_computer_smartphone_error.text = ""
                addeditdeletefaqpage1_instance.ids.faq_category_button.text = "Choose Category"
                addeditdeletefaqpage1_instance.ids.faq_subcategory.text = ""
                addeditdeletefaqpage1_instance.ids.faq_category_subcategory_error.text = ""
                addeditdeletefaqpage1_instance.ids.faq_keywords.text = ""
                addeditdeletefaqpage1_instance.ids.faq_keywords_error.text = ""
                addeditdeletefaqpage1_instance.ids.faq_delete_error.text = ""

                addeditdeletefaqpage2_instance.ids.faq_partname.text = ""
                addeditdeletefaqpage2_instance.ids.faq_partname_error.text = ""
                addeditdeletefaqpage2_instance.ids.faq_url.text = ""
                addeditdeletefaqpage2_instance.ids.faq_url_error.text = ""
                addeditdeletefaqpage2_instance.ids.faq_content.text = ""
                addeditdeletefaqpage2_instance.ids.faq_content_error.text = ""
                addeditdeletefaqpage2_instance.ids.faq_upload_error.text = ""

        def uploadFAQ(self):

                if MainApp.checkFAQ(self, "") == 1:
                        return

                addeditdeletefaqpage1_instance = self.root.get_screen("AddEditDeleteFAQPage1")
                addeditdeletefaqpage2_instance = self.root.get_screen("AddEditDeleteFAQPage2")

                title = addeditdeletefaqpage1_instance.ids.faq_title.text.strip()

                if addeditdeletefaqpage1_instance.ids.computer_togglebutton.state == "down":
                        isForComputer = 1
                else:
                        isForComputer = 0

                if addeditdeletefaqpage1_instance.ids.smartphone_togglebutton.state == "down":
                        isForSmartphone = 1
                else:
                        isForSmartphone = 0

                category = addeditdeletefaqpage1_instance.ids.faq_category_button.text.lower()
                subcategory = addeditdeletefaqpage1_instance.ids.faq_subcategory.text.strip()
                keyword = addeditdeletefaqpage1_instance.ids.faq_keywords.text.strip()
                partName = addeditdeletefaqpage2_instance.ids.faq_partname.text.strip()
                url = addeditdeletefaqpage2_instance.ids.faq_url_error.text.strip()
                content = addeditdeletefaqpage2_instance.ids.faq_content.text.strip()

                if CURRENT_USER_ROLE == "administrator":
                        if addeditdeletefaqpage2_instance.ids.addeditdeletefaqpage2_title.text == "Add FAQ (Page 2)":
                                uploadMessage = addFAQ(CURRENT_USER_EMAIL, isForComputer, isForSmartphone, category, title, keyword, subcategory, content, partName, url)
                        else:
                                uploadMessage = editFAQ(CURRENT_USER_EMAIL, faqDetails[0], isForComputer, isForSmartphone, category, title, keyword, subcategory, content, partName, url)
                        addeditdeletefaqpage2_instance.ids.faq_upload_error.text = str(uploadMessage)
                        if uploadMessage == "FAQ is edited.":
                                MainApp.clearFAQList(self, "faqDetailsOnly")
                                MainApp.loadFAQs(self)

        def removeFAQ(self):

                addeditdeletefaqpage1_instance = self.root.get_screen("AddEditDeleteFAQPage1")
                addeditdeletefaqpage2_instance = self.root.get_screen("AddEditDeleteFAQPage2")

                deleteMessage = deleteFAQ(CURRENT_USER_EMAIL, faqDetails[0])
                if self.root.current == "AddEditDeleteFAQPage1":
                        addeditdeletefaqpage1_instance.ids.faq_delete_error.text = str(deleteMessage)
                else:
                        addeditdeletefaqpage2_instance.ids.faq_upload_error.text = str(deleteMessage)
                if deleteMessage == "FAQ is deleted.":
                        for faq in faqList:
                                if faq[0] == faqDetails[0]:
                                        remove = faq
                                        break
                        faqList.remove(faq)
                        MainApp.clearFAQ(self)
                        MainApp.clearFAQList(self, "faqDetailsOnly")
                        if len(faqList) == 0:
                                faqlist_instance = self.root.get_screen("FAQList")
                                faqlist_instance.ids.faqlistitem1.text = "There is no FAQ available."
                        else:
                                global faqcurrentLastNumber
                                faqcurrentLastNumber = -1
                                MainApp.loadFAQList(self, "next")

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

class helpdeskformlist(Screen):
        pass

class viewhelpdeskform(Screen):
        pass

class viewimage(Screen):
        pass

class Helpdeskformlist_sort_dropdown(DropDown):
        pass

class addeditdeletefaqpage1(Screen):
        pass

class addeditdeletefaqpage2(Screen):
        pass

class FAQ_category_dropdown(DropDown):
        pass

class faqlist(Screen):
        pass

class viewfaq(Screen):
        pass

class FAQlist_sort_dropdown(DropDown):
        pass

class FAQlist_catdev_dropdown(DropDown):
        pass

class WindowManager(ScreenManager):
        pass

if __name__ == '__main__':
        MainApp().run()
