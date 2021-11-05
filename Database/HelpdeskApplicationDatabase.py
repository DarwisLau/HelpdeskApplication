import sqlite3

def createDatabase():
    try:
        dbConnection = sqlite3.connect("HelpdeskApplication.sqlite")
        dbCursor = dbConnection.cursor()
        dbCursor.execute('''
        CREATE TABLE User(
         userID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
         userEmail VARCHAR(150) NOT NULL UNIQUE,
         userPassword VARCHAR(20) NOT NULL CHECK(LENGTH(userPassword) >= 8),
         userIsLoggedIn BOOLEAN NOT NULL DEFAULT 0
        );
        ''')

        dbCursor.execute('''
        CREATE TABLE Administrator(
         administratorID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
         administratorEmail VARCHAR(150) NOT NULL UNIQUE,
         administratorPassword VARCHAR(20) NOT NULL CHECK(LENGTH(administratorPassword) >= 8),
         administratorIsLoggedIn BOOLEAN NOT NULL DEFAULT 0
         );
        ''')

        dbCursor.execute('''
        CREATE TABLE Form(
         formNumber INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
         userID INTEGER NOT NULL,
         formEmail VARCHAR(150),
         formDescription TEXT NOT NULL,
         formIsSolved BOOLEAN NOT NULL DEFAULT 0,
         formImage BLOB,
         FOREIGN KEY (userID)
          REFERENCES User(userID)
        );
        ''')

        dbCursor.execute('''
        CREATE TABLE FrequentlyAskedQuestion(
         FAQNumber INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
         FAQIsForComputer BOOLEAN NOT NULL,
         FAQIsForSmartphone BOOLEAN NOT NULL,
         FAQCategory VARCHAR(15) NOT NULL CHECK(FAQCategory IN ('hardware', 'security', 'architecture', 'connections')),
         FAQTitle VARCHAR(300) NOT NULL,
         FAQKeyword VARCHAR(300),
         FAQSubcategory VARCHAR(100) CHECK(FAQSubCategory NOT IN ('computer', 'smartphone', 'hardware', 'security', 'architecture', 'connections')),
         FAQContent TEXT NOT NULL,
         FAQLinkPartName VARCHAR(200) CHECK(FAQLinkURL != NULL),
         FAQLinkURL TEXT CHECK(FAQLinkPartName != NULL)
        );
        ''')

        dbCursor.execute('''
        CREATE TABLE UserViewingOfFAQ(
         userID INTEGER NOT NULL,
         FAQIsHelpful BOOLEAN NOT NULL DEFAULT 0,
         FAQDateTimeViewed TIMESTRING NOT NULL,
         FAQNumber INTEGER NOT NULL,
         FOREIGN KEY (userID)
          REFERENCES UserViewingOfFAQ(userID),
         FOREIGN KEY (FAQNumber)
          REFERENCES FrequentlyAskedQuestion(FAQNumber)
        );
        ''')

        dbCursor.execute('''
        CREATE TABLE AdministratorEditingOfFAQ(
         administratorID INTEGER NOT NULL,
         FAQDateTimeEdited TIMESTRING NOT NULL,
         FAQNumber INTEGER NOT NULL,
         FOREIGN KEY (administratorID)
          REFERENCES Administrator(administratorID),
         FOREIGN KEY (FAQNumber)
          REFERENCES FrequentlyAskedQuestion(FAQNumber)
        );
        ''')

        dbCursor.execute('''
        CREATE TABLE AdministratorViewingOfForm(
         administratorID INTEGER NOT NULL,
         formDateTimeViewed TIMESTRING NOT NULL,
         formSetAsSolved BOOLEAN,
         formNumber INTEGER NOT NULL,
         FOREIGN KEY (administratorID)
          REFERENCES Administrator(administratorID),
         FOREIGN KEY (formNumber)
          REFERENCES Form(formNumber)
        );
        ''')

        dbConnection.commit()

    except sqlite3.Error as errorMessage:
        return errorMessage

    finally:
        dbConnection.close()



def dropDatabase():
    try:
        dbConnection = sqlite3.connect("HelpdeskApplication.sqlite")
        dbCursor = dbConnection.cursor()

        dbCursor.execute('''
        DROP TABLE User;
        ''')

        dbCursor.execute('''
        DROP TABLE Administrator;
        ''')

        dbCursor.execute('''
        DROP TABLE Form;
        ''')

        dbCursor.execute('''
        DROP TABLE FrequentlyAskedQuestion;
        ''')

        dbCursor.execute('''
        DROP TABLE UserViewingOfFAQ;
        ''')

        dbCursor.execute('''
        DROP TABLE AdministratorEditingOfFAQ;
        ''')

        dbCursor.execute('''
        DROP TABLE AdministratorViewingOfForm;
        ''')

    except sqlite3.Error as errorMessage:
        return errorMessage
    finally:
        dbConnection.close()


def checkUser():
    try:
        dbConnection = sqlite3.connect("HelpdeskApplication.sqlite")
        dbCursor = dbConnection.cursor()

        dbCursor.execute('''
        SELECT * FROM User;
        ''')
        for info in dbCursor:
            return info

    except sqlite3.Error as errorMessage:
        return errorMessage
    finally:
        dbConnection.close()
