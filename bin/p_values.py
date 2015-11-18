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
filename_1 = sys.argv[1]
filename_2 =sys.argv[2]
savename = sys.argv[3]

def main():

	# loading datasets into python using data_load function
	# assigning a variable to these loaded datasets for future reference
	gwv_data = data_load(filename_1)
	zoo = data_load(filename_2)
	
	# Using spring_wk function to munge data and develop a new dataframe for munged data
	# Munging to average significant wave height, sea surface temperature and Zooplankton Abundance weekly over the spring plankton bloom season for each year of plankton collection  
	comb_2012 = spring_wk(2012, gwv_data.sig_wave_height, gwv_data.sea_surface_temperature, zoo.Total_Zooplankton_Abundance)
	comb_2011 = spring_wk(2011, gwv_data.sig_wave_height, gwv_data.sea_surface_temperature, zoo.Total_Zooplankton_Abundance)
	comb_2010 = spring_wk(2010, gwv_data.sig_wave_height, gwv_data.sea_surface_temperature, zoo.Total_Zooplankton_Abundance)
	comb_2009 = spring_wk(2009, gwv_data.sig_wave_height, gwv_data.sea_surface_temperature, zoo.Total_Zooplankton_Abundance)
	
	# Making a multivariate linear model for significant wave height, sea surface temperature, and Zooplankton Abundance for each spring bloom season
	lm_2012 = linear_model_multi_interaction(comb_2012.sig_wave_height, comb_2012.sea_surface_temperature, comb_2012.Total_Zooplankton_Abundance)
	lm_2011 = linear_model_multi_interaction(comb_2011.sig_wave_height, comb_2011.sea_surface_temperature, comb_2011.Total_Zooplankton_Abundance)
	lm_2010 = linear_model_multi_interaction(comb_2010.sig_wave_height, comb_2010.sea_surface_temperature, comb_2010.Total_Zooplankton_Abundance)
	lm_2009 = linear_model_multi_interaction(comb_2009.sig_wave_height, comb_2009.sea_surface_temperature, comb_2009.Total_Zooplankton_Abundance)

	# Making a table to hold the p-value from each spring's multivariate linear model
	p_2012 = pvalue_table(2012, lm_2012)
	p_2011 = pvalue_table(2011, lm_2011)
	p_2010 = pvalue_table(2010, lm_2010)
	p_2009 = pvalue_table(2009, lm_2009)
	
	# Combines all the tables together for easy comparison and saves master table to the results folder
	master_ptable(p_2012, p_2011, p_2010, p_2009, savename)

def data_load(filename):
	'''For each dataset: Loads data in CSV format, produces pandas dataframe for data, 
	and converts index to datetime, only inputs required are 
	 the file paths'''
	''' input must have date column labeled 'DATE', and file path 
	must be in quotes'''
	
	# loading the first dataset and changing the index column to the date
	dataset = pd.read_csv(filename, sep=',', index_col='DATE')
	# converting the date index to datetime
	dataset.index = pd.to_datetime(dataset.index)
	
	return dataset

def spring_wk(year, column_1, column_2, column_3):
	'''For either of my two datasets, this function will average any 3 variables
	on a weekly basis for any spring between 2009-2012. The outputs of this munged data 
	is inserted into a new dataframe'''
	
	assert 2009 <= int(year) <= 2012, 'Year should be between 2009 and 2012'
	assert len(column_1) > 1, 'column should must have at least one entry'
	assert len(column_2) > 1, 'column should must have at least one entry'
	assert len(column_3) > 1, 'column should must have at least one entry'
	
	# Resampling the columns from dataset_1 into weekly averages
	column_1_weekly = column_1.resample('W', how=('mean'))
	column_2_weekly = column_2.resample('W', how=('mean'))
       
	# Subsetting the columns from dataset_1 for the spring plankton bloom in the specified year
	if year == 2009:
		first = '2009-02-24'
		last = '2009-07-05' 
	if year == 2010:
		first = '2010-03-03'
		last = '2010-6-28'   
	if year == 2011:
		first = '2011-03-07'
		last = '2011-07-03'
	if year == 2012:
		first = '2012-03-30'
		last = '2012-07-01'
	print(first)
	column_1_weekly_year = column_1_weekly[first:last]
	column_2_weekly_year = column_2_weekly[first:last]
	

	# dropping the rows where naN's are present in dataset_1
	column_1_weekly_year_new = column_1_weekly_year.dropna()
	column_2_weekly_year_new = column_2_weekly_year.dropna()
	
	# Now resampling column from dataset_2 into weekly averages over the desired spring
	if year == 2009:
		yr = '2009'
	if year == 2010:
		yr = '2010'
	if year == 2011:
		yr = '2011'
	if year == 2012:
		yr = '2012'
	column_3_year = column_3[yr]
	column_3_year_weekly = column_3_year.resample('W', how=('mean'))
	
	# Combines the three columns across the two datasets into a single dataframe
	combination_data = pd.DataFrame({column_1.name : column_1_weekly_year_new, column_2.name : column_2_weekly_year_new, column_3.name : column_3_year_weekly})
	
	return combination_data
	
def linear_model_multi_interaction(x1_variable, x2_variable, y_variable):
    '''Function creates multivaraite interaction linear model and produces 
    a statistical summary'''
    
    assert len(x1_variable) > 1, 'The length of x variable 1 should be larger than 1'
    assert len(x2_variable) > 1, 'The length of x variable 2 should be larger than 1'
    assert len(y_variable) > 1, 'The length of the y variable should be larger than 1'
    
    # Assigning a variable to y_variable input
    Y = y_variable
    # Creating a dataframe to hold both x variables and their interaction term
    X = pd.DataFrame({x1_variable.name :x1_variable, x2_variable.name :x2_variable, x2_variable.name+' '+'&'+' '+ x1_variable.name:(x1_variable*x2_variable)})
    # Adding a constant to the dataframe (essential to obtain the constant in the linear model)
    X = sm.add_constant(X)
    
    # Producing a multivariate linear model with an interaction term
    lm = sm.OLS(Y, X).fit()
    
    # Returning this linear model
    return lm
        
def pvalue_table(year, linear_model):
    '''Function creates a table of p-values for a specified 
    linear model. Only required inputs are the year linear 
    model data and linear model name'''
    
    assert 2009 <= year <=2012, 'The year should be between 2009 and 2012'
    
    # Inputting the linear model p-values into a dataframe
    # Contextual information added into dataframe
    # Dataframe assigned to a variable
    lmp_1 = pd.DataFrame({'value': linear_model.pvalues, 'test': 'linear regression', 'year': year})
    
    # Changing the index column to years
    # Creating a new column for index inputs (doubling the index column)
    lmp_1.insert(3, 'variable',lmp_1.index)
    # changing the index to year (doubling the year column)
    lmp_1.index = lmp_1.year
    # Deleting the extra year column
    del lmp_1['year']
    
    # returning the p-value table
    return lmp_1
    
def master_ptable(p_1, p_2, p_3, p_4, savename):
    '''Function combines four p-value tables toegther into a master table.
    Function requires 4 p-value tables (must have the same column titles),
    and a savename in quotations as input'''
    
    assert type(savename) == str, 'the savename must be in a string format'
    
    # appending the tables together to create a master table
    p_a = p_1.append(p_2)
    p_b = p_a.append(p_3)
    p_c = p_b.append(p_4)
    
    # saving the table under the specified savename into project results
    p_c.to_csv('../results/computational_experiments/'+savename+'.csv')

main()