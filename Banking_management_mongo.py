
# import pymongo -interface for connecting with mongo database

import pandas as pd
from pymongo import MongoClient
from datetime import datetime


# connect to database

client=MongoClient("mongodb://root:bhagya@localhost:27017/bankdb")
print(client.list_database_names())
db=client.bankdb   # create database bankdb if it doesn't exist
users_col=db.users    # create collection users if it doesn't exist
trans_col=db.transactions
print(db.list_collection_names())

#insert model data

def insert_model_data():
    d={}
    d['account_no']=1
    d['name']='bhagya'
    d['mobile_no']='1122334455'
    d['address']='Thrissur'
    d['country']='India'
    d['email']='b@gmail.com'
    d['balance']=100

    xy=users_col.insert_one(d)

    d2={}
    d2['account_no']=1
    d2['trans_type']='credit'
    d2['trans_amount']=100
    d2['trans_date']=datetime.now()
    d2['current_balnce']=100

    xy=trans_col.insert_one(d2)

#insert_model_data()


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


        print('*'*100)
        print("enter your details to create account!")
        name=input("enter your name : ")
        mobile=input("enter your mobile no : ")
        address=input("enter your adress : ")
        country=input("enter your contry : ")
        email=input("enter your email : ")

        records={}
        records['account_no']=users_col.count_documents({})+1  ## need to work on autoincrement in mongodb.
        records['name']=name
        records['mobile_no']=mobile
        records['address']=address
        records['country']=country
        records['email']=email
        records['balance']=0
        
        print(records)
        rec=users_col.insert_one(records)
        print('Account created successfully!')
        print('*'*100)

#add_account()


def display_records(sort_by):

     try:

        data=[]
        for x in users_col.find({},{'_id':0,'balance':0}).sort(sort_by):
           data.append(x)  
        print(data)
         
        if len(data)!=0:
            print('='*100)
            df=pd.DataFrame(data)
            print(df.to_string()) # 'to_string' used to display all columns ,otherwise df will reduce the columns
            print('='*100)
        else:
            print("no records found!")

     except:
         print("invalid input")

#display_records


def search_records(search_by):

     try:

        data=[]
        for x in users_col.find({'account_no':search_by}):
           data.append(x)  
        print(data)
         

        if len(data)!=0:
            print('='*100)
            df=pd.DataFrame(data,columns=['account_no','name','mobile_no','address','country','email','balance'])
            print(df.to_string()) # 'to_string' used to display all columns ,otherwise df will reduce the columns
            print('='*100)
        else:
            print("no records found!")
     except:
         print("invalid input")


def update_records(acc_no,update_by,set_inp):

  try:

    data=users_col.update_one({'account_no':acc_no},{'$set':{update_by:set_inp}})
    #print(data.modified_count)
    data=[]
    for x in users_col.find({'account_no':acc_no}):
           data.append(x)  
    
    if len(data)!=0 :
        print('='*100)
        df=pd.DataFrame(data,columns=['account_no','name','mobile_no','address','country','email','balance'])
        print(df.to_string()) # 'to_string' used to display all columns ,otherwise df will reduce the columns
        print('='*100)
    else:
        print("no records found!")

  except:
         print("invalid input")



def delete_record(acc_no):
  try:

    data=users_col.delete_one({'account_no':acc_no})
    del_count=data.deleted_count


    if del_count!=0:
       print(data,"data deleted succesfully!")
    else:
        print("no records found!")

  except:
         print("invalid input")
         



def trans_record(acc_no,trans_type,trans_amt):

  try:
      
    
    data= users_col.find_one({'account_no':acc_no},{'balance':1,'_id':0})
    balance=data['balance']
    if trans_type=="debit":
            curr_balance=balance-trans_amt
    if trans_type=="credit":
            curr_balance=balance+trans_amt
    
    if curr_balance>0:

            d2={}
            d2['account_no']=acc_no
            d2['trans_type']=trans_type
            d2['trans_amount']=trans_amt
            d2['trans_date']=datetime.now()
            d2['current_balance']=curr_balance

            xy=trans_col.insert_one(d2)

            
            bal_up=users_col.update_one({'account_no':acc_no},{'$set':{'balance':curr_balance}})
            print(bal_up.modified_count)
            print(" Transaction done successfully!.current balance is {}".format(curr_balance))

         
            
    else:
        print("Insufficent balance")

  except:
         print("No record found")
         


def display_trans(search_by):

     try:

        data=[]
        for i in trans_col.find({'account_no':search_by},{'_id':0}):
            data.append(i)
       
        if len(data)!=0:
            print('='*100)
            df=pd.DataFrame(list(data),columns=['account_no','trans_type','trans_amount','trans_date','current_balance'])
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
            display_records('name')

        if sub_input=='c':
            display_records('balance')

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
            update_by='name'
        if up_inp=='2':
            update_by='mobile_no'
        if up_inp=='3':
            update_by='address'
        if up_inp=='4':
            update_by='email'
        if up_inp=='5':
            update_by='country'

        set_inp=str(input("enter that details : "))
        update_records(int(acc_inp),update_by,set_inp)


    # delete the user record

    if user_input=='5':
        acc_inp=input("enter the account no : ")
        delete_record(int(acc_inp))


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

        trans_record(int(acc_inp),trans_type,int(trans_amt))

    # display transactions

    if user_input=='7':
        acc_inp=input("enter the account no : ")
        display_trans(int(acc_inp))


    # exit loop

    if user_input=='8':
        loop=False
        print("exiting.................")



