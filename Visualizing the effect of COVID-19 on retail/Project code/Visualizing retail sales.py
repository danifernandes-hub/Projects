#Basic data processing libraries
import pandas as pd
import numpy as np


#Graph Libraries
import cufflinks as cf
import chart_studio.plotly as py1
import plotly.express as px
import plotly.offline as py
py.init_notebook_mode()
from plotly import tools
cf.go_offline()
py.init_notebook_mode(connected=True)
from plotly.offline import init_notebook_mode, iplot
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

#Reading the data and checking out the results

retail_year = {}

for year in range(2):
    retail_year[year] = pd.read_excel('../Data/mrtssales92-present.xls', sheet_name = year, skiprows = [0, 1, 2])
    retail_year[year] = retail_year[year].loc[:, ~retail_year[year].isnull().all(axis=0)]
    retail_year[year].columns = list(retail_year[year].columns[0:2]) + list(retail_year[year].iloc[0].dropna())
    retail_year[year] = retail_year[year].iloc[1:]
    
retail_year[0].head(20)

#Dividing data into adjusted and unadjusted 
adjusted = {}
not_adjusted = {}

for year in range(2):
    adjust_index = retail_year[year][retail_year[year]['Kind of Business'] == 'ADJUSTED(2)'].index.values.astype(int)
    not_adjusted[year] = retail_year[year].iloc[0:int(adjust_index)]
    adjusted[year] = retail_year[year].iloc[int(adjust_index):]
    adjusted[year] = adjusted[year].loc[:, ~adjusted[year].isnull().all(axis=0)]


#Isolating retail data from 2020
retail_2020 = adjusted[0].reset_index(drop = True)[0:38]
months = ['Jan. 2020', 'Feb. 2020', 'Mar. 2020', 'Apr. 2020', 'May 2020 (p)']
for month in months:
    retail_2020[month] = retail_2020[month].replace('(S)', '0').astype(float)

#dropping Jewelry Stores from the dataset because it lacks data
retail_2020.drop(26, axis = 0, inplace = True)

#Graphing the impact in a line
line = pd.Series(retail_2020.iloc[0, 1:])
line[1:].iplot(kind='line',
         values='Retail and food services sales', 
         title='Fall in absolute numbers', color = ['#00CED1'], width = 4, xaxis_title='Month',
                   yaxis_title='Million of dollars')

#Obtaining relative variations
retail_2019 = adjusted[1].reset_index(drop = True)
retail_2020_relative = retail_2020.copy()
for month in months:
    if month == 'Jan. 2020':
        retail_2020_relative[month] = ((retail_2020_relative[month].astype(float) - retail_2019['Dec. 2019'].astype(float))/retail_2019['Dec. 2019'].astype(float))*100
    else:
        index = months.index(month) - 1
        retail_2020_relative[month] = ((retail_2020_relative[month] - retail_2020[months[index]])/retail_2020[months[index]])*100
        
#Checking out the results
retail_2020_relative.head()

#Month-Month %variation
line = pd.Series(retail_2020_relative.iloc[0, 1:])

fig = px.bar(line, x=line.index.values.tolist()[1:], y=line[1:], text = line[1:], template='plotly_white', 
             hover_name= line.index.values.tolist()[1:])

fig.update_traces(marker_color='#80dfff', marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=0.45, textposition='outside', texttemplate = '%{text:.2f}', 
                  hovertemplate=None, hoverinfo='skip')

fig.update_layout(title_text='Month-Month % variation in 2020', xaxis=dict(showgrid=False, zeroline=True),
    yaxis=dict(showgrid=False, zeroline=True), uniformtext_minsize=8, uniformtext_mode='hide')

fig.update_xaxes(showline=True, linewidth=0.5, linecolor='white', title_text='')
fig.update_yaxes(showline=True, linewidth=1.5, linecolor='lightgray', zerolinecolor='lightgray', title_text='')


fig.show()

#Graphing variations in January
retail_2020_relative['variation'] = retail_2020_relative['Jan. 2020'].apply(lambda x: '+' if x > 0 else '-')

fig = px.bar(retail_2020_relative[7:].sort_values(by = 'Jan. 2020'), y='Kind of Business', color = 'variation',
             x='Jan. 2020', template='plotly_white', width=900, height=850, 
            color_discrete_sequence = ['#DB4437', '#00CED1'])

fig.update_layout(title_text='% Growth of retail sales in the USA by sector in January 2020', 
                  showlegend=False, xaxis=dict(showgrid=True),
    yaxis=dict(showgrid=True))
fig.show()

#Graphing variations in February
retail_2020_relative['variation'] = retail_2020_relative['Feb. 2020'].apply(lambda x: '+' if x > 0 else '-')

fig = px.bar(retail_2020_relative[7:].sort_values(by = 'Feb. 2020'), y='Kind of Business', color = 'variation',
             x='Feb. 2020', template='plotly_white', width=900, height=850, 
            color_discrete_sequence = ['#DB4437', '#00CED1'])

fig.update_layout(title_text='% Growth of retail sales in the USA by sector in February 2020', 
                  showlegend=False, xaxis=dict(showgrid=True),
    yaxis=dict(showgrid=True))
fig.show()

retail_2020_relative['variation'] = retail_2020_relative['Mar. 2020'].apply(lambda x: '+' if x > 0 else '-')

#Graphing variations in March
fig = px.bar(retail_2020_relative[7:].sort_values(by = 'Mar. 2020'), y='Kind of Business', color = 'variation',
             x='Mar. 2020', template='plotly_white', width=900, height=850, 
            color_discrete_sequence = ['#DB4437', '#00CED1'])

fig.update_layout(title_text='% Growth of retail sales in the USA by sector in March 2020', showlegend = False)
fig.show()

#Graphing variations in April
retail_2020_relative['variation'] = retail_2020_relative['Apr. 2020'].apply(lambda x: '+' if x > 0 else '-')


fig = px.bar(retail_2020_relative[7:].sort_values(by = 'Apr. 2020'), y='Kind of Business', color = 'variation',
             x='Apr. 2020', template='plotly_white', width=900, height=850, 
            color_discrete_sequence = ['#DB4437', '#00CED1'])

fig.update_layout(title_text='% Growth of retail sales in the USA by sector in April 2020', showlegend = False)
fig.show()

#Plotting recovery
fig = px.bar(retail_2020_relative[7:].sort_values(by = 'May 2020 (p)', ascending = True).tail(10), y='Kind of Business',
             x='May 2020 (p)', template='plotly_white', width=950, height=450, text = 'May 2020 (p)')

fig.update_traces(marker_color='#00CED1',
                  marker_line_width=1.5, opacity=0.85, textposition='inside', texttemplate = '%{text:.2f}%')

fig.update_xaxes(showline=True, linewidth=0.5, linecolor='white', title_text='')
fig.update_yaxes(showline=True, linewidth=1.5, linecolor='lightgray', zerolinecolor='lightgray', title_text='')

fig.update_layout(title_text='Top 10 Sales Recovery by Sector')
fig.show()

#May vs Jan plot
retail_2020['total_effect'] = ((retail_2020['May 2020 (p)'] - retail_2020['Jan. 2020'])/retail_2020['Jan. 2020']) * 100
retail_2020['variation'] = retail_2020['total_effect'].apply(lambda x: '+' if x > 0 else '-')


fig = px.bar(retail_2020[7:].sort_values(by = 'total_effect'), y='Kind of Business', color = 'variation',
             x='total_effect', template='plotly_white', width=900, height=850, 
            color_discrete_sequence = ['#DB4437', '#00CED1'])

fig.update_layout(title_text='% Variation in sales from January to May, by sector', showlegend = False)
fig.show()
