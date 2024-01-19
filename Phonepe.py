#**Clone_the_required_github_repository[Phone pe Pulse]**

#***!git clone https://github.com/PhonePe/pulse.git***

#Import_Required libraries for the program

import streamlit as st

import streamlit_option_menu

from streamlit_option_menu import *

import numpy as np

import pandas as pd

#import psycopg2 as pg2

import mysql.connector as sql

import matplotlib.pyplot as plt

from  plotly.subplots import make_subplots

import plotly_express as px

import plotly.graph_objects as go

#from streamlit_vertical_slider import vertical_slider

from streamlit_extras import *

from streamlit_extras.metric_cards import style_metric_cards

import math

from streamlit_card import card

from streamlit_extras.colored_header import colored_header

from streamlit_extras.stoggle import stoggle

from PIL import Image

from subprocess import check_output
#____________________________________________________________________________________________________________________________________________________________________________

# SQL CONNECTIVITY

connect = sql.connect(host='localhost', user='root', password='12345', database='phonepe_pulse')
cursor = connect.cursor()

#_____________________________________________________________________________________________________________________________________________________________________________

# PAGE CONFIGURATION

phn = Image.open(r"C:\Users\sony\Desktop\Phonepe.jpg")
st.set_page_config(page_title = 'PhonePe_Pulse',page_icon = phn,layout = 'wide')
st.title(":violet[Phonepe Pulse Data Visualization and Exploration]")

#______________________________________________________________________________________________________________________________________________________________________________

                                                                    # PROGRAMS INITIATED

with st.sidebar:     # Navbar


    selected = option_menu(
                               menu_title="Phonepe Pulse",
                               options=['Intro','View Data Source','Transaction Type Analysis',"User Brand Analysis","SDP Analysis",'Time-based Analysis','Insights'],
                               icons = ['mic-fill',"database-fill",'coin','person-circle','geo-alt-fill','hourglass-split','clipboard-data-fill'],
                               menu_icon='alexa',
                               default_index=0,
                               styles={
        "container": {"padding": "0!important", "background-color": "#FFFFFF"},
        "nav-link": {"font-size": "25px", "text-align": "left", "margin":"0px", "--hover-color": "#6739B7"},
        "nav-link-selected": {"background-color": "#6739B7"}}
)
#__________________________________________________________________________________________________________________________________________________________________________________________---
                                                                 #________________________________________Condition_____________________________________#

if selected == "Intro":
    #col1,col2, = st.columns(2)
    #with col1:
        #st.image("Phonepe.jpg")
        #st.image("phonepeExplore.jpg")
        st.image("phnpe.jpg") 
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")
        st.markdown(":black[**PhonePe  is an Indian digital payments and financial technology company headquartered in Bengaluru, Karnataka, India. PhonePe was founded in December 2015, by Sameer Nigam, Rahul Chari and Burzin Engineer. The PhonePe app, based on the Unified Payments Interface (UPI), went live in August 2016. It is owned by Flipkart, a subsidiary of Walmart.**]")    

    #with col2:
        
        st.markdown(":black[**The Indian digital payments story has truly captured the world's imagination."
                 " From the largest towns to the remotest villages, there is a payments revolution being driven by the penetration of mobile phones, mobile internet and state-of-the-art payments infrastructure built as Public Goods championed by the central bank and the government."
                 " Founded in December 2015, PhonePe has been a strong beneficiary of the API driven digitisation of payments in India. When we started, we were constantly looking for granular and definitive data sources on digital payments in India. "
                 "PhonePe Pulse is our way of giving back to the digital payments ecosystem.**]")

elif selected == "Insights":
    ### Phonepe Dashboard Link :
     if st.button("Click to view my Dashboard"):
         file_name = 'Phonepe.pbix'
         check_output("start " + file_name, shell=True)

### Dashboard Pic

     st.image("Phonepe_PBI.png")

elif selected == "Transaction Type Analysis":
        col1, col2 ,col3 , col4  ,col6= st.columns([8,8,8,8,8])
        st.markdown("<style>div.block-container{padding-top:3rem;}</style>", unsafe_allow_html=True)

        # FILTERS

        # 1) state

        cursor.execute('select distinct(state) from map_transaction order by state desc')
        state_names = [i[0] for i in cursor.fetchall()]  # State Names

        # 2) year

        cursor.execute('select distinct(year) from top_user order by year asc')
        y_values = [i[0] for i in cursor.fetchall()]

        # 3) Quater

        cursor.execute('select distinct(quater) from aggregated_transaction order by quater asc')
        q_values = [i[0] for i in cursor.fetchall()]

        # Year , Quater Combined
        with col3:
            year = st.select_slider('CHOOSE YEAR', options=y_values)
            q = st.select_slider('CHOOSE QUATER', options=q_values)

        with col4:
            state_selected = st.selectbox('CHOOSE STATE', state_names)
            option = st.selectbox("CHOOSE VALUE", ['Transaction Amount', 'Transaction count'])
        with col6:    
            query = "select distinct(transaction_type) from aggregated_transaction"
            cursor.execute(query)
            res = [i[0] for i in cursor.fetchall()]
            type_selected = st.selectbox("Choose Transaction Type", res)
            st.write("")
            order = st.selectbox('CHOOSE ORDER',['Top 10','Bottom 10'])


        #____________________________________________________________________________________________________________________________________________

        #_______________________________________________________________________________________________________________________________________________________________

                                                                      #__________METRICS __________#

        # Metrics 1 : Total Transaction count
        query_1 = f"select sum(count) from map_transaction where year = '{year}' and quater = {q} and state = '{state_selected}' group by state"
        cursor.execute(query_1)
        total_transaction_count = [int(i[0]) for i in cursor.fetchall()]
        col1.metric(label="Transaction count", value=f"{round(((total_transaction_count[0]/100000)/10),2)}M",
                      delta=total_transaction_count[0])
        #________________________________________________________________________________________________________________________________________________________________

        # Metrics 2 : Total Transaction Amount
        query_2 = f"select sum(amount) from map_transaction where year = '{year}' and quater = {q} and state = '{state_selected}' group by state"
        cursor.execute(query_2)
        total_transaction_amount = [int(i[0]) for i in cursor.fetchall()]
        col1.metric(label="Transaction Amount", value=f"{round(((total_transaction_amount[0]/100000)/10),2)}M",
                    delta=total_transaction_amount[0])
        #__________________________________________________________________________________________________________________________________________________________________

        # Metrics 3 : Avg Transaction Amount

        query_1 = f"select avg(amount) from map_transaction where year = '{year}' and quater = {q} and state = '{state_selected}' group by state"
        cursor.execute(query_1)
        total_transaction_count = [int(i[0]) for i in cursor.fetchall()]

        col2.metric(label="Average Transaction Amount", value=f"{round(((total_transaction_count[0]/100000)/10),2)}M",
                    delta=total_transaction_count[0]/100)

        #_________________________________________________________________________________________________________________________________________________
        # Metrics 4 : Avg Transaction count

        query_1 = f"select avg(count) from map_transaction where year = '{year}' and quater = {q} and state = '{state_selected}' group by state"
        cursor.execute(query_1)
        total_transaction_count = [int(i[0]) for i in cursor.fetchall()]

        col2.metric(label="Average Transaction count", value=f"{round(((total_transaction_count[0] / 100000) / 10), 2)}M",
                    delta=total_transaction_count[0] / 100)
        style_metric_cards(
            border_left_color='#08EED2',
            background_color='#e8f4ea', border_color="#0E1117")
#___________________________________________________________________________________________________________________________________________________________________

                                                                      #____________CHARTS___________#
        #______________________________________________________________________________________________________________________________________________________________________

        col1 , col2 = st.columns([10,10])

        # PIE Chart : Total Transaction Type By count

        # Pie 1 : Total Transaction Type By count

        query_3 = f"select  transaction_type , sum(transaction_count)as Total_Transaction from aggregated_transaction where year = {year} and quater = {q} and state = '{state_selected}' group by transaction_type;"
        cursor.execute(query_3)
        total_transaction_type_by_amount = [i for i in cursor.fetchall()]
        df = pd.DataFrame(total_transaction_type_by_amount, columns=['Transaction Type',"Transaction count"])
        pie = px.pie(df, names='Transaction Type', values='Transaction count', hole=0.6,color_discrete_sequence=['#0DF0D4', '#169E8D', '#64F4D6 ', '#B5EEE2 ','#51B9A3 ' ])   # change color
        pie.update_traces(textposition='outside')
        pie.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                          hoverlabel_font_color="#0DF0D4")
        pie.update_layout(paper_bgcolor='#e8f4ea')
        with col1.expander(f"Total Transaction count By Transaction Type In {state_selected} "):

             st.plotly_chart(pie, theme=None, use_container_width=True)
        #______________________________________________________________________________________________________________________________________________________________________

        # Pie 2 : Total Transaction Type By Amount

        query_3 = f"select  transaction_type , sum(transaction_amount)as Total_Transaction from aggregated_transaction where year = {year} and quater = {q} and state = '{state_selected}' group by transaction_type;"
        cursor.execute(query_3)
        total_transaction_type_by_amount = [i for i in cursor.fetchall()]
        df = pd.DataFrame(total_transaction_type_by_amount, columns=['Transaction Type',"Transaction Amount"])
        pie = px.pie(df, names='Transaction Type', values='Transaction Amount', hole=0.6,color_discrete_sequence=['#0DF0D4', '#169E8D', '#64F4D6 ', '#B5EEE2 ','#51B9A3 ' ])   # change color
        pie.update_traces(textposition='outside')
        pie.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                          hoverlabel_font_color="#0DF0D4")
        pie.update_layout(
                paper_bgcolor='#e8f4ea')
        with col2.expander(f"Total Transaction Amount By Transaction Type In {state_selected}"):

             st.plotly_chart(pie, theme=None, use_container_width=True)


        #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        # 3D - Charts :

        # col1, col2, col3 = st.columns([1, 200, 1])
        if option == 'Transaction count':
            query = f"select state , transaction_type , transaction_count,year ,quater from aggregated_transaction where state = '{state_selected}'order by year"
            cursor.execute(query)
            res = [i for i in cursor.fetchall()]
            df = pd.DataFrame(res, columns=['State','Transaction Type', 'Transaction count', 'Year','Quater'])

            fig = px.bar(df, x="Transaction Type", y="Transaction count", animation_frame="Year",hover_name='State',
                         color_discrete_sequence=['#0DF0D4', '#169E8D', '#64F4D6 '])
            fig.update_layout(title_x=1)
            fig.update_layout(
                plot_bgcolor='#FAC898',
                paper_bgcolor='#e8f4ea',
                xaxis_title_font=dict(color='#6739b7'),
                yaxis_title_font=dict(color='#6739b7')
            )
            fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                          hoverlabel_font_color="#0DF0D4")

            with st.expander(f"{option} Of {state_selected} From 2018 To 2022"):
                st.plotly_chart(fig, theme=None, use_container_width=True)
        elif option == 'Transaction Amount':
            query = f"select state , transaction_type , transaction_amount,year ,quater from aggregated_transaction where state = '{state_selected}'order by year"
            cursor.execute(query)
            res = [i for i in cursor.fetchall()]
            df = pd.DataFrame(res, columns=['State','Transaction Type', 'Transaction Amount', 'Year','Quater'])

            fig = px.bar(df, x="Transaction Type", y="Transaction Amount", animation_frame="Year",hover_name='State',
                         color_discrete_sequence=['#0DF0D4', '#169E8D', '#64F4D6 '])
            fig.update_layout(title_x=1)
            fig.update_layout(
                plot_bgcolor='#FAC898',
                paper_bgcolor='#e8f4ea',
                xaxis_title_font=dict(color='#6739b7'),
                yaxis_title_font=dict(color='#6739b7')
            )
            fig.update_traces(hoverlabel=dict(bgcolor="#FFFFFF"),
                          hoverlabel_font_color="#0DF0D4")

            with st.expander(f"{option} Of {state_selected} From 2018 TO 2022"):
                st.plotly_chart(fig, theme=None, use_container_width=True)

        #________________________________________________________________________________________________________________________________________________________________________

        # # Top / Bottom 10 states By transaction Type filter year option
        if option == "Transaction count":
            if order  == 'Top 10':
                query = f"select state , sum(transaction_count) as val,transaction_type   from aggregated_transaction where  year = '{year}' and quater = {q} and transaction_type ='{type_selected}' group by state,transaction_type order by val desc limit 10"
                cursor.execute(query)
                res = [i for i in cursor.fetchall()]
                df = pd.DataFrame(res, columns=['State', 'Transaction count',"Transaction Type"])

                fig = px.bar(df, x="State", y="Transaction count",hover_name='Transaction Type',
                             color_discrete_sequence=['#0DF0D4', '#169E8D', '#64F4D6 '])
                fig.update_layout(title_x=1)
                fig.update_layout(
                    plot_bgcolor='#FAC898',
                    paper_bgcolor='#e8f4ea',
                    xaxis_title_font=dict(color='#6739b7'),
                    yaxis_title_font=dict(color='#6739b7')
                )
                fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                  hoverlabel_font_color="#0DF0D4")

                with st.expander(f"{order} States By {option} In year {year}"):
                    st.plotly_chart(fig, theme=None, use_container_width=True)
            elif order == 'Bottom 10':
                query = f"select state , sum(transaction_count) as val,transaction_type   from aggregated_transaction where  year = '{year}' and quater = {q} and transaction_type ='{type_selected}' group by state,transaction_type order by val limit 10"
                cursor.execute(query)
                res = [i for i in cursor.fetchall()]
                df = pd.DataFrame(res, columns=['State', 'Transaction count', "Transaction Type"])

                fig = px.bar(df, x="State", y="Transaction count", hover_name='Transaction Type',
                             color_discrete_sequence=['#0DF0D4', '#169E8D', '#64F4D6 '])
                fig.update_layout(title_x=1)
                fig.update_layout(
                    plot_bgcolor='#FAC898',
                    paper_bgcolor='#e8f4ea',
                    xaxis_title_font=dict(color='#6739b7'),
                    yaxis_title_font=dict(color='#6739b7')
                )
                fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                  hoverlabel_font_color="#0DF0D4")

                with st.expander(f"{order} States By {option} In year {year}"):
                    st.plotly_chart(fig, theme=None, use_container_width=True)

        elif option == "Transaction Amount":
            if order  == 'Top 10':
                query = f"select state , sum(transaction_amount) as val,transaction_type   from aggregated_transaction where  year = '{year}' and quater = {q} and transaction_type ='{type_selected}' group by state,transaction_type order by val desc limit 10"
                cursor.execute(query)
                res = [i for i in cursor.fetchall()]
                df = pd.DataFrame(res, columns=['State', 'Transaction Amount',"Transaction Type"])

                fig = px.bar(df, x="State", y="Transaction Amount",hover_name='Transaction Type',
                             color_discrete_sequence=['#0DF0D4', '#169E8D', '#64F4D6 '])
                fig.update_layout(title_x=1)
                fig.update_layout(
                    plot_bgcolor='#FAC898',
                    paper_bgcolor='#e8f4ea',
                    xaxis_title_font=dict(color='#6739b7'),
                    yaxis_title_font=dict(color='#6739b7')
                )
                fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                  hoverlabel_font_color="#0DF0D4")

                with st.expander(f"{order} States By {option} In year {year}"):
                    st.plotly_chart(fig, theme=None, use_container_width=True)
            elif order == 'Bottom 10':
                query = f"select state , sum(transaction_amount) as val,transaction_type   from aggregated_transaction where  year = '{year}' and quater = {q} and transaction_type ='{type_selected}' group by state,transaction_type order by val limit 10"
                cursor.execute(query)
                res = [i for i in cursor.fetchall()]
                df = pd.DataFrame(res, columns=['State', 'Transaction Amount', "Transaction Type"])

                fig = px.bar(df, x="State", y="Transaction Amount", hover_name='Transaction Type',
                             color_discrete_sequence=['#0DF0D4', '#169E8D', '#64F4D6 '])
                fig.update_layout(title_x=1)
                fig.update_layout(
                    plot_bgcolor='#FAC898',
                    paper_bgcolor='#e8f4ea',
                    xaxis_title_font=dict(color='#6739b7'),
                    yaxis_title_font=dict(color='#6739b7')
                )
                fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                  hoverlabel_font_color="#0DF0D4")

                with st.expander(f"{order} States By {option} In year {year}"):
                    st.plotly_chart(fig, theme=None, use_container_width=True)
        # #_______________________________________________________________________________________________________________________________________________________________________________________
        st.write("")
        st.write("")
        st.write("")
        st.write("")  # #262730

        colored_header(
            label="CONCLUSION",
            description="Financial and Other services had lower level in Both Transaction count and Amount",
            color_name="blue-green-70",
        )
        #____________________________________________________________________________________________________________________________________________________________________'

        if st.button("Click Me"):
            if option == "Transaction count":
                query = f"select sum(transaction_count) as val,transaction_type   from aggregated_transaction  group by transaction_type order by val "
                cursor.execute(query)
                res = [i for i in cursor.fetchall()]
                df = pd.DataFrame(res, columns=['Transaction count', 'Transaction Type'])

                fig = px.bar(df, x="Transaction Type", y="Transaction count", hover_name='Transaction Type',
                             color_discrete_sequence=['#0DF0D4', '#169E8D', '#64F4D6 '])
                fig.update_layout(title_x=1)
                fig.update_layout(
                    plot_bgcolor='#FAC898',
                    paper_bgcolor='#e8f4ea',
                    xaxis_title_font=dict(color='#6739b7'),
                    yaxis_title_font=dict(color='#6739b7')
                )
                fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                  hoverlabel_font_color="#0DF0D4")

                with st.expander(f"Which Transaction Type  had  lower {option}?"):
                    st.plotly_chart(fig, theme=None, use_container_width=True)
            elif option == 'Transaction Amount':
                query = f"select sum(transaction_amount) as val,transaction_type   from aggregated_transaction  group by transaction_type order by val "
                cursor.execute(query)
                res = [i for i in cursor.fetchall()]
                df = pd.DataFrame(res, columns=['Transaction Amount', 'Transaction Type'])

                fig = px.bar(df, x="Transaction Type", y="Transaction Amount", hover_name='Transaction Type',
                             color_discrete_sequence=['#0DF0D4', '#169E8D', '#64F4D6 '])
                fig.update_layout(title_x=1)
                fig.update_layout(
                    plot_bgcolor='#FAC898',
                    paper_bgcolor='#e8f4ea',
                    xaxis_title_font=dict(color='#6739b7'),
                    yaxis_title_font=dict(color='#6739b7')
                )
                fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                  hoverlabel_font_color="#0DF0D4")

                with st.expander(f"Which  Transaction Type had  lower {option}?"):
                    st.plotly_chart(fig, theme=None, use_container_width=True)


#_______________________________________________________________________________________________________________________________________________________________________________________________
elif selected == "User Brand Analysis":



    col1, col2, col3, col4, col5 = st.columns([8, 5, 5,5,5])

    st.markdown("<style>div.block-container{padding-top:3rem;}</style>", unsafe_allow_html=True)

                                                                             #__________FILTERS___________#

    # 1) Year
    cursor.execute('select distinct(year) from top_user order by year asc')
    y_values = [i[0] for i in cursor.fetchall()]

    # 2) Quater
    cursor.execute('select distinct(quater) from aggregated_transaction order by quater asc')
    q_values = [i[0] for i in cursor.fetchall()]
    with col5:
        year = st.select_slider(':violet[CHOOSE YEAR]', options=y_values)
        q = st.select_slider(':violet[CHOOSE QUATER]', options=q_values)


    # 3) State
    cursor.execute('select distinct(state) from map_transaction order by state desc')
    state_names = [i[0] for i in cursor.fetchall()]  # State Names



    # 4) Brand

    cursor.execute(f"select distinct(brands) from aggregated_user where brands!='Not Mentioned' order by brands  ")
    y_values = [i[0] for i in cursor.fetchall()]

    with col4:
        state_selected = st.selectbox(':violet[CHOOSE STATE]', state_names)
        st.write("")
        st.write("")

#_____________________________________________________________________________________________________________________________________________________________________________

                                    #_____________________________METRICS______________________#

    # State Name

    col1.metric(label = ":violet[STATE]", value = state_selected)

    # metrics 1: Total User Registered:

    query_5 = f"select sum(RegisteredUser) from top_user where state = '{state_selected}'  and year = '{year}'   and quater = {q} group by state;"

    cursor.execute(query_5)

    total_reg_user = [i[0] for i in cursor.fetchall()]

   # with col2.expander(":violet[Total Registered users]"):
    col3.metric(label = ':violet[Total Registered users]',value = f'{math.ceil((total_reg_user[0]/100000)/10)}M', delta =   int(total_reg_user[0]))
    style_metric_cards(
            border_left_color='#08EED2',
            background_color='#e8f4ea', border_color="#0E1117")

    #_____________________________________________________________________________________________________________________________________________________________________

    # Metrices 2 : Appopens

    query_6 = f"select  sum(count) from aggregated_user where state = '{state_selected}' and year = '{year}'  and quater = {q} group by state"
    cursor.execute(query_6)

    total_app_opens = [i[0] for i in cursor.fetchall()]

    col2.metric(label = ':violet[USER APPOPENS]', value = f'{math.ceil((total_app_opens[0]/100000)/10)}M' , delta=int(total_app_opens[0]))
    

    st.write("")
    st.write("")
    st.write("")

   #______________________________________________________________________________________________________________________________________________________________________________

                                                                                        #_______CHARTS_______#


    col1,col2,col3,col4,col5 = st.columns([3,7,2,7,3])
    with col2:
        option = st.selectbox(":violet[Choose Option]", ['App Opens', 'Registered Users'])
    with col4:
        brand = st.selectbox(':violet[CHOOSE BRAND]', options=y_values)
    st.write("")
    st.write("")

    col1,col2 ,col3= st.columns([8,8,8])

    # 1 ) Quater  and appopens and RU in (filter year , state , year )

    if option == "Registered Users":
        query = f"select quater , sum(count) from aggregated_user where year = '{year}' and brands = '{brand}' and state = '{state_selected}'group by quater order by quater asc"
        cursor.execute(query)
        res = [i for i in cursor.fetchall()]
        df = pd.DataFrame(res,columns=['Quater','Registered Users'])
        fig = px.bar(df, x="Quater", y="Registered Users")
        fig.update_layout(title_x=1)
        fig.update_layout(
            plot_bgcolor='#FAC898',
            paper_bgcolor='#e8f4ea',
            xaxis_title_font=dict(color='#6739b7'),
            yaxis_title_font=dict(color='#6739b7')
        )
        fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                          hoverlabel_font_color="#F500E6")
        fig.update_traces(marker_color='#d450b0')
        with col1.expander(f"{brand} brand in {state_selected} {option} Over The Quaters {year} "):
             st.plotly_chart(fig, theme=None, use_container_width=True)

    elif option == "App Opens":
        query = f"select quater , sum(count) from aggregated_user where year = '2021' and brands = 'Vivo' and state = 'tamil-nadu' group by quater order by quater asc"
        cursor.execute(query)
        res = [i for i in cursor.fetchall()]
        df = pd.DataFrame(res,columns=['Quater','App Opens'])
        pie = px.pie(df, names='Quater', values='App Opens', hole=0.7,
                     color_discrete_sequence=['#6a0578', '#a7269e', '#d450b0', '#eb8adb',
                                              '#CA8DE1'])  # change color

        pie.update_traces(hoverlabel=dict(bgcolor="#FAC898"),
                          hoverlabel_font_color="#F500E6",
                          textposition='outside')
        pie.update_layout(paper_bgcolor='#e8f4ea')

        with col1.expander(f"{brand} brand in {state_selected} {option} Over The Quaters of {year}"):
             st.plotly_chart(pie, theme=None, use_container_width=True)

    #______________________________________________________________________________________________________________________________________________________________________

    # 2) brand in RU /AP  over the year

    if option == "Registered Users":
        query = f"select year , sum(count) from aggregated_user where  brands = '{brand}' and state = '{state_selected}' group by year order by year  asc"
        cursor.execute(query)
        res = [i for i in cursor.fetchall()]
        df = pd.DataFrame(res,columns=['Year','Registered Users'])
        fig = px.line(df, x="Year", y="Registered Users",markers='D')
        fig.update_layout(title_x=1)
        fig.update_layout(
            plot_bgcolor='#FAC898',
            paper_bgcolor='#e8f4ea',
            xaxis_title_font=dict(color='#6739b7'),
            yaxis_title_font=dict(color='#6739b7')
        )
        fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                          hoverlabel_font_color="#F500E6")
        fig.update_traces(marker_color='#d450b0')
        with col2.expander(f"{brand} brand in {state_selected} {option} Over The Years "):
             st.plotly_chart(fig, theme=None, use_container_width=True)
             st.write('')
             st.write('')

    elif option == "App Opens":
        query = f"select year , sum(count) from aggregated_user where  brands = 'Vivo' and state = 'tamil-nadu' group by year order by year  asc"
        cursor.execute(query)
        res = [i for i in cursor.fetchall()]
        df = pd.DataFrame(res,columns=['Year','App Opens'])
        fig = px.line(df, x="Year", y="App Opens", markers='D')
        fig.update_layout(title_x=1)
        fig.update_layout(
            plot_bgcolor='#FAC898',
            paper_bgcolor='#e8f4ea',
            xaxis_title_font=dict(color='#6739b7'),
            yaxis_title_font=dict(color='#6739b7')
        )
        fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                          hoverlabel_font_color="#F500E6")
        fig.update_traces(marker_color='#d450b0')

        with col2.expander(f"{brand} brand in {state_selected} {option} Over The Year"):
             st.plotly_chart(fig, theme=None, use_container_width=True)





    # 3) State - wise Brand Engagement of Ao/Ru
    if option == "Registered Users":
        query = f"select state , sum(count) as val from aggregated_user where year = '{year}' and quater = {q} and brands = '{brand}' group by state order by val desc limit 10;"
        cursor.execute(query)
        res = [i for i in cursor.fetchall()]
        df = pd.DataFrame(res,columns=['State','Registered Users'])

        fig = px.bar(df, x="State", y="Registered Users")
        fig.update_layout(title_x=1)
        fig.update_layout(
            plot_bgcolor='#FAC898',
            paper_bgcolor='#e8f4ea',
            xaxis_title_font=dict(color='#6739b7'),
            yaxis_title_font=dict(color='#6739b7')
        )
        fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                          hoverlabel_font_color="#F500E6")
        fig.update_traces(marker_color='#d450b0')
        with col3.expander(f"{brand} Brand {option} Over The Year {year} In India States "):
            st.plotly_chart(fig, theme=None, use_container_width=True)
    elif option == 'App Opens':

        query = f"select state , sum(count) as val from aggregated_user where year = '{year}' and quater = {q} and brands = '{brand}' group by state order by val desc limit 10;"
        cursor.execute(query)
        res = [i for i in cursor.fetchall()]
        df = pd.DataFrame(res, columns=['State', 'App opens'])

        fig = px.bar(df, x="State", y="App opens")
        fig.update_layout(title_x=1)
        fig.update_layout(
            plot_bgcolor='#FAC898',
            paper_bgcolor='#e8f4ea',
            xaxis_title_font=dict(color='#6739b7'),
            yaxis_title_font=dict(color='#6739b7')
        )
        fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                          hoverlabel_font_color="#F500E6")
        fig.update_traces(marker_color='#d450b0')
        with col3.expander(f"{brand} Brand {option} Over The Year {year} In India States "):
            st.plotly_chart(fig, theme=None, use_container_width=True)
    st.write("")
    st.write('')
    st.write("")
    st.write('')
    st.write("")
    st.write('')
   #_____________________________________________________________________________________________________________________________________________________________
    col1,col2,col3 = st.columns([20,100,1])
    col2.header(":violet[Top 10 Brands By Registered Users in State (Particular Year)]")
    st.write("")

    # 4) Top 10 brand in each state

    col1, col2, col3 = st.columns([1, 100, 1])
    query = f"select brands , sum(count) as val  from aggregated_user where year = '{year}' and quater = {q} and state = '{state_selected}' group by brands order by val desc limit 10"
    cursor.execute(query)
    res = [i for i in cursor.fetchall()]
    df = pd.DataFrame(res,columns=['Brand','Registered Users'])

    fig = px.bar(df, x="Brand", y="Registered Users")
    fig.update_layout(title_x=1)
    fig.update_layout(
        plot_bgcolor='#FAC898',
        paper_bgcolor='#e8f4ea',
        xaxis_title_font=dict(color='#6739b7'),
        yaxis_title_font=dict(color='#6739b7')
    )
    fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                      hoverlabel_font_color="#F500E6")
    fig.update_traces(marker_color='#d450b0')
    with col2.expander(f"Top 10 Brands By Registered Users In  {state_selected} In The Year  {year} And {q}th Quater  "):
        st.plotly_chart(fig, theme=None, use_container_width=True)
    st.write("")
    st.write("")
    st.write("")


    #__________________________________________________________________________________________________________________________________________________________________________________________

    col1, col2, col3 = st.columns([20, 100, 1])
    col2.header(":violet[Top 10 Brands By Registered Users in State  From 2018 to 2022]")
    st.write("")

    # 4) Top 10 brand in each state

    col1, col2, col3 = st.columns([1, 100, 1])
    query = f"select year, brands , sum(count) as val  from aggregated_user where  state = '{state_selected}'  and brands != 'Not Mentioned' group by brands , year order by  year "
    cursor.execute(query)
    res = [i for i in cursor.fetchall()]
    df = pd.DataFrame(res, columns=['Year','Brand', 'Registered Users'])

    fig = px.bar(df, x="Brand", y="Registered Users",animation_frame="Year", color_discrete_sequence=[ '#eb8adb','#CA8DE1','#a7269e' ])
    fig.update_layout(title_x=1)
    fig.update_layout(
        plot_bgcolor='#FAC898',
        paper_bgcolor='#e8f4ea',
        xaxis_title_font=dict(color='#6739b7'),
        yaxis_title_font=dict(color='#6739b7')
    )
    fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                      hoverlabel_font_color="#F500E6")
    fig.update_traces(marker_color='#d450b0')
    with col2.expander(f"Top 10 Brands By Registered Users In  {state_selected} From 2018 to 2022"):
        st.plotly_chart(fig, theme=None, use_container_width=True)


    #____________________________________________________________________________________________________
#_______________________________________________________________________________________________________________________________________________________________________________________________
elif selected == "SDP Analysis":

    #with st.sidebar:
    selected_1 = option_menu(
            menu_title="",
            options=['Choose Option', 'Transaction', "User"],
            icons=['', 'coin', 'person-circle'],
            default_index=0,
             styles={
        "container": {"padding": "0!important", "background-color": "#FFFFFF"},
        "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#CD87CF"},
        "nav-link-selected": {"background-color": "#FE6862"}}
            )

    if selected_1 == 'Transaction':

        # info :
        col1, col2, col3, = st.columns([4, 10, 1])
        col2.title(':violet[State Transactions Analysis]')
        col2.markdown("<style>div.block-container{padding-top:2rem;}</style>", unsafe_allow_html=True)

    #_____________________________________________________________________________________________________________________________

                                                         #____________FILTERS___________#

        col1,col2,col3,col4,col5 = st.columns([7,7,7,7,7])

        # 1) Year
        cursor.execute('select distinct(year) from top_user order by year asc')
        y_values = [i[0] for i in cursor.fetchall()]

        # 2) Quater
        cursor.execute('select distinct(quater) from aggregated_transaction order by quater asc')
        q_values = [i[0] for i in cursor.fetchall()]


        # 3) State
        cursor.execute('select distinct(state) from map_transaction order by state desc')
        state_names = [i[0] for i in cursor.fetchall()]  # State Names

        col5.write("")
        with col1:
            st.write("")
            state_selected = st.selectbox(':violet[CHOOSE STATE]', state_names)
        with col2:
            st.write("")
            year = st.select_slider(':violet[CHOOSE YEAR]', options=y_values)
        with col3:   
            st.write("")
            q = st.select_slider(':violet[CHOOSE QUATER]', options=q_values)
        with col4:    
            st.write("")
            order = st.selectbox(":violet[CHOOSE ORDER]",['Top','Bottom'])


        #_________________________________________________________________________________________________________________________________

                                                          #________________METRICS__________________#

        # 1) Metric  : Top State By Amount
        query = f"select state , sum(transaction_amount) as val from top_transaction  where year= '{year}' and quater= {q} group by state order by val desc limit 1;"
        cursor.execute(query)
        res = [i[0] for i in cursor.fetchall()]
        cursor.execute(query)
        res1=[i[1] for i in cursor.fetchall()]
        with col1:
            st.metric(label = ":violet[Top State By Amount]",value=res[0],delta=f"{round(((res1[0]/100000)/10),2)}M")

        #________________________________________________________________________________________________________________________________________________________________________________________

        # 2) Metric  : Top State By count

        Query = f"select state , sum(transaction_count) as val from top_transaction where year= '{year}' and quater= {q} group by state order by val desc limit 1;"
        cursor.execute(Query)
        res = [i[0] for i in cursor.fetchall()]    # Name
        cursor.execute(Query)
        res1 = [i[1] for i in cursor.fetchall()]   # count
        #print (len(res1))
        with col2:
            st.metric(label = ":violet[Top State By count]", value=res[0], delta=f"{round(((res1[0]/100000)/10),2)}M")

        #______________________________________________________________________________________________________________________________________________________________________________________________

        # 3) Metric  : Current State By Amount

        Query_1 = f"select state , sum(transaction_amount) as val from top_transaction where year= '{year}' and quater = {q} and state = '{state_selected}' group by state;"

        cursor.execute(Query_1)
        res = [i[0] for i in cursor.fetchall()]  # Name
        cursor.execute(Query_1)
        res1 = [i[1] for i in cursor.fetchall()]  # count
        with col3:
            st.metric(label = ":violet[Current State By Amount]", value=res[0], delta=f"{round(((res1[0]/100000)/10),2)}M")

        #_______________________________________________________________________________________________________________________________________________________________________________________________________

        # 4) Metric  : Current State By count

            Query_1 = f"select state , sum(transaction_count) as val from top_transaction where year= '{year}' and quater = {q} and state = '{state_selected}' group by state;"

            cursor.execute(Query_1)
            res = [i[0] for i in cursor.fetchall()]  # Name
            cursor.execute(Query_1)
            res1 = [i[1] for i in cursor.fetchall()]  # count
            with col4:
                st.metric(label = ":violet[Current State By count]", value=res[0], delta=f"{round(((res1[0]/100000)/10),2)}M")
                style_metric_cards(
            border_left_color='#08EED2',
            background_color='#e8f4ea', border_color="#0E1117")



        #____________________________________________________________________________________________________________________________________________________________________________________________________


                                                                                      #___________CHARTS___________#

        col1,col2 = st.columns([7,7])

        #_____________________________________________________________________________________________________________________________________________________________________________

        # 1) Bar : Top/Bottom  1o States By count

        if order == 'Bottom':
            query=f"select state , sum(transaction_count) as val from top_transaction where year= '{year}' and quater= {q} group by state order by val asc limit 10;"
            cursor.execute(query)
            res = [i for i in cursor.fetchall()]
            df = pd.DataFrame(res, columns=['State', 'Transaction count'])
            fig = px.bar(df, x="State", y="Transaction count")
            fig.update_layout(title_x=1)
            fig.update_layout(
                plot_bgcolor='#FAC898',
                paper_bgcolor='#e8f4ea',
                xaxis_title_font=dict(color='#6739b7'),
                yaxis_title_font=dict(color='#6739b7')
            )
            fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                              hoverlabel_font_color="#F500E6")
            fig.update_traces(marker_color='#d450b0')
            with col1.expander("Bottom 10 State By Transaction count"):
                st.plotly_chart(fig, theme=None, use_container_width=True)

        elif order == "Top":
                query = f"select state , sum(transaction_count) as val from top_transaction where year= '{year}' and quater= {q} group by state order by val desc limit 10;"
                cursor.execute(query)
                res = [i for i in cursor.fetchall()]
                df = pd.DataFrame(res, columns=['State', 'Transaction count'])
                fig = px.bar(df, x="State", y="Transaction count")
                fig.update_layout(title_x=1)
                fig.update_layout(
                    plot_bgcolor='#FAC898',
                    paper_bgcolor='#e8f4ea',
                    xaxis_title_font=dict(color='#6739b7'),
                    yaxis_title_font=dict(color='#6739b7')
                )
                fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                  hoverlabel_font_color="#F500E6")
                fig.update_traces(marker_color='#d450b0')
                with col1.expander("Top 10 State By Transaction count"):
                    st.plotly_chart(fig, theme=None, use_container_width=True)

        #____________________________________________________________________________________________________________________________________________________________________________________________________

        # 1) Bar : Top/Bottom  1o States By count

        if order == 'Bottom':
            query=f"select state , sum(transaction_amount) as val from top_transaction where year= '{year}' and quater= {q} group by state order by val asc limit 10;"
            cursor.execute(query)
            res = [i for i in cursor.fetchall()]
            df = pd.DataFrame(res, columns=['State', 'Transaction Amount'])
            fig = px.bar(df, x="State", y="Transaction Amount")
            fig.update_layout(title_x=1)
            fig.update_layout(
                plot_bgcolor='#FAC898',
                paper_bgcolor='#e8f4ea',
                xaxis_title_font=dict(color='#6739b7'),
                yaxis_title_font=dict(color='#6739b7')
            )
            fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                              hoverlabel_font_color="#F500E6")
            fig.update_traces(marker_color='#d450b0')
            with col2.expander("Bottom 10 State By Transaction Amount"):
                st.plotly_chart(fig, theme=None, use_container_width=True)

        elif order == "Top":
                query = f"select state , sum(transaction_amount) as val from top_transaction where year= '{year}' and quater= {q} group by state order by val desc limit 10;"
                cursor.execute(query)
                res = [i for i in cursor.fetchall()]
                df = pd.DataFrame(res, columns=['State', 'Transaction Amount'])
                fig = px.bar(df, x="State", y="Transaction Amount")
                fig.update_layout(title_x=1)
                fig.update_layout(
                    plot_bgcolor='#FAC898',
                    paper_bgcolor='#e8f4ea',
                    xaxis_title_font=dict(color='#6739b7'),
                    yaxis_title_font=dict(color='#6739b7')
                )
                fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                  hoverlabel_font_color="#F500E6")
                fig.update_traces(marker_color='#d450b0')
                with col2.expander("Top 10 State By Transaction Amount"):
                    st.plotly_chart(fig, theme=None, use_container_width=True)
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")


    #_____________________________________________________________________________________________________________________________________________________________________________________________________________________________

                                                                                  #_______DISTRICTS-WISE ANALYSIS___________#

        # info :
        col1, col2, col3, = st.columns([4, 10, 1])
        col2.title(':violet[District Transactions Analysis]')
        col2.markdown("<style>div.block-container{padding-top:2rem;}</style>", unsafe_allow_html=True)

        #___________________________________________________________________________________________________________________________________________________________________________________________________

                                                                         #__________FILTERS____________#\

        col1, col2, col3, col4, col5 = st.columns([7, 7, 7, 7, 7])


        # 1) Year
        cursor.execute('select distinct(year) from top_user order by year asc')
        y_values = [i[0] for i in cursor.fetchall()]

        # 2) Quater
        cursor.execute('select distinct(quater) from aggregated_transaction order by quater asc')
        q_values = [i[0] for i in cursor.fetchall()]

        # 3) State
        cursor.execute('select distinct(district) from top_transaction order by district;')
        dist_names = [i[0] for i in cursor.fetchall()]  # dist Names

        col5.write("")
        with col1:
            st.write("")
            dist_selected = st.selectbox(':violet[CHOOSE DISTRICT]', dist_names)
        with col2:
            st.write("")
            year = st.select_slider(':violet[YEAR]', options=y_values)
        with col3:    
            st.write("")
            q = st.select_slider(':violet[QUATER]', options=q_values)
        with col4:    
            st.write("")
            order = st.selectbox(":violet[ORDER]", ['Top', 'Bottom'])

        #_________________________________________________________________________________________________________________________________________________________________________________________________________________

                                                                          #_____________METRICS___________#

        # 1) Metric  : Top District By Amount
        query = f"select district , sum(transaction_amount) as val from top_transaction  where year= '{year}' and quater= {q} group by district order by val desc limit 1;"
        cursor.execute(query)
        res = [i[0] for i in cursor.fetchall()]
        cursor.execute(query)
        res1 = [i[1] for i in cursor.fetchall()]
        with col1:
            st.metric(label = ":violet[Top District By Amount]", value=res[0], delta=f"{round(((res1[0]/100000)/10),2)}M")

        # ________________________________________________________________________________________________________________________________________________________________________________________

        # 2) Metric  : Top district  By count

        Query = f"select district , sum(transaction_count) as val from top_transaction  where year= '{year}' and quater= {q} group by district order by val desc limit 1;"
        cursor.execute(Query)
        res = [i[0] for i in cursor.fetchall()]  # Name
        cursor.execute(Query)
        res1 = [i[1] for i in cursor.fetchall()]  # count
        with col2:
            st.metric(label = ":violet[Top District By count]", value=res[0], delta=f"{round(((res1[0]/100000)/10),2)}M")

        # ______________________________________________________________________________________________________________________________________________________________________________________________

        # 3) Metric  : Current District By Amount

        #Query_1 = f"select  district, sum(transaction_amount) as val from top_transaction  where year= '{year}' and quater = {q} and  district = '{dist_selected}' group by  district;"

        #cursor.execute(Query_1)
        #res = [i[0] for i in cursor.fetchall()]  # Name

        #cursor.execute(Query_1)
        #res1 = [i[1] for i in cursor.fetchall()]  # amount
        #with col3:
         #   st.metric(label = ":violet[Current District By Amount]", value=res[0], delta=f"{round(((res1[0]/100000)/10),2)}M")

        # _____________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

        # # 4) Metric  : Current district By count

        #Query_1 = f"select  district, sum(transaction_count) as val from top_transaction  where year= '{year}' and quater = {q} and  district = '{dist_selected}' group by  district;"

        #cursor.execute(Query_1)
        #res = [i[0] for i in cursor.fetchall()]  # Name
        #cursor.execute(Query_1)
        #res1 = [i[1] for i in cursor.fetchall()]  # count
        #with col4:
         #   st.metric(label = ":violet[Current State By count]", value=res[0], delta=f"{round(((res1[0]/100000)/10),2)}M")

        #_________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________



                                                                                      #___________CHARTS___________#

        col1,col2 = st.columns([7,7])

        #_____________________________________________________________________________________________________________________________________________________________________________

        # 1) Bar : Top/Bottom  1o districts By count

        if order == 'Bottom':
            query=f"select district , sum(transaction_count) as val from top_transaction where year= '{year}' and quater= {q} group by district order by val asc limit 10;"
            cursor.execute(query)
            res = [i for i in cursor.fetchall()]
            df = pd.DataFrame(res, columns=['District', 'Transaction count'])
            fig = px.bar(df, x="District", y="Transaction count")
            fig.update_layout(title_x=1)
            fig.update_layout(
                plot_bgcolor='#FAC898',
                paper_bgcolor='#e8f4ea',
                xaxis_title_font=dict(color='#6739b7'),
                yaxis_title_font=dict(color='#6739b7')
            )
            fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                              hoverlabel_font_color="#F500E6")
            fig.update_traces(marker_color='#d450b0')
            with col1.expander("Bottom 10 District By Transaction count"):
                st.plotly_chart(fig, theme=None, use_container_width=True)

        elif order == "Top":
                query = f"select district, sum(transaction_count) as val from top_transaction where year= '{year}' and quater= {q} group by district order by val desc limit 10;"
                cursor.execute(query)
                res = [i for i in cursor.fetchall()]
                df = pd.DataFrame(res, columns=['District', 'Transaction count'])
                fig = px.bar(df, x="District", y="Transaction count")
                fig.update_layout(title_x=1)
                fig.update_layout(
                    plot_bgcolor='#FAC898',
                    paper_bgcolor='#e8f4ea',
                    xaxis_title_font=dict(color='#6739b7'),
                    yaxis_title_font=dict(color='#6739b7')
                )
                fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                  hoverlabel_font_color="#F500E6")
                fig.update_traces(marker_color='#d450b0')
                with col1.expander("Top 10 District By Transaction count"):
                    st.plotly_chart(fig, theme=None, use_container_width=True)

        #____________________________________________________________________________________________________________________________________________________________________________________________________

        # 2) Bar : Top/Bottom  1o districts By amount

        if order == 'Bottom':
            query=f"select district , sum(transaction_amount) as val from top_transaction where year= '{year}' and quater= {q} group by district  order by val asc limit 10;"
            cursor.execute(query)
            res = [i for i in cursor.fetchall()]
            df = pd.DataFrame(res, columns=['District', 'Transaction Amount'])
            fig = px.bar(df, x="District", y="Transaction Amount")
            fig.update_layout(title_x=1)
            fig.update_layout(
                plot_bgcolor='#FAC898',
                paper_bgcolor='#e8f4ea',
                xaxis_title_font=dict(color='#6739b7'),
                yaxis_title_font=dict(color='#6739b7')
            )
            fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                              hoverlabel_font_color="#F500E6")
            fig.update_traces(marker_color='#d450b0')
            with col2.expander("Bottom 10 Districts By Transaction Amount"):
                st.plotly_chart(fig, theme=None, use_container_width=True)

        elif order == "Top":
                query = f"select district , sum(transaction_amount) as val from top_transaction where year= '{year}' and quater= {q} group by district order by val desc limit 10;"
                cursor.execute(query)
                res = [i for i in cursor.fetchall()]
                df = pd.DataFrame(res, columns=['District', 'Transaction Amount'])
                fig = px.bar(df, x="District", y="Transaction Amount")
                fig.update_layout(title_x=1)
                fig.update_layout(
                    plot_bgcolor='#FAC898',
                    paper_bgcolor='#e8f4ea',
                    xaxis_title_font=dict(color='#6739b7'),
                    yaxis_title_font=dict(color='#6739b7')
                )
                fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                  hoverlabel_font_color="#F500E6")
                fig.update_traces(marker_color='#d450b0')
                with col2.expander("Top 10 District By Transaction Amount"):
                    st.plotly_chart(fig, theme=None, use_container_width=True)
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        #_________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

                                                                                                      # _______PINCODE TRANSACTION ANALYSIS___________#


        col1, col2, col3, = st.columns([4, 10, 1])
        col2.title(':violet[Pincode Transactions Analysis]')

        st.write("")
        st.write("")

        #______________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

                                                                                                        #_____________FILTER_____________________#

        col1, col2, col3, col4, col5 = st.columns([7, 7, 7, 7, 7])

        # 1) Year
        cursor.execute('select distinct(year) from top_user order by year asc')
        y_values = [i[0] for i in cursor.fetchall()]

        # 2) Quater
        cursor.execute('select distinct(quater) from aggregated_transaction order by quater asc')
        q_values = [i[0] for i in cursor.fetchall()]

        with col3:
            st.write("")
            year = st.select_slider(':violet[SELECT YEAR]', options=y_values)
        with col4:    
            st.write("")
            q = st.select_slider(':violet[SELECT QUATER]', options=q_values)
        with col2:

            st.write("")
            order = st.selectbox(":violet[SELECT ORDER]", ['Top', 'Bottom'])

       #______________________________________________________________________________________________________________________________________________________________________________________________________________________________
                                                                                              #____________CHARTS____________#


        col1,col2 = st.columns([7,7])


         # 1)  Top 10 Pincode By Transaction Amount


        if order == "Top":
            query_pin = f"select district, sum(transaction_amount) as val from top_transaction where year = '{year}' and quater = {q} group by  district order by val desc limit 10;"
            cursor.execute(query_pin)
            res = [i for i in cursor.fetchall()]
            df = pd.DataFrame(res, columns=['Pincode', 'Transaction Amount'])
            pie = px.pie(df, names='Pincode', values='Transaction Amount', hole=0.7,
                         color_discrete_sequence=['#6a0578', '#a7269e', '#d450b0', '#eb8adb',
                                                  '#CA8DE1'])  # change color
            pie.update_traces(textposition='outside')
            pie.update_layout(paper_bgcolor='#e8f4ea')
            with col1.expander("Top 10 Pincode By Transaction Amount"):
                 st.plotly_chart(pie, theme=None, use_container_width=True)

        elif order == "Bottom":
            query_pin = f"select district, sum(transaction_amount) as val from top_transaction where year = '{year}' and quater = {q} group by  district order by val asc limit 10;"
            cursor.execute(query_pin)
            res = [i for i in cursor.fetchall()]
            df = pd.DataFrame(res, columns=['Pincode', 'Transaction Amount'])
            pie = px.pie(df, names='Pincode', values='Transaction Amount', hole=0.7,
                         color_discrete_sequence=['#6a0578', '#a7269e', '#d450b0', '#eb8adb',
                                                  '#CA8DE1'])  # change color
            pie.update_traces(textposition='outside')
            pie.update_layout(paper_bgcolor='#e8f4ea')
            with col1.expander("Bottom 10 Pincode By Transaction Amount"):
               st.plotly_chart(pie, theme=None, use_container_width=True)


        #_____________________________________________________________________________________________________________________________________________________________________________________________________________________________________

        # 2) Top 10 Pincode By Transaction count

        if order == 'Top':
            query_pin_1 = f"select district, sum(transaction_count) as val from top_transaction where year = '{year}' and quater = {q} group by  district order by val desc limit 10;"
            cursor.execute(query_pin_1)
            res = [i for i in cursor.fetchall()]
            df = pd.DataFrame(res, columns=['Pincode', 'Transaction count'])
            pie = px.pie(df, names='Pincode', values='Transaction count', hole=0.7,
                         color_discrete_sequence=['#6a0578', '#a7269e', '#d450b0', '#eb8adb',
                                                  '#CA8DE1'])  # change color
            pie.update_traces(textposition='outside')
            pie.update_layout(paper_bgcolor='#e8f4ea')
            with col2.expander("Top 10 Pincode By Transaction count"):
                 st.plotly_chart(pie, theme=None, use_container_width=True)

        if order == 'Bottom':
            query_pin_1 = f"select district, sum(transaction_count) as val from top_transaction where year = '{year}' and quater = {q} group by  district order by val asc limit 10;"
            cursor.execute(query_pin_1)
            res = [i for i in cursor.fetchall()]
            df = pd.DataFrame(res, columns=['Pincode', 'Transaction count'])
            pie = px.pie(df, names='Pincode', values='Transaction count', hole=0.7,
                         color_discrete_sequence=['#6a0578', '#a7269e', '#d450b0', '#eb8adb',
                                                  '#CA8DE1'])  # change color
            pie.update_traces(textposition='outside')
            pie.update_layout(paper_bgcolor='#e8f4ea')
            with col2.expander("Bottom 10 Pincode By Transaction count"):
                  st.plotly_chart(pie, theme=None, use_container_width=True)

        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        #_________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________


                                                                         #_____________SDP Transaction Amount Concentration________________________#

        col1, col2, col3, = st.columns([2, 10, 1])

        col2.title(':violet[SDP Transaction Amount Concentration Analysis]')

        st.write("")
        st.write("")

        #___________________________________________________________________________________________________________________________________________________________________________________________________________________________________


                                                                                        #_______________FILTERS___________________#

        col1, col2, col3, col4, col5 = st.columns([7, 7, 7, 7, 7])

        # 1) Year
        cursor.execute('select distinct(year) from top_user order by year asc')
        y_values = [i[0] for i in cursor.fetchall()]

        # 2) Quater
        cursor.execute('select distinct(quater) from aggregated_transaction order by quater asc')
        q_values = [i[0] for i in cursor.fetchall()]

        with col4:
            st.write("")
            year = st.select_slider(':violet[Pick YEAR]', options=y_values)
            st.write("")
        with col2:
            q = st.select_slider(':violet[Pick QUATER]', options=q_values)

        # with col2.expander(":violet[FILTER]"):
        #     st.write("")
        #     order = st.selectbox(":violet[ ORDER]", ['Top', 'Bottom'])

       #__________________________________________________________________________________________________________________________________________________________________________________________________________________________________

                                                                                                                      #__________CHARTS_______________#


        col1,col2,col3 = st.columns([7,7,7])

                                                                                                                    #_________State_Level__________#

        querys_top = f"select sum(transaction_amount) as val from top_transaction where year = '{year}' and quater = {q}  group by state order by val desc limit 10;"
        cursor.execute(querys_top)
        res = [i for i in cursor.fetchall()]
        df_1 = pd.DataFrame(res, columns=['Amount Top'])

        querys_bottom = f"select sum(transaction_amount) as val from top_transaction where year = '{year}' and quater = {q}  group by state order by val asc limit 10;"

        cursor.execute(querys_bottom)
        res = [i for i in cursor.fetchall()]
        df_2 = pd.DataFrame(res, columns=['Amount Bottom'])

        state_last = {"Names": [], 'value': []}
        state_last['Names'].append("Top 10 States")
        state_last['Names'].append("Other States")

        state_last['value'].append(int(sum(df_1['Amount Top'])))
        state_last['value'].append(int(sum(df_2['Amount Bottom'])))

        df = pd.DataFrame(state_last)

        pie = px.pie(df, names='Names', values='value', labels={'Names': 'State Type', 'value': 'Transaction Amount'},
                     hole=0.7,
                     color_discrete_sequence=['#a7269e', '#e35be1'])  # change color
        pie.update_traces(textposition='outside')
        pie.update_layout(paper_bgcolor='#e8f4ea')

        with col1.expander("TOP 10 STATES :orange[Vs]  OTHER STATES"):
            st.plotly_chart(pie, theme=None, use_container_width=True)

        #_________________________________________________________________________________________________________________________________________________________________________________________________________________________________

                                                                                                              #______________Districts Level__________#

            # Metrics 3 : District Transaction Concentration :

        query_top = f"select sum(transaction_amount) as val  from top_transaction where year = '{year}' and quater = {q} group by district order by val desc limit 10;"
        cursor.execute(query_top)
        res = [i for i in cursor.fetchall()]
        df = pd.DataFrame(res, columns=['Amount Top'])
        last = {'Names': [], 'value': []}
        last['Names'].append("Top 10 Districts")
        last['value'].append(int(sum(df['Amount Top'])))

        query_bottom = f"select sum(transaction_amount) as val from top_transaction where year = '{year}' and quater = {q}  group by district order by val asc limit 10;"
        cursor.execute(query_bottom)
        res = [i for i in cursor.fetchall()]
        df = pd.DataFrame(res, columns=['Amount Bottom'])


        last['Names'].append("Other Districts")
        last['value'].append(int(sum(df['Amount Bottom'])))

        df = pd.DataFrame(last)  # '#a7269e', '#d450b0', '#eb8adb',
        pie = px.pie(df, names='Names', values='value', hole=0.7,
                     labels={'Names': 'District Type', 'value': 'Transaction Amount'},
                     color_discrete_sequence=['#a7269e', '#e35be1'])  # change color
        pie.update_traces(textposition='outside')
        pie.update_layout(paper_bgcolor='#e8f4ea')

        with col2.expander("TOP 10 DISTRICTS :orange[Vs]  OTHER DISTRICTS"):
              st.plotly_chart(pie, theme=None, use_container_width=True)

        #______________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

                                                                                                   #________________________#

        query_top = f"select sum(transaction_amount) as val  from top_transaction where year = '{year}' and quater = {q} group by state order by val desc limit 10;"
        cursor.execute(query_top)
        res = [i for i in cursor.fetchall()]
        df = pd.DataFrame(res, columns=['Amount Top'])
        last = {'Names': [], 'value': []}
        last['Names'].append("Top 10 Pincodes")
        last['value'].append(int(sum(df['Amount Top'])))

        query_bottom = f"select sum(transaction_amount) as val  from top_transaction where year = '{year}' and quater = {q} group by state order by val asc limit 10;"
        cursor.execute(query_bottom)
        res = [i for i in cursor.fetchall()]
        df = pd.DataFrame(res, columns=['Amount Bottom'])

        last['Names'].append("Other Pincodes")
        last['value'].append(int(sum(df['Amount Bottom'])))

        df = pd.DataFrame(last)
        pie = px.pie(df, names='Names', values='value', hole=0.7,
                     labels={'Names': 'Pincode Type', 'value': 'Transaction Amount'},
                     color_discrete_sequence=['#a7269e', '#e35be1'])  # change color
        pie.update_traces(textposition='outside')
        pie.update_layout(paper_bgcolor='#e8f4ea')

        with col3.expander("TOP 10 PINCODES :orange[Vs]  OTHER PINCODES"):
            st.plotly_chart(pie, theme=None, use_container_width=True)

        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
    #_______________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________


                                                               #___________________Top 10 DP In State By Transaction Amount_______________#

        col1,col2,col3 = st.columns([2,8,1])


        col2.title(':violet[Top 10 DP In State By Transaction Amount]')
        st.write("")
        st.write("")

    #_________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
                                                                                          #___________FILTERS_______________#

        col1, col2, col3 ,col4, col5 = st.columns([5,5, 5,5,5])

    #_____________________________________________________________________________________________________________________________________________________
    # 1) State
        query="select distinct(state) from top_transaction order by state desc"
        cursor.execute(query)
        res = [i[0] for i in cursor.fetchall()]
        with col1:
            state_selected =  st.selectbox(":violet[PICK STATE]",res)

    # 2) Districts and Pincodes

        with col2:
            vary = st.selectbox(':violet[PICK OPTION]',['District','Pincode'])

    # 3) Amount and count

        with col3:
            Choice = st.selectbox(':violet[PICK CHOICE]', ['Amount', 'count'])

    # 4) Year and Quater

        # 1) Year
        cursor.execute('select distinct(year) from top_user order by year asc')
        y_values = [i[0] for i in cursor.fetchall()]

        # 2) Quater
        cursor.execute('select distinct(quater) from aggregated_transaction order by quater asc')
        q_values = [i[0] for i in cursor.fetchall()]

        with col4:
            year = st.select_slider(":violet[Choose Year]", options=y_values)
            st.write("")
            q = st.select_slider(':violet[Choose Quater]', options=q_values)
        st.write("")
        st.write('')

    # 5) Top / Bottom 10

        with col5:
            order = st.selectbox(":violet[Choose Order]",['desc','asc'])

#____________________________________________________________________________________________________________________________________________________________________________________________________

                                                                                           #_____CONDITION METRICS_____#
        col1,col2,col3  = st.columns([1,100,1])

        if vary == "District":
                 if Choice == "Amount":
                     query_1 = f"select district , sum(transaction_amount) as val from top_transaction where year = '{year}' and quater = {q} and state = '{state_selected}' group by district order by val {order} limit 10;"
                     cursor.execute(query_1)
                     res = [i for i in cursor.fetchall()]
                     df = pd.DataFrame(res, columns=['District', 'Transaction Amount'])
                     fig = px.bar(df, x="District", y="Transaction Amount")
                     fig.update_layout(title_x=1)
                     fig.update_layout(
                         plot_bgcolor='#FAC898',
                         paper_bgcolor='#e8f4ea',
                         xaxis_title_font=dict(color='#6739b7'),
                         yaxis_title_font=dict(color='#6739b7')
                     )
                     fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                       hoverlabel_font_color="#F500E6")
                     fig.update_traces(marker_color='#d450b0')
                     with col2.expander("Top 10 District By Transaction Amount"):
                         st.plotly_chart(fig, theme=None, use_container_width=True)

                 elif Choice == "count":
                     query_1 = f"select district , sum(transaction_count) as val from top_transaction where year = '{year}' and quater = {q} and state = '{state_selected}' group by district order by val {order} limit 10;"
                     cursor.execute(query_1)
                     res = [i for i in cursor.fetchall()]
                     df = pd.DataFrame(res, columns=['District', 'Transaction count'])
                     fig = px.bar(df, x="District", y="Transaction count")
                     fig.update_layout(title_x=1)
                     fig.update_layout(
                         plot_bgcolor='#FAC898',
                         paper_bgcolor='#e8f4ea',
                         xaxis_title_font=dict(color='#6739b7'),
                         yaxis_title_font=dict(color='#6739b7')
                     )
                     fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                       hoverlabel_font_color="#F500E6")
                     fig.update_traces(marker_color='#d450b0')
                     with col2.expander("Top 10 District By Transaction count"):
                         st.plotly_chart(fig, theme=None, use_container_width=True)





        elif vary == "Pincode":
                if Choice == "Amount":
                    query_pin = f"select transaction_count , sum(transaction_amount) as val from top_transaction where year = '{year}' and quater = {q} and state = '{state_selected}' group by transaction_count order by val {order} limit 10;"
                    cursor.execute(query_pin)
                    res = [i for i in cursor.fetchall()]
                    df = pd.DataFrame(res,columns=["Pincode","Transaction Amount"])
                    pie = px.pie(df, names='Pincode', values="Transaction Amount", hole=0.7,
                                 color_discrete_sequence=['#a7269e', '#e35be1'])  # change color
                    pie.update_traces(textposition='outside')

                    pie.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                      hoverlabel_font_color="#F500E6")
                    pie.update_layout(paper_bgcolor='#e8f4ea')


                    with col2.expander("Top 10 Pincode By Transaction Amount"):
                        st.plotly_chart(pie, theme=None, use_container_width=True)

                elif Choice == "count":
                    query_pin = f"select transaction_amount, sum(transaction_count) as val from top_transaction where year = '{year}' and quater = {q} and state = '{state_selected}' group by transaction_amount order by val {order} limit 10;"
                    cursor.execute(query_pin)
                    res = [i for i in cursor.fetchall()]
                    df = pd.DataFrame(res, columns=["Pincode", "Transaction count"])
                    pie = px.pie(df, names='Pincode', values="Transaction count", hole=0.7,
                                 color_discrete_sequence=['#a7269e', '#e35be1'])  # change color
                    pie.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                      hoverlabel_font_color="#F500E6")
                    pie.update_traces(textposition='outside')
                    pie.update_layout(paper_bgcolor='#e8f4ea')

                    with col2.expander("Top 10 Pincode By Transaction count"):
                        st.plotly_chart(pie, theme=None, use_container_width=True)



    elif selected_1 == "User":


        #_________________________________________________________________________________________________________________________________________________________________

                                                                                              #____State Registered Users Analysis____#
        # info :
        col1, col2, col3, = st.columns([4, 10, 1])
        col2.title(':violet[State RegisteredUsers Analysis]')
        st.markdown("<style>div.block-container{padding-top:2rem;}</style>", unsafe_allow_html=True)
        # __________________________________________________________________________________________________________________________________________________________________

                                                                                               # ____________FILTERS___________#

        col1, col3, col4, col5 ,col6 = st.columns([8,  8, 8, 8,6])

        # 1) Year
        cursor.execute('select distinct(year) from top_user order by year asc')
        y_values = [i[0] for i in cursor.fetchall()]

        # 2) Quater
        cursor.execute('select distinct(quater) from aggregated_transaction order by quater asc')
        q_values = [i[0] for i in cursor.fetchall()]

        # 3) State
        cursor.execute('select distinct(state) from top_user order by state desc')
        state_names = [i[0] for i in cursor.fetchall()]  # State Names

        with col4:
            st.write("")
            state_selected = st.selectbox(':violet[CHOOSE STATE]', state_names)
            # st.write("")
            # st.write("")

        with col6:
            st.write("")
            year = st.select_slider(':violet[CHOOSE YEAR]', options=y_values)

            q = st.select_slider(':violet[CHOOSE QUATER]', options=q_values)

        with col5:
            st.write("")
            order = st.selectbox(":violet[CHOOSE ORDER]", ['Top', 'Bottom'])

    #_____________________________________________________________________________________________________________________________________________________________________________

                                                                    # ________________METRICS__________________#

    # 1) Metric  : Top State By RU

        query = f"select state , sum(RegisteredUser) as val from top_user where year= '{year}' and quater= {q} group by state order by val desc limit 1;"
        cursor.execute(query)
        res = [i[0] for i in cursor.fetchall()]
        cursor.execute(query)
        res1 = [i[1] for i in cursor.fetchall()]
        col1.metric(label = "Top State By Registered Users", value=res[0], delta=f"{round((res1[0]/100000)/10,2)}M")
        style_metric_cards(
            border_left_color='#08EED2',
            background_color='#e8f4ea', border_color="#0E1117")
    # ________________________________________________________________________________________________________________________________________________________________________________________

    # 2) Metric  : Current State By RU

        Query_1 = f"select state , sum(RegisteredUser) as val from top_user where year= '{year}' and quater= {q} and state = '{state_selected}' group by state order by val desc limit 1;"
        cursor.execute(Query_1)
        res = [i[0] for i in cursor.fetchall()]  # Name
        cursor.execute(Query_1)
        res1 = [i[1] for i in cursor.fetchall()]  # count
        col3.metric(label = "Current State By RegisteredUsers", value=res[0], delta=f"{round((res1[0]/100000)/10,2)}M")

    #_______________________________________________________________________________________________________________________________________________________________________________________________________

                                                                                    # ___________CHARTS___________#

        col1, col2,col3 = st.columns([1, 100,1])

    # _____________________________________________________________________________________________________________________________________________________________________________

    # 1) Bar : Top/Bottom  1o States By (RU)

        if order == 'Bottom':
            query = f"select state , sum(RegisteredUser) as val from top_user where year= '{year}' and quater= {q} group by state order by val asc limit 10;"
            cursor.execute(query)
            res = [i for i in cursor.fetchall()]
            df = pd.DataFrame(res, columns=['State', 'Registered Users'])
            fig = px.bar(df, x="State", y="Registered Users")
            fig.update_layout(title_x=1)
            fig.update_layout(
                plot_bgcolor='#FAC898',
                paper_bgcolor='#e8f4ea',
                xaxis_title_font=dict(color='#6739b7'),
                yaxis_title_font=dict(color='#6739b7')
            )
            fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                              hoverlabel_font_color="#F500E6")
            fig.update_traces(marker_color='#d450b0')
            with col2.expander("Bottom 10 State By Registered Users"):
                st.plotly_chart(fig, theme=None, use_container_width=True)

        elif order == "Top":
            query = f"select state , sum(RegisteredUser) as val from top_user where year= '{year}' and quater= {q} group by state order by val desc limit 10;"
            cursor.execute(query)
            res = [i for i in cursor.fetchall()]
            df = pd.DataFrame(res, columns=['State', 'Registered Users'])
            fig = px.bar(df, x="State", y="Registered Users")
            fig.update_layout(title_x=1)
            fig.update_layout(
                plot_bgcolor='#FAC898',
                paper_bgcolor='#e8f4ea',
                xaxis_title_font=dict(color='#6739b7'),
                yaxis_title_font=dict(color='#6739b7')
            )
            fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                              hoverlabel_font_color="#F500E6")
            fig.update_traces(marker_color='#d450b0')
            with col2.expander("Top 10 State By Registered Users"):
                st.plotly_chart(fig, theme=None, use_container_width=True)

        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")

# ____________________________________________________________________________________________________________________________________________________________________________________________________

                                                                                         # _______DISTRICTS-WISE ANALYSIS___________#

            # info :
        col1, col2, col3, = st.columns([4, 10, 1])
        col2.title(':violet[District Registered Users Analysis]')
        col2.markdown("<style>div.block-container{padding-top:2rem;}</style>", unsafe_allow_html=True)


    # ___________________________________________________________________________________________________________________________________________________________________________________________________

                                                                                         # __________FILTERS____________#\

        col1, col3, col4, col5,col6 = st.columns([9,  8, 7, 7,6])

        # 1) Year
        cursor.execute('select distinct(year) from top_user order by year asc')
        y_values = [i[0] for i in cursor.fetchall()]

        # 2) Quater
        cursor.execute('select distinct(quater) from aggregated_transaction order by quater asc')
        q_values = [i[0] for i in cursor.fetchall()]

        # 3) State
        cursor.execute(
            'select distinct(district) from top_transaction order by district;')
        dist_names = [i[0] for i in cursor.fetchall()]  # dist Names


        with col3:
            st.write("")
            # st.write("")
            dist_selected = st.selectbox(':violet[CHOOSE DISTRICT]', dist_names)
        with col6:
            st.write("")
            year = st.select_slider(':violet[YEAR]', options=y_values)
        with col5:    
            st.write("")
            q = st.select_slider(':violet[QUATER]', options=q_values)
        with col4:
            st.write("")
            order = st.selectbox(":violet[ORDER]", ['Top', 'Bottom'])

        # _________________________________________________________________________________________________________________________________________________________________________________________________________________

                                                                                                  # _____________METRICS___________#

        # 1) Metric  : Top District By Amount
        query = f"select district, sum(RegisteredUser) as val from  top_user where year= '{year}' and quater= {q} group by district order by val desc limit 1;"
        cursor.execute(query)
        res = [i[0] for i in cursor.fetchall()]
        cursor.execute(query)
        res1 = [i[1] for i in cursor.fetchall()]
        col1.metric(label = "Top District By Registered Users", value=res[0], delta=f"{round((res1[0]/100000)/10,2)}M")

        # ______________________________________________________________________________________________________________________________________________________________________________________________

        # 3) Metric  : Current State By RU

        #Query_1 = f"select district, sum(RegisteredUser) as val from  top_user where year= '{year}' and quater= {q} and district = '{dist_selected}' group by district order by val desc limit 1;"

        #cursor.execute(Query_1)
        #res = [i[0] for i in cursor.fetchall()]  # Name

        #cursor.execute(Query_1)
        #res1 = [i[1] for i in cursor.fetchall()]  # count
        #with col3.expander(":violet[Current District By Registered Users]"):
         #   st.metric("", value=res[0], delta=f"{round((res1[0]/100000)/10,2)}M")

        # _________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

                                                                                                         # ___________CHARTS___________#

        col1, col2 ,col3= st.columns([1,100 ,1])

        #_____________________________________________________________________________________________________________________________________________________________________________

        # 1) Bar : Top/Bottom  1o districts By RU

        if order == 'Bottom':
            query = f"select state, sum(RegisteredUser) as val from top_user where year= '{year}' and quater= {q} group by RegisteredUser, state order by val  limit 10;"
            cursor.execute(query)
            res = [i for i in cursor.fetchall()]
            df = pd.DataFrame(res, columns=['District', 'Registered Users'])
            fig = px.bar(df, x="District", y="Registered Users")
            fig.update_layout(title_x=1)
            fig.update_layout(
                plot_bgcolor='#FAC898',
                paper_bgcolor='#e8f4ea',
                xaxis_title_font=dict(color='#6739b7'),
                yaxis_title_font=dict(color='#6739b7')
            )
            fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                              hoverlabel_font_color="#F500E6")
            fig.update_traces(marker_color='#d450b0')
            with col2.expander("Bottom 10 District By Registered Users"):
                st.plotly_chart(fig, theme=None, use_container_width=True)

        elif order == "Top":
            query = f"select state, sum(RegisteredUser) as val from top_user where year= '2022' and quater= 1 group by RegisteredUser, state order by val desc limit 10;"
            cursor.execute(query)
            res = [i for i in cursor.fetchall()]
            df = pd.DataFrame(res, columns=['State', 'Registered Users'])
            fig = px.bar(df, x="State", y="Registered Users")
            fig.update_layout(title_x=1)
            fig.update_layout(
                plot_bgcolor='#FAC898',
                paper_bgcolor='#e8f4ea',
                xaxis_title_font=dict(color='#6739b7'),
                yaxis_title_font=dict(color='#6739b7')
            )
            fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                              hoverlabel_font_color="#F500E6")
            fig.update_traces(marker_color='#d450b0')
            with col2.expander("Top 10 District By Registered Users"):
                st.plotly_chart(fig, theme=None, use_container_width=True)
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")

        # ____________________________________________________________________________________________________________________________________________________________________________________________________

                                                                                                # _______ TRANSACTION ANALYSIS___________#

        col1, col2, col3, = st.columns([4, 10, 1])
        col2.title(':violet[Pincode Registers Users Analysis]')

        st.write("")
        st.write("")

        # ______________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

                                                                                                 # _____________FILTER_____________________#

        col1, col2, col3, col4, col5 = st.columns([7, 7, 7, 7, 7])

        # 1) Year
        cursor.execute('select distinct(year) from top_user order by year asc')
        y_values = [i[0] for i in cursor.fetchall()]

        # 2) Quater
        cursor.execute('select distinct(quater) from aggregated_transaction order by quater asc')
        q_values = [i[0] for i in cursor.fetchall()]

        with col4:
            st.write("")
            year = st.select_slider(':violet[SELECT YEAR]', options=y_values)
        with col3:    
            st.write("")
            q = st.select_slider(':violet[SELECT QUATER]', options=q_values)
        with col2:

            st.write("")
            order = st.selectbox(":violet[SELECT ORDER]", ['Top', 'Bottom'])

        # ______________________________________________________________________________________________________________________________________________________________________________________________________________________________
                                                                                                       # ____________CHARTS____________#

        col1, col2 ,col3= st.columns([1,100,1])

        # 1)  Top 10 Pincode By Transaction Amount

        if order == "Top":
            query_pin = f"select district , sum(RegisteredUser) as val from top_user where year = '{year}' and quater = {q} group by  district order by val desc limit 10;"
            cursor.execute(query_pin)
            res = [i for i in cursor.fetchall()]
            df = pd.DataFrame(res, columns=['Pincode', 'Registered Users'])
            pie = px.pie(df, names='Pincode', values='Registered Users', hole=0.7,
                         color_discrete_sequence=['#6a0578', '#a7269e', '#d450b0', '#eb8adb',
                                                  '#CA8DE1'])  # change color
            pie.update_traces(textposition='outside')
            pie.update_layout(paper_bgcolor='#e8f4ea')
            with col2.expander("Top 10 Pincode By Registered Users"):
                st.plotly_chart(pie, theme=None, use_container_width=True)

        elif order == "Bottom":
            query_pin = f"select district , sum(RegisteredUser) as val from top_user where year = '{year}' and quater = {q} group by  district order by val  limit 10;"
            cursor.execute(query_pin)
            res = [i for i in cursor.fetchall()]
            df = pd.DataFrame(res, columns=['Pincode', 'Registered Users'])
            pie = px.pie(df, names='Pincode', values='Registered Users', hole=0.7,
                         color_discrete_sequence=['#6a0578', '#a7269e', '#d450b0', '#eb8adb',
                                                  '#CA8DE1'])  # change color
            pie.update_traces(textposition='outside')
            pie.update_layout(paper_bgcolor='#e8f4ea')
            with col2.expander("Bottom 10 Pincode By Registered Users"):
                st.plotly_chart(pie, theme=None, use_container_width=True)




        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        # _________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

                                                                                   # _____________SDP Registered User  Concentration________________________#

        col1, col2, col3, = st.columns([2, 10, 1])

        col2.title(':violet[SDP RegisteredUser Concentration Analysis]')

        st.write("")
        st.write("")

        # ___________________________________________________________________________________________________________________________________________________________________________________________________________________________________

                                                                                                # _______________FILTERS___________________#

        col1, col2, col3, col4, col5 = st.columns([7, 7, 7, 7, 7])

        # 1) Year
        cursor.execute('select distinct(year) from top_user order by year asc')
        y_values = [i[0] for i in cursor.fetchall()]

        # 2) Quater
        cursor.execute('select distinct(quater) from aggregated_transaction order by quater asc')
        q_values = [i[0] for i in cursor.fetchall()]

        with col4:
            st.write("")
            year = st.select_slider(':violet[Pick YEAR]', options=y_values)

        with col2:
            st.write("")
            q = st.select_slider(':violet[Pick QUATER]', options=q_values)


        # __________________________________________________________________________________________________________________________________________________________________________________________________________________________________

                                                                                                      # __________CHARTS_______________#

        col1, col2, col3 = st.columns([7, 7, 7])

                                                                                                       # _________State_Level__________#

        querys_top = f"select sum(RegisteredUser) as val from top_user where year = '{year}' and quater = {q}  group by state order by val desc limit 10;"
        cursor.execute(querys_top)
        res = [i for i in cursor.fetchall()]
        df_1 = pd.DataFrame(res, columns=['Amount Top'])

        querys_bottom = f"select state, sum(RegisteredUser) as val from top_user where year = '{year}' and quater ={q} and state group by state order by val desc limit 10;"
        cursor.execute(querys_bottom)
        res = [i for i in cursor.fetchall()]
        df_2 = pd.DataFrame(res, columns=['Amount Bottom'])

        state_last = {"Names": [], 'value': []}
        state_last['Names'].append("Top 10 States")
        state_last['Names'].append("Other States")

        state_last['value'].append(int(sum(df_1['Amount Top'])))
        state_last['value'].append(int(sum(df_2['Amount Bottom'])))

        df = pd.DataFrame(state_last)

        pie = px.pie(df, names='Names', values='value', labels={'Names': 'State Type', 'value': 'Registered Users'},
                     hole=0.7,
                     color_discrete_sequence=['#a7269e', '#eda1ec'])  # change color
        pie.update_traces(textposition='outside')
        pie.update_layout(paper_bgcolor='#e8f4ea')

        with col1.expander("TOP 10 STATES :orange[Vs]  OTHER STATES"):
            st.plotly_chart(pie, theme=None, use_container_width=True)

        # _________________________________________________________________________________________________________________________________________________________________________________________________________________________________

                                                                                                       # ______________Districts Level__________#

        # Metrics 3 : District Transaction Concentration :

        query_top = f"select  sum(RegisteredUser) as val from top_user where year = '{year}' and quater = {q}  group by district order by val desc limit 10"
        cursor.execute(query_top)
        res = [i for i in cursor.fetchall()]
        df = pd.DataFrame(res, columns=['Amount Top'])
        last = {'Names': [], 'value': []}
        last['Names'].append("Top 10 Districts")
        last['value'].append(int(sum(df['Amount Top'])))

        query_bottom = f"select  sum(RegisteredUser)  from top_user where year = '{year}' and quater ={q} and district group by district  order by sum(RegisteredUser) desc limit 10;"
        cursor.execute(query_bottom)
        res = [i for i in cursor.fetchall()]
        df = pd.DataFrame(res, columns=['Amount Bottom'])

        last['Names'].append("Other Districts")
        last['value'].append(int(sum(df['Amount Bottom'])))

        df = pd.DataFrame(last)  # '#a7269e', '#d450b0', '#eb8adb',
        pie = px.pie(df, names='Names', values='value', hole=0.7,
                     labels={'Names': 'District Type', 'value': 'Registered Users'},
                     color_discrete_sequence=['#a7269e', '#eda1ec'])  # change color
        pie.update_traces(textposition='outside')
        pie.update_layout(paper_bgcolor='#e8f4ea')

        with col2.expander("TOP 10 DISTRICTS :orange[Vs]  OTHER DISTRICTS"):
            st.plotly_chart(pie, theme=None, use_container_width=True)

        # ______________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

                                                                                                 #_________________________#

        query_top = f"select sum(RegisteredUser) as val  from top_user where year = '{year}' and quater = {q} group by district order by val desc limit 10"
        cursor.execute(query_top)
        res = [i for i in cursor.fetchall()]
        df = pd.DataFrame(res, columns=['Amount Top'])
        last = {'Names': [], 'value': []}
        last['Names'].append("Top 10 Pincodes")
        last['value'].append(int(sum(df['Amount Top'])))

        query_bottom = f"select  sum(RegisteredUser)  from  top_user where year = '{year}' and quater ={q} and district group by district  order by sum(RegisteredUser) desc limit 10;"
        cursor.execute(query_bottom)
        res = [i for i in cursor.fetchall()]
        df = pd.DataFrame(res, columns=['Amount Bottom'])

        last['Names'].append("Other Pincodes")
        last['value'].append(int(sum(df['Amount Bottom'])))

        df = pd.DataFrame(last)
        pie = px.pie(df, names='Names', values='value', hole=0.7,
                     labels={'Names': 'Pincode Type', 'value': 'Registered Userst'},
                     color_discrete_sequence=['#a7269e', '#eda1ec'])  # change color
        pie.update_traces(textposition='outside')
        pie.update_layout(paper_bgcolor='#e8f4ea')

        with col3.expander("TOP 10 PINCODES :orange[Vs]  OTHER PINCODES"):
            st.plotly_chart(pie, theme=None, use_container_width=True)

        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        # _______________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________

                                                                                                 # ___________________Top 10 DP In State By Transaction Amount_______________#

        col1, col2, col3 = st.columns([2, 8, 1])

        col2.title(':violet[Top 10 DP In State By Registered User]')
        st.write("")
        st.write("")

        # _________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
                                                                                                                        # ___________FILTERS_______________#

        col1, col2, col3, col4, col5 = st.columns([5, 5, 5, 5, 5])

        # ________________________________________________________________________________________________________________________________________________________________________________________
        # 1) State

        query = "select distinct(state) from top_transaction order by state desc"
        cursor.execute(query)
        res = [i[0] for i in cursor.fetchall()]
        with col1:
            st.write("")

            state_selected = st.selectbox(":violet[PICK STATE]", res)

        # 2) Districts and Pincodes

        with col2:
            st.write("")
            vary = st.selectbox(':violet[PICK OPTION]', ['District', 'Pincode'])



        # 1) Year
        cursor.execute('select distinct(year) from top_user order by year asc')
        y_values = [i[0] for i in cursor.fetchall()]

        # 2) Quater
        cursor.execute('select distinct(quater) from aggregated_transaction order by quater asc')
        q_values = [i[0] for i in cursor.fetchall()]

        with col4:
            year = st.select_slider(":violet[Choose Year]", options=y_values)

        with col3:
            q = st.select_slider(':violet[Choose Quater]', options=q_values)
        st.write("")
        st.write('')

        # 5) Top / Bottom 10

        with col5:
            st.write("")
            order = st.selectbox(":violet[Choose Order]", ['desc', 'asc'])

        # ____________________________________________________________________________________________________________________________________________________________________________________________________

                                                                                                           # _____CONDITION METRICS_____#
        col1, col2, col3 = st.columns([1, 100, 1])

        if vary == "District":

                query_1 = f"select district, sum(RegisteredUser) as val from top_user where year = '{year}' and quater = {q} and state = '{state_selected}' group by district order by val {order} limit 10;"
                cursor.execute(query_1)
                res = [i for i in cursor.fetchall()]
                df = pd.DataFrame(res, columns=['District', 'Registered Users'])
                fig = px.bar(df, x="District", y="Registered Users")
                fig.update_layout(title_x=1)
                fig.update_layout(
                    plot_bgcolor='#FAC898',
                    paper_bgcolor='#e8f4ea',
                    xaxis_title_font=dict(color='#6739b7'),
                    yaxis_title_font=dict(color='#6739b7')
                )
                fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                  hoverlabel_font_color="#F500E6")
                fig.update_traces(marker_color='#d450b0')
                with col2.expander("Top 10 District By Registered User"):
                    st.plotly_chart(fig, theme=None, use_container_width=True)





        elif vary == "Pincode":

                query_pin = f"select district, sum(RegisteredUser) as val from top_user where year = '{year}' and quater = {q} and state = '{state_selected}' group by district order by val {order}  limit 10;"
                cursor.execute(query_pin)
                res = [i for i in cursor.fetchall()]
                df = pd.DataFrame(res, columns=["Pincode", "Registered Users"])
                pie = px.pie(df, names='Pincode', values="Registered Users", hole=0.7,
                             color_discrete_sequence=['#a7269e', '#e35be1'])  # change color
                pie.update_traces(textposition='outside')

                pie.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                  hoverlabel_font_color="#F500E6")
                pie.update_layout(paper_bgcolor='#e8f4ea')

                with col2.expander("Top 10 Pincode By Registered Users"):
                    st.plotly_chart(pie, theme=None, use_container_width=True)
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
elif selected == 'View Data Source':
    st.markdown("<style>div.block-container{padding-top:2rem;}</style>", unsafe_allow_html=True)

    selected = option_menu(
               menu_title="",
               options=['Aggregated Transaction', 'Aggregated User', 'Map Transaction', "Map User", "Top Transaction", 'Top User'],
               icons=['table', 'table', 'table', 'table', 'table', 'table', 'table', 'table'],
               menu_icon='database-fill-check',
               default_index=0,
               orientation='horizontal',
               styles={
        "container": {"padding": "0!important", "background-color": "#FFFFFF"},
        "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#6739B7"},
        "nav-link-selected": {"background-color": "#6739B7"}}
           )

    if selected == "Aggregated Transaction":
        query_1 = "select * from aggregated_transaction"
        cursor.execute(query_1)
        res = [i for i in cursor.fetchall()]
        df  = pd.DataFrame(res,columns =['state', 'year', 'quater', 'transaction_type', 'transaction_count', 'transaction_amount'])
        st.dataframe(df)

    elif selected =="Aggregated User":
        query_1 = "select * from aggregated_user"
        cursor.execute(query_1)
        res = [i for i in cursor.fetchall()]
        df = pd.DataFrame(res, columns=['state', 'year', 'quater', 'brands', 'count', 'percentage'])
        st.dataframe(df)


    elif selected =="Map Transaction":
        query_1 = "select * from map_transaction"
        cursor.execute(query_1)
        res = [i for i in cursor.fetchall()]
        df = pd.DataFrame(res, columns=['state'	,'year', 'quater', 'district', 'count', 'amount'])
        st.dataframe(df)

    elif selected =="Map User":
        query_1 = "select * from map_user"
        cursor.execute(query_1)
        res = [i for i in cursor.fetchall()]
        df = pd.DataFrame(res, columns=['state', 'year', 'quater', 'district', 'RegisteredUser'])
        st.dataframe(df)

    elif selected =="Top Transaction":
        query_1 = "select * from top_transaction"
        cursor.execute(query_1)
        res = [i for i in cursor.fetchall()]
        df = pd.DataFrame(res, columns=['state', 'year', 'quater', 'pincode', 'transaction_count', 'transaction_amount'])
        st.dataframe(df)

    elif selected =="Top User":
        query_1 = "select * from top_user"
        cursor.execute(query_1)
        res = [i for i in cursor.fetchall()]
        df = pd.DataFrame(res, columns=['state', 'year','quater', 'top_user_pincode', 'RegisteredUser'])
        st.dataframe(df)
#________________________________________________________________________________________________________________________________________________________________________________________________
elif selected == "Time-based Analysis":

    c1,c2,c3 = st.columns([50,100,1])
    st.markdown("<style>div.block-container{padding-top:3rem;}</style>", unsafe_allow_html=True)

    c2.title(':violet[Time Based Analysis]')
    st.write("")

    #______________________________________________________________________________________________________________________________________________________________________

                                                                         #________FILTER____________#

    col1, col2, col3,col4 ,col5= st.columns([7,7,7,7,7])

    # Select State or District
    with col1:
        select = st.selectbox(':violet[PICK OPTION]',['State','District'])

    # State
    query = "select distinct(state) from map_transaction  order by state asc"
    cursor.execute(query)
    res = [i[0] for i in cursor.fetchall()]
    with col2:
        state_selected = st.selectbox(":violet[CHOOSE STATE]",res)

    # District

    query_1 = f"select distinct(district) from map_transaction  where state = '{state_selected}' order by district asc"

    cursor.execute(query_1)
    res_1 = [i[0] for i in cursor.fetchall()]
    with col3:
        dist_selected  = st.selectbox(":violet[CHOOSE DISTRICT]", res_1)

    # Year

    query_2 = "select distinct(year) from map_transaction  order by year asc"

    cursor.execute(query_2)
    res_2 = [i[0] for i in cursor.fetchall()]
    with col4:
        year = st.selectbox(":violet[CHOOSE YEAR]", res_2)


    # Option

    with col5:
       option =  st.selectbox(":violet[CHOOSE OPTION]",['Transaction Amount',"Transaction count","Registered Users"])
    st.write("")
    st.write("")



    #__________________________________________________________________________________________________________________________________________________________________________________________

    c1, c2, c3 = st.columns([50, 100, 1])

    c2.title(':violet[Quater-wise Analysis ]')
    st.write("")

    #________________________________________________________________________________________________________________________________________________________________________________________________________

                                                                                            #_______CHARTS_______#
    #
    c1, c2, c3 = st.columns([1, 100, 1])



    # # 1)  Total Amount , count , RU By state , year , District

    if select == "State":

        if option == 'Transaction Amount':

                query = f"select quater , sum(amount) from map_transaction where state = '{state_selected}' and year = '{year}' group by quater order by quater asc"

                cursor.execute(query)
                res = [i for i in cursor.fetchall()]
                df = pd.DataFrame(res, columns=['Quater', 'Transaction Amount'])
                fig = px.line(df, x="Quater", y="Transaction Amount", markers='D')
                fig.update_layout(title_x=1)
                fig.update_layout(
                    plot_bgcolor='#FAC898',
                    paper_bgcolor='#e8f4ea',
                    xaxis_title_font=dict(color='#6739b7'),
                    yaxis_title_font=dict(color='#6739b7')
                )
                fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                  hoverlabel_font_color="#F500E6")
                fig.update_traces(marker_color='#d450b0')
                with c2.expander(f"{option} in {state_selected} Over the quaters of {year}"):
                    st.plotly_chart(fig, theme=None, use_container_width=True)

        elif option == "Transaction count":

               query = f"select quater , sum(count) from map_transaction where state = '{state_selected}' and year = '{year}' group by quater order by quater asc;"
               cursor.execute(query)
               res = [i for i in cursor.fetchall()]
               df = pd.DataFrame(res, columns=['Quater', 'Transaction count'])
               fig = px.line(df, x="Quater", y="Transaction count", markers='D')
               fig.update_layout(title_x=1)
               fig.update_layout(
                   plot_bgcolor='#FAC898',
                   paper_bgcolor='#e8f4ea',
                   xaxis_title_font=dict(color='#6739b7'),
                   yaxis_title_font=dict(color='#6739b7')
               )
               fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                 hoverlabel_font_color="#F500E6")
               fig.update_traces(marker_color='#d450b0')
               with c2.expander(f"{option} in {state_selected} Over the quaters of {year}"):
                   st.plotly_chart(fig, theme=None, use_container_width=True)



        elif option == "Registered Users":

            query = f"select quater , sum(RegisteredUser)  from map_user where year ='{year}' and state = '{state_selected}' group by quater order by quater asc"

            cursor.execute(query)
            res = [i for i in cursor.fetchall()]
            df = pd.DataFrame(res, columns=['Quater', 'Registered Users'])
            fig = px.line(df, x="Quater", y="Registered Users", markers='D')
            fig.update_layout(title_x=1)
            fig.update_layout(
                plot_bgcolor='#FAC898',
                paper_bgcolor='#e8f4ea',
                xaxis_title_font=dict(color='#6739b7'),
                yaxis_title_font=dict(color='#6739b7')
            )
            fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                              hoverlabel_font_color="#F500E6")
            fig.update_traces(marker_color='#d450b0')
            with c2.expander(f"{option} in {state_selected} Over the quaters of {year}"):
                st.plotly_chart(fig, theme=None, use_container_width=True)

    elif select == "District":

        if option == 'Transaction Amount':

                query = f"select quater , sum(amount) from map_transaction where district = '{dist_selected}' and year = '{year}' group by quater order by quater asc"

                cursor.execute(query)
                res = [i for i in cursor.fetchall()]
                df = pd.DataFrame(res, columns=['Quater', 'Transaction Amount'])
                fig = px.line(df, x="Quater", y="Transaction Amount", markers='D')
                fig.update_layout(title_x=1)
                fig.update_layout(
                    plot_bgcolor='#FAC898',
                    paper_bgcolor='#e8f4ea',
                    xaxis_title_font=dict(color='#6739b7'),
                    yaxis_title_font=dict(color='#6739b7')
                )
                fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                  hoverlabel_font_color="#F500E6")
                fig.update_traces(marker_color='#d450b0')
                with c2.expander(f"{option} in {dist_selected} Over the quaters of {year}"):
                    st.plotly_chart(fig, theme=None, use_container_width=True)

        elif option == "Transaction count":

               query = f"select quater , sum(count) from map_transaction where district = '{dist_selected}' and year = '{year}' group by quater order by quater asc;"
               cursor.execute(query)
               res = [i for i in cursor.fetchall()]
               df = pd.DataFrame(res, columns=['Quater', 'Transaction count'])
               fig = px.line(df, x="Quater", y="Transaction count", markers='D')
               fig.update_layout(title_x=1)
               fig.update_layout(
                   plot_bgcolor='#FAC898',
                   paper_bgcolor='#e8f4ea',
                   xaxis_title_font=dict(color='#6739b7'),
                   yaxis_title_font=dict(color='#6739b7')
               )
               fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                                 hoverlabel_font_color="#F500E6")
               fig.update_traces(marker_color='#d450b0  ')
               with c2.expander(f"{option} in {dist_selected} Over the quaters of {year}"):
                   st.plotly_chart(fig, theme=None, use_container_width=True)



        elif option == "Registered Users":

            query = f"select quater , sum(RegisteredUser)  from map_user where year ='{year}' and district = '{dist_selected}' group by quater order by quater asc"

            cursor.execute(query)
            res = [i for i in cursor.fetchall()]
            df = pd.DataFrame(res, columns=['Quater', 'Registered Users'])
            fig = px.line(df, x="Quater", y="Registered Users", markers='D')
            fig.update_layout(title_x=1)
            fig.update_layout(
                plot_bgcolor='#FAC898',
                paper_bgcolor='#e8f4ea',
                xaxis_title_font=dict(color='#6739b7'),
                yaxis_title_font=dict(color='#6739b7')
            )
            fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                              hoverlabel_font_color="#F500E6")
            fig.update_traces(marker_color='#d450b0')
            with c2.expander(f"{option} in {dist_selected} Over the quaters of {year}"):
                st.plotly_chart(fig, theme=None, use_container_width=True)
    st.write("")
    st.write("")
    st.write("")
    st.write("")

   #_____________________________________________________________________________________________________________________________________________________________________________________________________________

    c1, c2, c3 = st.columns([50, 100, 1])

    c2.title(':violet[Year-wise Analysis]')
    st.write("")

    #__________________________________________________________________________________________________________________________________________________________________________________________________________________

    c1, c2, c3 = st.columns([1, 100, 1])

    # # 1)  Total Amount , count , RU By state , year , District

    if select == "State":

        if option == 'Transaction Amount':

            query = f"select year , sum(amount) from map_transaction where state = '{state_selected}'  group by year order by year asc"

            cursor.execute(query)
            res = [i for i in cursor.fetchall()]
            df = pd.DataFrame(res, columns=['Year', 'Transaction Amount'])
            fig = px.line(df, x="Year", y="Transaction Amount", markers='D')
            fig.update_layout(title_x=1)
            fig.update_layout(
                plot_bgcolor='#FAC898',
                paper_bgcolor='#e8f4ea',
                xaxis_title_font=dict(color='#6739b7'),
                yaxis_title_font=dict(color='#6739b7')
            )
            fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                              hoverlabel_font_color="#F500E6")
            fig.update_traces(marker_color='#d450b0')
            with c2.expander(f"{option} in {state_selected}  Over The Years From 2018 To 2022"):
                st.plotly_chart(fig, theme=None, use_container_width=True)

        elif option == "Transaction count":

            query = f"select year , sum(count) from map_transaction where state = '{state_selected}'  group by year order by year asc;"
            cursor.execute(query)
            res = [i for i in cursor.fetchall()]
            df = pd.DataFrame(res, columns=['Year', 'Transaction count'])
            fig = px.line(df, x="Year", y="Transaction count", markers='D')
            fig.update_layout(title_x=1)
            fig.update_layout(
                plot_bgcolor='#FAC898',
                paper_bgcolor='#e8f4ea',
                xaxis_title_font=dict(color='#6739b7'),
                yaxis_title_font=dict(color='#6739b7')
            )
            fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                              hoverlabel_font_color="#F500E6")
            fig.update_traces(marker_color='#d450b0')
            with c2.expander(f"{option} in {state_selected}  Over The Years From 2018 To 2022"):
                st.plotly_chart(fig, theme=None, use_container_width=True)



        elif option == "Registered Users":

            query = f"select year , sum(RegisteredUser)  from map_user where state = '{state_selected}'  group by year order by year asc;"

            cursor.execute(query)
            res = [i for i in cursor.fetchall()]
            df = pd.DataFrame(res, columns=['Year', 'Registered Users'])
            fig = px.line(df, x="Year", y="Registered Users", markers='D')
            fig.update_layout(title_x=1)
            fig.update_layout(
                plot_bgcolor='#FAC898',
                paper_bgcolor='#e8f4ea',
                xaxis_title_font=dict(color='#6739b7'),
                yaxis_title_font=dict(color='#6739b7')
            )
            fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                              hoverlabel_font_color="#F500E6")
            fig.update_traces(marker_color='#d450b0')
            with c2.expander(f"{option} in {state_selected}  Over The Years From 2018 To 2022"):
                st.plotly_chart(fig, theme=None, use_container_width=True)

    elif select == "District":

        if option == 'Transaction Amount':

            query = f"select year , sum(amount) from map_transaction where district = '{dist_selected}'  group by year order by year asc"

            cursor.execute(query)
            res = [i for i in cursor.fetchall()]
            df = pd.DataFrame(res, columns=['Year', 'Transaction Amount'])
            fig = px.line(df, x="Year", y="Transaction Amount", markers='D')
            fig.update_layout(title_x=1)
            fig.update_layout(
                plot_bgcolor='#FAC898',
                paper_bgcolor='#e8f4ea',
                xaxis_title_font=dict(color='#6739b7'),
                yaxis_title_font=dict(color='#6739b7')
            )
            fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                              hoverlabel_font_color="#F500E6")
            fig.update_traces(marker_color='#d450b0')
            with c2.expander(f"{option} in {dist_selected}  Over The Years From 2018 To 2022"):
                st.plotly_chart(fig, theme=None, use_container_width=True)

        elif option == "Transaction count":

            query = f"select year , sum(count) from map_transaction where  district = '{dist_selected}'  group by year order by year asc;"
            cursor.execute(query)
            res = [i for i in cursor.fetchall()]
            df = pd.DataFrame(res, columns=['Year', 'Transaction count'])
            fig = px.line(df, x="Year", y="Transaction count", markers='D')
            fig.update_layout(title_x=1)
            fig.update_layout(
                plot_bgcolor='#FAC898',
                paper_bgcolor='#e8f4ea',
                xaxis_title_font=dict(color='#6739b7'),
                yaxis_title_font=dict(color='#6739b7')
            )
            fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                              hoverlabel_font_color="#F500E6")
            fig.update_traces(marker_color='#d450b0  ')
            with c2.expander(f"{option} in {dist_selected}  Over The Years From 2018 To 2022"):
                st.plotly_chart(fig, theme=None, use_container_width=True)



        elif option == "Registered Users":

            query = f"select year , sum(RegisteredUser)  from map_user where  district = '{dist_selected}'  group by year order by year asc;"

            cursor.execute(query)
            res = [i for i in cursor.fetchall()]
            df = pd.DataFrame(res, columns=['Quater', 'Registered Users'])
            fig = px.line(df, x="Quater", y="Registered Users", markers='D')
            fig.update_layout(title_x=1)
            fig.update_layout(
                plot_bgcolor='#FAC898',
                paper_bgcolor='#e8f4ea',
                xaxis_title_font=dict(color='#6739b7'),
                yaxis_title_font=dict(color='#6739b7')
            )
            fig.update_traces(hoverlabel=dict(bgcolor="#0E1117"),
                              hoverlabel_font_color="#F500E6")
            fig.update_traces(marker_color='#d450b0')
            with c2.expander(f"{option} in {dist_selected}  Over The Years From 2018 To 2022"):
                st.plotly_chart(fig, theme=None, use_container_width=True)
    st.write("")
    st.write("")
    st.write("")
    st.write("")
#_________________________________________________________________________________________________________________________________________________________________________________________________________________________
