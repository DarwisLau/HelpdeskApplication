import sqlite3
from HelpdeskApplicationDatabase import createDatabase, dropDatabase


def registerUser (dataEmail, dataPassword):

    """Function to register a new user account and return "Registration was
       successful." if the registration was successful, whereas return an error
       message if the registration was not successful.
       Input should be string.
       Output is string."""

    #dropDatabase() #Used when the structure of database is changed, normally commented
    #Create a new database if database does not exist
    try:
        createDatabase()
    except sqlite3.Error:
        pass
    
    #Insert into database
    try:
        dbConnection = sqlite3.connect('HelpdeskApplication.sqlite')
        dbCursor = dbConnection.cursor()

        #Check whether the user exists or not
        dbCursor.execute('''
        SELECT EXISTS(
         SELECT userEmail FROM User
          WHERE userEmail = ?);
        ''',
        (dataEmail,))
        existUser = dbCursor.fetchone()
        if existUser[0] == 1:
            return "This user already exists."

        #Check whether the email address is used by an administrator or not
        dbCursor.execute('''
        SELECT EXISTS(
         SELECT administratorEmail FROM Administrator
          WHERE administratorEmail = ?);
        ''',
        (dataEmail,))
        existAdministrator = dbCursor.fetchone()
        if existAdministrator[0] == 1:
            return "This email address has been used to register an administrator account, so the same email address cannot be used to register a user account."

        #Insert into database
        dbCursor.execute('''
        INSERT INTO User (
        userEmail, userPassword)
        VALUES (
        ?,?);
        ''',
        (dataEmail, dataPassword,))
        dbConnection.commit()

        #Check whether the insertion was successful or not
        dbCursor.execute('''
        SELECT IIF((
         (SELECT userEmail FROM User
          WHERE userEmail = ?) = ? AND
         (SELECT userPassword FROM User
          WHERE userEmail = ?) = ?),
         "Registration was successful.",
         "Something wrong when inserting the information into the database. Please try again."
         ) message;
        ''',
        (dataEmail, dataEmail,
         dataEmail, dataPassword,))
        returnMessage = dbCursor.fetchone()
        return returnMessage[0]

    except sqlite3.Error as errorMessage:
        return errorMessage
    finally:
        dbConnection.close()



def loginAndGetRole (dataEmail, dataPassword):

    """Function for a user or an administrator to login and return the role
       (either "user" or "administrator") if the user or the administrator has
       successfully logged in, whereas return an error message if the login
       was not successful.
       Input should be string.
       Output is string."""
    

    #Create a new database if database does not exist
    try:
        createDatabase()
    except sqlite3.Error:
        pass

    #Check with the database
    try:
        dbConnection = sqlite3.connect('HelpdeskApplication.sqlite')
        dbCursor = dbConnection.cursor()

        #Check whether the person is a user or not
        dbCursor.execute('''
        SELECT EXISTS(
         SELECT userEmail FROM User
          WHERE userEmail = ?);
        ''',
        (dataEmail,))
        existUser = dbCursor.fetchone()
        if existUser[0] == 1:

            #Check password
            dbCursor.execute('''
            SELECT IIF ((
             SELECT userPassword FROM User
              WHERE userEmail = ?) = ?,
             1,
             0
             ) isCorrect;
            ''',
            (dataEmail, dataPassword,))
            passwordIsCorrect = dbCursor.fetchone()
            if passwordIsCorrect[0] == 0:
                return "Password is not correct."
            else:

                #Set status as logged in
                dbCursor.execute('''
                UPDATE User
                 SET userIsLoggedIn = 1
                  WHERE userEmail = ?;
                ''',
                (dataEmail,))
                dbConnection.commit()

                #Check whether status was set as logged in or not
                dbCursor.execute('''
                SELECT IIF((
                 SELECT userIsLoggedIn FROM User
                  WHERE userEmail = ?) = 1,
                 "user",
                 "Something wrong when logging in. Please try again."
                 ) message;
                ''',
                (dataEmail,))
                returnMessage = dbCursor.fetchone()
                return returnMessage[0]

        else:

            #Check whether the person is an administrator or not
            dbCursor.execute('''
            SELECT EXISTS(
             SELECT administratorEmail FROM Administrator
              WHERE administratorEmail = ?);
            ''',
            (dataEmail,))
            existAdministrator = dbCursor.fetchone()
            if existAdministrator[0] == 0:
                return "This user or administrator does not exist."
            else:

                #Check password
                dbCursor.execute('''
                SELECT IIF((
                 SELECT administratorPassword FROM Administrator
                  WHERE administratorEmail = ?) = ?,
                 1,
                 0
                ) isCorrect;
                ''',
                (dataEmail, dataPassword,))
                passwordIsCorrect = dbCursor.fetchone()
                if passwordIsCorrect[0] == 0:
                    return "Password is not correct"
                else:

                    #Set status as logged in
                    dbCursor.execute('''
                    UPDATE Administrator
                     SET administratorIsLoggedIn = 1
                      WHERE administratorEmail = ?;
                    ''',
                    (dataEmail,))
                    dbConnection.commit()

                    #Check whether status was set as logged in or not
                    dbCursor.execute('''
                    SELECT IIF((
                     SELECT administratorIsLoggedIn FROM Administrator
                      WHERE administratorEmail = ?) = 1,
                     "administrator",
                     "Something wrong when logging in. Please try again."
                    ) message;
                    ''',
                    (dataEmail,))
                    returnMessage = dbCursor.fetchone()
                    return returnMessage[0]
                
    except sqlite3.Error as errorMessage:
        return errorMessage
    finally:
        dbConnection.close()



def logoutUserAndAdministrator (dataEmail, theRole):

    """Function for a user or an administrator to logout and return "You have
       logged out." if the logout was successful, whereas return an error
       message if the logout was not successful.
       Input should be string.
       Output is string."""
    

    try:
        dbConnection = sqlite3.connect('HelpdeskApplication.sqlite')
        dbCursor = dbConnection.cursor()

        #User logout
        if theRole == "user":
            dbCursor.execute('''
            UPDATE User
             SET userIsLoggedIn = 0
              WHERE userEmail = ?;
            ''',
            (dataEmail,))
            dbConnection.commit()

            #Check whether the logout was successful or not
            dbCursor.execute('''
            SELECT IIF((
             SELECT userIsLoggedIn FROM User
              WHERE userEmail = ?) = 0,
             "You have logged out.",
             "Something wrong when logging out. Please try again."
             ) message;
             ''',
            (dataEmail,))
            returnMessage = dbCursor.fetchone()
            return returnMessage[0]

        #Administrator logout
        elif theRole == "administrator":
            dbCursor.execute('''
            UPDATE Administrator
             SET administratorIsLoggedIn = 0
              WHERE administratorEmail = ?;
            ''',
            (dataEmail,))
            dbConnection.commit()

            #Check whether the logout was successful or not
            dbCursor.execute('''
            SELECT IIF((
             SELECT administratorIsLoggedIn FROM Administrator
              WHERE administratorEmail = ?) = 0,
            "You have logged out.",
            "Something wrong when logging out. Please try again."
            ) message;
            ''',
            (dataEmail,))
            returnMessage = dbCursor.fetchone()
            return returnMessage[0]
    
    except sqlite3.Error as errorMessage:
        return errorMessage
    finally:
        dbConnection.close()



def registerAdministrator (dataEmail, dataPassword):

    """Function to register a new administrator account from the backend.
       Input should be both string.
       Output is string."""

    #Create a database if database does not exist
    try:
        createDatabase()
    except sqlite3.Error:
        pass

    #Insert into database
    try:
        dbConnection = sqlite3.connect('HelpdeskApplication.sqlite')
        dbCursor = dbConnection.cursor()

        #Check whether the administrator exists or not
        dbCursor.execute('''
        SELECT EXISTS(
         SELECT administratorEmail FROM Administrator
          WHERE administratorEmail = ?);
        ''',
        (dataEmail,))
        existAdministrator = dbCursor.fetchone()
        if existAdministrator[0] == 1:
            return "This administrator already exists."

        #Check whether the email address is used by a user or not
        dbCursor.execute('''
        SELECT EXISTS(
         SELECT userEmail FROM User
          WHERE userEmail = ?);
        ''',
        (dataEmail,))
        existUser = dbCursor.fetchone()
        if existUser[0] == 1:
            return "This email address has been used to register a user account, so the same email address cannot be used to register an administrator account."

        #Insert into database
        dbCursor.execute('''
        INSERT INTO Administrator (
        administratorEmail, administratorPassword)
        VALUES (
        ?,?);
        ''',
        (dataEmail, dataPassword,))
        dbConnection.commit()

        #Check whether the insertion was successful or not
        dbCursor.execute('''
        SELECT IIF((
         (SELECT administratorEmail FROM Administrator
          WHERE administratorEmail = ?) = ? AND
         (SELECT administratorPassword FROM Administrator
          WHERE administratorEmail = ?) = ?),
         "Registration was successful.",
         "Something wrong when inserting the information to the database. Please try again."
         ) message;
        ''',
        (dataEmail, dataEmail,
         dataEmail, dataPassword,))
        returnMessage = dbCursor.fetchone()
        return returnMessage[0]

    except sqlite3.Error as errorMessage:
        return errorMessage
    finally:
        dbConnection.close()

#print(loginAndGetRole("chan2@mail.com","18010392"))
'''MDRectangleFlatButton:
			text:"Back"
			font_size: 15
			size_hint_y: None
			pos_hint:{"x":0.75,"y":0.85}
			text_color:("#99c742")
			on_press:
				app.clearSelectedForm()
				root.ids.container.clear_widgets()
				app.root.current = "Main Menu"
				root.manager.transition.direction = "down"

		MDLabel:
			text:"List of Helpdesk Forms"
			font_style: "H4"
			size_hint_y: None
			pos_hint:{"x":0.05,"y":0.85}
			height: self.texture_size[1]
			padding_y:15

		MDList:
			id:container
			pos_hint:{"x":0.05,"y":0.40}

		MDRectangleFlatButton:
			text:"View Form"
			id: view_form_button
			font_size: 15
			size_hint_y: None
			pos_hint:{"x":150/800,"y":70/500}
			text_color:("#99c742")
			on_press: 
				app.loadSelectedForm() if view_form_button.text == "ViewForm" else app.loadImage()
				app.root.current = "ViewHelpdeskForm" if view_form_message.text == "Loading image..." else "Helpdesk Form List"
				root.ids.view_form_message.text = "" if view_form_message.text == "Loading image..." else view_form_message.text
				root.manager.transition.direction = "left"

		MDRectangleFlatButton:
			text:"New Form"
			font_size: 15
			size_hint_y: None
			pos_hint:{"x":485/800,"y":70/500}
			text_color:("#99c742")
			on_press:
				app.clearSelectedForm()
				root.ids.container.clear_widgets()
				root.ids.view_form_message.text = ""
				app.root.current = "Helpdesk form"
				root.manager.transition.direction = "left"

		MDLabel:
			id: view_form_message
			text:" "
			size_hint_y: None
			font_size: 15
			pos_hint:{"x":150/800,"y":50/500}
			height: self.texture_size[1]'''
'''
	ScrollView:
		do_scroll_x: False
		MDList:
			MDRectangleFlatIconButton:
				text:"Back"
				font_size: 15
				size_hint_y: None
				pos_hint: {"right":1}
				text_color:("#99c742")
				on_press: 
					app.clearHelpdeskFormList("formDetailsOnly")
					root.ids.form_description_user.text = ""
					root.ids.form_image_user.source = None
					app.root.current = "HelpdeskFormList"
					root.manager.transition.direction = "right"

			MDLabel:
				text:"View Helpdesk Forms"
				font_style: "H4"
				size_hint_y: None
				height: self.texture_size[1]
				padding_y:15

			MDLabel:
				id: form_description_user
				text:""
				size_hint_y: None
				font_size:20
				height: self.texture_size[1]

			Image:
				id: form_image_user
				source: None

<viewhelpdeskformadministrator>
	name:"ViewHelpdeskFormAdministrator"
	
	ScrollView:
		do_scroll_x: False
		MDList:
			MDRectangleFlatIconButton:
				text:"Back"
				font_size: 15
				size_hint_y: None
				text_color:("#99c742")
				on_press: 
					app.clearHelpdeskFormList("formDetailsOnly")
					root.ids.form_description_administrator.text = ""
					root.ids.form_image_administrator.source = None
					root.ids.solved_message.text = ""
					app.root.current = "HelpdeskFormList"
					root.manager.transition.direction = "right"

			MDLabel:
				text:"View Helpdesk Forms"
				font_style: "H4"
				size_hint_y: None
				height: self.texture_size[1]
				padding_y:15

			MDLabel:
				id: form_description_administrator
				text:""
				size_hint_y: None
				font_size:20
				height: self.texture_size[1]

			Image:
				id: form_image_administrator
				source: None
'''
'''if CURRENT_USER_ROLE == "user":
                        viewhelpdeskformuser_instance = self.root.get_screen("ViewHelpdeskFormUser")
                else:
                        viewhelpdeskformadministrator_instance = self.root.get_screen("ViewHelpdeskFormAdministrator")
                
                global formList, currentLastNumber, formDetails

                try:
                        if currentLastNumber < 0:
                                return
                except NameError:
                        return

                if currentLastNumber == len(formList) - 1:
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
                        if CURRENT_USER_ROLE == "user":
                                viewhelpdeskformuser_instance.ids.form_description_user.text = "Obtaining Helpdesk Form details..."
                        else:
                                viewhelpdeskformadministrator_instance.ids.form_description_administrator.text = "Obtaining Helpdesk Form details..."
                        formDetails = viewForm(CURRENT_USER_ROLE, CURRENT_USER_EMAIL, formNumber)
                        if type(formDetails) == str:
                                if CURRENT_USER_ROLE == "user":
                                        viewhelpdeskformuser_instance.ids.form_description_user.text = formDetails
                                else:
                                        viewhelpdeskformadministrator_instance.ids.form_description_administrator.text = formDetails
                        else:
                                formList = None
                                currentLastNumber = None
                                if CURRENT_USER_ROLE == "user":
                                        viewhelpdeskformuser_instance.ids.form_description_user.text = "Loading Helpdesk Form..."
                                else:
                                        viewhelpdeskformadministrator_instance.ids.form_description_administrator.text = "Loading Helpdesk Form.."
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
                                if CURRENT_USER_ROLE == "user":
                                        viewhelpdeskformuser_instance.ids.form_description_user.text = helpdeskform_title + helpdeskform_linebelowtitle + helpdeskform_email + helpdeskform_description
                                else:
                                        viewhelpdeskformadministrator_instance.ids.form_description_administrator.text = helpdeskform_title + helpdeskform_linebelowtitle + helpdeskform_email + helpdeskform_description
                                if formDetails[6] == 1:
                                        if CURRENT_USER_ROLE == "user":
                                                viewhelpdeskformuser_instance.ids.form_image_user.source = formDetails[5]
                                        else:
                                                viewhelpdeskformadministrator_instance.ids.form_image_administrator.source = formDetails[5]'''
'''viewhelpdeskformadministrator_instance = self.root.get_screen("ViewHelpdeskFormAdministrator")

                if CURRENT_USER_ROLE == "administrator":
                        solvedMessage = setFormAsSolved(CURRENT_USER_EMAIL, formDetails[0])
                        if solvedMessage == "Status is updated.":
                                formDetails[1] = 1
                                viewhelpdeskformadministrator_instance.form_description_administrator.text = viewhelpdeskformadministrator_instance.form_description_administrator.text.replace("Pending", "Solved", 1)
                        else:
                                viewhelpdeskformadministrator_instance.solved_message.text = solvedMessage'''

#print(registerAdministrator("chan10@mail.com","18010392"))
#print(loginAndGetRole("chan10@mail.com","18010392"))
