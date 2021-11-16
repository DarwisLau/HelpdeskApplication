from ValidateData import validate_loginCredentials, validate_FAQData
import sqlite3
import random


def addFAQ (dataAdministratorEmail, dataFAQIsForComputer, dataFAQIsForSmartphone, dataFAQCategory, dataFAQTitle, dataFAQKeyword, dataFAQSubcategory, dataFAQContent, dataFAQLinkPartName, dataFAQLinkURL):


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
        
        dbCursor.execute('''
        SELECT administratorIsLoggedIn FROM Administrator
         WHERE administratorEmail = ?;
        ''',
        (dataAdministratorEmail,))
        administratorLoggedIn = dbCursor.fetchone()
        if administratorLoggedIn[0] == 0:
            return "You have logged out. Please log in again."

        allNumber = []
        dbCursor.execute('''
        SELECT FAQNumber FROM FrequentlyAskedQuestion;
        ''',)
        for number in dbCursor:
            allNumber.append(number)
        dataFAQNumber = random.randint(1, 150)
        while dataFAQNumber in allNumber:
            dataFAQNumber = random.randint(1, 150)

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

        dbCursor.execute('''
        INSERT INTO AdministratorEditingOfFAQ(
         administratorID, FAQDateTimeEdited, FAQNumber)
        VALUES(
         (SELECT administratorID FROM Administrator
          WHERE administratorEmail = ?),
         (SELECT datetime("now")),
         ?);
         ''',
        (dataAdministratorEmail, dataFAQNumber,))

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
        if created[0] == 0:
            return "Something wrong when adding the FAQ to the database."

        dbCursor.execute('''
        SELECT IIF(
         (SELECT administratorID FROM AdministratorEditingOfFAQ
          WHERE FAQNumber = ?) =
         (SELECT administratorID FROM Administrator
          WHERE administratorEmail = ?),
         "FAQ is added.",
         "Something wrong when recording the administrator's creating of FAQ."
         ) message;
         ''',
        (dataFAQNumber, dataAdministratorEmail,))
        returnMessage = dbCursor.fetchone()
        if returnMessage[0] == "FAQ is added.":
            dbConnection.commit()
        return returnMessage[0]
        
    except sqlite3.Error as errorMessage:
        return errorMessage
    finally:
        dbConnection.close()




def editFAQ (dataAdministratorEmail, dataFAQNumber, dataFAQIsForComputer, dataFAQIsForSmartphone, dataFAQCategory, dataFAQTitle, dataFAQKeyword, dataFAQSubcategory, dataFAQContent, dataFAQLinkPartName, dataFAQLinkURL):


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
         (SELECT administratorID FROM Administrator
          WHERE administratorEmail = ?),
         (SELECT datetime("now")),
         ?);
         ''',
        (dataAdministratorEmail, dataFAQNumber,))

        dbCursor.execute('''
        UPDATE FrequentlyAskedQuestion
         SET FAQIsForComputer = ?,
          FAQIsForSmartphone = ?,
          FAQCategory = ?,
          FAQTitle = ?,
          FAQKeyword = ?,
          FAQSubcategory = ?,
          FAQContent = ?,
          FAQLinkPartName = ?,
          FAQLinkURL = ?
        WHERE FAQNumber = ?;
        ''',
        (dataFAQIsForComputer,
         dataFAQIsForSmartphone,
         dataFAQCategory,
         dataFAQTitle,
         dataFAQKeyword,
         dataFAQSubcategory,
         dataFAQContent,
         dataFAQLinkPartName,
         dataFAQLinkURL,
         dataFAQNumber,))

        dbCursor.execute('''
        SELECT a.administratorEmail, MAX(e.FAQDateTimeEdited)
         FROM AdministratorEditingOfFAQ e, Administrator a
          WHERE
           e.FAQNumber = ? AND
           e.administratorID = a.administratorID;
        ''',
        (dataFAQNumber,))
        isRecorded = dbCursor.fetchone()
        if isRecorded[0] != dataAdministratorEmail:
            return "Something wrong when recording the administrator who edited the FAQ."

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
         "FAQ is edited.",
         "Something wrong when saving the FAQ to the database."
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
        if returnMessage[0] == "FAQ is edited.":
            dbConnection.commit()
        return returnMessage[0]

    except sqlite3.Error as errorMessage:
        return errorMessage
    finally:
        dbConnection.close()



def deleteFAQ (dataAdministratorEmail, dataFAQNumber):

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

        dbCursor.execute('''
        DELETE FROM FrequentlyAskedQuestion
         WHERE FAQNumber = ?;
        ''',
        (dataFAQNumber,))

        dbCursor.execute('''
        SELECT EXISTS(
         SELECT FAQNumber FROM AdministratorEditingOfFAQ
          WHERE FAQNumber = ?);
        ''',
        (dataFAQNumber,))
        existFAQ = dbCursor.fetchone()
        if existFAQ == 1:
            return "Something wrong when deleting the record of administrators who edited the FAQ."
        
        dbCursor.execute('''
        SELECT IIF(
         (SELECT EXISTS(
          SELECT FAQNumber FROM FrequentlyAskedQuestion
           WHERE FAQNumber = ?)) = 1,
         "Something wrong when deleting the FAQ from the database.",
         "FAQ is deleted."
         ) message;
         ''',
        (dataFAQNumber,))
        returnMessage = dbCursor.fetchone()
        if returnMessage[0] == "FAQ is deleted.":
            dbConnection.commit()
        return returnMessage[0]

    except sqlite3.Error as errorMessage:
        return errorMessage
    finally:
        dbConnection.close()




def getAllFAQs (dataClientRole, dataClientEmail):


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

            dbCursor.execute('''
            SELECT administratorIsLoggedIn FROM Administrator
             WHERE administratorEmail = ?;
            ''',
            (dataClientEmail,))
            administratorLoggedIn = dbCursor.fetchone()
            if administratorLoggedIn[0] == 0:
                return "You have logged out. Please log in again."

        FAQNumberList = []

        dbCursor.execute('''
        SELECT FAQNumber FROM FrequentlyAskedQuestion;
        ''')
        for number in dbCursor:
            FAQNumberList.append(number[0])

        FAQList = []
    
        for dataFAQNumber in FAQNumberList:
            dbCursor.execute('''
            SELECT
             DISTINCT f.FAQNumber,
             f.FAQIsForComputer,
             f.FAQIsForSmartphone,
             f.FAQCategory,
             f.FAQTitle,
             datetime(MAX(e.FAQDateTimeEdited), "localtime")
             FROM
              FrequentlyAskedQuestion f,
              AdministratorEditingOfFAQ e
               WHERE
                f.FAQNumber = ? AND
                f.FAQNumber = e.FAQNumber;
            ''',
            (dataFAQNumber,))
            FAQ = dbCursor.fetchone()
            FAQList.append(FAQ)

        for num in range(0, len(FAQList), 1):
            faq = list(FAQList[num])
            dbCursor.execute('''
            SELECT
             COUNT(DISTINCT userID)
              FROM UserViewingOfFAQ
               WHERE
                FAQIsHelpful = 1 AND
                 FAQNumber = ?;
            ''',
            (faq[0],))
            helpnum = dbCursor.fetchone()
            if helpnum is not None:
                faq.append(helpnum[0])
            else:
                faq.append(0)
            faq = tuple(faq)
            FAQList[num] = faq

        return FAQList

    except sqlite3.Error as errorMessage:
        return errorMessage
    finally:
        dbConnection.close()





def searchFAQByWord (dataClientRole, dataClientEmail, dataSearchWord):


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
    if (dataSearchWord.lower()).find("computer") != -1:
        groupList.append("computer")
    elif (dataSearchWord.lower()).find("smartphone") != -1:
        groupList.append("smartphone")
    elif (dataSearchWord.lower()).find("hardware") != -1:
        groupList.append("hardware")
    elif (dataSearchWord.lower()).find("security") != -1:
        groupList.append("security")
    elif (dataSearchWord.lower()).find("architecture") != -1:
        groupList.append("architecture")
    elif (dataSearchWord.lower()).find("connections") != -1:
        groupList.append("connections")

    wordList = (dataSearchWord.lower()).split(" ")       

    try:
        dbConnection = sqlite3.connect("HelpdeskApplication.sqlite")
        dbCursor = dbConnection.cursor()
        for group in groupList:
            if group == "computer":
                dbCursor.execute('''
                SELECT FAQNumber FROM FrequentlyAskedQuestion
                 WHERE FAQIsForComputer = 1;
                ''')
                for FAQNumber in dbCursor:
                    if FAQNumber[0] not in FAQNumberList:
                        FAQNumberList.append(FAQNumber[0])
            elif group == "smartphone":
                dbCursor.execute('''
                SELECT FAQNumber FROM FrequentlyAskedQuestion
                 WHERE FAQIsForSmartphone = 1;
                ''')
                for FAQNumber in dbCursor:
                    if FAQNumber[0] not in FAQNumberList:
                        FAQNumberList.append(FAQNumber[0])
            else:
                dbCursor.execute('''
                SELECT FAQNumber FROM FrequentlyAskedQuestion
                 WHERE FAQCategory = ?;
                ''',
                (group,))
                for FAQNumber in dbCursor:
                    if FAQNumber[0] not in FAQNumberList:
                        FAQNumberList.append(FAQNumber[0])

        dbCursor.execute('''
        SELECT LOWER(FAQTitle), FAQNumber FROM FrequentlyAskedQuestion;
        ''')
        for titleAndNumber in dbCursor:
            for word in wordList:
                if titleAndNumber[0].find(word) != -1 and titleAndNumber[1] not in FAQNumberList:
                    FAQNumberList.append(titleAndNumber[1])

        dbCursor.execute('''
        SELECT LOWER(FAQKeyword), FAQNumber FROM FrequentlyAskedQuestion;
        ''')
        for keywordAndNumber in dbCursor:
            for word in wordList:
                if keywordAndNumber[0].find(word) != -1 and keywordAndNumber[1] not in FAQNumberList:
                    FAQNumberList.append(keywordAndNumber[1])

        dbCursor.execute('''
        SELECT LOWER(FAQSubcategory), FAQNumber FROM FrequentlyAskedQuestion;
        ''')
        for subcategoryAndNumber in dbCursor:
            for word in wordList:
                if subcategoryAndNumber[0].find(word) != -1 and subcategoryAndNumber[1] not in FAQNumberList:
                    FAQNumberList.append(subcategoryAndNumber[1])

        dbCursor.execute('''
        SELECT LOWER(FAQLinkPartName), FAQNumber FROM FrequentlyAskedQuestion;
        ''')
        for linkPartNameAndNumber in dbCursor:
            for word in wordList:
                if linkPartNameAndNumber[0].find(word) != -1 and linkPartNameAndNumber[1] not in FAQNumberList:
                    FAQNumberList.append(linkPartNameAndNumber[1])

        FAQList = []
    
        for dataFAQNumber in FAQNumberList:
            dbCursor.execute('''
            SELECT
             DISTINCT f.FAQNumber,
             f.FAQIsForComputer,
             f.FAQIsForSmartphone,
             f.FAQCategory,
             f.FAQTitle,
             datetime(MAX(e.FAQDateTimeEdited), "localtime")
              FROM
               FrequentlyAskedQuestion f,
               AdministratorEditingOfFAQ e
                WHERE
                 f.FAQNumber = ? AND
                 f.FAQNumber = e.FAQNumber;
            ''',
            (dataFAQNumber,))
            FAQ = dbCursor.fetchone()
            FAQList.append(FAQ)

        for num in range(0, len(FAQList), 1):
            faq = list(FAQList[num])
            dbCursor.execute('''
            SELECT
             COUNT(DISTINCT userID)
              FROM UserViewingOfFAQ
               WHERE
                FAQIsHelpful = 1 AND
                 FAQNumber = ?;
            ''',
            (faq[0],))
            helpnum = dbCursor.fetchone()
            if helpnum[0] is not None:
                faq.append(helpnum[0])
            else:
                faq.append(0)
            faq = tuple(faq)
            FAQList[num] = faq

        return FAQList

    except sqlite3.Error as errorMessage:
        return errorMessage
    finally:
        dbConnection.close()
              
        
        
def viewFAQ (dataClientRole, dataClientEmail, dataFAQNumber):


    try:

        dbConnection = sqlite3.connect("HelpdeskApplication.sqlite")
        dbCursor = dbConnection.cursor()

        #Check whether the person is a user or not
        if dataClientRole == "user":
            dbCursor.execute('''
            SELECT EXISTS(
             SELECT userEmail FROM User
              WHERE userEmail = ?);
            ''',
            (dataClientEmail,))
            existUser = dbCursor.fetchone()
            if existUser[0] == 0:
                return "Something wrong about the login credentials (email address). Please log in again."

            dbCursor.execute('''
            SELECT userIsLoggedIn FROM User
             WHERE userEmail = ?;
            ''',
            (dataClientEmail,))
            userLoggedIn = dbCursor.fetchone()
            if userLoggedIn[0] == 0:
                return "You have logged out. Please log in again."

            dbCursor.execute('''
            INSERT INTO UserViewingOfFAQ(
             userID, FAQDateTimeViewed, FAQNumber)
              VALUES(
               (SELECT userID FROM User
                WHERE userEmail = ?),
               (SELECT DATETIME("now")),
               ?);
            ''',
            (dataClientEmail, dataFAQNumber,))
            dbConnection.commit()

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
             datetime(MAX(e.FAQDateTimeEdited), "localtime"),
             a.administratorEmail
              FROM
               FrequentlyAskedQuestion f,
               AdministratorEditingOfFAQ e,
               Administrator a
                WHERE
                 f.FAQNumber = ? AND
                 f.FAQNumber = e.FAQNumber AND
                 e.administratorID = a.administratorID;
            ''',
            (dataFAQNumber,))
            FAQDetails = dbCursor.fetchone()

            dbCursor.execute('''
            SELECT
             FAQIsHelpful,
             MAX(FAQDateTimeViewed)
              FROM UserViewingOfFAQ
               WHERE FAQNumber = ?
               AND userID = (SELECT userID FROM User
                WHERE userEmail = ?);
            ''',
            (dataFAQNumber, dataClientEmail,))
            FAQHelpful = dbCursor.fetchone()
            FAQDetails = list(FAQDetails)
            FAQDetails.append(FAQHelpful[0])
            FAQDetails = tuple(FAQDetails)
            return FAQDetails

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
             datetime(MAX(e.FAQDateTimeEdited), "localtime"),
             a.administratorEmail
              FROM
               FrequentlyAskedQuestion f,
               AdministratorEditingOfFAQ e,
               Administrator a
                WHERE
                 f.FAQNumber = ? AND
                 f.FAQNumber = e.FAQNumber AND
                 e.administratorID = a.administratorID;
            ''',
            (dataFAQNumber,))
            FAQDetails = dbCursor.fetchone()
            return FAQDetails

    except sqlite3.Error as errorMessage:
        return errorMessage
    finally:
        dbConnection.close()




def rateFAQ (dataUserEmail, dataFAQNumber, dataFAQIsHelpful):


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

        dbCursor.execute('''
        SELECT userIsLoggedIn FROM User
         WHERE userEmail = ?;
        ''',
        (dataUserEmail,))
        userLoggedIn = dbCursor.fetchone()
        if userLoggedIn[0] == 0:
            return "You have logged out. Please log in again."

        dbCursor.execute('''
        SELECT EXISTS(
          SELECT FAQNumber FROM UserViewingOfFAQ
           WHERE
            userID =
             (SELECT userID FROM User
              WHERE userEmail = ?) AND
               FAQNumber = ?);
        ''',
        (dataUserEmail, dataFAQNumber,))
        hasRecord = dbCursor.fetchone()
        if hasRecord[0] == 0:
                return "Something wrong about the record of your viewing of FAQ."

        dbCursor.execute('''
        UPDATE UserViewingOfFAQ
         SET FAQIsHelpful = ?
          WHERE
           userID =
            (SELECT userID FROM User
             WHERE userEmail = ?) AND
           FAQNumber = ? AND
           FAQDateTimeViewed =
            (SELECT MAX(FAQDateTimeViewed) FROM UserViewingOfFAQ
              WHERE userID = (SELECT userID FROM User WHERE userEmail = ?));
        ''',
        (dataFAQIsHelpful, dataUserEmail, dataFAQNumber, dataUserEmail,))

        dbCursor.execute('''
        SELECT FAQIsHelpful
         FROM UserViewingOfFAQ
          WHERE
           userID =
            (SELECT userID FROM User
             WHERE userEmail = ?) AND
           FAQNumber = ? AND
           FAQDateTimeViewed =
            (SELECT MAX(FAQDateTimeViewed) FROM UserViewingOfFAQ
              WHERE userID = (SELECT userID FROM User WHERE userEmail = ?));
        ''',
        (dataUserEmail, dataFAQNumber, dataUserEmail,))
        ratingChanged = 1
        for rating in dbCursor:
            if rating[0] != dataFAQIsHelpful:
                ratingChanged = 0
                break
        if ratingChanged == 1:
            dbConnection.commit()
            return "Rating is updated."
        else:
            return "Something wrong when updating the rating in the database."

    except sqlite3.Error as errorMessage:
        return errorMessage
    finally:
        dbConnection.close()
