from ValidateData import validate_loginCredentials
import sqlite3
import base64
from HelpdeskApplicationDatabase import createDatabase


def registerUser (dataEmail, dataPassword):

    """Function to register a new user account and return "Registration was
       successful." if the registration was successful, whereas return an error
       message if the registration was not successful.
       Input should be string.
       Output is string."""


    #Create a new database if database does not exist
    try:
        createDatabase()
    except:
        pass

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
    except:
        pass
    
    #Remove the spaces in front and back of email address since it is the unique identifier
    dataEmail = dataEmail.strip()

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
    
    dataEmail = dataEmail.strip()
    
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
       No output."""

    #Encrypt password and validate data
    dataEmail = dataEmail.strip()
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
         "Something wrong when inserting the information to the database. Please try again."
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
