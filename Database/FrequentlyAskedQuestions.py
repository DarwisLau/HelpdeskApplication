from ValidateData import validate_loginCredentials, validate_FAQData
import sqlite3
import random


def addFAQ (dataAdministratorEmail, dataAdministratorPassword, dataFAQIsForComputer, dataFAQIsForSmartphone, dataFAQCategory, dataFAQTitle, dataFAQKeyword, dataFAQSubcategory, dataFAQContent, dataFAQLinkPartName, dataFAQLinkURL):

    dataAdministratorEmail = dataAdministratorEmail.strip()
    errorMessage = validate(dataAdministratorEmail, dataAdministratorPassword)
    if errorMEssage != None:
        return errorMessage

    dataCFAQCategory = dataFAQCategory.lower()
    errorMessage = validate_FAQData(dataFAQIsForComputer, dataFAQIsForSmartphone, dataFAQCategory, dataFAQTitle, dataFAQKeyword, dataFAQSubcategory, dataFAQContent, dataFAQLinkPartName, dataFAQLinkURL)
    if errorMessage != None:
        return erroMessage

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
        dbCursor.execute('''
        SELECT administratorIsLoggedIn FROM Administrator
         WHERE administratorEmail = ?;
        ''',
        (dataAdministratorEmail,))
        administratorLoggedIn = dbCursor.fetchone()
        if administratorLoggedIn[0] == 0:
            return "You have logged out. Please log in again."
        dbCursor.execute('''
        SELECT FAQNumber FROM FrequentlyAskedQuestions;
        ''',)
        listOfFAQNumber = []
        for number in dbCursor:
            listOfFAQNumber.append(number)
        dataFAQNumber = random.randint(1, 1000)
        while dataFAQNumber in listOfFAQNumber:
            dataFAQNumber = random.randint(1, 1000)
        dbCursor.execute('''
        INSERT INTO FrequentlyAskedQuestion(
         FAQNumber,
         FAQIsForComputer,
         FAQIsForSmartphone,
         FAQCategory,
         FAQTitle,
         FAQKeyword,
         FAQSubcategory,
         FAQContent,
         FAQLinkPartName,
         FAQLinkURL)
        VALUES(
         ?,
         ?,
         ?,
         ?,
         ?,
         ?,
         ?,
         ?,
         ?);
        ''',
        (dataFAQNumber,
         dataFAQIsForComputer,
         dataFAQIsForSmartphone,
         dataFAQCategory,
         dataFAQTitle,
         dataFAQKeyword,
         dataFAQSubcategory,
         dataFAQContent,
         dataFAQLinkPartName,
         dataFAQLinkURL,))
        dbConnection.commit()
        dbCursor.execute('''
        SELECT IIF(
         (SELECT FAQIsForComputer FROM FrequentlyAskedQuestion
          WHERE FAQNumber = ?) = ? AND
         (SELECT FAQIsForSmartphone FROM FrequentlyAskedQuestion
          WHERE FAQNumber = ?) = ? AND
         (SELECT FAQCategory FROM FrequentlyAskedQuestion
          WHERE FAQNumber = ?) = ? AND
         (SELECT FAQTitle FROM FrequentlyAskedQuestion
          WHERE FAQNumber = ?) = ? AND
         (SELECT FAQKeyword FROM FrequentlyAskedQuestion
          WHERE FAQNumber = ?) = ? AND
         (SELECT FAQSubcategory FROM FrequentlyAskedQuestion
          WHERE FAQNumber = ?) = ? AND
         (SELECT FAQContent FROM FrequentlyAskedQuestion
          WHERE FAQNumber = ?) = ? AND
         (SELECT FAQLinkPartName FROM FrequentlyAskedQuestion
          WHERE FAQNumber = ?) = ? AND
         (SELECT FAQLinkURL FROM FrequentlyAskedQuestion
          WHERE FAQNumber = ?) = ?,
         1,
         0) isAdded;
         ''',
        (dataFAQNumber, dataFAQIsForComputer,
         dataFAQNumber, dataFAQIsForSmartphone,
         dataFAQNumber, dataFAQCategory,
         dataFAQNumber, dataFAQTitle,
         dataFAQNumber, dataFAQKeyword,
         dataFAQNumber, dataFAQSubcategory,
         dataFAQNumber, dataFAQContent,
         dataFAQNumber, dataFAQLinkPartName,
         dataFAQNumber, dataFAQLinkURL,))
        created = dbCursor.fetchone()
        if isAdded[0] == 0:
            return "Something wrong when adding the FAQ to FrequentlyAskedQuestion."
        dbCursor.execute('''
        INSERT INTO AdministratorEditingOfFAQ(
         administratorID, FAQDateTimeEdited, FAQNumber)
        VALUES(
         SELECT administratorID FROM Administrator
          WHERE administratorEmail = ?,
         SELECT datetime("now"),
         ?);
         ''',
        (dataAdministratorEmail, dataFAQNumber,))
        dbConnection.commit()
        dbCursor.execute('''
        SELECT IIF(
         (SELECT administratorID FROM AdministratorViewingOfFAQ
          WHERE FAQNumber = ?) =
         (SELECT administratorID FROM Administrator
          WHERE administratorEmail = ?),
         "The FAQ is added.,
         "Something wrong when recording in AdministratorEditingOfFAQ."
         ) message;
         ''',
        (dataAdministratorEmail, dataFAQNumber,
         dataAdministratorEmail, dataFAQNumber,))
        returnMessage = dbCursor.fetchone()
        return returnMessage
        
    except sqlite3.Error as errorMessage:
        return errorMessage
    finally:
        dbConnection.close()




def editFAQ (dataAdministratorEmail, dataAdministratorPassword, dataFAQNumber, dataFAQIsForComputer, dataFAQIsForSmartphone, dataFAQCategory, dataFAQTitle, dataFAQKeyword, dataFAQSubcategory, dataFAQContent, dataFAQLinkPartName, dataFAQLinkURL):

    dataAdministratorEmail = dataAdministratorEmail.strip()
    errorMessage = validate(dataAdministratorEmail, dataAdministratorPassword)
    if errorMEssage != None:
        return errorMessage

    dataCFAQCategory = dataFAQCategory.lower()
    errorMessage = validate_FAQData(dataFAQIsForComputer, dataFAQIsForSmartphone, dataFAQCategory, dataFAQTitle, dataFAQKeyword, dataFAQSubcategory, dataFAQContent, dataFAQLinkPartName, dataFAQLinkURL)
    if errorMessage != None:
        return erroMessage

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
        dbCursor.execute('''
        SELECT administratorIsLoggedIn FROM Administrator
         WHERE administratorEmail = ?;
        ''',
        (dataAdministratorEmail,))
        administratorLoggedIn = dbCursor.fetchone()
        if administratorLoggedIn[0] == 0:
            return "You have logged out. Please log in again."
        dbCursor.execute('''
        SELECT EXISTS(
         SELECT FAQNumber FROM FrequentlyAskedQuestion
          WHERE FAQNumber = ?);
        ''',
        (dataFAQNumber,))
        existFAQ = dbCursor.fetchone()
        if existFAQ == 0:
            return "The FAQ does not exists."
        dbCursor.execute('''
        INSERT INTO AdministratorEditingOfFAQ(
         administratorID, FAQDateTimeEdited, FAQNumber)
        VALUES(
         SELECT administratorID FROM Administrator
          WHERE administratorEmail = ?,
         SELECT datetime("now"),
         ?);
         ''',
        (dataAdministratorEmail, dataFAQNumber,))
        dbConnection.commit()
        dbCursor.execute('''
        SELECT IIF(
         SELECT EXISTS(
          SELECT formNumber FROM AdministratorViewingOfFAQ
           WHERE
            administratorID = (
             SELECT administratorID FROM Administrator
              WHERE administratorEmail = ?) AND
            formNumber = ?) AND
         ((SELECT datetime("now") -
          (SELECT MAX(FAQdateTimeEdited) FROM AdministratorViewingOfFAQ
           WHERE
            administratorID =
             (SELECT administratorID FROM Administrator
              WHERE administratorEmail = ?) AND
            FAQNumber = ?))*(24*60)) < 1,
         1,
         0
         ) isRecordedInEditingWithinOneMinutesAgo;
         ''',
        (dataAdministratorEmail, dataFAQNumber,
         dataAdministratorEmail, dataFAQnumber,))
        isRecordedInEditingWithinOneMinutesAgo = dbCursor.fetchone()
        if isRecordedInEditingWithinOneMinutesAgo[0] == 0:
            return "Something wrong when recording in AdministratorEditingOfFAQ."
        dbCursor.execute('''
        INSERT INTO FrequentlyAskedQuestion(
         FAQNumber,
         FAQIsForComputer,
         FAQIsForSmartphone,
         FAQCategory,
         FAQTitle,
         FAQKeyword,
         FAQSubcategory,
         FAQContent,
         FAQLinkPartName,
         FAQLinkURL)
        VALUES(
         ?,
         ?,
         ?,
         ?,
         ?,
         ?,
         ?,
         ?,
         ?);
        ''',
        (dataFAQNumber,
         dataFAQIsForComputer,
         dataFAQIsForSmartphone,
         dataFAQCategory,
         dataFAQTitle,
         dataFAQKeyword,
         dataFAQSubcategory,
         dataFAQContent,
         dataFAQLinkPartName,
         dataFAQLinkURL,))
        dbConnection.commit()
        dbCursor.execute('''
        SELECT IIF(
         (SELECT FAQIsForComputer FROM FrequentlyAskedQuestion
          WHERE FAQNumber = ?) = ? AND
         (SELECT FAQIsForSmartphone FROM FrequentlyAskedQuestion
          WHERE FAQNumber = ?) = ? AND
         (SELECT FAQCategory FROM FrequentlyAskedQuestion
          WHERE FAQNumber = ?) = ? AND
         (SELECT FAQTitle FROM FrequentlyAskedQuestion
          WHERE FAQNumber = ?) = ? AND
         (SELECT FAQKeyword FROM FrequentlyAskedQuestion
          WHERE FAQNumber = ?) = ? AND
         (SELECT FAQSubcategory FROM FrequentlyAskedQuestion
          WHERE FAQNumber = ?) = ? AND
         (SELECT FAQContent FROM FrequentlyAskedQuestion
          WHERE FAQNumber = ?) = ? AND
         (SELECT FAQLinkPartName FROM FrequentlyAskedQuestion
          WHERE FAQNumber = ?) = ? AND
         (SELECT FAQLinkURL FROM FrequentlyAskedQuestion
          WHERE FAQNumber = ?) = ?,
         "The FAQ is edited."
         "Something wrong when editing the FAQ in FrequentlyAskedQuestion."
         ) message;
         ''',
        (dataFAQNumber, dataFAQIsForComputer,
         dataFAQNumber, dataFAQIsForSmartphone,
         dataFAQNumber, dataFAQCategory,
         dataFAQNumber, dataFAQTitle,
         dataFAQNumber, dataFAQKeyword,
         dataFAQNumber, dataFAQSubcategory,
         dataFAQNumber, dataFAQContent,
         dataFAQNumber, dataFAQLinkPartName,
         dataFAQNumber, dataFAQLinkURL,))
        returnMessage = dbCursor.fetchone()
        return returnMessage[0]

    except sqlite3.Error as errorMessage:
        return errorMessage
    finally:
        dbConnection.close()



def deleteFAQ (dataAdministratorEmail, dataAdministratorPassword, dataFAQNumber):

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
        dbCursor.execute('''
        SELECT administratorIsLoggedIn FROM Administrator
         WHERE administratorEmail = ?;
        ''',
        (dataAdministratorEmail,))
        administratorLoggedIn = dbCursor.fetchone()
        if administratorLoggedIn[0] == 0:
            return "You have logged out. Please log in again."
        dbCursor.execute('''
        SELECT EXISTS(
         SELECT FAQNumber FROM FrequentlyAskedQuestion
          WHERE FAQNumber = ?);
        ''',
        (dataFAQNumber,))
        existFAQ = dbCursor.fetchone()
        if existFAQ == 0:
            return "The FAQ does not exists."
        dbCursor.execute('''
        DELETE FROM AdministratorEditingOfFAQ
         WHERE FAQNumber = ?;
        ''',
        (dataFAQNumber,))
        dbConnection.commit()
        dbCursor.execute('''
        SELECT EXISTS(
         SELECT FAQNumber FROM AdministratorEditingOfFAQ
          WHERE FAQNumber = ?);
        ''',
        (dataFAQNumber,))
        existFAQ = dbCursor.fetchone()
        if existFAQ == 1:
            return "Something wrong when deleting the record of the FAQ from AdministratorEditingOfFAQ."
        dbCursor.execute('''
        DELETE FROM FrequentlyAskedQuestion
         WHERE FAQNumber = ?;
        ''',
        (dataFAQNumber,))
        dbConnection.commit()
        dbCursor.execute('''
        SELECT IIF(
         SELECT EXISTS(
          SELECT FAQNumber FROM FrequentlyAskedQuestion
           WHERE FAQNumber = ?),
         "Something wrong when deleting the FAQ from FrequentlyAskedQuestion.",
         "The FAQ is deleted."
         ) message;
         ''',
        (dataFAQNumber,))
        returnMessage = dbCursor.fetchone()
        return returnMessage

    except sqlite3.Error as errorMessage:
        return errorMessage
    finally:
        dbConnection.close()




def getAllFAQs (dataClientEmail, dataClientPassword):

    dataClientEmail = dataClientEmail.strip()
    errorMessage = validate_loginCredentials(dataClientEmail, dataClientPassword)
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
        (dataClientEmail,))
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
            dbCursor.execute('''
            SELECT userIsLoggedIn FROM User
             WHERE userEmail = ?;
            ''',
            (dataClientEmail,))
            userLoggedIn = dbCursor.fetchone()
            if userLoggedIn[0] == 0:
                return "You have logged out. Please log in again."
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
            dbCursor.execute('''
            SELECT administratorIsLoggedIn FROM Administrator
             WHERE administratorEmail = ?;
            ''',
            (dataClientEmail,))
            administratorLoggedIn = dbCursor.fetchone()
            if administratorLoggedIn[0] == 0:
                return "You have logged out. Please log in again."
        dbCursor.execute('''
        SELECT
         FAQNumber,
         FAQIsForComputer,
         FAQIsForSmartphone,
         FAQCategory,
         FAQTitle,
         substr(FAQContent, 1, 100)
          FROM FrequentlyAskedQuestion;
        ''',
        (dataFAQNumber,))
        listOfFAQs = []
        for FAQ in dbCursor:
            listOfFAQs.append(FAQ)
        return listOfFAQs

    except sqlite3.Error as errorMessage:
        return errorMessage
    finally:
        dbConnection.close()





def searchFAQByWord (dataClientEmail, dataClientPassword, dataSearchWord):

    dataClientEmail = dataClientEmail.strip()
    errorMessage = validate_loginCredentials(dataClientEmail, dataClientPassword)
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
        (dataClientEmail,))
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
            dbCursor.execute('''
            SELECT userIsLoggedIn FROM User
             WHERE userEmail = ?;
            ''',
            (dataClientEmail,))
            userLoggedIn = dbCursor.fetchone()
            if userLoggedIn[0] == 0:
                return "You have logged out. Please log in again."
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
            dbCursor.execute('''
            SELECT administratorIsLoggedIn FROM Administrator
             WHERE administratorEmail = ?;
            ''',
            (dataClientEmail,))
            administratorLoggedIn = dbCursor.fetchone()
            if administratorLoggedIn[0] == 0:
                return "You have logged out. Please log in again."
    except sqlite3.Error as errorMessage:
        return errorMessage
    finally:
        dbConnection.close()
        
    FAQNumberList = []
    groupList = []
    if (dataSearchWord.lower()).find("computer") != 0:
        groupList.append("computer")
    elif (dataSearchWord.lower()).find("smartphone") != 0:
        groupList.append("smartphone")
    elif (dataSearchWord.lower()).find("hardware") != 0:
        groupList.append("hardware")
    elif (dataSearchWord.lower()).find("security") != 0:
        groupList.append("security")
    elif (dataSearchWord.lower()).find("architecture") != 0:
        groupList.append("architecture")
    elif (dataSearchWord.lower()).find("connections") != 0:
        groupList.append("connections")

    wordList = (dataSearchWord.lower()).split(" ")
    for punctuation in [",", ".", "?", "(", ")", "/", ":", ";"]:
        punctuationWordList = []
        removeWordList = []
        for word in wordList:
            word = word.strip()
            if word.find(","):
                newWordList = word.split(",")
                for newWord in newWordList:
                    newWord = newWord.strip()
                    punctuationWordList.append(newWord)
                removeWordList.append(word)
        for punctuationWord in punctuationWordList:
            wordList.append(punctuationWord)
        for removeWord in removeWordList:
            wordList.remove(removeWord)       

    try:
        dbConnection = sqlite3.connect("HelpdeskApplication.sqlite")
        dbCursor = dbConnection.cursor()
        for group in groupList:
            if group == "computer":
                dbCursor.execute('''
                SELECT FAQNumber FROM FrequentlyAskedQuestion
                 WHERE FAQIsForCcomputer = 1;
                ''')
                for FAQNumber in dbCursor:
                    FAQNumberList.append(FAQNumber)
            elif group == "smartphone":
                dbCursor.execute('''
                SELECT FAQNumber FROM FrequentlyAskedQuestion
                 WHERE FAQIsForSmartphone = 1;
                ''')
                for FAQNumber in dbCursor:
                    FAQNumberList.append(FAQNumber)
            else:
                dbCursor.execute('''
                SELECT FAQNumber FROM FrequentlyAskedQuestion
                 WHERE FAQCategory = ?;
                ''',
                (group,))
                for FAQNumber in FAQNumberList:
                    FAQNumberList.append(FAQNumber)

        dbCursor.execute('''
        SELECT LOWER(FAQTitle), FAQNumber FROM FrequentlyAskedQuestion;
        ''')
        for titleAndNumber in dbCursor:
            for word in wordList:
                if titleAndNumber[0].find(word) != 0:
                    FAQNumberList.append(titleAndNumber[1])

        dbCursor.execute('''
        SELECT LOWER(FAQKeyword), FAQNumber FROM FrequentlyAskedQuestion;
        ''')
        for keywordAndNumber in dbCursor:
            for word in wordList:
                if keywordAndNumber[0].find(word) != 0:
                    FAQNumberList.append(keywordAndNumber[1])

        dbCursor.execute('''
        SELECT LOWER(FAQSubcategory), FAQNumber FROM FrequentlyAskedQuestion;
        ''')
        for subcategoryAndNumber in dbCursor:
            for word in wordList:
                if subcategoryAndNumber[0].find(word) != 0:
                    FAQNumberList.append(subcategoryAndNumber[1])

        dbCursor.execute('''
        SELECT LOWER(FAQLinkPartName), FAQNumber FROM FrequentlyAskedQuestion;
        ''')
        for linkPartNameAndNumber in dbCursor:
            for word in wordList:
                if linkPartNameAndNumber[0].find(word) != 0:
                    FAQNumberList.append(linkPartNameAndNumber[1])

    except sqlite3.Error as errorMessage:
        return errorMassage
    finally:
        dbConnection.close()

    FAQNumberAndSortingNumber = {}
    for FAQNumber in FAQNumberList:
        if FAQNumber in FAQNumberAndSortingNumber:
            FAQNumberAndSortingNumber[FAQNumber] += 1
        else:
            FAQNumberAndSortingNumber[FAQNumber] = 1

    FAQNumberListDistinct = []
    for FAQNumber in FAQNumberList:
        if FAQNumber not in FAQNumberListDistinct:
            FAQNumberListDistinct.append(FAQNumber)

    try:
        dbConnection = sqlite3.connect("HelpdeskApplication.sqlite")
        dbCursor = dbConnection.cursor()

        for dataFAQNumber in FAQNumberListDistinct:
            dbCursor.execute('''
            SELECT COUNT(DISTINCT userID) FROM UserViewingOfFAQ
             WHERE
              FAQIsHelpful = 1 AND
              FAQNumber = ?;
            ''',
            (dataFAQNumber,))
            numberOfIsHelpful = dbCursor.fetchone()
            FAQNumberAndSortingNumber[FAQNumber] += numberOfIsHelpful[0]

        for dataFAQNumber in FAQNumberListDistinct:
            dbCursor.execute('''
            SELECT COUNT(FAQDateTimeViewed) FROM UserViewingOfFAQ
             WHERE FAQNumber = ?;
            ''',
            (dataFAQNumber,))
            numberOfViews = dbCursor.fetchone()
            FAQNumberAndSortingNumber[FAQNumber] += numberOfViews[0]

    except sqlite3.Error as errorMessage:
        return errorMessage
    finally:
        dbConnection.close()

    FAQNumberListDistinct.sort(reverse = True, key = lambda FAQNumber: FAQNumberAndSortingNumber[FAQNumber])
        
    try:
        dbConnection = sqlite3.connect("HelpdeskApplication.sqlite")
        dbCursor = dbConnection.cursor()
    
        FAQList = []
        for dataFAQNumber in FAQNumberListDistinct:
            dbCursor.execute('''
            SELECT
             FAQNumber,
             FAQIsForComputer, 
             FAQIsForSmartphone,
             FAQCategory,
             FAQTitle,
             substr(FAQSubcategory, 1, 100)
              FROM FrequentlyAskedQuestion
               WHERE FAQNumber = ?;
            ''',
            (dataFAQNumber,))
            FAQ = dbCursor.fetchone()
            FAQList.append(FAQ)
        return FAQList

    except sqlir3.Error as errorMessage:
        return errorMessage
    finally:
        dbConnection.close()
              
        
        
def viewFAQ (dataClientEmail, dataClientPassword, dataFAQNumber):

    dataClientEmail = dataClientEmail.strip()
    errorMessage = validate_loginCredentials(dataClientEmail, dataClientPassword)
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
        (dataClientEmail,))
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
            dbCursor.execute('''
            SELECT userIsLoggedIn FROM User
             WHERE userEmail = ?;
            ''',
            (dataClientEmail,))
            userLoggedIn = dbCursor.fetchone()
            if userLoggedIn[0] == 0:
                return "You have logged out. Please log in again."
            dbCursor.execute('''
            SELECT IIF(
             SELECT EXISTS(
              SELECT FAQNumber FROM UserViewingOfFAQ
               WHERE
                userID =
                 (SELECT userID FROM User
                  WHERE userEmail = ?) AND
                FAQNumber = ?) AND
             (SELECT DATETIME("now") -
              (SELECT MAX(FAQDateTimeViewed) FROM UserViewingOfFAQ
               WHERE
                userID =
                 (SELECT userID FROM User
                  WHERE userEmail - ?) AND
                FAQNumber = ?)) <= 1,
             1,
             0
            ) isRecordedWithinOneDayAgo;
            ''',
            (dataClientEmail, dataFAQNumber,
             dataClientEmail, dataFAQNumber,))
            viewingIsRecordedWithinOneDayAgo = dbCursor.fetchone()
            if viewingIsRecordedWithinOneDayAgo[0] == 0:
                dbCursor.execute('''
                INSERT INTO UserViewingOfFAQ(
                 userID, FAQDateTimeViewed, FAQNumber)
                VALUES(
                 SELECT userID FROM User
                  WHERE userEmail = ?,
                 SELECT DATETIME("now"),
                 ?);
                ''',
                (dataClientEmail, dataFAQNumber,))
                dbConnection.commit()
                dbCursor.execute('''
                SELECT IIF(
                 SELECT EXISTS(
                  SELECT FAQNumber FROM UserViewingOfFAQ
                   WHERE
                    userID =
                     (SELECT userID FROM User
                      WHERE userEmail = ?) AND
                    FAQNumber = ?) AND
                 ((SELECT DATETIME("now") -
                  (SELECT MAX(FAQDateTimeViewed) FROM UserViewingOfFAQ
                   WHERE
                    userID =
                     (SELECT userID FROM User
                      WHERE userEmail - ?) AND
                    FAQNumber = ?))*(24*60)) <= 1,
                 1,
                 0
                ) isRecordedWithinOneMinuteAgo;
                ''',
                (dataClientEmail, dataFAQNumber,
                 dataClientEmail, dataFAQNumber,))
                viewingIsRecordedWithinOneMinuteAgo = dbCursor.fetchone()
                if viewingIsRecordedWithinOneMinuteAgo[0] == 0:
                    return "Something wrong when recording in UserViewingOfFAQ."
            dbCursor.execute('''
            SELECT
             f.FAQNumber,
             f.FAQIsForComputer,
             f.FAQIsForSmartphone,
             f.FAQCategory,
             f.FAQTitle,
             f.FAQKeyword,
             f.FAQSubCategory,
             f.FAQContent,
             f.FAQLinkPartName,
             f.FAQLinkURL,
             u.FAQIsHelpful,
             MAX(u.FAQDateTimeViewed)
              FROM FequentlyAskedQuestion f, UserViewingOfFAQ u
               WHERE
                u.userID =
                 (SELECT userID FROM UserViewingOfFAQ
                  WHERE userEmail = ?) AND
                f.FAQNumber = ? AND
                f.FAQNumber = u.FAQNumber;
            ''',
            (dataUserEmail, dataFAQNumber,))
            FAQDetails = dbCursor.fetchone()
            return FAQDetails[0]
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
            dbCursor.execute('''
            SELECT administratorIsLoggedIn FROM Administrator
             WHERE administratorEmail = ?;
            ''',
            (dataClientEmail,))
            administratorLoggedIn = dbCursor.fetchone()
            if administratorLoggedIn[0] == 0:
                return "You have logged out. Please log in again."
            dbCursor.execute('''
            SELECT
             FAQNumber,
             FAQIsForComputer,
             FAQIsForSmartphone,
             FAQCategory,
             FAQTitle,
             FAQKeyword,
             FAQSubCategory,
             FAQContent,
             FAQLinkPartName,
             FAQLinkURL
              FROM FequentlyAskedQuestion
               WHERE FAQNumber = ?;
            ''',
            (dataFAQNumber,))
            FAQDetails = dbCursor.fetchone()
            return FAQDetails[0]

    except sqlite3.Error as errorMessage:
        return errorMessage
    finally:
        dbConnection.close()




def rateFAQ (dataUserEmail, dataUserPassword, dataFAQIsHelpful):

    if dataFAQIsHelpful not in [0, 1]:
        return "FAQIsHelpful should either be 0 or 1."

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
        dbCursor.execute('''
        SELECT userIsLoggedIn FROM User
         WHERE userEmail = ?;
        ''',
        (dataUserEmail,))
        userLoggedIn = dbCursor.fetchone()
        if userLoggedIn[0] == 0:
            return "You have logged out. Please log in again."
        dbCursor.execute('''
        SELECT IIF(
         SELECT EXISTS(
          SELECT FAQNumber FROM UserViewingOfFAQ
           WHERE
            userID =
             (SELECT userID FROM User
              WHERE userEmail = ?) AND
               FAQNumber = ?) AND
         (SELECT DATETIME("now") -
          (SELECT MAX(FAQDateTimeViewed) FROM UserViewingOfFAQ
           WHERE
            userID =
             (SELECT userID FROM User
              WHERE userEmail - ? AND
               FAQNumber = ?)) <= 1,
         1,
         0
        ) isRecordedWithinOneDayAgo;
        ''',
        (dataClientEmail, dataFAQNumber,
         dataClientEmail, dataFAQNumber,))
        viewingIsRecordedWithinOneDayAgo = dbCursor.fetchone()
        if viewingIsRecordedWithinOneDayAgo[0] == 0:
            dbCursor.execute('''
            INSERT INTO UserViewingOfFAQ(
             userID, FAQDateTimeViewed, FAQNumber)
            VALUES(
             SELECT userID FROM User
              WHERE userEmail = ?,
             SELECT DATETIME("now"),
             ?);
            ''',
            (dataClientEmail, dataFAQNumber,))
            dbConnection.commit()
            dbCursor.execute('''
            SELECT IIF(
             SELECT EXISTS(
              SELECT FAQNumber FROM UserViewingOfFAQ
               WHERE
                userID =
                 (SELECT userID FROM User
                  WHERE userEmail = ?) AND
                 FAQNumber = ?) AND
             ((SELECT DATETIME("now") -
              (SELECT MAX(FAQDateTimeViewed) FROM UserViewingOfFAQ
               WHERE
                userID =
                 (SELECT userID FROM User
                  WHERE userEmail - ?) AND
                 FAQNumber = ?))*(24*60)) <= 1,
             1,
             0
            ) isRecordedWithinOneMinuteAgo;
            ''',
            (dataClientEmail, dataFAQNumber,
             dataClientEmail, dataFAQNumber,))
            viewingIsRecordedWithinOneMinuteAgo = dbCursor.fetchone()
            if viewingIsRecordedWithinOneMinuteAgo[0] == 0:
                return "Something wrong when recording in UserViewingOfFAQ."
        dbCursor.execute('''
        UPDATE UserViewingOfFAQ
         SET FAQIsHelpful = ?
          WHERE
           userID =
            (SELECT userID FROM User
             WHERE userEmail = ?) AND
           FAQNumber = ? AND
           FAQDateTimeViewed =
            (SELECT MAX(FAQDatetimeViewed) FROM UserViewingOfFAQ
             WHERE
              userID =
               (SELECT userID FROM User
                WHERE userEmail = ?) AND
              FAQNumber = ?);
        ''',
        (dataFAQIsHelpful, dataUserEmail, dataFAQNumber,
         dataUserEmail, dataFAQNumber,))
        dbConnection.commit()
        dbCursor.execute('''
        SELECT IIF(
         SELECT FAQIsHelpful FROM UserViewingOfFAQ
          WHERE
           userID =
            (SELECT userID FROM User
             WHERE userEmail = ?) AND
           FAQNumber = ? AND
           FAQDateTimeViewed =
            (SELECT MAX(FAQDatetimeViewed) FROM UserViewingOfFAQ
             WHERE
              userID =
               (SELECT userID FROM User
                WHERE userEmail = ?) AND
              FAQNumber = ?) = ?,
         "The rating is updated."
         "Something wrong when updating the rating in UserViewingOfFAQ."
        ) message;
        ''',
        (dataUserEmail, dataFAQNumber,
         dataUserEmail, dataFAQNumber,
         dataFAQIsHelpful,))
        returnMessage = dbCursor.fetchone()
        return returnMessage[0]

    except sqlite3.Error as errorMessage:
        return errorMessage
    finally:
        dbConnection.close()
