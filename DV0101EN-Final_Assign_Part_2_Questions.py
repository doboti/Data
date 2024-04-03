#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

# Load the data using pandas
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Set the title of the dashboard
#app.title = "Automobile Statistics Dashboard"

#---------------------------------------------------------------------------------
# Create the dropdown menu options
dropdown_options = [
    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
]
# List of years 
year_list = [i for i in range(1980, 2024, 1)]
#---------------------------------------------------------------------------------------
# Create the layout of the app
app.layout = html.Div([
    #TASK 2.1 Add title to the dashboard
    
    html.H1("Automobile Sales Statistics Dashboard", style={'textAlign': 'center', 'color': '#503D36', 'font-size': '24px'}),
    html.Div([#TASK 2.2: Add two dropdown menus
        html.Label("Select Report Type:"),
        dcc.Dropdown(
            id='dropdown-statistics',
            options=dropdown_options,
            value='Yearly Statistics',
            placeholder='Select a report type...',
            style={'width': '80%', 'padding': '3px', 'fontSize': '20px', 'textAlignLast': 'center'}
        )
    ]),
    html.Div([
        html.Label("Select Year:"),
        dcc.Dropdown(
            id='select-year',
            options=[{'label': str(i), 'value': i} for i in year_list],
            placeholder='Select a year...',
            style={'width': '80%', 'padding': '3px', 'fontSize': '20px', 'textAlignLast': 'center'}
        )
    ]),
    html.Div(id='output-container', className='chart-grid', style={'display': 'flex'})
])
#TASK 2.4: Creating Callbacks
# Callback to enable or disable the input container based on the selected statistics
@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Input(component_id='dropdown-statistics', component_property='value')
)
def update_input_container(selected_statistics):
    if selected_statistics == 'Yearly Statistics':
        return False
    else:
        return True

# Callback for plotting output graphs for the respective report types
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='select-year', component_property='value'), 
     Input(component_id='dropdown-statistics', component_property='value')]
)
def update_output_container(year_value, selected_statistics):
    # Filter the data for recession periods
    recession_data = data[data['Recession'] == 1]
    
    if selected_statistics == 'Recession Period Statistics':
        # Plot 1: Automobile sales fluctuate over recession period (year wise)
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(figure=px.line(yearly_rec, x='Year', y='Automobile_Sales', title="Average Automobile Sales fluctuation over Recession Period"))
        
        # Plot 2: Average number of vehicles sold by vehicle type
        average_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(figure=px.bar(average_sales, x='Vehicle_Type', y='Automobile_Sales', title='Average Vehicles Sold by Vehicle Type during Recession Period'))
        
        # Plot 3: Pie chart for total expenditure share by vehicle type during recessions
        if 'Expenditure' in recession_data.columns:
            exp_rec = recession_data.groupby('Vehicle_Type')['Expenditure'].sum().reset_index()
            R_chart3 = dcc.Graph(figure=px.pie(exp_rec, values='Expenditure', names='Vehicle_Type', title='Total Expenditure Share by Vehicle Type during Recession Period'))
        else:
            R_chart3 = html.Div("Expenditure data not available")
        
        # Plot 4: Bar chart for the effect of unemployment rate on vehicle type and sales
        if 'Unemployment_Rate' in recession_data.columns:
            unemployment_effect = recession_data.groupby(['Vehicle_Type', 'Unemployment_Rate'])['Automobile_Sales'].mean().reset_index()
            R_chart4 = dcc.Graph(figure=px.bar(unemployment_effect, x='Vehicle_Type', y='Automobile_Sales', color='Unemployment_Rate', title='Effect of Unemployment Rate on Vehicle Type and Sales during Recession Period'))
        else:
            R_chart4 = html.Div("Unemployment Rate data not available")
        
        return [html.Div(className='chart-item', children=[R_chart1, R_chart2]), 
                html.Div(className='chart-item', children=[R_chart3, R_chart4])]
    
    elif selected_statistics == 'Yearly Statistics':
        if year_value:
            yearly_data = data[data['Year'] == year_value]
            
            # Plot 1: Yearly Automobile sales using line chart for the whole period
            yas = yearly_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
            Y_chart1 = dcc.Graph(figure=px.line(yas, x='Year', y='Automobile_Sales', title='Yearly Automobile Sales for the Whole Period'))
            
            # Plot 2: Total monthly automobile sales using line chart
            monthly_sales = yearly_data.groupby('Month')['Automobile_Sales'].sum().reset_index()
            Y_chart2 = dcc.Graph(figure=px.line(monthly_sales, x='Month', y='Automobile_Sales', title='Total Monthly Automobile Sales'))
            
            # Plot 3: Bar chart for average number of vehicles sold during the given year
            average_sales = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
            Y_chart3 = dcc.Graph(figure=px.bar(average_sales, x='Vehicle_Type', y='Automobile_Sales', title='Average Vehicles Sold by Vehicle Type during the Year'))
            
            # Plot 4: Pie chart for total advertisement expenditure by vehicle type
            if 'Advertisement_Expenditure' in yearly_data.columns:
                ad_exp = yearly_data.groupby('Vehicle_Type')['Advertisement_Expenditure'].sum().reset_index()
                Y_chart4 = dcc.Graph(figure=px.pie(ad_exp, values='Advertisement_Expenditure', names='Vehicle_Type', title='Total Advertisement Expenditure by Vehicle Type during the Year'))
            else:
                Y_chart4 = html.Div("Advertisement Expenditure data not available")
            
            return [html.Div(className='chart-item', children=[Y_chart1, Y_chart2]), 
                    html.Div(className='chart-item', children=[Y_chart3, Y_chart4])]
        else:
            return None
    
    else:
        return None

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
