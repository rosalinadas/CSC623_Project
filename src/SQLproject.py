#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import sqlite3
import pandas as pd


# In[ ]:


# Connects to an existing database file in the current directory
# If the file does not exist, it creates it in the current directory

db_connect = sqlite3.connect('petsclinic.db')


# In[ ]:


# Instantiate cursor object for executing queries
cursor = db_connect.cursor()


# In[ ]:


# String variable for passing queries to cursor
query_clinic = """
    CREATE TABLE IF NOT EXISTS Clinic(
    clinicNo INT,
    cName VARCHAR(100) NOT NULL,
    cAddress VARCHAR(100),
    cPhone INT NOT NULL,
    PRIMARY KEY(clinicNo)
    );
    """

query_staff = """
    CREATE TABLE IF NOT EXISTS Staff(
    staffNo INT,
    sName VARCHAR(100) NOT NULL,
    sAddress VARCHAR(100),
    sPhone INT,
    sDOB TEXT NOT NULL,
    sPosition VARCHAR(100) NOT NULL,
    salary INT NOT NULL,
    clinicNo INT,
    FOREIGN KEY (clinicNo) REFERENCES Clinic(clinicNo) ON UPDATE CASCADE ON DELETE SET NULL, 
    PRIMARY KEY(staffNo)
    );
    """
    
query_owner = """
    CREATE TABLE IF NOT EXISTS PetOwner(
    ownerNo INT,
    oName VARCHAR(100) NOT NULL,
    oAddress VARCHAR(100),
    oPhone INT NOT NULL,
    clinicNo INT,
    PRIMARY KEY(ownerNo),
    FOREIGN KEY (clinicNo) REFERENCES Clinic(clinicNo) ON UPDATE CASCADE ON DELETE SET NULL
    );
    """

query_pet = """
    CREATE TABLE IF NOT EXISTS Pet(
    petNo INT,
    pName VARCHAR(100) NOT NULL,
    pDOB TEXT NOT NULL,
    pSpecies VARCHAR(100),
    pBreed VARCHAR(100),
    pColor VARCHAR(100),
    ownerNo INT,
    clinicNo INT,
    PRIMARY KEY(petNo),
    FOREIGN KEY (clinicNo) REFERENCES Clinic(clinicNo) ON UPDATE CASCADE ON DELETE SET NULL,
    FOREIGN KEY (ownerNo) REFERENCES PetOwner(ownerNo)  ON UPDATE CASCADE ON DELETE SET NULL
    );
    """

query_exam = """
    CREATE TABLE IF NOT EXISTS Examination(
    examNo INT,
    complaint VARCHAR(100),
    description VARCHAR(100),
    date TEXT NOT NULL,
    action VARCHAR(100),
    petNo INT,
    staffNo INT,
    PRIMARY KEY(examNo),
    FOREIGN KEY (petNo) REFERENCES Pet(petNo) ON UPDATE CASCADE ON DELETE SET NULL,
    FOREIGN KEY (staffNo) REFERENCES Staff(staffNo) ON UPDATE CASCADE ON DELETE SET NULL
    );
    """


# In[ ]:


# Execute query, the result is stored in cursor
cursor.execute(query_clinic)
cursor.execute(query_staff)
cursor.execute(query_owner)
cursor.execute(query_pet)
cursor.execute(query_exam)


# In[ ]:


# Insert row into table Clinic
query_clinic = """
    INSERT INTO Clinic
    VALUES 
    ("c001", "Pethealth", "123 Baker St", "3051234567"),
    ("c002", "Petsrus", "119 Douglas Ave", "3051237890"),
    ("c003", "Paws", "200 Bark Lane", "3054567899"),
    ("c004", "Howlclinic", "650 Forest Ave", "3054442345"),
    ("c005", "Healthypets", "300 Woodland Drive", "3051234789")
    ;
    """
cursor.execute(query_clinic)


# In[ ]:


# Insert row into table Staff
query_staff = """
    INSERT INTO Staff
    VALUES 
    ("emp001", "John Smith", "233 Vail Rd", "7862344567", "12-Dec-1970", "Manager", "37000", "c001"),
    ("emp002", "Jane Doe", "445 Colorado St", "3053337890", "14-Jun-1978", "Sr. Medical Assistant", "36000", "c002"),
    ("emp003", "Tom Hanks", "601 Utah Ave", "3054422899", "04-Jul-1965", "Sr. Technician", "42000", "c003"),
    ("emp004", "Jane Austen", "9875 Foothill Dr", "3051214445", "03-Feb-1980", "Technician", "36000", "c003"),
    ("emp005", "Enid Blyton", "112 Iowa St", "7861234890", "08-Aug-1985", "Surgeon", "75000", "c004"),
    ("emp006", "David Blake", "100 Pearson St", "3051112222", "18-Aug-1965", "Manager", "78000", "c005")
    ;
    """
cursor.execute(query_staff)


# In[ ]:


# Insert row into table PetOwner
query_owner = """
    INSERT INTO PetOwner
    VALUES 
    ("own1", "Jack Smith", "410 Park St", "7861245600", "c001"),
    ("own2", "Thomas Jefferson", "325 Minorca Ave", "7865557890", "c002"),
    ("own3", "Teddy Roosevelt", "546 Gables Lane", "3051112222", "c002"),
    ("own4", "John Marshall", "980 Miami Ave", "3053337777", "c003"),
    ("own5", "Hilary Clinton", "311 Lewis Rd", "3054446666", "c005"),
    ("own6", "Elena Monsoon", "555 Privet Rd", "3052340990", "c004")
    ;
    """
cursor.execute(query_owner)


# In[ ]:


# Insert row into table Pet
query_pet = """
    INSERT INTO Pet
    VALUES 
    ("p1", "Tim", "09-Feb-2021", "Dog", "Labrador", "white", "own1", "c001"),
    ("p2", "Bella", "10-Mar-2022", "Cat", "Mix", "black", "own6", "c002"),
    ("p3", "Rufus", "03-Apr-2021", "Dog", "Labrador", "black", "own2", "c002"),
    ("p4", "Tipsy", "09-May-2020", "Dog", "Labrador", "brown", "own4", "c003"),
    ("p5", "Barky", "07-May-2019", "Dog", "Poodle", "white", "own3", "c005"),
    ("p6", "Maggie", "06-Jun-2022", "Parrot", "Tropical", "red", "own5", "c004")
    ;
    """
cursor.execute(query_pet)


# In[ ]:


# Insert row into table Examination
query_exam = """
    INSERT INTO Examination
    VALUES 
    ("ex01", "fleas", "moderate", "05-Nov-2022", "oral medicine", "p1", "emp003"),
    ("ex02", "fleas", "mild", "05-Dec-2022", "oral medicine", "p2", "emp002"),
    ("ex03", "fleas", "mild", "07-Nov-2022", "oral medicine", "p3", "emp002"),
    ("ex04", "fracture", "right paw", "08-Nov-2022", "cast", "p4", "emp003"),
    ("ex05", "fracture", "right paw", "09-Nov-2022", "cast", "p5", "emp003"),
    ("ex06", "winginjury", "left wing", "01-Dec-2022", "surgery", "p6", "emp004")
    ;
    """
cursor.execute(query_exam)


# In[ ]:


#Steps to select data from tables and read into a Pandas dataframe
# Select data
query = """
    SELECT *
    FROM Clinic
    """
cursor.execute(query)

# Extract column names from cursor
column_names = [row[0] for row in cursor.description]

# Fetch data and load into a pandas dataframe
clinic_data = cursor.fetchall()
df1 = pd.DataFrame(clinic_data, columns=column_names)

# Examine dataframe
print(df1)
print(df1.columns)


# In[ ]:


# Select data
query = """
    SELECT *
    FROM Staff
    """
cursor.execute(query)

# Extract column names from cursor
column_names = [row[0] for row in cursor.description]

# Fetch data and load into a pandas dataframe
staff_data = cursor.fetchall()
df2 = pd.DataFrame(staff_data, columns=column_names)

# Examine dataframe
print(df2)
print(df2.columns)


# In[ ]:


# Select data
query = """
    SELECT *
    FROM PetOwner
    """
cursor.execute(query)

# Extract column names from cursor
column_names = [row[0] for row in cursor.description]

# Fetch data and load into a pandas dataframe
owner_data = cursor.fetchall()
df3 = pd.DataFrame(owner_data, columns=column_names)

# Examine dataframe
print(df3)
print(df3.columns)


# In[ ]:


# Select data
query = """
    SELECT *
    FROM Pet
    """
cursor.execute(query)

# Extract column names from cursor
column_names = [row[0] for row in cursor.description]

# Fetch data and load into a pandas dataframe
pet_data = cursor.fetchall()
df4 = pd.DataFrame(pet_data, columns=column_names)

# Examine dataframe
print(df4)
print(df4.columns)


# In[ ]:


# Select data
query = """
    SELECT *
    FROM Examination
    """
cursor.execute(query)

# Extract column names from cursor
column_names = [row[0] for row in cursor.description]

# Fetch data and load into a pandas dataframe
exam_data = cursor.fetchall()
df5 = pd.DataFrame(exam_data, columns=column_names)

# Examine dataframe
print(df5)
print(df5.columns)


# In[ ]:


# Commit any changes to the database
db_connect.commit()


# In[ ]:


#Execute five SQL queries from  data in petsclinic database

#Example Query 1: List all staff who work at clinic c003
query1 = """
    SELECT *
    FROM Staff
    WHERE clinicNo = "c003"
    """
cursor.execute(query1)
column_names = [row[0] for row in cursor.description]
result = cursor.fetchall()
df1 = pd.DataFrame(result, columns=column_names)
print(df1)


# In[ ]:


#Example Query 2: List details of the examination performed by a staff member
query2 = """
    SELECT *
    FROM Examination
    WHERE staffNo = "emp002"
    """
cursor.execute(query2)
column_names = [row[0] for row in cursor.description]
result = cursor.fetchall()
df2 = pd.DataFrame(result, columns=column_names)
print(df2)


# In[ ]:


#Example Query 3: List the pet species and breeds by clinic
query3 = """
    SELECT pSpecies, pBreed
    FROM Pet
    WHERE clinicNo = "c002"
    """
cursor.execute(query3)
column_names = [row[0] for row in cursor.description]
result = cursor.fetchall()
df3 = pd.DataFrame(result, columns=column_names)
print(df3)


# In[ ]:


#Example Query 4: List exam details performed on pet p1
query4 = """
    SELECT *
    FROM Examination
    WHERE petNo = "p1"
    """
cursor.execute(query4)
column_names = [row[0] for row in cursor.description]
result = cursor.fetchall()
df4 = pd.DataFrame(result, columns=column_names)
print(df4)


# In[ ]:


#Example Query 5: List details of all the clinic managers 
query5 = """
    SELECT *
    FROM Staff
    WHERE sPosition = "Manager"
    """
cursor.execute(query5)
column_names = [row[0] for row in cursor.description]
result = cursor.fetchall()
df5 = pd.DataFrame(result, columns=column_names)
print(df5)


# In[ ]:


db_connect.close()

