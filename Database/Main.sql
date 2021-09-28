CREATE DATABASE HelpdeskApplication;
USE HelpdeskApplication;

CREATE TABLE Person (
personID int NOT NULL,
personEmail varchar(100) NOT NULL,
personPassword varchar(20) NOT NULL,
personRole varchar(15) NOT NULL DEFAULT "User");

CREATE TABLE Form (
personID int NOT NULL,
formEmail varchar(100) NULL,
formDevice varchar(10) NOT NULL,
formCategory varchar(15) NOT NULL,
formTitle varchar(100) NOT NULL,
formDescription varchar(3000) NOT NULL,
formIsSolved bit(1) NOT NULL DEFAULT 0,
formImage1_Description varchar(100) NULL,
formImage1_Data mediumblob NULL,
formImage2_Description varchar(100) NULL,
formImage2_Data mediumblob NULL,
formImage3_Description varchar(100) NULL,
formImage3_Data mediumblob NULL,
formImage4_Description varchar(100) NULL,
formImage4_Data mediumblob NULL,
formImage5_Description varchar(100) NULL,
formImage5_Data mediumblob NULL);

CREATE TABLE ViewingOfFAQ (
personID int NOT NULL,
isHelpful bit(1) NULL,
FAQ_Number int NOT NULL);

CREATE TABLE FrequentlyAskedQuestion (
FAQ_Number int NOT NULL,
FAQ_Device varchar(10) NOT NULL,
FAQ_Category varchar(15) NOT NULL,
FAQ_Title varchar(100) NOT NULL,
FAQ_Keyword varchar(100) NULL,
FAQ_SubCategory varchar(50) NULL,
FAQ_Content varchar(5000) NOT NULL,
FAQLink1_PartName varchar(50) NULL,
FAQLink1_URL varchar(200) NULL,
FAQLink2_PartName varchar(50) NULL,
FAQLink2_URL varchar(200) NULL,
FAQLink3_PartName varchar(50) NULL,
FAQLink3_URL varchar(200) NULL,
FAQLink4_PartName varchar(50) NULL,
FAQLink4_URL varchar(200) NULL,
FAQLink5_PartName varchar(50) NULL,
FAQLink5_URL varchar(200) NULL);


#Define primary keys, unique key, and add auto increment 
ALTER TABLE Person
  ADD CONSTRAINT personID_pk PRIMARY KEY (personID),
  MODIFY COLUMN personID int AUTO_INCREMENT;

ALTER TABLE FrequentlyAskedQuestion
  ADD CONSTRAINT FAQ_Number_pk PRIMARY KEY(FAQ_Number),
  MODIFY COLUMN FAQ_Number int AUTO_INCREMENT;

ALTER TABLE Person
  ADD CONSTRAINT UC_personEmail UNIQUE (personEmail);


#Define foreign keys
ALTER TABLE Form
  ADD CONSTRAINT fk_personID_Form
    FOREIGN KEY (personID)
    REFERENCES Person(personID);

ALTER TABLE ViewingOfFAQ
  ADD CONSTRAINT fk_personID_ViewingOfFAQ
    FOREIGN KEY (personID)
    REFERENCES Person(personID),
  ADD CONSTRAINT fk_FAQ_Number_ViewingOfFAQ
    FOREIGN KEY (FAQ_Number)
    REFERENCES FrequentlyAskedQuestion(FAQ_Number);


#Fix the 2 roles, 2 types of devices and the 4 categories
ALTER TABLE Person
  ADD CONSTRAINT Check_personRole
    CHECK (personRole IN ("User", "Administrator"));

ALTER TABLE Form
  ADD CONSTRAINT Check_Device_Form
    CHECK (formDevice IN ("Smartphone", "Computer")),
  ADD CONSTRAINT Check_Category_Form
    CHECK (formCategory IN ("Hardware", "Security", "Architecture", "Connections"));

ALTER TABLE FrequentlyAskedQuestion
  ADD CONSTRAINT Check_Device_FAQ
    CHECK (FAQ_Device IN ("Smartphone", "Computer")),
  ADD CONSTRAINT Check_Category_FAQ
    CHECK (FAQ_Category IN ("Hardware", "Security", "Architecture", "Connections"));


#Limit the length of password
ALTER TABLE Person
  ADD CONSTRAINT Check_PasswordLength
    CHECK (length(personPassword) BETWEEN 8 AND 20); 
