import numpy as np
import pandas as pd
import json
import os

path = "C://Users//SriramvelM//Desktop//sklearn_vs//pulse//data//aggregated//transaction//country//india//state" 
agg_trans_s_d = os.listdir(path)
agg_trans_s_d

for i in agg_trans_s_d:
  s_p = path+'//'+i+'//'
  print(s_p)

for i in agg_trans_s_d:
  s_p = path+'//'+i+'//'
  s_y = os.listdir(s_p)
  for j in s_y:
    s_y_path = s_p+j+'//'
    s_y_dir = os.listdir(s_y_path)
    for k in s_y_dir:
      json_file = s_y_path+k
      data = open(json_file, 'r')
      out = json.load(data)
      print(out)
      break

out['success']
out['data']
out['data']['transactionData']

############# Aggregated Transaction Data by State ################################################
agg_trans_d = dict(State = [], Year=[], Quarter = [], 
Transaction_type = [], Transaction_count = [], Transaction_amount = [])

for i in agg_trans_s_d:
  s_p = path+'//'+i+'//'
  s_y = os.listdir(s_p)
  for j in s_y:
    s_y_path = s_p+j+'//'
    s_y_dir = os.listdir(s_y_path)
    for k in s_y_dir:
      json_file = s_y_path+k
      data = open(json_file, 'r')
      out = json.load(data)
      for l in out['data']['transactionData']:
        name = l['name']
        count = l['paymentInstruments'][0]['count']
        amount = l['paymentInstruments'][0]['amount']
        agg_trans_d['Transaction_type'].append(name)
        agg_trans_d['Transaction_count'].append(count)
        agg_trans_d['Transaction_amount'].append(amount)
        agg_trans_d['Quarter'].append('Q'+k[0])
        agg_trans_d['Year'].append(j)
        agg_trans_d['State'].append(i)

agg_trans_df = pd.DataFrame(agg_trans_d)
agg_trans_df.tail()

agg_trans_df.to_csv('agg_trans_df.csv',index=False) 
#################### Aggregated user by state ###########################################################
path = "C://Users//SriramvelM//Desktop//sklearn_vs//pulse//data//aggregated//user//country//india//state" 
agg_user_s_d = os.listdir(path)
agg_user_s_d

agg_user_d = dict(State = [], Year=[], Quarter = [],
Brand_type = [], Brand_count = [], Brand_percentage = [])

agg_user_d1 = dict(Users = [], AppOpen_count = [])

for i in agg_user_s_d:
  state_path = path+'//'+i+'//'
  state_year = os.listdir(state_path)
  for j in state_year:
    st_yr_path = state_path+j+'//'
    st_yr_dir = os.listdir(st_yr_path)
    for k in st_yr_dir:
      j_file = st_yr_path+k
      j_data = open(j_file, 'r')
      out1 = json.load(j_data)
      agg_user_d1['Users'].append(out1['data']['aggregated']['registeredUsers'])
      agg_user_d1['AppOpen_count'].append(out1['data']['aggregated']['appOpens'])
      try:      
       for l in out1['data']['usersByDevice']:
        brand = l['brand']
        count = l['count']
        percentage = l['percentage']
        agg_user_d['Brand_type'].append(brand)
        agg_user_d['Brand_count'].append(count)
        agg_user_d['Brand_percentage'].append(percentage)
        agg_user_d['Quarter'].append('Q'+k[0])
        agg_user_d['Year'].append(j)
        agg_user_d['State'].append(i)
      except TypeError:
       pass

agg_user_df = pd.DataFrame(agg_user_d)
agg_user_df.head()

agg_user_df1 = pd.DataFrame(agg_user_d1)
agg_user_df1.tail()

agg_user_df.to_csv('agg_user_df.csv',index=False)
agg_user_df1.to_csv('agg_user_df1.csv',index=False)
################### Map Transaction by States ###############################################################
path='C://Users//SriramvelM//Desktop//sklearn_vs//pulse//data//map//transaction//hover//country//india//state'
hover_state_d =os.listdir(path)

map_trans_dt = dict(State=[], Year=[], Quater=[], District=[],Transaction_count=[], Transaction_amount=[])

for i in hover_state_d:
  state_path = path+'//'+i+'//'
  state_year = os.listdir(state_path)
  for j in state_year:
    st_yr_path = state_path+j+'//'
    st_yr_dir = os.listdir(st_yr_path)
    for k in st_yr_dir:
      j_file = st_yr_path+k
      j_data = open(j_file, 'r')
      out1 = json.load(j_data)
      try:
        for l in out1['data']["hoverDataList"]:
          district = l['name']
          trans_count = l['metric'][0]['count']
          trans_amount = l['metric'][0]['amount']
          map_trans_dt['State'].append(i)
          map_trans_dt['Year'].append(j)
          map_trans_dt['Quater'].append('Q'+k[0])
          map_trans_dt['District'].append(district)
          map_trans_dt['Transaction_count'].append(trans_count)
          map_trans_dt['Transaction_amount'].append(trans_amount)
      except TypeError:
        pass
      
map_trans_df = pd.DataFrame(map_trans_dt)
map_trans_df.head()
map_trans_df.shape

map_trans_df.to_csv('map_trans_df.csv',index=False)
################# Map Users by State ###################################################################
path='C://Users//SriramvelM//Desktop//sklearn_vs//pulse//data//map//user//hover//country//india//state'
state_map_user =os.listdir(path)

map_user_dt = dict(State= [], Year= [], Quater= [], District= [], Registered_User= [], App_Opening= [])

for i in state_map_user:
  state_path = path+'//'+i+'//'
  state_year = os.listdir(state_path)
  for j in state_year:
    st_yr_path = state_path+j+'//'
    st_yr_dir = os.listdir(st_yr_path)
    for k in st_yr_dir:
      j_file = st_yr_path+k
      j_data = open(j_file, 'r')
      out1 = json.load(j_data)
      try:
        for l in out1['data']["hoverData"]:
          registeredUser =  out1['data']["hoverData"][l]["registeredUsers"]
          app_opening = out1['data']["hoverData"][l]["appOpens"]
          map_user_dt['District'].append(l)
          map_user_dt['Registered_User'].append(registeredUser)
          map_user_dt['App_Opening'].append(app_opening)
          map_user_dt['State'].append(i)
          map_user_dt['Year'].append(j)
          map_user_dt['Quater'].append('Q'+k[0])
      except TypeError:
        pass      
      
map_user_df = pd.DataFrame(map_user_dt)
map_user_df.head()
map_user_df.shape

map_user_df.to_csv('map_user_df.csv',index=False)

#################### top map ############################################
path='C://Users//SriramvelM//Desktop//sklearn_vs//pulse//data//top//transaction//country//india//state'
state_top_trans =os.listdir(path)

top_trans_dt = dict(State= [], Year=[], Quarter=[], District= [], Dt_Transaction_amount= [],
                    Dt_Transaction_count= [])

top_trans_dt1 = dict(State= [], Year=[], Quarter=[],
                     Pincode= [], P_Transaction_amount= [], P_Transaction_count= [])

for i in state_top_trans:
  state_path = path+'//'+i+'//'
  state_year = os.listdir(state_path)
  for j in state_year:
    st_yr_path = state_path+j+'//'
    st_yr_dir = os.listdir(st_yr_path)
    for k in st_yr_dir:
      j_file = st_yr_path+k
      j_data = open(j_file, 'r')
      out1 = json.load(j_data)
      print(out1)  
      try:
         for l in out1['data']['districts']:
            District = l['entityName']
            Dt_trans_amount = l['metric']['amount']
            Dt_trans_count = l['metric']['count']
            top_trans_dt['State'].append(i)
            top_trans_dt['Year'].append(j)
            top_trans_dt['Quarter'].append('Q'+k[0])
            top_trans_dt['District'].append(District)
            top_trans_dt['Dt_Transaction_amount'].append(Dt_trans_amount)
            top_trans_dt['Dt_Transaction_count'].append(Dt_trans_count)
         for m in out1['data']['pincodes']:
            pincode = m['entityName']
            P_trans_amount = m['metric']['amount']
            P_Trans_count = m['metric']['count']
            top_trans_dt1['State'].append(i)
            top_trans_dt1['Year'].append(j)
            top_trans_dt1['Quarter'].append('Q'+k[0])
            top_trans_dt1['Pincode'].append(pincode)
            top_trans_dt1['P_Transaction_amount'].append(P_trans_amount)
            top_trans_dt1['P_Transaction_count'].append(P_Trans_count)
      except TypeError:
        pass      

top_trans_df = pd.DataFrame(top_trans_dt)
top_trans_df.head()
top_trans_df.shape

# top_trans_df = top_trans_df[(top_trans_df['District'] != top_trans_df['State'])]

top_trans_df1 = pd.DataFrame(top_trans_dt1)
top_trans_df1.shape
top_trans_df1.head()

# out1['data']['districts'][0]['entityName']
# out1['data']['districts'][0]['metric']['count']
# out1['data']['districts'][1]['entityName']
# out1['data']['pincodes'][0]['metric']['count']
############## Inserting into mysql database ############################
import mysql.connector as mc
from mysql.connector import Error
try:
    conn = mc.connect(host='localhost', database='sriram', user='root', password='qwerty@ybl')
    if conn.is_connected():
        cursor = conn.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
        cursor.execute('DROP TABLE IF EXISTS map_user;')
        # passing create table statement
        cursor.execute("CREATE TABLE map_user(State varchar(255),Year int,Quarter varchar(10),District varchar(255),Registered_User  int,App_Opening int)")
        print("Table Created")
        #loop through the data frame
        for i,row in map_user_df.iterrows():
            #here %S means string values 
            sql = "INSERT INTO sriram.map_user VALUES (%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, tuple(row))
            print("Record inserted")
            conn.commit()
except Error as e:
            print("Error while connecting to MySQL", e)   

######################## map_transaction ####################################
try:
    conn = mc.connect(host='localhost', database='sriram', user='root', password='qwerty@ybl')
    if conn.is_connected():
        cursor = conn.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
        cursor.execute('DROP TABLE IF EXISTS map_transaction;')
        # passing create table statement
        cursor.execute("CREATE TABLE map_transaction(State varchar(255),Year int,Quarter varchar(10),District varchar(255),Transaction_count int,Transaction_amount int)")
        print("Table Created")
        #loop through the data frame
        for i,row in map_user_df.iterrows():
            #here %S means string values 
            sql = "INSERT INTO sriram.map_transaction VALUES (%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, tuple(row))
            print("Record inserted")
            conn.commit()
except Error as e:
            print("Error while connecting to MySQL", e)   

######################## Agg_transaction ##########################################3
try:
    conn = mc.connect(host='localhost', database='sriram', user='root', password='qwerty@ybl')
    if conn.is_connected():
        cursor = conn.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
        cursor.execute('DROP TABLE IF EXISTS agg_transaction;')
        # passing create table statement
        cursor.execute("CREATE TABLE agg_transaction(State varchar(255),Year int,Quarter varchar(10),Transaction_type varchar(255),Transaction_cout int,Transaction_amount int)")
        print("Table Created")
        #loop through the data frame
        for i,row in map_user_df.iterrows():
            #here %S means string values 
            sql = "INSERT INTO sriram.agg_transaction VALUES (%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, tuple(row))
            print("Record inserted")
            conn.commit()
except Error as e:
            print("Error while connecting to MySQL", e)   

################### Agg_user ###########################################
try:
    conn = mc.connect(host='localhost', database='sriram', user='root', password='qwerty@ybl')
    if conn.is_connected():
        cursor = conn.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
        cursor.execute('DROP TABLE IF EXISTS agg_user;')
        # passing create table statement
        cursor.execute("CREATE TABLE agg_user(State varchar(255),Year int,Quarter varchar(10),Brand_type varchar(255),Brand_count int,Brand_percentage int)")
        print("Table Created")
        #loop through the data frame
        for i,row in map_user_df.iterrows():
            #here %S means string values 
            sql = "INSERT INTO sriram.agg_user VALUES (%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, tuple(row))
            print("Record inserted")
            conn.commit()
except Error as e:
            print("Error while connecting to MySQL", e)   

######################## District_transaction ##########################################3
try:
    conn = mc.connect(host='localhost', database='sriram', user='root', password='qwerty@ybl')
    if conn.is_connected():
        cursor = conn.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
        cursor.execute('DROP TABLE IF EXISTS top_Dt_Transaction;')
        # passing create table statement
        cursor.execute("CREATE TABLE top_Dt_Transaction(State varchar(255),Year int,Quarter varchar(10),District varchar(255),Dt_Transaction_count bigint,Transaction_amount bigint)")
        print("Table Created")
        #loop through the data frame
        for i,row in top_trans_df.iterrows():
            #here %S means string values 
            sql = "INSERT INTO sriram.top_Dt_Transaction VALUES (%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, tuple(row))
            print("Record inserted")
            conn.commit()
except Error as e:
            print("Error while connecting to MySQL", e)  

######################## Pincode_transaction ##########################################3
try:
    conn = mc.connect(host='localhost', database='sriram', user='root', password='qwerty@ybl')
    if conn.is_connected():
        cursor = conn.cursor()
        cursor.execute("select database();")
        record = cursor.fetchone()
        print("You're connected to database: ", record)
        cursor.execute('DROP TABLE IF EXISTS top_P_Transaction;')
        # passing create table statement
        cursor.execute("CREATE TABLE top_P_Transaction(State varchar(255),Year int,Quarter varchar(10),Pincode varchar(255),P_Transaction_count bigint,Pransaction_amount bigint)")
        print("Table Created")
        #loop through the data frame
        for i,row in top_trans_df1.iterrows():
            #here %S means string values 
            sql = "INSERT INTO sriram.top_P_Transaction VALUES (%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql, tuple(row))
            print("Record inserted")
            conn.commit()
except Error as e:
            print("Error while connecting to MySQL", e)   