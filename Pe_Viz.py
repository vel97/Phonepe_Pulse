import base64
import pandas as pd
import mysql.connector as mc
from mysql.connector import Error
import plotly.express as px
import geopandas as gpd
import streamlit as st
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt

############### Getting Data from MySql ###############################
try:
    connect = mc.connect(host='localhost',database='sriram',user='root',password='qwerty@ybl')
    if connect.is_connected():
        cursor = connect.cursor()
        #Retrieving and placing the data in dataframes through sql commands
        #agg_trans
        cursor.execute("SELECT * FROM agg_transaction")
        data1 = cursor.fetchall()
        agg_transaction = pd.DataFrame(data1,columns=[i[0] for i  in cursor.description])
        #agg_user
        cursor.execute("SELECT * FROM agg_user")
        data2 = cursor.fetchall()
        agg_user = pd.DataFrame(data2,columns=[i[0] for i in cursor.description])
        #map_trans
        cursor.execute("SELECT * FROM map_transaction")
        data3 = cursor.fetchall()
        map_transaction = pd.DataFrame(data3,columns=[i[0] for i in cursor.description])
        #map_user
        cursor.execute("SELECT * FROM map_user")
        data4 = cursor.fetchall()
        map_user = pd.DataFrame(data4,columns=[i[0] for i in cursor.description])
        #top_Dt_transaction
        cursor.execute("SELECT * FROM top_Dt_Transaction")
        data5 = cursor.fetchall()
        top_district = pd.DataFrame(data5,columns=[i[0] for i in cursor.description])
        #top_P_transaction
        cursor.execute("SELECT * FROM top_P_Transaction")
        data6 = cursor.fetchall()
        top_Pincode = pd.DataFrame(data6,columns=[i[0] for i in cursor.description])
        
        connect.commit()
        cursor.close()
        connect.close()
except Error as e:
    pass

############################# Back ground ##########################################
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url(data:image/{"jpg"};base64,{encoded_string.decode()});
        background-size: cover
    }}
    </style>
    """,
    unsafe_allow_html=True
    )
add_bg_from_local('upi1.jpg')  
############################# Data inputs ###########################################
State = ('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh','assam',
'bihar','chandigarh', 'chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa',
'gujarat','haryana', 'himachal-pradesh', 'jammu-&-kashmir', 'jharkhand','karnataka', 'kerala',
'ladakh','lakshadweep', 'madhya-pradesh','maharashtra', 'manipur', 'meghalaya', 'mizoram',
'nagaland','odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim','tamil-nadu', 'telangana',
'tripura','uttar-pradesh','uttarakhand', 'west-bengal')
Year = ('2018', '2019', '2020', '2021', '2022')
Quarter = ('Q1', 'Q2', 'Q3', 'Q4')

########################### Home Page ##################################################
with st.sidebar:
    Option_list = option_menu('Menu Bar',['Home','App Registered','Mobile Brand','Transaction','Map'],
        icons=['house', 'app', 'phone', 'phone','geo-alt'],
        default_index=0, orientation="Horizontal",styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "#F0FFFF", "font-size": "20px"}, 
        "nav-link": {"font-size": "25px","font-color":"#006400", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "#4169E1"}
    })    

if Option_list == 'Home':
     st.markdown("<h1 style='text-align:center; color:#7FFFD4;'"
                ">Phonepe Pulse Data Visualization</h1>",unsafe_allow_html=True)
     
     st.write("<h1 style='text-align:left; font-size:30px; color:#F0FFFF;'"
                ">PhonePe is an Indian digital payments and financial services company headquartered in Bengaluru, Karnataka, India.PhonePe was founded in December 2015, by Sameer Nigam, Rahul Chari and Burzin Engineer.The PhonePe app, based on the Unified Payments Interface (UPI), went live in August 2016",
             "The PhonePe app is available in 11 Indian languages.Using PhonePe, users can send and receive money, recharge mobile, DTH, data cards, make utility payments, pay at shops, invest in tax saving funds, liquid funds, buy insurance, mutual funds, and digital gold.",
             "PhonePe is licensed by the Reserve Bank of India for the issuance and operation of a Semi Closed Prepaid Payment system with Authorisation Number: 75/2014 dated 22 August 2014.</h1>",unsafe_allow_html=True)
    
######################### App registered #####################################################
if Option_list =='App Registered':
    st.markdown("<h1 style='text-align:center; color:#F0FFFF;'"
                ">Registered User By District with respect to State, Year and Quarter</h1>",
                unsafe_allow_html=True)
  
    css = '''
    <style>
        .stSelectbox [data-testid='stMarkdownContainer'] {
            color: #F0FFFF;
        } 
    </style>'''
    st.markdown(css, unsafe_allow_html=True)
    
    bYear = st.selectbox("Year", options=Year)
    state = st.selectbox('Select the State:', State, index=30)
    quarter = st.selectbox("Quarter:", Quarter)
    map_user_dt_filter = map_user[(map_user['State'] == state)& (map_user['Year'] == int(bYear)) & 
    (map_user['Quarter'] == quarter)]

    dist_reg_bar = map_user_dt_filter.groupby(['District']).sum(numeric_only=True)['Registered_User']
    dist_reg_bar = dist_reg_bar.reset_index()

    fig = px.bar(dist_reg_bar,
                  x="District",
                  y=["Registered_User"],
                  color='District',
                  title=f"Registred users of {state} (District wise):")
    fig.update_traces(width=1)
    st.plotly_chart(fig)

    st.markdown("<h1 style='text-align:center; color:#F0FFFF;'"
                ">Registered User By State, year & Quarter</h1>",
                unsafe_allow_html=True)
   
    Filt = st.selectbox('Group',options=("State", "Year", "Quarter"))
    if Filt == "State":
        map_user_by_state = map_user.groupby('State').sum(numeric_only=True)['Registered_User']
        map_user_by_state = map_user_by_state.reset_index()
        fig = px.pie(map_user_by_state, values="Registered_User", names="State",title="State wise registered users")
        st.plotly_chart(fig)

    if Filt == "Year":
        map_user_by_year = map_user.groupby('Year').sum(numeric_only=True)['Registered_User']
        map_user_by_year = map_user_by_year.reset_index()
        fig = px.pie(map_user_by_year, values="Registered_User", names="Year",title="Year wise registered users")
        st.plotly_chart(fig)

    if Filt == "Quarter":
        map_user_by_quarter = map_user.groupby('Quarter').sum(numeric_only=True)['Registered_User']
        map_user_by_quarter = map_user_by_quarter.reset_index()
        fig = px.pie(map_user_by_quarter, values="Registered_User", names="Quarter",title="Quarter wise registered users")
        st.plotly_chart(fig)

############################ Mobile Brand Analysis #######################################################

if Option_list == 'Mobile Brand':
    st.markdown("<h1 style='text-align:center; color:#F0FFFF;'"
                ">Mobile Brand Analysis</h1>",
                unsafe_allow_html=True)

    css = '''
    <style>
        .stSelectbox [data-testid='stMarkdownContainer'] {
            color: #F0FFFF;
        } 
    </style>'''
    
    st.markdown(css, unsafe_allow_html=True)
    state = st.selectbox('State', State)
    year = st.selectbox('Year:', Year)
    quarter = st.selectbox('Quarter:', Quarter)

    agg_user_filt = agg_user[(agg_user['State'] == state) & (agg_user['Year'] == int(year))
    & (agg_user['Quarter'] == quarter)]

    bar = px.bar(agg_user_filt,x='Brand_type',y='Brand_count',color='Brand_type',title='Brand Analysis')
    st.plotly_chart(bar)

    ################ distribution of brands using box plot ################################
    st.markdown("<h1 style='text-align:center; color:#F0FFFF;'"
                ">Distribution of Brands by Count and Percentage</h1>",unsafe_allow_html=True)

    Filt_time = st.selectbox('Group',options=("State", "Year", "Quarter"))
    Filt_Brand = st.selectbox('Brand',options=('Brand_count', 'Brand_percentage'))

    if Filt_time == 'State' and Filt_Brand == 'Brand_count':
        agg_user_filt_st = agg_user[(agg_user['State'] == state)]
        fig = px.box(agg_user_filt_st, x="Brand_type", y="Brand_count", color='Brand_type',points="outliers")
        st.plotly_chart(fig)

    if Filt_time == 'Year' and Filt_Brand == 'Brand_count':
        agg_user_filt_st = agg_user[(agg_user['Year'] == int(year))]
        fig = px.box(agg_user_filt_st, x="Brand_type", y="Brand_count", color='Brand_type',points="outliers")
        st.plotly_chart(fig)

    if Filt_time == 'Quarter' and Filt_Brand == 'Brand_count':
        agg_user_filt_st = agg_user[(agg_user['Quarter'] == quarter)]
        fig = px.box(agg_user_filt_st, x="Brand_type", y="Brand_count", color='Brand_type',points="outliers")
        st.plotly_chart(fig)

    if Filt_time == 'State' and Filt_Brand == 'Brand_percentage':
        agg_user_filt_st = agg_user[(agg_user['State'] == state)]
        fig = px.box(agg_user_filt_st, x="Brand_type", y="Brand_percentage", color='Brand_type',points="outliers")
        st.plotly_chart(fig)

    if Filt_time == 'Year' and Filt_Brand == 'Brand_percentage':
        agg_user_filt_st = agg_user[(agg_user['Year'] == int(year))]
        fig = px.box(agg_user_filt_st, x="Brand_type", y="Brand_percentage", color='Brand_type',points="outliers")
        st.plotly_chart(fig)

    if Filt_time == 'Quarter' and Filt_Brand == 'Brand_percentage':
        agg_user_filt_st = agg_user[(agg_user['Quarter'] == quarter)]
        fig = px.box(agg_user_filt_st, x="Brand_type", y="Brand_percentage", color='Brand_type',points="outliers")
        st.plotly_chart(fig)

############################ Transactions ###################################################
if Option_list == 'Transaction':
    st.markdown("<h1 style='text-align:center; color:#F0FFFF;'"
                ">Analysis of Transactions</h1>",
                unsafe_allow_html=True)

    css = '''
    <style>
        .stSelectbox [data-testid='stMarkdownContainer'] {
            color: #F0FFFF;
        } 
    </style>'''
    
    st.markdown(css, unsafe_allow_html=True)

    Filt_Trans = st.selectbox('Group',options=('State', 'Year', 'Quater'))
    scatter = px.scatter(map_transaction, x='Transaction_count', y='Transaction_amount',color=Filt_Trans)
    st.plotly_chart(scatter) 

    st.markdown("<h1 style='text-align:center; color:#F0FFFF;'"
                ">Transactions with respect to District</h1>",
                unsafe_allow_html=True)
    
    t_state = st.selectbox('State', options=State)
    Filt_State_top = top_district[(top_district['State'] == t_state)]
    Filt_top = st.selectbox('Group',options=('T_count', 'T_amount'))
    
    if Filt_top == 'T_count':
        top_district_filt = Filt_State_top.groupby('District').sum(numeric_only=True)['Dt_Transaction_count']
        top_district_filt = top_district_filt.reset_index()
        fig = px.pie(top_district_filt, values="Dt_Transaction_count", names="District",title="District wise Transaction_count")
        st.plotly_chart(fig)

    if Filt_top == 'T_amount':
        top_district_filt = Filt_State_top.groupby('District').sum(numeric_only=True)['Transaction_amount']
        top_district_filt = top_district_filt.reset_index()
        fig = px.pie(top_district_filt, values="Transaction_amount", names="District",title="District wise Transaction_amount")
        st.plotly_chart(fig)

        st.markdown("<h1 style='text-align:center; color:#F0FFFF;'"
                ">Transactions with respect to Pincode</h1>",
                unsafe_allow_html=True)
    
    Filt_Pin_top = top_Pincode[(top_Pincode['State'] == t_state)]
    
    if Filt_top == 'T_count':
        fig1 = px.bar(Filt_Pin_top,
                  x="Pincode",
                  y="P_Transaction_count",
                  color='Pincode',
                  title=f"P_Transaction_count of {t_state} (Pincode wise):")
        fig1.update_traces(width=1)
        st.plotly_chart(fig1)

    if Filt_top == 'T_amount':
        fig2 = px.bar(Filt_Pin_top,
                  x="Pincode",
                  y="Pransaction_amount",
                  color='Pincode',
                  title=f"Transaction_amount of {t_state} (Pincode wise):")
        fig2.update_traces(width=1)
        st.plotly_chart(fig2)
# ############################ Geo Visualization #################################################
lat_long = pd.read_csv("C://Users//SriramvelM//Downloads//archive//poptable.csv")
lat_long.head()

if Option_list == 'Map':
    st.markdown("<h1 style='text-align:center; color:#F0FFFF;'"
                ">Transaction with respect to State</h1>",
                unsafe_allow_html=True)
    
    css = '''
    <style>
        .stSelectbox [data-testid='stMarkdownContainer'] {
            color: #F0FFFF;
        } 
    </style>'''
    st.markdown(css, unsafe_allow_html=True)
    G_year = st.selectbox('Year:', Year)
    G_quarter = st.selectbox('Quarter:', Quarter)

    agg_transaction_geo_filt = agg_transaction.groupby(['State', 'Year', 'Quarter']).sum(numeric_only=True)[['Transaction_count','Transaction_amount']]
    agg_transaction_geo_filt = agg_transaction_geo_filt.reset_index()

    Geofilt_Y_Qtr = agg_transaction_geo_filt[(agg_transaction_geo_filt['Year'] == int(G_year)) & (agg_transaction_geo_filt['Quarter'] == G_quarter)]
    Geofilt_Y_Qtr = Geofilt_Y_Qtr[Geofilt_Y_Qtr.State != 'telangana']
    # Geofilt_Y_Qtr.to_csv('State.csv',index=False)
    Geofilt_Y_Qtr1 = pd.read_csv("C://Users//SriramvelM//Desktop//sklearn_vs//State.csv")  

    url = "https://raw.githubusercontent.com/Subhash9325/GeoJson-Data-of-Indian-States/master/Indian_States"
    gdf = gpd.read_file(url)
    gdf = gdf.drop(['ID_0', 'NL_NAME_1','NAME_0', 'filename', 'filename_1','ISO', 'ID_1', 'filename_2', 'filename_3', 'filename_4'], axis=1)
    gdf = gdf.drop(['VARNAME_1', 'TYPE_1', 'ENGTYPE_1'], axis=1)
    gdf = gdf.rename(columns={"NAME_1": "State"})

    #merge
    merge = pd.merge(gdf, Geofilt_Y_Qtr1)
    
    fig, ax = plt.subplots(1, figsize=(12, 12))
    ax.axis('off')
    ax.set_title(f"Transaction_count of Year {G_year} under Quarter {G_quarter}:",
             fontdict={'fontsize': '15', 'fontweight' : '3'})
    ind = merge.plot(column='Transaction_count',cmap='YlOrRd',ax=ax, linewidth=0.8,legend=True)
    fig = ind.get_figure()
    st.pyplot(fig)


########### Use the command **streamlit run Pe_Viz.py** to run the file #################