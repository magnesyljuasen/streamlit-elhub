
comments = """
st.markdown("---")
start_date = '2023-01-08T00:00:00'
end_date = '2023-01-15T00:00:00'
id = '3107'
url = f"https://api.elhub.no/energy-data/v0/municipalities/{id}?dataset=CONSUMPTION_PER_GROUP_MUNICIPALITY_HOUR&startDate={start_date}%2B02:00&endDate={end_date}%2B02:00&productionGroup=hydro"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    # Process the data as needed
    #st.write(data)
    hourly_data = (data['data'][0]['attributes']['consumptionPerGroupMunicipalityHour'])
    production_list = []
    time_list = []
    for i in range(0, len(hourly_data)):
        production_list.append(hourly_data[i]['quantityKwh'])
        time_list.append(hourly_data[i]['startTime'])
    st.caption(f"Forbruk i kommune {id} fra {start_date} til {end_date}")
    df = pd.DataFrame({
        'time' : time_list,
        'kWh' : production_list
    })
    st.bar_chart(df, x = 'time', y = 'kWh')
else:
    st.write(f"Error: {response.status_code} - {response.text}")

st.markdown("---")
start_date = '2023-01-15T00:00:00'
end_date = '2023-01-22T00:00:00'
id = '3107'
url = f"https://api.elhub.no/energy-data/v0/municipalities/{id}?dataset=CONSUMPTION_PER_GROUP_MUNICIPALITY_HOUR&startDate={start_date}%2B02:00&endDate={end_date}%2B02:00&productionGroup=hydro"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    # Process the data as needed
    #st.write(data)
    hourly_data = (data['data'][0]['attributes']['consumptionPerGroupMunicipalityHour'])
    production_list = []
    time_list = []
    for i in range(0, len(hourly_data)):
        production_list.append(hourly_data[i]['quantityKwh'])
        time_list.append(hourly_data[i]['startTime'])
    st.caption(f"Forbruk i kommune {id} fra {start_date} til {end_date}")
    df = pd.DataFrame({
        'time' : time_list,
        'kWh' : production_list
    })
    st.bar_chart(df, x = 'time', y = 'kWh')
else:
    st.write(f"Error: {response.status_code} - {response.text}")


with st.expander("NO1"):
    st.header("NO1")
    st.markdown("---")
    start_date = '2023-09-01T00:00:00'
    end_date = '2023-10-01T00:00:00'
    url = f"https://api.elhub.no/energy-data/v0/price-areas?dataset=PRODUCTION_PER_GROUP_MBA_HOUR&startDate={start_date}%2B02:00&endDate={end_date}%2B02:00&productionGroup=hydro"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        # Process the data as needed
        #st.write(data)
        hourly_data = (data['data'][0]['attributes']['productionPerGroupMbaHour'])
        production_list = []
        for i in range(0, len(hourly_data)):
            production_list.append(hourly_data[i]['quantityKwh'])
        st.caption(f"Forbruk i NO1 (kWh) fra {start_date} til {end_date}")
        st.bar_chart(production_list)
        st.write(f"Antall dager: {len(production_list) / 24}")
    else:
        st.write(f"Error: {response.status_code} - {response.text}")

"""