import requests 
import plotly.express as px
import plotly.graph_objects as pgo
import pandas as pd
# api token for REDcap: DD0E88BF0EF8E12ACD577F664A515337

all_scales = ['goitre39', 'hyperthyroidscore', 'hypothyroidscore', 'eyescore', 'tirednessscore',
                    'cognitivescore', 'anxietyscore', 'depressivityscore', 'emotionalscore', 'sociallifescore',
                    'dailylifescore','cosmeticscore','overallqolscore','compositescore']

# ------------------------------------------------------------------------------------ #

def fetch_n_data_list(recordID, scales): # contacts the API and returns a 2D list with thypro scores for a recordID
    api_call = { 
        'token': 'DD0E88BF0EF8E12ACD577F664A515337', # api token
        'content': 'record',
        'format': 'json',
        'type': 'flat',
        'records[0]': f'{recordID}', # hvilken record du vil svar ud for
        'fields[0]': '', # er initially None
        'forms[0]': 'record_id', # specifies we are searching with a recordID
        'returnFormat': 'json'}
        
    thypro_scale_values= {}
    for scale in scales: # makes the list for holding the data
        thypro_scale_values[f'{scale}'] = 0 # tilføjer skalaen til dicten

        api_call['fields[0]'] = scale
        response = requests.post('https://redcap.regionh.dk/api/', data=api_call) # contacts the API and gets the response

        if (str(response.status_code) == '200'): # if the API call is succesfull
            json_response = response.json()

            scale_value = json_response[0][scale] 
            if(scale_value == '-1' or scale_value == ''): # if a value is not present, it returns -1 or maybe ''?? 
                scale_value = 0
        
            thypro_scale_values[scale] = scale_value # updates the result from the API call in the stored dict
        else:
            print(f"HTTP get request failed with {str(response.status_code)} status code")

    values_raw = [float(x) for x in list(thypro_scale_values.values())] # a list with only the values from thypro_scale_values dict
    scales_raw = [x for x in list(thypro_scale_values.keys())]
    all_data = [scales_raw, values_raw]
    print(all_data)

    return all_data

# ------------------------------------------------------------------------------------ #

def plot_radar(scales, values, values1=None, values2=None): # function for plotting ThyPRO data
    fig = pgo.Figure() 

    fig.add_trace(pgo.Scatterpolar(r=values, theta=scales, name='Record A'))

    if(values1 != None):
        fig.add_trace(pgo.Scatterpolar(r=values1, theta=scales, name='Record B'))

    if(values2 != None):
        fig.add_trace(pgo.Scatterpolar(r=values2, theta=scales, name='Record C'))
    
    fig.update_layout(polar=dict(radialaxis=dict(visible=True,range=[0, 100])),showlegend=True)
    fig.show()

# ------------------------------------------------------------------------------------ # 

def plot_line(scales_list, recordID_list): # er ind the making

    all_values_for_single_scale = []

    for scale in scales_list:
        for recordID in recordID_list:
            data_result = fetch_n_data_list(recordID, scale) # returnerer 2D liste med resultaterne
            all_values_for_single_scale.append(data_result[1])

    dataframe = pd.DataFrame(dict(r=values, theta=scale))
    fig = px.line(dataframe, x=scale, y=all_values_for_single_scale, title='ThyPRO Score')
    
    fig.show()

# ------------------------------------------------------------------------------------ # 


# --- Main --- #
# records that work: 29, 28, 27
#thypro_results2 = fetch_full_data_list(24)
#thypro_results1 = fetch_full_data_list(27) # method call - returns a 2D list
thypro_results = fetch_n_data_list(28, ['goitre39', 'hyperthyroidscore', 'hypothyroidscore'])
plot_radar(thypro_results[0], thypro_results[1]) # method call for plotting the data
