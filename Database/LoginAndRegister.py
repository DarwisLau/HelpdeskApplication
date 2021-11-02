from ValidateData import validate_loginCredentials
import sqlite3
from HelpdeskApplicationDatabase import createDatabase
import base64



def registerUser (dataEmail, dataPassword):

    """Function to register a new user account and return "Registration was
       successful." if the registration was successful, whereas return an error
       message if the registration was not successful.
       Both inputs should be string.
       Output is string."""


    #Remove the spaces in front and back of email address since it is the unique identifier
    dataEmail = dataEmail.strip()

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
         "Something wrong when inserting the information into the database."
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

    """Function for a user or an administrator to login and return "Welcome
       user, you have successfully logged in." if the user has successfully
       logged in, whereas return "Welcome administrator, you have successfully
       logged in." if the administrator has successfully logged in, whereas
       return an error message if the login was not successful.
       The first argument should be string, whereas the second argument (password)
       should be base64 byte.
       Output is string."""
    

    #Validate data
    dataEmail = dataEmail.strip()
    errorMessage = validate_loginCredentials(dataEmail, dataPassword)
    if errorMessage != None:
        return errorMessage

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
                 "Welcome user, you have successfully logged in.",
                 "Something wrong when logging in (database)."
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
                     "Welcome administrator, you have successfully logged in.",
                     "Something wrong when logging in (database)."
                    ) message;
                    ''',
                    (dataEmail,))
                    returnMessage = dbCursor.fetchone()
                    return returnMessage[0]
                
    except sqlite3.Error as errorMessage:
        return errorMessage
    finally:
        dbConnection.close()



def logout (dataEmail, theRole):

    """Function for a user or an administrator to logout and return "You have
       successfully logged out." if the logout was successful, whereas return
       an error message if the logout was not successful.
       Input should be both string.
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
             "You have successfully logged out.",
             "Something wrong when logging out (database)."
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
            "You have successfully logged out.",
            "Something wrong then logging out (database)."
            ) message;
            ''',
            (dataEmail,))
            returnMessage = dbCursor.fetchone()
            return returnMessage[0]

        else:
            return "Something wrong when logging out (the role is neither 'user' nor 'administrator')."
    
    except sqlite3.Error as errorMessage:
        return errorMessage
    finally:
        dbConnection.close()



def registerAdministrator (dataEmail, dataPassword):

    """Function to register a new administrator account from the backend.
       Input should be both string.
       No output."""

    #Encrypt password and validate data
    dataEmail = dataEmail.strip()
    dataPassword = dataPassword.encode("utf-8")
    dataPassword = base64.b64encode(dataPassword)
    errorMessage = validate_loginCredentials(dataEmail, dataPassword)
    if errorMessage != None:
        print(errorMessage)
        return

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
            print("This administrator already exists.")
            return

        #Check whether the email address is used by a user or not
        dbCursor.execute('''
        SELECT EXISTS(
         SELECT userEmail FROM User
          WHERE userEmail = ?);
        ''',
        (dataEmail,))
        existUser = dbCursor.fetchone()
        if existUser[0] == 1:
            print("This email address has been used to register a user account, so the same email address cannot be used to register an administrator account.")
            return

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
         "The registration was successful.",
         "Something wrong when inserting the information to the database."
         ) message;
        ''',
        (dataEmail, dataEmail,
         dataEmail, dataPassword,))
        returnMessage = dbCursor.fetchone()
        print(returnMessage[0])
        return

    except sqlite3.Error as errorMessage:
        print(errorMessage)
        return
    finally:
        dbConnection.close()

#Note the email address and password
pw = "q!@opi9043mflkr90*&r"
pw1 = pw.encode("utf-8")
pw2 = base64.b64encode(pw1)
print(registerUser("p18010002@student.newinti.edu.my",pw))
print(login("p18010002@student.newinti.edu.my",pw))
pw = None
print(logout("p18010002@student.newinti.edu.my", "user"))
pw = "q9075yutrJ78$lt"
registerAdministrator("p18000001@student.newinti.edu.my",pw)
pw = pw.encode("utf-8")
pw = base64.b64encode(pw)
print(login("p18000001@student.newinti.edu.my",pw))
print(logout("p18000001@student.newinti.edu.my","administrator"))
pw = None
