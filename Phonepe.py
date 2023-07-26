import pandas as pd
import PIL
from PIL import Image
import os
import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import matplotlib.pyplot as plt
import requests
import geopandas as gpd
import sqlite3



# connect to sql
db_path = r'C:\Users\Vijai\Documents\Projects\venv\phonepe_pulse.db'
connection = sqlite3.connect(db_path)
cursor = connection.cursor()

st.set_page_config(layout="wide")
st.title("Phonepe Pulse Data Visualization")

st.sidebar.header(":wave: :violet[**Hello! Welcome to the dashboard**]")
with st.sidebar:
    select = option_menu(menu_title ="Menu",
                          options = ["Home", "Basic insights", "About", "Contact"],
                          icons = ["house", "graph-up-arrow", "exclamation-circle", "at"],
                          menu_icon="cast",
                          default_index =0, )

#--------------------------------Home---------------------------
if select == "Home":
    st.image(Image.open(r"C:\Users\Vijai\Documents\Projects\venv\phonepe.png"), width=500)
    st.subheader(
        "PhonePe  is an Indian digital payments and financial technology company headquartered in Bengaluru, Karnataka, India. PhonePe was founded in December 2015, by Sameer Nigam, Rahul Chari and Burzin Engineer. The PhonePe app, based on the Unified Payments Interface (UPI), went live in August 2016. It is owned by Flipkart, a subsidiary of Walmart.")
    st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")

    Year = st.slider("**Year**", min_value=2018, max_value=2022)
    Quarter = st.slider("Quarter", min_value=1, max_value=4)
    Type = st.selectbox("**Type**", ["Transactions", "Users"])
    tab1, tab2 = st.tabs(['Transactions Amount','Transactions Count'])
    #Explore Transactions
    if Type == "Transactions":
        # Overall State Data - TRANSACTIONS AMOUNT - INDIA MAP
        with tab1:
            st.markdown("## :violet[Overall State Data - Transactions Amount]")
            cursor.execute(
                f"select state, sum(count) as Total_Transactions, sum(amount) as Total_amount from map_transactions where year = {Year} and quarter = {Quarter} group by state order by state")
            df1 = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Transactions', 'Total_amount'])
            df2 = pd.read_csv(r'C:\Users\Vijai\Documents\Projects\venv\Statenames.csv')
            df1.State = df2
        fig = px.choropleth(df1,
                            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                            featureidkey='properties.ST_NM',
                            locations='State',
                            color='Total_amount',
                            color_continuous_scale='Reds')

        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig, use_container_width=True)

        with tab2:
            st.markdown("## :violet[Overall State Data - Transactions Count]")
            cursor.execute(
                f"select state, sum(count) as Total_Transactions, sum(amount) as Total_amount from map_transactions where year = {Year} and quarter = {Quarter} group by state order by state")
            df1 = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Transactions', 'Total_amount'])
            df2 = pd.read_csv(r'C:\Users\Vijai\Documents\Projects\venv\Statenames.csv')
            df1.Total_Transactions = df1.Total_Transactions.astype(int)
            df1.State = df2

            fig = px.choropleth(df1,
                                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                                featureidkey='properties.ST_NM',
                                locations='State',
                                color='Total_Transactions',
                                hover_name = 'State',
                                color_continuous_scale='sunset')

            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig, use_container_width=True)
        # BAR CHART - TOP PAYMENT TYPE
        st.markdown("## :violet[Top Payment Type]")
        cursor.execute(
            f"select Transaction_type, sum(Transaction_count) as Total_Transactions, sum(Transaction_amount) as Total_amount from agg_transactions where year= {Year} and quarter = {Quarter} group by transaction_type order by Transaction_type")
        df = pd.DataFrame(cursor.fetchall(), columns=['Transaction_type', 'Total_Transactions', 'Total_amount'])

        fig = px.bar(df,
                    title='Transaction Types vs Total_Transactions',
                    x="Transaction_type",
                    y="Total_Transactions",
                    orientation='v',
                    color='Total_amount',
                    color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig, use_container_width=False)

        # BAR CHART TRANSACTIONS - DISTRICT WISE DATA
        st.markdown("# ")
        st.markdown("# ")
        st.markdown("# ")
        st.markdown("## :violet[Select any State to explore District-Wise]")
        selected_state = st.selectbox("",
                                  ('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh', 'assam', 'bihar',
                                   'chandigarh', 'chhattisgarh', 'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi', 'goa',
                                   'gujarat', 'haryana',
                                   'himachal-pradesh', 'jammu-&-kashmir', 'jharkhand', 'karnataka', 'kerala', 'ladakh',
                                   'lakshadweep',
                                   'madhya-pradesh', 'maharashtra', 'manipur', 'meghalaya', 'mizoram',
                                   'nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim',
                                   'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh', 'uttarakhand', 'west-bengal'),
                                  index=30)

        cursor.execute(
            f"select State, District,year,quarter, sum(count) as Total_Transactions, sum(amount) as Total_amount from map_transactions where year = {Year} and quarter = {Quarter} and State = '{selected_state}' group by State, District,year,quarter order by state,district")

        df1 = pd.DataFrame(cursor.fetchall(), columns=['State', 'District', 'Year', 'Quarter',
                                                     'Total_Transactions', 'Total_amount'])
        fig = px.bar(df1,
                 title=selected_state,
                 x="District",
                 y="Total_Transactions",
                 orientation='v',
                 color='Total_amount',
                 color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig, use_container_width=True)

    # EXPLORE DATA - USERS
    if Type == "Users":
        # Overall State Data - TOTAL APPOPENS - INDIA MAP
        st.markdown("## :violet[Overall State Data - User App opening frequency]")
        cursor.execute(
            f"select state, sum(Registered_user) as Total_Users, sum(App_opens) as Total_Appopens from map_users where year = {Year} and quarter = {Quarter} group by state order by state")
        df1 = pd.DataFrame(cursor.fetchall(), columns=['State', 'Total_Users', 'Total_Appopens'])
        df2 = pd.read_csv(r'C:\Users\Vijai\Documents\Projects\venv\Statenames.csv')
        df1.Total_Appopens = df1.Total_Appopens.astype(float)
        df1.State = df2

        fig = px.choropleth(df1,
                            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                            featureidkey='properties.ST_NM',
                            locations='State',
                            color='Total_Appopens',
                            color_continuous_scale='sunset')

        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig, use_container_width=True)

        # BAR CHART TOTAL UERS - DISTRICT WISE DATA
        st.markdown("## :violet[Select any State to explore more]")
        selected_state = st.selectbox("",
                                      ('andaman-&-nicobar-islands', 'andhra-pradesh', 'arunachal-pradesh', 'assam',
                                       'bihar',
                                       'chandigarh', 'chhattisgarh', 'dadra-&-nagar-haveli-&-daman-&-diu', 'delhi',
                                       'goa', 'gujarat', 'haryana',
                                       'himachal-pradesh', 'jammu-&-kashmir', 'jharkhand', 'karnataka', 'kerala',
                                       'ladakh', 'lakshadweep',
                                       'madhya-pradesh', 'maharashtra', 'manipur', 'meghalaya', 'mizoram',
                                       'nagaland', 'odisha', 'puducherry', 'punjab', 'rajasthan', 'sikkim',
                                       'tamil-nadu', 'telangana', 'tripura', 'uttar-pradesh', 'uttarakhand',
                                       'west-bengal'), index=30)

        cursor.execute(
            f"select State,year,quarter,District,sum(Registered_user) as Total_Users, sum(App_opens) as Total_Appopens from map_users where year = {Year} and quarter = {Quarter} and state = '{selected_state}' group by State, District,year,quarter order by state,district")

        df = pd.DataFrame(cursor.fetchall(),
                          columns=['State', 'year', 'quarter', 'District', 'Total_Users', 'Total_Appopens'])
        df.Total_Users = df.Total_Users.astype(int)

        fig = px.bar(df,
                     title=selected_state,
                     x="District",
                     y="Total_Users",
                     orientation='v',
                     color='Total_Users',
                     color_continuous_scale=px.colors.sequential.Agsunset)
        st.plotly_chart(fig, use_container_width=True)


#-----------------------Basic insights-----------------------------------

if select == "Basic insights":
    st.title("BASIC INSIGHTS")
    st.write("----")
    st.subheader("Let's know some basic insights about the data")
    options = ["--select--",
                "Top 10 states based on year and amount of transaction",
                "List 10 states based on type and amount of transaction",
                "Top 5 Transaction_Type based on Transaction_Amount",
                "Top 10 Registered-users based on States",
                "Top 10 Districts based on states and Count of transaction",
                "List 10 Districts based on states and amount of transaction",
                "List 10 Transaction_Count based on Districts and states",
                "Top 10 RegisteredUsers based on states and District"]

    selects = st.selectbox("Select the option", options)
    if selects == "Top 10 states based on year and amount of transaction":
        cursor.execute(
            "SELECT DISTINCT State, Year, SUM(Transaction_amount) AS Total_Transaction_Amount FROM top_transaction GROUP BY State,Year ORDER BY Total_Transaction_Amount DESC LIMIT 10");
        df = pd.DataFrame(cursor.fetchall(),columns=['State','Year','Transaction_amount'])
        tab1, tab2 = st.tabs(['Data Results','Data Viz'])
        with tab1:
            st.write(df)
        with tab2:
            st.title("Top 10 states and amount of transaction")
            st.bar_chart(data=df, x="State", y="Transaction_amount", use_container_width=True)

    elif selects == "List 10 states based on type and amount of transaction":
        cursor.execute(
            "SELECT DISTINCT State, SUM(Transaction_count) as Total FROM top_transaction GROUP BY State ORDER BY Total ASC LIMIT 10");
        df = pd.DataFrame(cursor.fetchall(),columns = ['State','Total_transaction'])
        tab1, tab2 = st.tabs(['Data Results', 'Data Viz'])
        with tab1:
            st.write(df)
        with tab2:
            st.title("10 states based on type and amount of transaction")
            st.bar_chart(data=df, x="State", y="Total_transaction", use_container_width=True)

    elif selects == "Top 5 Transaction_Type based on Transaction_Amount":
        cursor.execute(
            "SELECT DISTINCT Transaction_type, SUM(Transaction_amount) AS Amount FROM agg_transactions GROUP BY Transaction_type ORDER BY Amount DESC LIMIT 5")
        df = pd.DataFrame(cursor.fetchall(),columns=['Transaction_type', 'Transaction_amount'])
        tab1, tab2 = st.tabs(['Data Results', 'Data Viz'])
        with tab1:
            st.write(df)
        with tab2:
            st.title("Top 5 Transaction_Type based on Transaction_Amount")
            st.bar_chart(data=df, x="Transaction_type", y="Transaction_amount", width=0,height=0)

    elif selects== "Top 10 Registered-users based on States":
            cursor.execute("SELECT DISTINCT State, SUM(Registered_users) AS Users FROM top_user GROUP BY State ORDER BY Users DESC");
            df = pd.DataFrame(cursor.fetchall(),columns=['State','RegisteredUsers'])
            tab1, tab2 = st.tabs(['Data Results', 'Data Viz'])
            with tab1:
                st.write(df)
            with tab2:
                st.title("Top 10 Registered-users based on States and District")
                st.bar_chart(data=df,y="RegisteredUsers",x="State")

    elif selects == "Top 10 Districts based on states and Count of transaction":
            cursor.execute("SELECT DISTINCT State ,District,SUM(Count) AS Counts FROM map_transactions GROUP BY State ,District ORDER BY Counts DESC LIMIT 10");
            df = pd.DataFrame(cursor.fetchall(),columns=['States','District','Transaction_Count'])
            tab1, tab2 = st.tabs(['Data Results', 'Data Viz'])
            with tab1:
                st.write(df)
            with tab2:
                st.title("Top 10 Registered-users based on States and District")
                st.bar_chart(data=df, x="States",y="Transaction_Count", use_container_width=True)

    elif selects== "List 10 Districts based on states and amount of transaction":
            cursor.execute("SELECT DISTINCT State ,Year,SUM(Transaction_amount) AS Amount FROM agg_transactions GROUP BY State, Year ORDER BY Amount ASC LIMIT 10");
            df = pd.DataFrame(cursor.fetchall(),columns=['States','Transaction_year','Transaction_Amount'])
            tab1, tab2 = st.tabs(['Data Results', 'Data Viz'])
            with tab1:
                st.write(df)
            with tab2:
                st.title("Top 10 Registered-users based on States and District")
                st.bar_chart(data=df, x="States", y="Transaction_Amount", use_container_width=True)

    elif selects== "List 10 Transaction_Count based on Districts and states":
            cursor.execute("SELECT DISTINCT State, District, SUM(Count) AS Counts FROM map_transactions GROUP BY State,District ORDER BY Counts ASC LIMIT 10");
            df = pd.DataFrame(cursor.fetchall(),columns=['States','District','Transaction_Count'])
            tab1, tab2 = st.tabs(['Data Results', 'Data Viz'])
            with tab1:
                st.write(df)
            with tab2:
                st.title("Top 10 Registered-users based on States and District")
                st.bar_chart(data=df, x="States", y="Transaction_Count", use_container_width=True)

    elif selects== "Top 10 RegisteredUsers based on states and District":
            cursor.execute("SELECT DISTINCT State ,District, SUM(Registered_User) AS Users FROM map_users GROUP BY State,District ORDER BY Users DESC LIMIT 10");
            df = pd.DataFrame(cursor.fetchall(),columns = ['States','District','RegisteredUsers'])
            tab1, tab2 = st.tabs(['Data Results', 'Data Viz'])
            with tab1:
                st.write(df)
            with tab2:
                st.title("Top 10 Registered-users based on States and District")
                st.bar_chart(data=df, x="States", y="RegisteredUsers", use_container_width=True)

#_____________________________About________________________________________#
# MENU 4 - ABOUT
if select == "About":
    st.write(" ")
    st.write(" ")
    st.markdown("### :violet[About PhonePe Pulse:] ")
    st.write(
            "##### BENGALURU, India, On Sept. 3, 2021 PhonePe, India's leading fintech platform, announced the launch of PhonePe Pulse, India's first interactive website with data, insights and trends on digital payments in the country. The PhonePe Pulse website showcases more than 2000+ Crore transactions by consumers on an interactive map of India. With  over 45% market share, PhonePe's data is representative of the country's digital payment habits.")

    st.write(
            "##### The insights on the website and in the report have been drawn from two key sources - the entirety of PhonePe's transaction data combined with merchant and customer interviews. The report is available as a free download on the PhonePe Pulse website and GitHub.")

    st.markdown("### :violet[About PhonePe:] ")
    st.write(
            "##### PhonePe is India's leading fintech platform with over 300 million registered users. Using PhonePe, users can send and receive money, recharge mobile, DTH, pay at stores, make utility payments, buy gold and make investments. PhonePe forayed into financial services in 2017 with the launch of Gold providing users with a safe and convenient option to buy 24-karat gold securely on its platform. PhonePe has since launched several Mutual Funds and Insurance products like tax-saving funds, liquid funds, international travel insurance and Corona Care, a dedicated insurance product for the COVID-19 pandemic among others. PhonePe also launched its Switch platform in 2018, and today its customers can place orders on over 600 apps directly from within the PhonePe mobile app. PhonePe is accepted at 20+ million merchant outlets across Bharat")

    # st.write("**:violet[My Project GitHub link]** ⬇️")
    # st.write("https://github.com/IamJafar/Phonepe_Pulse_Data_Visualization")
    # st.write("**:violet[Image and content source]** ⬇️")
    # st.write(
    #         "https://www.prnewswire.com/in/news-releases/phonepe-launches-the-pulse-of-digital-payments-india-s-first-interactive-geospatial-website-888262738.html")

if select == "Contact":
    name = "Vijai Gowtham R"
    mail = (f'{"Mail :"}  {"vijaysriram118@gmail.com"}')
    social_media = {
        "GITHUB": "https://github.com/VijaiGR",
        "LINKEDIN": "https://www.linkedin.com/in/vijai-r-3a9304166/"}

    col1, col2,= st.columns(2)
    col2.image(Image.open(r"C:\Users\Vijai\Documents\Projects\venv\phn.png"), width=375)
    with col1:
        st.write(
            "The goal of this project is to extract data from the Phonepe pulse Github repository, transform and clean the data, insert it into a MySQL database, and create a live geo visualization dashboard using Streamlit and Plotly in Python. The dashboard will display the data in an interactive and visually appealing manner, with at least 10 different dropdown options for users to select different facts and figures to display. The solution must be secure, efficient, and user-friendly, providing valuable insights and information about the data in the Phonepe pulse Github repository.")
        st.write("---")
        st.subheader(mail)
    st.write("#")
    cols = st.columns(len(social_media))
    for index, (platform, link) in enumerate(social_media.items()):
        cols[index].write(f"[{platform}]({link})")


