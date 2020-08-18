import pandas as pd
from bs4 import BeautifulSoup
import requests

#URL
URL = 'https://www.aphis.usda.gov/aphis/ourfocus/animalhealth/sa_one_health/sars-cov-2-animals-us'

#Final list of results
list_of_results = []

#Scraping the data
animals = requests.get(URL)
animals_content = animals.content
parser = BeautifulSoup(animals_content, 'html.parser')
results1 = parser.find_all('tbody')
for x in results1:
    element = x.find_all('td')
    for y in element: 
        list_of_results.append(y.text.replace('\n', '').strip())
        
#Separating the data into different lists
animals = list_of_results[0::4]
date = list_of_results[1::4]
state = list_of_results[2::4]
method = list_of_results[3::4]

#Making a dataframe to work from
data = pd.DataFrame()
data[animals[0]] = animals[1:]
data[date[0]] = date[1:]
data[state[0]] = state[1:]
data[method[0]] = method[1:]

#Original dataset that will remain untouched through the analysis
original = data

#Adding a column that checks whether or not the animal had contact with 

def human_checker(row):
    if '~' in row:
        return 'Yes'
    else: 
        return 'No'
data['Contact with infected Human'] = data['Type of Animal'].apply(human_checker)

#Taking care of weird data points
import re
pattern1 = r'([0-9]\s+\w+\s?)'

def replacer(row):
    rate = re.findall(pattern1, row)
    if not rate:
        return row
    else:
        if len(rate) > 1:
            new_string = []
            for each in rate:
                each = each.strip()
                pattern2 = r'([0-9])'
                match_num = re.findall(pattern2, each)
                pattern3 = r'(\s+\w+\s?)'
                match_animal = re.findall(pattern3, each)
                match_num = ''.join(str(e) for e in match_num)
                result = str(int(match_num) * match_animal)
                new_string.append(result)
            final = ' '.join(str(e) for e in new_string).strip()
            final = final.replace('[', '').replace(']', '').replace('\'', '').replace(',', '')
            return final  
        else:
            new_string = []
            rate = str(rate).strip()
            pattern2 = r'([0-9])'
            match_num = re.findall(pattern2, rate)
            match_num = ''.join(str(e) for e in match_num)
            pattern3 = r'(\s+\w+\s?)'
            match_animal = re.findall(pattern3, rate)
            new_string = int(match_num) * match_animal
            final = ''.join(str(e) for e in new_string).strip()
            return final
    
data['Type of Animal'] = data['Type of Animal'].apply(replacer)

#Separating the data
data['Type of Animal'] = data['Type of Animal'].str.strip()
data = data.set_index(['Date Confirmed', 'State', 'Method of Initial Diagnosis*', 
                       'Contact with infected Human']).apply(lambda x: x.str.split().explode()).reset_index()
data['Type of Animal'] = data['Type of Animal'].str.strip()
data['Type of Animal'] = data['Type of Animal'].str.replace(r's$', '').str.strip()

#Cleaning the data, starting with the type of animal (Tanking care of notes)
data['Type of Animal'] = data['Type of Animal'].apply(lambda x: x.split(',')[0])
data['Type of Animal'] = data['Type of Animal'].str.replace('~', '').str.strip() #getting rid of ~

#Isolating the month where each case was detected
data["Month"] = data['Date Confirmed'].apply(lambda x:x.split()[0])
data.drop('Date Confirmed', axis = 1, inplace = True)

#First graph, importing plotting libraries
import plotly.express as px

fig = px.pie(data, names = 'Contact with infected Human', title = 'Percentage of animals had exposure to a probable or confirmed human',
             color_discrete_sequence = ['#3BCCFF', '#FF3333'])

fig.update_layout(showlegend = False)

fig.update_traces(hole = 0.5)
fig.update_traces(textposition='inside', textinfo='percent+label')
fig.show()

fig = px.pie(data, names = 'Type of Animal', title = 'Percentage of cases by animal species',
             color_discrete_sequence = ['#3BCCFF', '#FF3333', '#FFD400', '#48FF48', '#DDA0DD'])

fig.update_traces(hole = 0.5)

fig.show()

#Second Graph, by the month they contracted the infection in
fig = px.histogram(data, x = 'Month', 
             template = 'plotly_white')

fig.update_traces(marker_color=['#3BCCFF', '#FF3333', '#FFD400', '#48FF48'])
'#0F9D58'
fig.update_layout(
    showlegend = False,
    title_text='Month when the infection was recorded', # title of plot
    xaxis_title_text='Month', # xaxis label
    yaxis_title_text='Count', # yaxis label
    bargap=0.1, # gap between bars of adjacent location coordinates
)

fig.show()

#Cases reported by state
fig = px.histogram(data, x = 'State', 
             template = 'plotly_white')


fig.update_traces(marker_color='#3BCCFF')

fig.update_xaxes(categoryorder = 'total descending')

fig.update_layout(
    showlegend = False,
    title_text='State where the infection was reported', # title of plot
    xaxis_title_text='State', # xaxis label
    yaxis_title_text='', # yaxis label
    bargap=0.4, # gap between bars of adjacent location coordinates
)

fig.show()

#Last Graph, test used to get the results
fig = px.pie(data, names = 'Method of Initial Diagnosis*', title = 'Cases detected by diagnosis method used',
             color_discrete_sequence = ['#3BCCFF', '#FF3333', '#FFD400', '#0F9D58'])

fig.update_traces(hole = 0.5)

fig.show()





