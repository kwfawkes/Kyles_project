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
	combination_data = data_munge_monthly(dataset, dataset.sea_surface_temperature, dataset.sig_wave_height)

	# plotting and saving a linear regression model for sea surface temperature and significant wave height over all months between 2009 and 2012
	linear_regression(combination_data.sea_surface_temperature, combination_data.sig_wave_height, savename)


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
    
def linear_model_plot(x_variable, y_variable):
    '''Function develops linear model for x and y variable inputs and plots regression line on top of scatter plot'''
    
    assert len(x_variable) > 1, 'length of x_variable should be larger than 1'
    assert len(y_variable) > 1, 'length of y_variable should be larger than 1'
    
    # assigning function variables to response and predictor variables
    y = y_variable # response variable
    X = x_variable # predictor variable
    X = sm.add_constant(X)  # Adds a constant term to the predictor (essential to obtain the constant in the formula)
    
    # Calculating the linear model for the two variables
    lm = sm.formula.OLS(y, X).fit()
    
    # Developing the plot of the linear model
    # making a range of the x variable to pass to the y prediction
    x_pred = np.linspace(x_variable.min(), x_variable.max())
    
    # Adding a constant to this range of x values (essential to obtain the constant in the formula)
    x_pred2 = sm.add_constant(x_pred)

    # Passing the linear model predictor the range of x values to model over
    y_pred = lm.predict(x_pred2)

    # Plotting these predicitons on the graph
    plt.plot(x_pred, y_pred, color='k', linewidth=2)

    # Obtaining linear regression 
    return plt.plot()
    
def linear_regression(x_variable, y_variable, savename):
    '''This function produces a plot showing the linear 
    regression line between two specified varaibles '''
    
    assert len(x_variable) > 1, 'length of x_variable should be larger than 1'
    assert len(y_variable) > 1, 'length of y_variable should be larger than 1'
    
    # adjusting the figure size
    fig = plt.figure(figsize=(10, 7)) 
    # Creating a title for the plot
    plt.title(x_variable.name, fontsize=16, y=1.01)
    
    # Plroducing scatter plot of relationship between two varaibles
    plt.scatter(x_variable, y_variable)
    
    # Creates the linear model and applies linear regression to subplot
    linear_model_plot(x_variable, y_variable)
    
    
    # Creating axis labels and title
    plt.ylabel(x_variable.name)
    plt.xlabel(y_variable.name)
    
    plt.savefig('../results/computational_experiments/'+savename+'.pdf')
    
main()