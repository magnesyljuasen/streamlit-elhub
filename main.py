import requests
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

#############
# pip install requests
# pip install streamlit
# streamlit run main.py
#############

# hente data fra elhub API og lagre i dataframe
def elhub_api(start_date, end_date, id = '3107'): 
    url = f"https://api.elhub.no/energy-data/v0/municipalities/{id}?dataset=CONSUMPTION_PER_GROUP_MUNICIPALITY_HOUR&startDate={start_date}%2B02:00&endDate={end_date}%2B02:00"
    response = requests.get(url) # kall mot API'et
    data = response.json() 
    hourly_data = (data['data'][0]['attributes']['consumptionPerGroupMunicipalityHour'])
    production_list = []
    time_list = []
    group_list = []
    for i in range(0, len(hourly_data)):
        production_list.append(hourly_data[i]['quantityKwh'])
        group_list.append(hourly_data[i]['consumptionGroup'])
        time_list.append(hourly_data[i]['startTime'])
    df = pd.DataFrame({
        'tidspunkt' : time_list,
        'forbruker' : group_list,
        'kW' : production_list
    })        
    return df

# lage liste med start og sluttdatoer for input til elhub_api
def create_date_list(start_date, number_of_dates): 
    start_date_object = datetime.strptime(start_date, '%Y-%m-%dT%H:%M:%S')
    start_dates = [start_date_object + timedelta(days=7*i) for i in range(number_of_dates)]
    dates_list = [date.strftime('%Y-%m-%dT%H:%M:%S') for date in start_dates]
    return dates_list

########################################
########################################
########################################

def show_charts(concatenated_df, type):
    st.write(f"**{type}**")
    concatenated_df = concatenated_df[concatenated_df['forbruker'] == type]
    st.bar_chart(concatenated_df, x = 'tidspunkt', y = 'kW') # plotter dataframen i streamlit
    c1, c2 = st.columns(2)
    with c1:
        st.metric("Energi", value = f"{int(np.sum(concatenated_df['kW'])):,} kWh".replace(",", " "))
    with c2:
        st.metric("Maksimal effekt", value = f"{int(np.max(concatenated_df['kW'])):,} kWh".replace(",", " "))

# kjøring av skriptet
if __name__ == '__main__':
    with open("main.css") as f:
        st.markdown("<style>{}</style>".format(f.read()), unsafe_allow_html=True)

    st.title("Test av Elhub API")
    year = st.number_input("År", value = 2023, min_value = 2021, max_value = 2023)
    weeks = st.number_input("Antall uker fra 1. januar", min_value = 1, max_value = 52, value = 1)
    municipality = st.selectbox("Kommune", options = ["Fredrikstad", "Sarpsborg"])
    if municipality == "Fredrikstad":
        id = '3107'
    else:
        id = '3105'
    start_date_list = create_date_list(start_date = f'{year}-01-01T00:00:00', number_of_dates = weeks)
    end_date_list = create_date_list(start_date = f'{year}-01-07T23:59:00', number_of_dates = weeks)
    df_list = []
    with st.spinner("Ved mange uker kan uthentingen av data fra API'et ta litt tid..."):
        for i in range(0, len(start_date_list)): # løkke gjennom datolisten
            #st.write(f"Iterasjon nr. {i}")
            start_date = start_date_list[i]
            end_date = end_date_list[i]
            
            try:
                df = elhub_api(start_date = start_date, end_date = end_date, id = id) # kaller Elhub API og skriver skriver til dataframe
                df_list.append(df) # legger dataframe i en liste. Bygger opp en liste med dataframes. 
            except Exception: 
                pass # om Elhub API feiler på en iterasjon-> skriptet fortsetter
        
        concatenated_df = pd.concat(df_list, ignore_index=True) # trekker sammen listen til en stor dataframe

        st.markdown("---")
        show_charts(concatenated_df, type = "business")
        st.markdown("---")
        show_charts(concatenated_df, type = "industry")
        st.markdown("---")
        show_charts(concatenated_df, type = "private")
               