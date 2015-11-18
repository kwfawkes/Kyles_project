# importing packages
import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# importing statistical packages
import statsmodels.api as sm
import scipy
from statsmodels.formula.api import ols

# defining variables for shell inputs using sys 
script = sys.argv[0]
filename = sys.argv[1]
savename = sys.argv[2]

def main():
	
	# loading the dataset desired 
	dataset = data_load(filename)
	
	# munging the data into monthly means over the timeline of the zooplankton collection 2009-2012
	background_data = data_munge_monthly(dataset, dataset.sea_surface_temperature, dataset.sig_wave_height)
	
	# Executing the linear model function for munged sea surface temperature and significant wave height data
	wave_temp = linear_model(background_data.sea_surface_temperature, background_data.sig_wave_height)
	
	# Creating a p-value table for significant wave height and sea surface temperature relationship
	p_wave_temp = extract_pvalues(wave_temp)
	
	# creating an r-value table for significant wave height and sea surface temperature relationship
	r_wave_temp = extract_rvalues(wave_temp)

	# Combining the r-squared table and the p-value table together and saving into results
	master_table(p_wave_temp, r_wave_temp, savename)
	
def data_load(filename):
    '''For each dataset: Loads data in CSV format, produces pandas dataframe for data, 
    and converts index to datetime, only inputs required are 
     the file paths'''
    ''' input must have date column labeled 'DATE', and file path 
    must be in quotes'''
    
    assert type(filename) == str, 'the filename should be a string'
    
    # loading the first dataset and changing the index column to the date
    dataset = pd.read_csv(filename, sep=',', index_col='DATE')
    # converting the date index to datetime
    dataset.index = pd.to_datetime(dataset.index)
    
    return dataset
    
def data_munge_monthly(dataset, column_1, column_2):
    '''Function munges data by resampling into monthly means,  
    subsetting over the zooplankton collection years and inputting 
    columns into a new table'''

    # Collapsing the data so that all data are averaged over an annual perdiod
    column_1_monthly = column_1.resample('M', how=('mean'))
    column_2_monthly = column_2.resample('M', how=('mean'))

    # Subsetting the data for the last 11 years (this is the time period for which the plankton data have been collected)
    column_1_monthly_modern = column_1_monthly['2009-01-01':'2012-10-31']
    column_2_monthly_modern = column_2_monthly['2009-01-01':'2012-10-31']

    # dropping the rows where naN's are present in anticipation of calculating the linear model
    column_1_monthly_modern = column_1_monthly_modern.dropna()
    column_2_monthly_modern = column_2_monthly_modern.dropna()
    
    # Combines both columns into one dataset
    combination_data = pd.DataFrame({column_1.name : column_1_monthly_modern, column_2.name : column_2_monthly_modern})
    return combination_data
    
def linear_model(x_variable, y_variable):
    '''Function creates linear model and produces 
    a statistical summary'''
    
     # assigning function variables to response and predictor variables
    y = y_variable # response
    X = x_variable # predictor
    X = sm.add_constant(X)  # Adds a constant term to the predictor (essential to obtain the constant in the formula)
    
    # Producing the linear model
    lm = sm.formula.OLS(y, X).fit()
    
    # returning the linear model's summary
    return lm
    
def extract_pvalues(linear_model):
    '''Function creates a table of p-values for a specified 
    linear model. Only required inputs are the year of linear 
    model data and linear model name'''
    
    # Inputting the linear model p-values into a dataframe
    # Contextual information added into dataframe
    # Dataframe assigned to a variable
    lmp_1 = pd.DataFrame({'value': linear_model.pvalues, 'test': 'linear regression', 'timeframe': '2009-2012', 'stat': 'p-value'})
    
    # Changing the index column to years
    # Creating a new column for index inputs (doubling the index column)
    lmp_1.insert(3, 'variable',lmp_1.index)
    # changing the index to year (doubling the year column)
    lmp_1.index = lmp_1.stat
    # Deleting the extra year column
    del lmp_1['stat']
    
    # returning the p-value table
    return lmp_1
    
def extract_rvalues(linear_model):
    '''Function creates a table of r-squared values for a specified 
    linear model. Only required input is the linear 
    model  name'''
    
    # Inputting the linear model r-squared values into a dataframe
    # Contextual information added into dataframe
    # Dataframe assigned to a variable
    lmp_2 = pd.DataFrame({ 'value' : [linear_model.rsquared], 'test': ['linear regression'], 'timeframe' : '2009-2012', 'stat': 'r-squared'})
    
    # Changing the index column to years
    # Creating a new column for index inputs (doubling the index column)
    lmp_2.insert(3, 'variable',lmp_2.index)
    # changing the index to stat (doubling the year column)
    lmp_2.index = lmp_2.stat
    # Deleting the extra year column
    del lmp_2['stat']
    
    # returing the r-squared table
    return lmp_2
    
def master_table(p_value_table, r_value_table, savename):
    '''Function combines r-squared and p-value tables toegther into a master table.
    Function requires 1 r-squared table, 1 p-value table (must have the same column titles),
    and a savename (must be in quotations) as input'''
    
    assert type(savename) == str, 'the savename must be in a string format'
    
    # appending the tables together to create a master table
    r_a = p_value_table.append(r_value_table)
    
    r_a.to_csv('../results/computational_experiments/'+savename+'.csv')

main()  