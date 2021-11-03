from ValidateData import validate_loginCredentials, validate_formData
import sqlite3



def submitForm (dataUserEmail, dataUserPassword, dataFormEmail, dataFormDescription, imagePath):


    dataUserEmail = dataUseremail.strip()
    errorMessage = validate_loginCredentials(dataUserEmail, dataUserPassword)
    if errorMessage != None:
        return errorMessage

    dataFormEmail = dataFormEmail.strip()
    errorMessage = validate_formData(dataEmail, dataDescription)
    if errorMessage != None:
        return errorMessage

    imageFileConnection = open(imagePath, "rb")
    dataFormImage = imageFileConnection.write()

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
        #Check password
        dbCursor.execute('''
        SELECT IIF ((
         SELECT userPassword FROM User
          WHERE userEmail = ?) = ?,
         1,
         0
        ) isCorrect;
        ''',
        (dataUserEmail, dataUserPassword,))
        passwordIsCorrect = dbCursor.fetchone()
        if passwordIsCorrect[0] == 0:
            dbCursor.execute('''
            UPDATE User
             SET userIsLoggedIn = 0
              WHERE userEmail = ?;
            ''',
            (dataUserEmail,))
            dbConnection.commit()
            return "Something wrong about the login credentials (password). You have been automatically logged out. Please log in again. Sorry for any inconvinience caused."
        dbCursor.execute(dbCursor.execute('''
        SELECT userIsLoggedIn FROM User
         WHERE userEmail = ?;
        ''',
        (dataUserEmail,))
        userLoggedIn = dbCursor.fetchone()
        if userLoggedIn[0] == 0:
            return "You have logged out. Please log in again."
        dbCursor.execute('''
        INSERT INTO Form (
         userID, formEmail, formDescription, formImage)
        VALUES (
         (SELECT UserID FROM User
          WHERE userEmail = ?),
         ?,
         ?,
         ?);
        ''',
        (dataUserEmail, dataFormEmail, dataFormDescription, dataFormImage,))
        dbConnection.commit()
        dbCursor.execute('''
        SELECT IIF((
         (SELECT formEmail FROM Form
          WHERE userID =
           (SELECT userID FROM User
            WHERE userEmail = ?)) = ? AND
         (SELECT formDescription FROM Form
          WHERE userID =
           (SELECT userID FROM User
            WHERE userEmail = ?)) = ? AND
         (SELECT formImage FROM User
          WHERE userID =
           (SELECT userID FROM User
            WHERE userEmail = ?)) = ?),
         "Submission was successful.",
         "Something wrong when inserting the information into the database."
        ) message;
        ''',
        (dataUserEmail, dataFormEmail,
        dataUserEmail, dataFormDescription,
        dataUserEmail, dataFormImage,))
        returnMessage = dbCursor.fetchone()
            return returnMessage[0]

    except sqlite3.Error as errorMessage:
        return errorMessage
    finally:
        imageFileConnection.close()
        dbConnection.close()




def listFormsSubmitted (dataUserEmail, dataUserPassword):

    dataUserEmail = dataUserEmail.strip()
    errorMessage = validate_loginCredentials(dataUserEmail, dataUserPassword)
    if errorMessage != None:
        return errorMessage

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
        #Check password
        dbCursor.execute('''
        SELECT IIF ((
         SELECT userPassword FROM User
          WHERE userEmail = ?) = ?,
         1,
         0
        ) isCorrect;
        ''',
        (dataUserEmail, dataUserPassword,))
        passwordIsCorrect = dbCursor.fetchone()
        if passwordIsCorrect[0] == 0:
            dbCursor.execute('''
            UPDATE User
             SET userIsLoggedIn = 0
            WHERE userEmail = ?;
            ''',
            (dataUserEmail,))
            dbConnection.commit()
            return "Something wrong about the login credentials (password). You have been automatically logged out. Please log in again. Sorry for any inconvinience caused."
        dbCursor.execute(dbCursor.execute('''
        SELECT userIsLoggedIn FROM User
         WHERE userEmail = ?;
        ''',
        (dataUserEmail,))
        userLoggedIn = dbCursor.fetchone()
        if userLoggedIn[0] == 0:
            return "You have logged out. Please login again."
        dbCursor.execute('''
        SELECT formNumber, formDescription FROM Form
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




def viewForm (dataClientRole, dataClientEmail, dataClientPassword, dataFormNumber):

    dataClientRole = dataClientRole.lower()
    if dataClientRole not in ["user", "administrator"]:
        return "Invalid role."
    dataClientEmail = dataClientEmail.strip()
    errorMessage = validate_loginCredentials(dataClientEmail, dataClientPassword)
    if errorMessage != None:
        return errorMessage

    try:

        dbConnection = sqlite3.connect("HelpdeskApplication.sqlite")
        dbCursor = dbConnection.cursor()

        if dataClientRole == "User":
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
            #Check password
            dbCursor.execute('''
            SELECT IIF ((
             SELECT userPassword FROM User
              WHERE userEmail = ?) = ?,
             1,
             0
            ) isCorrect;
            ''',
            (dataClientEmail, dataClientPassword,))
            passwordIsCorrect = dbCursor.fetchone()
            if passwordIsCorrect[0] == 0:
                dbCursor.execute('''
                UPDATE User
                 SET userIsLoggedIn = 0
                WHERE userEmail = ?;
                ''',
                (dataClientEmail,))
                dbConnection.commit()
                return "Something wrong about the login credentials (password). You have been automatically logged out. Please log in again. Sorry for any inconvinience caused."
            dbCursor.execute(dbCursor.execute('''
            SELECT userIsLoggedIn FROM User
             WHERE userEmail = ?;
            ''',
            (dataClientEmail,))
            userLoggedIn = dbCursor.fetchone()
            if userLoggedIn[0] == 0:
                return "You have logged out. Please log in again."
        else if dataClientRole == "Administrator":
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
            #Check password
            dbCursor.execute('''
            SELECT IIF ((
             SELECT administratorPassword FROM Administrator
              WHERE administratorEmail = ?) = ?,
            1,
            0
            ) isCorrect;
            ''',
            (dataClientEmail, dataClientPassword,))
            passwordIsCorrect = dbCursor.fetchone()
            if passwordIsCorrect[0] == 0:
                dbCursor.execute('''
                UPDATE Administrator
                 SET administratorIsLoggedIn = 0
                WHERE administratorEmail = ?;
                ''',
                (dataClientEmail,))
                dbConnection.commit()
                return "Something wrong about the login credentials (password). You have been automatically logged out. Please log in again. Sorry for any inconvinience caused."
            dbCursor.execute(dbCursor.execute('''
            SELECT administratorIsLoggedIn FROM Administrator
             WHERE administratorEmail = ?;
            ''',
            (dataClientEmail,))
            administratorLoggedIn = dbCursor.fetchone()
            if administratorLoggedIn[0] == 0:
                return "You have logged out. Please log in again."
            dbCursor.execute('''
            INSERT INTO AdministratorViewingOfForm (
             administratorID, formDateTimeViewed, formNumber)
            VALUES(
             SELECT administratorID FROM Administrator
              WHERE administratorEmail = ?,
             SELECT datetime("now"),
             ?);
            ''',
            (dataClientEmail, dataFormNumber,))
            dbConnection.commit()
            dbCursor.execute('''
            SELECT IIF(
             (SELECT formNumber FROM AdministratorViewingOfForm
              WHERE administratorID =
             (SELECT administratorID FROM Administrator
              WHERE administratorEmail = ?) = ?,
             1,
             0
            ) isRecorded;
            ''',
            (dataClientEmail, dataFormNumber,))
            viewingIsRecorded = dbCursor.fetchone()
            if viewingIsRecorded[0] == 0:
                return "Something wrong when creating new record in AdministratorViewingOfForm)."                        
        dbCursor.execute('''
        SELECT formIsSolved, formEmail, formDescription, formImage FROM Form
         WHERE formNumber = ?;
        ''',
        (dataFormNumber,))
        formDetails = dbCursor.fetchone()
        return formDetails[0]

    except sqlite3.Error as errorMessage:
        return errorMessage
    finally:
        dbConnection.close()




def listAllForms (dataAdministratorEmail, dataAdministratorPassword):

    dataAdministratorEmail = dataAdministratorEmail.strip()
    errorMessage = validate_loginCredentials(dataAdministratorEmail, dataadministratorPassword)
    if errorMessage != None:
        return errorMessage

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
        #Check password
        dbCursor.execute('''
        SELECT IIF ((
         SELECT administratorPassword FROM Administrator
          WHERE administratorEmail = ?) = ?,
         1,
         0
        ) isCorrect;
        ''',
        (dataAdministratorEmail, dataAdministratorPassword,))
        passwordIsCorrect = dbCursor.fetchone()
        if passwordIsCorrect[0] == 0:
            dbCursor.execute('''
            UPDATE Administrator
             SET administratorIsLoggedIn = 0
            WHERE administratorEmail = ?;
            ''',
            (dataAdministratorEmail,))
            dbConnection.commit()
            return "Something wrong about the login credentials (password). You have been automatically logged out. Please log in again. Sorry for any inconvinience caused."
        dbCursor.execute(dbCursor.execute('''
        SELECT administratorIsLoggedIn FROM Administrator
         WHERE administratorEmail = ?;
        ''',
        (dataAdministratorEmail,))
        administratorLoggedIn = dbCursor.fetchone()
        if administratorLoggedIn[0] == 0:
            return "You have logged out. Please log in again."
        dbCursor.execute('''
        SELECT formNumber, formDescription FROM Form;
        ''',)
        formList = []
        for form in dbCursor:
            formList.append(form)
        return formList

    except sqlite3.Error as errorMessage:
        return errorMessage
    finally:
        dbConnection.close()




def setFormAsSolved (dataAdministratorEmail, dataAdministratorPassword, dataFormNumber):

    dataAdministratorEmail = dataAdministratorEmail.strip()
    errorMessage = validate(dataAdministratorEmail, dataAdministratorPassword)
    if errorMEssage != None:
        return errorMessage

    try:

        dbConnection.connect("HelpdeskApplication.sqlite")
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
        #Check password
        dbCursor.execute('''
        SELECT IIF ((
         SELECT administratorPassword FROM Administrator
          WHERE administratorEmail = ?) = ?,
         1,
         0
        ) isCorrect;
        ''',
        (dataAdministratorEmail, dataAdministratorPassword,))
        passwordIsCorrect = dbCursor.fetchone()
        if passwordIsCorrect[0] == 0:
            dbCursor.execute('''
            UPDATE Administrator
             SET administratorIsLoggedIn = 0
            WHERE administratorEmail = ?;
            ''',
            (dataAdministratorEmail,))
            dbConnection.commit()
            return "Something wrong about the login credentials (password). You have been automatically logged out. Please log in again. Sorry for any inconvinience caused."
        dbCursor.execute(dbCursor.execute('''
        SELECT administratorIsLoggedIn FROM Administrator
         WHERE administratorEmail = ?;
        ''',
        (dataAdministratorEmail,))
        administratorLoggedIn = dbCursor.fetchone()
        if administratorLoggedIn[0] == 0:
            return "You have logged out. Please log in again."
        dbCursor.execute('''
        SELECT formIsSolved FROM Form
         WHERE formNumber = ?;
        ''',
        (dataFormNumber,))
        isSolved = dbCursor.fetchone()
        if isSolved[0] == 1:
            return "The Helpdesk Form is already solved."
        dbCursor.execute('''
        SELECT EXISTS(
         SELECT formNumber FROM AdministratorViewingOfForm
          WHERE formNumber = ? AND
           formSetAsSolved = 1);
        ''',
        (dataFormNumber,))
        existRecord = dbCursor.fetchone()
        if existRecord == 0:
            dbCursor.execute('''
            SELECT IIF(
             SELECT EXISTS(
              SELECT formNumber FROM AdministratorViewingOfFAQ
               WHERE
                administratorID = (
                 SELECT administratorID FROM Administrator
                  WHERE administratorEmail = ?) AND
                formNumber = ?) AND
             ((SELECT datetime("now")) -
              (SELECT MAX(formDateTimeViewed) FROM AdministratorViewingOfFAQ
               WHERE
                administratorID = (
                 SELECT administratorID FROM Administrator
                  WHERE administratorEmail = ?) AND
                formNumber = ?)) <= 1),
             1,
             0
             ) hasRecordWithinOneDay;
             ''',
            (dataAdministratorEmail, dataFormNumber,
             dataAdministratorEmail, dataFormNumber,))
            hasRecordWithinOneDay = dbCursor.fetchone()
            if hasRecordWithinOneDay[0] == 0:
                dbCursor.execute('''
                INSERT INTO AdministratorViewingOfForm (
                 administratorID, formDateTimeViewed, formNumber)
                VALUES(
                 SELECT administratorID FROM Administrator
                  WHERE administratorEmail = ?,
                 SELECT datetime("now"),
                 ?);
                ''',
                (dataAdministratorEmail, dataAdministratorNumber,))
                dbConnection.commit()
                dbCursor.execute('''
                SELECT IIF(
                 (SELECT formNumber FROM AdministratorViewingOfForm
                  WHERE administratorID =
                   (SELECT administratorID FROM Administrator
                    WHERE administratorEmail = ?) = ?,
                 1,
                 0
                ) isRecorded;
                ''',
                (dataAdministratorEmail, dataFormNumber,))
                viewingIsRecorded = dbCursor.fetchone()
                if viewingIsRecorded[0] == 0:
                    return "Something wrong about creating new record in AdministratorViewingOfForm)."                        
            dbCursor.execute('''
            UPDATE AdministratorViewingOfForm 
             SET formSetAsSolved = 1
              WHERE formDateTimeViewed = (
               SELECT MAX(formDateTimeViewed) FROM AdministratorViewingOfForm
                WHERE
                 administratorID = (
                  SELECT administratorID FROM Administrator
                   WHERE administratorEmail = ?) AND
                 formNumber = ?);
            ''',
            (dataAdministratorEmail, dataFormNumber,))
            dbConnection.commit()
            dbCursor.execute('''
            SELECT formSetAsSolved FROM AdministratorViewingOfForm
             WHERE formDateTimeViewed = (
              SELECT MAX(formDateTimeViewed) FROM AdministratorViewingOfForm
               WHERE
                administratorID = (
                 SELECT administratorID FROM Administrator
                  WHERE administratorEmail = ?) AND
                formNumber = ?)
            ''',
            (dataAdministratorEmail, dataFormNumber,))
            recordedInViewing = dbCursor.execute()
            if recordedInViewing[0] == 0:
                return "Something wrong when updating record in AdministratorViewingOfForm)."
        dbCursor.execute('''
        UPDATE Form
         SET formIsSolved = 1
          WHERE formNumber = ?;
        ''',
        (dataFormNumber,))
        dbConnection.commit()
        dbCursor.execute('''
        SELECT IIF((
         SELECT formIsSolved FROM Form
          WHERE formNumber = ?) = 1,
         "Update was successful.",
         "Something wrong when updating the status in Form."
        ) message;
        ''',
        (dataFormNumber,))
        returnMessage = dbCursor.fetchone()
        return returnMessage[0]

    except sqlite3.Error as errorMessage:
        return errorMessage
    finally:
        dbConnection.close()
    
        
    
