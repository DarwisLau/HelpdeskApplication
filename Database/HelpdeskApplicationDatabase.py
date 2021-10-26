import sqlite3

dbConnection = sqlite3.connect('HelpdeskApplication.sqlite') #If database with this name exist in same folder as this file, access to database; if not, create a database with this name in the same folder as this file
dbCursor = dbConnection.cursor()

dbCursor.execute('''
CREATE TABLE User(
 userID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
 userEmail VARCHAR(150) NOT NULL UNIQUE,
 userPassword VARCHAR(28) NOT NULL CHECK(LENGTH(userPassword) >= 12),
 userIsLoggedIn BOOLEAN NOT NULL DEFAULT 0
);
''')

dbCursor.execute('''
CREATE TABLE Administrator(
 administratorID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
 administratorEmail VARCHAR(150) NOT NULL UNIQUE,
 administratorPassword VARCHAR(28) NOT NULL CHECK(LENGTH(administratorPassword) >= 12),
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
 FAQCategory VARCHAR(15) NOT NULL CHECK(FAQCategory IN ('Hardware', 'Security', 'Architecture', 'Connections')),
 FAQTitle VARCHAR(300) NOT NULL,
 FAQKeyword VARCHAR(300),
 FAQSubcategory VARCHAR(100),
 FAQContent TEXT NOT NULL,
 FAQLinkPartName VARCHAR(200),
 FAQLinkURL TEXT CHECK(FAQLinkPartName != NULL)
);
''')

dbCursor.execute('''
CREATE TABLE UserViewingOfFAQ(
 userID INTEGER NOT NULL,
 FAQIsHelpful BOOLEAN,
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
 formNumber INTEGER NOT NULL,
 FOREIGN KEY (administratorID)
  REFERENCES Administrator(administratorID),
 FOREIGN KEY (formNumber)
  REFERENCES Form(formNumber)
);
''')

dbConnection.commit()

dbConnection.close()
