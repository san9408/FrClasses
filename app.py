import streamlit as st
import requests
import json
import datetime
import pytz
import pandas as pd

time_zone = pytz.timezone("Europe/Paris") #America/Bogota
date_time_zone = datetime.datetime.now(time_zone)
date_formated = f'{date_time_zone.strftime('%Y-%m-%dT%H:%M:%S')}'
date_beauty = f'{date_time_zone.strftime('%a, %d %b %Y %H:%M')}'
class_id = ""

url_get_token = 'https://back-spc.azurewebsites.net/api/v1/auth/login'
url_get_class = f'https://back-spc.azurewebsites.net/api/v1/class?start_date={date_formated}&type=REGULAR'
url_get_registered_class = f'https://back-spc.azurewebsites.net/api/v1/class?start_date={date_formated}&type=REGISTERED'
url_get_class_details = f"https://back-spc.azurewebsites.net/api/v1/class/{class_id}/session"

def log_in(user):
    url = url_get_token
    body = {"customer_id":f"FR{user}","password":f"{user}"}
    x = requests.post(url, json = body)
    response = json.loads(x.text)
    try:
        token = response['token']
    except:
        token = ''
    return token

def get_classes(token, url):
    class_url = url
    get_class = requests.get(class_url, headers={'Authorization': 'Bearer ' + token})
    response_class = json.loads(get_class.text)
    return response_class

def submitted(user, type):
    print(type)
    my_token = log_in(user)
    if type=='all':
        get_my_classes = get_classes(my_token, url_get_class)
    else:
        get_my_classes = get_classes(my_token, url_get_registered_class)
    return get_my_classes

with st.form("my_form"):
   st.write('Disponibilidad de clases')
   user = st.text_input('Ingresa tu usuario')
   submit_btn = st.form_submit_button('Ver mis clases')

try:
    type = 'all'
    a = submitted(user, type)
    df = pd.DataFrame(a)
    my_df = df[["id", "start_date", "end_date", "teacher_name",]]
    my_df["selected"] = False
    st.write(f"Clases de frances disponibles a {date_beauty}")
    st.data_editor(
        my_df, 
        column_config={
            "start_date": st.column_config.DateColumn("Fecha de inicio", format="ddd, DD MMM YYYY HH:MM"),
            "end_date": st.column_config.DateColumn("Fecha de final", format="ddd, DD MMM YYYY HH:MM"),
            "teacher_name": "Profesor",
            "selected": st.column_config.CheckboxColumn(
                "Seleccionar", 
                default=False,
                )
            },
        disabled=["id", "start_date", "end_date", "teacher_name"],
        hide_index=True,
        )  
except:
    st.write("No classes to show")

try:
    type = 'registered'
    a = submitted(user, type)
    df = pd.DataFrame(a)
    my_df = df[["id", "start_date", "location_name", "teacher_name",]]
    st.write(f"Clases de frances registradas a {date_beauty}")
    st.data_editor(
        my_df, 
        column_config={
            "start_date": st.column_config.DateColumn("Fecha de inicio", format="ddd, DD MMM YYYY HH:MM"),
            #"end_date": st.column_config.DateColumn("Fecha de final", format="ddd, DD MMM YYYY HH:MM"),
            "location_name": "Zoom ID",
            "teacher_name": "Profesor",
            },
        disabled=["id", "start_date", "end_date", "teacher_name"],
        hide_index=True,
        )  
except:
    st.write("No programed classes to show")
