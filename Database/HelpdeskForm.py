from ValidateData import validate_loginCredentials, validate_formData
import sqlite3



def userSubmitForm (dataUserEmail, dataFormEmail, dataFormDescription, imagePath):


    try:
        dbConnection = sqlite3.connect("HelpdeskApplication.sqlite")
        dbCursor = dbConnection.cursor()

        #Check whether the person is a user or not
        dbCursor.execute('''
        SELECT EXISTS(
         SELECT userEmail FROM User
          WHERE userEmail = ?);
        ''',
        (dataUserEmail,))
        existUser = dbCursor.fetchone()
        if existUser[0] == 0:
            return "Something wrong about the login credentials (email address). Please log in again."

        #Check whether the user is currently logged in
        dbCursor.execute('''
        SELECT userIsLoggedIn FROM User
         WHERE userEmail = ?;
        ''',
        (dataUserEmail,))
        userLoggedIn = dbCursor.fetchone()
        if userLoggedIn[0] == 0:
            return "You have logged out. Please log in again."

    except sqlite3.Error as errorMessage:
        return errorMessage
    finally:
        dbConnection.close()

    #Open the image file
    try:
        if len(imagePath) > 0:
            imageFileConnection = open(imagePath, "rb")
            dataFormImage = imageFileConnection.read()
        else:
            dataFormImage = b""
    except FileNotFoundError as errorMessage:
        return errorMessage
    finally:
        try:
            imageFileConnection.close()
        except UnboundLocalError:
            pass

    try:
        dbConnection = sqlite3.connect("HelpdeskApplication.sqlite")
        dbCursor = dbConnection.cursor()
            
        #Set the form number
        dbCursor.execute('''
        SELECT MAX(formNumber) FROM Form;
        ''')
        maximumFormNumber = dbCursor.fetchone()
        if maximumFormNumber[0] is not None:
            dataFormNumber = maximumFormNumber[0] + 1
        else:
            dataFormNumber = 1


        #Inserting the form details into the database
        dbCursor.execute('''
        INSERT INTO Form (
         formNumber, userID, formEmail, formDescription, formImage)
        VALUES (
         ?,
         (SELECT UserID FROM User
          WHERE userEmail = ?),
         ?,
         ?,
         ?);
        ''',
        (dataFormNumber, dataUserEmail, dataFormEmail, dataFormDescription, dataFormImage,))

        #Check whether the insertion was successful or not
        dbCursor.execute('''
        SELECT IIF(
         (SELECT userID FROM Form
          WHERE formNumber = ?) =
           (SELECT userID FROM User
            WHERE userEmail = ?) AND
         (SELECT formEmail FROM Form
          WHERE formNumber = ?) = ? AND
         (SELECT formDescription FROM Form
          WHERE formNumber = ?) = ? AND
         (SELECT formImage FROM Form
          WHERE formNumber = ?) = ?,
         "Helpdesk Form is submitted.",
         "Something wrong when inserting the information into the database."
        ) message;
        ''',
        (dataFormNumber, dataUserEmail,
         dataFormNumber, dataFormEmail, 
         dataFormNumber, dataFormDescription,
         dataFormNumber, dataFormImage,))
        returnMessage = dbCursor.fetchone()
        if returnMessage[0] == "Helpdesk Form is submitted.":
            dbConnection.commit()
        return returnMessage[0]

    except sqlite3.Error as errorMessage:
        return errorMessage
    finally:
        dbConnection.close()




def listFormsSubmitted (dataUserEmail):


    try:

        dbConnection = sqlite3.connect("HelpdeskApplication.sqlite")
        dbCursor = dbConnection.cursor()

        #Check whether the person is a user or not
        dbCursor.execute('''
        SELECT EXISTS(
         SELECT userEmail FROM User
          WHERE userEmail = ?);
        ''',
        (dataUserEmail,))
        existUser = dbCursor.fetchone()
        if existUser[0] == 0:
            return "Something wrong about the login credentials (email address). Please log in again."
        
        #Check whether the user is logged in or not
        dbCursor.execute('''
        SELECT userIsLoggedIn FROM User
         WHERE userEmail = ?;
        ''',
        (dataUserEmail,))
        userLoggedIn = dbCursor.fetchone()
        if userLoggedIn[0] == 0:
            return "You have logged out. Please login again."

        #Get forms
        dbCursor.execute('''
        SELECT
         formNumber,
         formIsSolved,
         substr(formDescription, 1, 100)
          FROM Form
           WHERE userID =
            (SELECT userID FROM User
             WHERE userEmail = ?);
        ''',
        (dataUserEmail,))
        formList = []
        for form in dbCursor:
            formList.append(form)
        return formList

    except sqlite3.Error as errorMessage:
        return errorMessage
    finally:
        dbConnection.close()



def listAllForms (dataAdministratorEmail):


    try:

        dbConnection = sqlite3.connect("HelpdeskApplication.sqlite")
        dbCursor = dbConnection.cursor()

        #Check whether the person is an administrator or not
        dbCursor.execute('''
        SELECT EXISTS(
         SELECT administratorEmail FROM Administrator
          WHERE administratorEmail = ?);
        ''',
        (dataAdministratorEmail,))
        existAdministrator = dbCursor.fetchone()
        if existAdministrator[0] == 0:
            return "Something wrong about the login credentials (email adress). Please log in again."
        
        #Check whether the administrator is logged in or not
        dbCursor.execute('''
        SELECT administratorIsLoggedIn FROM Administrator
         WHERE administratorEmail = ?;
        ''',
        (dataAdministratorEmail,))
        administratorLoggedIn = dbCursor.fetchone()
        if administratorLoggedIn[0] == 0:
            return "You have logged out. Please log in again."

        #Get forms
        dbCursor.execute('''
        SELECT
         formNumber,
         formIsSolved,
         substr(formDescription, 1, 100)
          FROM Form;
        ''',)
        formList = []
        for form in dbCursor:
            formList.append(form)
        return formList

    except sqlite3.Error as errorMessage:
        return errorMessage
    finally:
        dbConnection.close()



def viewForm (dataClientRole, dataClientEmail, dataFormNumber):


    try:

        dbConnection = sqlite3.connect("HelpdeskApplication.sqlite")
        dbCursor = dbConnection.cursor()

        if dataClientRole == "user":
            #Check whether the person is a user or not
            dbCursor.execute('''
            SELECT EXISTS(
             SELECT userEmail FROM User
              WHERE userEmail = ?);
            ''',
            (dataClientEmail,))
            existUser = dbCursor.fetchone()
            if existUser[0] == 0:
                return "Something wrong about the login credentials (email address). Please log in again."

            #Check whether the user has logged in
            dbCursor.execute('''
            SELECT userIsLoggedIn FROM User
             WHERE userEmail = ?;
            ''',
            (dataClientEmail,))
            userLoggedIn = dbCursor.fetchone()
            if userLoggedIn[0] == 0:
                return "You have logged out. Please log in again."

            #Check whether the user is the user who submitted the Helpdesk Form
            dbCursor.execute('''
            SELECT IIF(
             (SELECT u.userEmail
              FROM User u, Form f
               WHERE
                f.formNumber = ? AND
                f.userID = u.userID) = ?,
             1,
             0
            ) isCorrectUser;
            ''',
            (dataFormNumber, dataClientEmail,))
            correctUser = dbCursor.fetchone()
            if correctUser[0] == 0:
                return "Something wrong about either the form number or the login credentials (email address). Please try to reload the form list or log in again."

        else:
            #Check whether the person is an administrator or not
            dbCursor.execute('''
            SELECT EXISTS(
             SELECT administratorEmail FROM Administrator
              WHERE administratorEmail = ?);
            ''',
            (dataClientEmail,))
            existAdministrator = dbCursor.fetchone()
            if existAdministrator[0] == 0:
                return "Something wrong about the login credentials (email address). Please log in again."

            #Check whether the administrator has logged in
            dbCursor.execute('''
            SELECT administratorIsLoggedIn FROM Administrator
             WHERE administratorEmail = ?;
            ''',
            (dataClientEmail,))
            administratorLoggedIn = dbCursor.fetchone()
            if administratorLoggedIn[0] == 0:
                return "You have logged out. Please log in again."

            #Record the viewing of the form by the administrator
            dbCursor.execute('''
            INSERT INTO AdministratorViewingOfForm (
             administratorID, formDateTimeViewed, formNumber)
            VALUES(
             (SELECT administratorID FROM Administrator
              WHERE administratorEmail = ?),
             (SELECT datetime("now")),
             ?);
            ''',
            (dataClientEmail, dataFormNumber,))

            dbCursor.execute('''
            SELECT a.administratorEmail, MAX(v.formDateTimeViewed)
             FROM Administrator a, AdministratorViewingOFForm v
              WHERE
               v.formNumber = ? AND
               v.administratorID = a.administratorID;
            ''',
            (dataFormNumber,))
            isRecorded = dbCursor.fetchone()
            if isRecorded[0] == dataClientEmail:
                dbConnection.commit()
            else:
                return "Something wrong when recording the administrator who viewed the form."

        #Get the form details
        dbCursor.execute('''
        SELECT
         f.formNumber,
         f.formIsSolved,
         f.formEmail,
         u.userEmail,
         f.formDescription,
         f.formImage
          FROM Form f, User u
           WHERE
            f.formNumber = ? AND
            f.userID = u.userID;
        ''',
        (dataFormNumber, ))
        formDetails = dbCursor.fetchone()

        #Get an indication of whether there is an image attached to the Helpdesk Form
        dbCursor.execute('''
        SELECT IIF(
         (SELECT formImage FROM Form
          WHERE formNumber = ?) = ?,
         0,
         1
        ) hasImage;
        ''',
        (dataFormNumber, b"",))
        hasImage = dbCursor.fetchone()
        formDetails = list(formDetails)
        formDetails.append(hasImage[0])

        #Get the administrator's email whom solved the Helpdesk Form if it is already solved
        if formDetails[1] == 1:
            dbCursor.execute('''
            SELECT a.administratorEmail
             FROM Administrator a, AdministratorViewingOfForm v
              WHERE
               v.formSetAsSolved = 1 AND
               v.formNumber = ? AND
               v.administratorID = a.administratorID;
            ''',
            (dataFormNumber,))
            administratorSolved = dbCursor.fetchone()
            formDetails.append(administratorSolved[0])

        return formDetails

    except sqlite3.Error as errorMessage:
        return errorMessage
    finally:
        dbConnection.close()



def setFormAsSolved (dataAdministratorEmail, dataFormNumber):


    try:

        dbConnection = sqlite3.connect("HelpdeskApplication.sqlite")
        dbCursor = dbConnection.cursor()

        #Check whether the person is an administrator or not
        dbCursor.execute('''
        SELECT EXISTS(
         SELECT administratorEmail FROM Administrator
          WHERE administratorEmail = ?);
        ''',
        (dataAdministratorEmail,))
        existAdministrator = dbCursor.fetchone()
        if existAdministrator[0] == 0:
            return "Something wrong about the login credentials (email address). Please log in again."

        #Check whether the administrator is loggeed in
        dbCursor.execute('''
        SELECT administratorIsLoggedIn FROM Administrator
         WHERE administratorEmail = ?;
        ''',
        (dataAdministratorEmail,))
        administratorLoggedIn = dbCursor.fetchone()
        if administratorLoggedIn[0] == 0:
            return "You have logged out. Please log in again."

        #Check whether the Helpdesk Form is solved or not
        dbCursor.execute('''
        SELECT formIsSolved FROM Form
         WHERE formNumber = ?;
        ''',
        (dataFormNumber,))
        isSolved = dbCursor.fetchone()
        if isSolved[0] == 1:
            return "The Helpdesk Form is already solved."

        #Insert the record of the administrator setting the Helpdesk Form as solved
        dbCursor.execute('''
        INSERT INTO AdministratorViewingOfForm (
         administratorID, formDateTimeViewed, formSetAsSolved, formNumber)
        VALUES(
         (SELECT administratorID FROM Administrator
          WHERE administratorEmail = ?),
         (SELECT datetime("now")),
         1,
         ?);
        ''',
        (dataAdministratorEmail, dataFormNumber,))

        #Set the form as solved
        dbCursor.execute('''
        UPDATE Form
         SET formIsSolved = 1
          WHERE formNumber = ?;
        ''',
        (dataFormNumber,))

        #Check the insertion just now was successful or not
        dbCursor.execute('''
        SELECT IIF(
         (SELECT v.formSetAsSolved
          FROM AdministratorViewingOfForm v, Administrator a
           WHERE
            v.formDateTimeViewed =
             (SELECT MAX(formDateTimeViewed)
              FROM AdministratorViewingOfForm
               WHERE formNumber = ?) AND
            v.formNumber = ? AND
            a.administratorEmail = ? AND
            v.administratorID = a.administratorID) = 1,
         1,
         0
        ) recorded;
        ''',
        (dataFormNumber, dataFormNumber, dataAdministratorEmail,))
        recordedInViewing = dbCursor.fetchone()
        if recordedInViewing[0] == 0:
            return "Something wrong when inserting record of administrator setting the Helpdesk Form as solved."

        #Check whether the update was successful or not
        dbCursor.execute('''
        SELECT IIF((
         SELECT formIsSolved FROM Form
          WHERE formNumber = ?) = 1,
         "Status is updated.",
         "Something wrong when updating the status in Form."
        ) message;
        ''',
        (dataFormNumber,))
        returnMessage = dbCursor.fetchone()
        if returnMessage[0] == "Status is updated.":
            dbConnection.commit()
        return returnMessage[0]

    except sqlite3.Error as errorMessage:
        return errorMessage
    finally:
        dbConnection.close()

