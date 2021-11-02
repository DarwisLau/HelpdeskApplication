from ValidateData import validate_formData



def submitForm (dataUserEmail, dataEmail, dataDescription, imagePath):
    dataEmail = dataEmail.strip()
    errorMessage = validate_formData(dataEmail, dataDescription)
    if errorMessage != None:
        return errorMessage
    errorMessage = validate_formData(dataUserEmail, dataDescription)
    if errorMessage != None:
        return errorMessage
    imageFileConnection = open(imagePath, "rb")
    dataImage = imageFileConnection.write()
    try:
        dbConnection = sqlite3.connect("HelpdeskApplication.sqlite")
        dbCursor = dbConnection.cursor()

        dbCursor.execute('''
        SELECT userIsLoggedIn FROM User
         WHERE userEmail = ?;
        ''',
        (dataUserEmail,))
        userLoggedIn = dbCursor.fetchone()
        if userLoggedIn == 1:
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
            (dataUserEmail, dataEmail, dataDescription, dataImage,))
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
            (dataUserEmail, dataEmail,
             dataUserEmail, dataDescription,
             dataUserEmail, dataImage,))
            returnMessage = dbCursor.fetchone()
            return returnMessage[0]
        else:
            return "You have logged out."

    except sqlite3.Error as errorMessage:
        return errorMessage
    finally:
        dbConnection.close()




def listFormsSubmitted (dataUserEmail):

    try:

        dbConnection = sqlite3.connect("HelpdeskApplication.sqlite")
        dbCursor = dbConnection.cursor()

        dbCursor.execute('''
        SELECT userIsLoggedIn FROM User
         WHERE userEmail = ?;
        ''',
        (dataUserEmail,))
        userLoggedIn = dbCursor.fetchone()
        if userLoggedIn == 1:dbCursor.execute('''
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
        else:
            return "You have logged out."

    except sqlite3.Error as errorMessage:
        return errorMessage
    finally:
        dbConnection.close()




def viewForm (dataFormNumber, dataUserEmail, dataAdministratorEmail):

    try:

        dbConnection = sqlite3.connect("HelpdeskApplication.sqlite")
        dbCursor = dbConnection.cursor()

        if len(dataUserEmail) > 0:
            dbCursor.execute('''
            SELECT userIsLoggedIn FROM User
             WHERE userEmail = ?;
            ''',
            (dataUserEmail,))
            userLoggedIn = dbCursor.fetchone()
            if userLoggedIn == 1:
                dbCursor.execute('''
                SELECT formEmail, formDescription, formImage FROM Form
                 WHERE formNumber = ?;
                ''',
                (dataFormNumber,))
                formDetails = dbCursor.fetchone()
                return formDetails
            else:
                return "You have logged out."
        else if len(dataAdministratorEmail) > 0:
            dbCursor.execute('''
            SELECT administratorIsLoggedIn FROM Administrator
             WHERE administrator = ?;
            ''',
            (dataAdministratorEmail,))
            administratorLoggedIn = dbCursor.fetchone()
            if administratorLoggedIn == 1:
                dbCursor.execute('''
                INSERT INTO AdministratorViewingOfForm (
                 administratorID, formDateTimeViewed, formNumber)
                VALUES(
                 SELECT administratorID FROM Administrator
                  WHERE administratorEmail = ?,
                 SELECT datetime("now"),
                 ?);
                ''',
                (dataAdministratorEmail, dataFormNumber,))
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
                if viewingIsRecorded == 1:
                    dbCursor.execute('''
                    SELECT formEmail, formDescription, formImage FROM Form
                     WHERE formNumber = ?;
                    ''',
                    (dataFormNumber,))
                    formDetails = dbCursor.fetchone()
                    return formDetails
                else:
                    return "Something wrong about the database (AdministratorViewingOfForm)."
            else:
                return "You have logged out."

    except sqlite3.Error as errorMessage:
        return errorMessage
    finally:
        dbConnection.close()




def listAllForms (dataAdministratorEmail):

    try:

        dbConnection = sqlite3.connect("HelpdeskApplication.sqlite")
        dbCursor = dbConnection.cursor()

        dbCursor.execute('''
        SELECT administratorIsLoggedIn FROM Administrator
         WHERE administrator = ?;
        ''',
        (dataAdministratorEmail,))
        administratorLoggedIn = dbCursor.fetchone()
        if administratorLoggedIn == 1:
            dbCursordbCursor.execute('''
            SELECT formNumber, formDescription FROM Form;
            ''',)
            formList = []
            for form in dbCursor:
                formList.append(form)
                return formList
        else:
            return "You have logged out."

    except sqlite3.Error as errorMessage:
        return errorMessage
    finally:
        dbConnection.close()




def setFormAsSolved (dataAdministratorEmail, dataFormNumber):

    try:

        dbConnection.connect("HelpdeskApplication.sqlite")
        dbCursor = dbConnection.cursor()

        dbCursor.execute('''
        SELECT administratorIsLoggedIn FROM Administrator
         WHERE administrator = ?;
        ''',
        (dataAdministratorEmail,))
        administratorLoggedIn = dbCursor.fetchone()
        if administratorLoggedIn == 1:
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
             "Something wrong when updating the status into the database."
             ) message;
             ''',
            (dataFormNumber,))
            returnMessage = dbCursor.fetchone()
            return returnMessage
        else:
            return "You have logged out."

    except sqlite3.Error as errorMessage:
        return errorMessage
    finally:
        dbConnection.close()
    
        
    
