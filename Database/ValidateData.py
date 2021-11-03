"""This file contains the definition of functions used to validate data before
   storing the data into the database."""

from validate_email import validate_email
        #Validate_email is a package for Python that check if an email is valid, properly formatted and really exists.
        #It is used to check whether the syntax of the email address is correct or not.
        #Source: https://pypi.org/project/validate_email/
import urllib



def validate_loginCredentials (email, password):

    """Function to check whether the login credentials are valid or not and
       return error message if any of the login credentials is not valid.
       The first argument should be string, whereas the second argument
       (password) should be base64 byte.
       Output is string or no output.
       Note: email VARCHAR(150) UNIQUE NOT NULL,
             password VARCHAR(28) NOT NULL *8-20 non-byte characters"""


    #Email address
    #Number of characters
    if len(email) > 150:
        return "The number of character of the email address exceeds the character limit for email address. The maximum number of characters allowed for email address is 150."
    elif len(email) == 0:
        return "Email address must be filled."
    #Check whether the syntax of the email address is correct or not
    elif validate_email(email) == False:
        return "The syntax of the email address is not correct."

    #Passoword
    #Number of characters
    else:
        if len(password) < 8:
            return "The number of character of the password is less than the minimum number of character for password. The minimum number of characters required for password is 8."
        elif len(password) > 20:
            return "The number of character of the password exceeds the character limit for password. The maximum number of characters allowed for password is 20."



def validate_formData (email, description):

    """Function to check whether these fields in a form are valid or not and
       return error message if any of the fields is not valid.
       Input should be both string.
       Output is string or no output.
       Note: formEmail VARCHAR(150),
             formDescription TEXT NOT NULL"""


    #Email address
    #Number of characters
    if len(email) > 150:
        return "The number of characters of the email address exceeds the character limit for email address. The maximum number of characters allowed for email address is 150."
    #Check whether the syntax of the email address is correct or not
    elif len(email) > 0 and validate_email(email) == False:
        return "The syntax of the email address is not correct."

    #Description
    #Number of characters
    elif len(description) == 0:
        return "Description should not be left blank."



def validate_FAQData (isForComputer, isForSmartphone, category, title, keyword, subCategory, content, linkPartName, linkURL):

    """Function to check whether these fields in a frequently asked question
       (FAQ) are valid or not and return error message if any of the fields is
       not valid.
       Input should be all string.
       Output is string or no output.
       Note: FAQIsForcomputer BOOLEAN NOT NULL,
             FAQIsForSmartphone BOOLEAN NOT NULL,
             FAQCategory VARCHAR(15) NOT NULL
             CHECK(FAQCategory IN ('hardware', 'security', 'architecture', 'connections')),
             FAQTitle VARCHAR(300) NOT NULL,
             FAQKeyword VARCHAR(300)
             CHECK(FAQSubCategory NOT IN ('computer', 'smartphone', 'hardware', 'security', 'architecture', 'connections')),
             FAQSubCategory VARCHAR(100)
             CHECK(FAQCategory NOT IN ('computer', 'smartphone', 'hardware', 'security' 'architecture', 'connections')),
             FAQContent TEXT NOT NULL,
             FAQLinkPartName VAECHAR(200) CHECK(FAQLinkURL != NULL),
             FAQLinkURL TEXT CHECK(FAQLinkPartName != NULL)
             """


    #isForComputer and isForSmartphone
    if isForComputer not in [0, 1]:
        return "Error for FAQIsForComputer (should either be 0 or 1).
    elif isForSmartphone not in [0, 1]:
        return "Error for FAQIsForSmartphone (should either be 0 or 1).
    elif isForComputer == 0 and isForSmartphone == 0:
        return "The FAQ should be written for either computer or smartphone, or both."

    #Category
    #Number of characters
    elif len(category) > 15:
        return "The length of category exceeds the character limit. The maximum number of characters allowed for category is 15."
    elif len(category) == 0:
        return "Category cannot be left blank."
    #Only four choices are allowed for category
    elif category not in ["hardware", "security", "architecture", "connections"]:
        return "Category should be one of the following: hardware, security, architecture, or connections."

    #Title
    #Number of characters
    if len(title) > 300:
        return "The length of title exceeds the character limit. The maximum number of characters allowed for title is 300."
    elif len(title) == 0:
        return "Title should not be left blank."

    #Keyword
    #Number of characters
    elif len(keyword) > 300:
        return "The total length of keyword(s) exceeds the character limit. The maximum number of characters allowed for keyword (including any comma) is 300."

    #Sub-category
    #Number of characters
    elif len(subCategory) > 100:
        return "The length of sub-category exceeds the character limit. The maximum number of characters allowed for sub-category is 100."
    #Make sure sub-category is different from category
    elif subcategory.lower() in ["computer", "smartphone", "hardware", "security", "architecture", "connections"]:
        return "Subcategory should be different from any category, so subcategory should not any of the following: hardware, security, architecture, connections. Subcategory should also not be 'computer' and 'smartphone'."

    #Content
    #Number of characters
    elif len(content) == 0:
        return "Content should not be left blank."
    
    #Link
    #The link have a URL if and only if the link have a part name
    elif len(linkPartName) > 0 and len(linkURL) == 0:
        return "The link does not have a URL."
    elif len(linkURL) == 0 and len(linkPartName) > 0:
        return "The link does not have a part name."
    elif len(linkPartName) > 0 and len(linkURL) > 0:
        #Number of characters
        if len(linkPartName) > 200:
            return "The part name of the link is too long. The maximum number of characters allowed for part name is 200."
        #Syntax of URL
        url1 = urllib.parse.urlparse(URLLink1) #break the URL (scheme://netloc/path;parameters?query#fragment) into 6 parts, if the URL has scheme and netloc, its syntax is correct
        if url1.scheme == '' or url.netloc == '':
            return "The syntax of the URL of the link is not correct."
    
