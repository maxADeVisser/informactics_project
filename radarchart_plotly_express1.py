import requests 
import plotly.express as px
import pandas as pd
# api token for REDcap: DD0E88BF0EF8E12ACD577F664A515337


def fetch_data_list(recordID): # contacts the API and returns a 2D list with thypro scores for a recordID
    api_call = { 
        'token': 'DD0E88BF0EF8E12ACD577F664A515337', # api token
        'content': 'record',
        'format': 'json',
        'type': 'flat',
        'records[0]': f'{recordID}', # hvilken record du vil svar ud for
        'fields[0]': '', # er initially None
        'forms[0]': 'record_id', # specifies we are searching with a recordID
        'returnFormat': 'json'
    }

    thypro_scale_values ={'goitre39' : 0, 'hyperthyroidscore' : 0, 'hypothyroidscore' : 0, 'eyescore' : 0, 'tirednessscore' : 0,
                    'cognitivescore' : 0, 'anxietyscore' : 0, 'depressivityscore' : 0, 'emotionalscore' : 0, 'sociallifescore' : 0,
                    'dailylifescore' : 0, 'cosmeticscore' : 0, 'overallqolscore' : 0, 'compositescore' : 0}

    scales_raw = list(thypro_scale_values.keys()) # makes a list of the keys in the dict thypro_scale_values

    for scale in scales_raw: # makes the list of holding the data
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
    all_data = [scales_raw, values_raw]

    return all_data

# ------------------------------------------------------------------------------------ # 

def plot_thyPRO_data(scales, values): # function for plotting ThyPRO data
    dataframe = pd.DataFrame(dict(r=values, theta=scales)) # creates a pandas dataframe with the inputs
    fig = px.line_polar(dataframe, r='r', theta='theta', line_close=True)
    fig.show()

# ------------------------------------------------------------------------------------ # 

# --- Main --- #
# records that work: 28, 27
#thypro_results = fetch_data_list(28) # method call - returns a 2D list
thypro_results = fetch_data_list(28)

plot_thyPRO_data(thypro_results[0], thypro_results[1]) # method call for plotting the data