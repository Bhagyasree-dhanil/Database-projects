'''

Scope of the project:

Implementing a banking management system using Mysql.


Features:

MAIN MENU

1.  Insert Record/Records
2.  Display records as per account number
             a. Sorted as per account number
             b. Sorted as per customer Name
             c. Sorted as per Customer Balance
3. Search record details as per the account number
4. Update record
5. Delete Record
6. TransactionDebit/Withdraw from the account
           a.	Debit/Withdraw from account
           b.	Credit into account
7. Exit


Step by step procedures:

•	1 .Download MySQL

Download Xampp control panel and use phpmy admin as UI
( port 3308 default 3306. But here 3306 already taken by mysql.so changed port to 3306)

•	Setting up password for root in phpMyAdmin

Click admin, it will open phpMyAdmin. In user_accounts -edit privileages in 3 root ..>
give password ..> generate ..>Go

In local storage:
Xampp ..> phpMyAdmin..> config.inc.php
Add password b/w ‘ ’
Xampp ..> mysql ..>bin ..>my.ini
After[mysql d]
Add one more line skip-grant-tables

 
2.Setting up MySQLdb

It is an interface for connecting to a MySQL database server from python.
For that we have to install two packages
1.	mysql-connector-python  (pip install mysql-connector-python)
2.	mysql-python (pip install mysql-python)
now import MySQLdb

3. Create database -bankdb

4. Create Table

user 
1.	Account_no
2.	Name
3.	Mobile number
4.	Address
5.	country
6.	Email
7.	Account Balance


transactions

1.  trans_no
2.  trans_type (debit/credit)
3.  trans time Credit/debit datetime
4.  Account current balance
5.  Transaction amount
6.  user_id( foreign key of account no)

5. write function for displaying menu

6. if 1 then - create a new account.insert the data given into users db

7. if 2 then display the sub menu and then use SELECT and ORDER query to show 
the user  in sorted way.

8.search records as per account no- use SELECT and WHERE clause .Use pandas dataframe to view as table.

9. Update account of the user - ask for account no --then choose what to updatw --Then use UPDATE clause

10 . Delete account -ask for acc_no and use DELETE clause

11.credit/credit - ask for credit or debit,amount - insert data into transactions db - update balance in users db

12. display transactions -- SELECT   from transaction table as per account no

13.exit - create while loop --if select exit --exit the while loop --else continue displaying menu bar.

'''






# import MySQLdb -interface for connecting with sql database

import MySQLdb
import pandas as pd


# connect to database

conn=MySQLdb.connect(
                     host="127.0.0.1",
                     user="root",
                     password="bhagya",
                     database="bankdb",
                     port=3308)

cursor=conn.cursor()


# Create Database

def create_db():

  cursor.excecute("CREATE DATABASE bankdb")


# create table

def create_table():
    
    cursor.execute("CREATE TABLE users (\
                            account_no INT NOT NULL AUTO_INCREMENT,\
                            Name VARCHAR(40) NOT NULL,\
                            Mobile_no VARCHAR(40) NOT NULL,\
                            Address VARCHAR(100) NOT NULL,\
                            Country VARCHAR(100) NOT NULL,\
                            Email VARCHAR(100) NOT NULL,\
                            Balance INT DEFAULT 0,\
                            PRIMARY KEY(account_no))")

    cursor.execute("CREATE TABLE transactions (\
        trans_no INT NOT NULL AUTO_INCREMENT,\
        user_id INT,\
        trans_type VARCHAR(40) NOT NULL,\
        Trans_date TIMESTAMP DEFAULT current_timestamp,\
        Trans_amount INT NOT NULL\
        Current_balance  INT NOT NULL,\
        PRIMARY KEY(trans_no),\
        FOREIGN KEY(user_id)\
          REFERENCES users(account_no))")

#create_table()


def add_demodata():

 cursor.execute("INSERT INTO users(Name,Mobile_no,Address,Country,Email)\
                VALUES('bhagya','5566778009','address city','india','bhagya@gmail.com'),\
                      ('bhavya','1166888009','add city','india','bhavya@gmail.com')")
 conn.commit()

#add_demodata()

# Function to define - menu bar


def menu():
  print('*'*100)
  print('Welcome to Bank servives')
  print('1.Add account')
  print('2.Display users')
  print('3.Search records as per account no')
  print('4.Update records of user')
  print('5.Delete records of user')
  print('6.credit to /debit from account')
  print('7.show transactions')
  print('8.exit')
  print('*'*100)

  try:
      user_input=input("enter the no of services : ")
      return(user_input)
  except:
      print("invalid input")


def sub_menu():
    print('a. sorted as per account no')
    print('b. sorted as per customer Name')
    print('c. sorted as per customer balnce')
    print('d. back to menu')
    print('*'*100)
    try:
        sub_input=input("enter any options listed : ")
        if sub_input=='d':
            menu
        return (sub_input)
    except:
        print("invalid input")



def add_account():
    try :
        
        print('*'*100)
        print("enter your details to create account!")
        name=input("enter your name : ")
        mobile=input("enter your mobile no : ")
        address=input("enter your adress : ")
        country=input("enter your contry : ")
        email=input("enter your email : ")
        records=[]
        records.append(name)
        records.append(mobile)
        records.append(address)
        records.append(country)
        records.append(email)


        print(records)
        cursor.execute("INSERT INTO users(Name,Mobile_no,Address,Country,Email)\
                    VALUES(%s,%s,%s,%s,%s)",records)
        conn.commit()
        print('Account created successfully!')
        print('*'*100)
    except:
        print("invalid input")


def display_records(sort_by):

     try:
        data=cursor.execute("SELECT * FROM users ORDER BY {}".format(sort_by))
        data=cursor.fetchall()

        if len(data)!=0:
            print('='*100)
            df=pd.DataFrame(list(data),columns=['Account_no','Name','Mobile_no','Address','Country','Email','Balance'])
            print(df.to_string()) # 'to_string' used to display all columns ,otherwise df will reduce the columns
            print('='*100)
        else:
            print("no records found!")
            
     except:
         print("invalid input")
         
    
def search_records(search_by):

     try:   
        data=cursor.execute("SELECT * FROM users WHERE account_no={} ".format(search_by))
        data=cursor.fetchall()

        if len(data)!=0:
            print('='*100)
            df=pd.DataFrame(list(data),columns=['Account_no','Name','Mobile_no','Address','Country','Email','Balance'])
            print(df.to_string()) # 'to_string' used to display all columns ,otherwise df will reduce the columns
            print('='*100)
        else:
            print("no records found!")
     except:
         print("invalid input")
         
         
def update_records(acc_no,update_by,set_inp):

  try:
        
    data=cursor.execute("UPDATE users SET {}='{}' WHERE account_no={}".format(update_by,set_inp,acc_no)) # give '' for values
    data=cursor.execute("SELECT * FROM users WHERE account_no={} ".format(acc_no))
    data=cursor.fetchall()
    if len(data)!=0 :
        print('='*100)
        df=pd.DataFrame(list(data),columns=['Account_no','Name','Mobile_no','Address','Country','Email','Balance'])
        print(df.to_string()) # 'to_string' used to display all columns ,otherwise df will reduce the columns
        print('='*100)
    else:
        print("no records found!")
    
  except:
         print("invalid input")

         

def delete_record(acc_no):
  try:
    data=cursor.execute("DELETE FROM users WHERE account_no= '%s'"%(acc_no))
    conn.commit()
    
    if data!=0:
       print(data,"data deleted succesfully!")
    else:
        print("no records found!")
    
  except:
         print("invalid input")

         

def trans_record(acc_no,trans_type,trans_amt):
    
  try:
    data=cursor.execute("SELECT Balance FROM users WHERE account_no={} ".format(acc_no))
    data=cursor.fetchall()

    if(len(data)!=0):
        balance=data[0][0]
        if trans_type=="debit":
            curr_balance=balance-trans_amt
        if trans_type=="credit":
            curr_balance=balance+trans_amt

        if curr_balance>0:
        
            cursor.execute("INSERT INTO transactions(user_id,trans_type,Trans_amount,Current_balance)\
                                VALUES({},'{}',{},{})".format(acc_no,trans_type,trans_amt,curr_balance))
            conn.commit()
            

            cursor.execute("UPDATE users SET Balance={}  WHERE account_no={}".format(curr_balance,acc_no))
            conn.commit()

            print(" Transaction done successfully!.current balance is {}".format(curr_balance))

        else:
            print("insufficent balance")
    else:
        print("No records found")
        
  except:
         print("invalid input")

    
def display_trans(search_by):

     try:   
        data=cursor.execute("SELECT * FROM transactions WHERE user_id={} ".format(search_by))
        data=cursor.fetchall()
        

        if len(data)!=0:
            print('='*100)
            df=pd.DataFrame(list(data),columns=['trans_id','Account no','type','Date','current balance','trans_amount'])
            print(df.to_string()) # 'to_string' used to display all columns ,otherwise df will reduce the columns
            print('='*100)
        else:
            print("No records found")
     except:
         print("invalid input")


#===========================call functions according to user input=========================
   
loop=True
while loop==True:
            
    user_input=menu()
    print(user_input)

    # create account
    if user_input=='1':
        add_account()

    # display record
    if user_input=='2':
        sub_input=sub_menu()

        if sub_input=='a':
            display_records('account_no')

        if sub_input=='b':
            display_records('Name')

        if sub_input=='c':
            display_records('Balance')

    # search by account no   
    if user_input=='3':
        acc_inp=input("enter the account no : ")
        search_records(int(acc_inp))
         

    # update user record             
    if user_input=='4':
        acc_inp=input("enter the account no : ")
        print("enter the record you want to edit")
        print("1.Name")
        print("2.Mobile_no")
        print("3.Address")
        print("4.Email")
        print("5.country")
              
        up_inp=input("enter the category : ")
        if up_inp=='1':
            update_by='Name'
        if up_inp=='2':
            update_by='Mobile_no'
        if up_inp=='3':
            update_by='Address'
        if up_inp=='4':
            update_by='Email'
        if up_inp=='5':
            update_by='Country'

        set_inp=str(input("enter that details : "))
        update_records(int(acc_inp),update_by,set_inp)


    # delete the user record

    if user_input=='5':
        acc_inp=input("enter the account no : ")
        delete_record(acc_inp)
                    
        
    # Credit or debit into account

    if user_input=='6':
        acc_inp=input("enter the account no : ")
        or_inp=input(" choose\
                a. credit\
                b. debit : ")
        if or_inp=='a':
             trans_type="credit"
        elif or_inp=='b':
             trans_type="debit"


        trans_amt=input("enter the amount")

        trans_record(acc_inp,trans_type,int(trans_amt))
       
    # display transactions

    if user_input=='7':
        acc_inp=input("enter the account no : ")
        display_trans(acc_inp)

   
    # exit loop
    
    if user_input=='8':
        loop=False
        print("exiting.................")    
       

        



    


