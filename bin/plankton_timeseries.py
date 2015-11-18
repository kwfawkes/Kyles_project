# importing packages
import sys
import pandas as pd
import matplotlib.pyplot as plt

# defining variables for shell inputs using sys 
script = sys.argv[0]
filename_1 = sys.argv[1]
filename_2 = sys.argv[2]
year = int(sys.argv[3])

def main():
	# Loading both my datasets
	gwv_data = data_load(filename_1)
	zoo = data_load(filename_2)
	
	# applying the spring wk function to munge the data and input to a new dataframe
	# Averages 3 variables on a weekly basis for input year, and outputs data into a new dataframe 
	combination_data = spring_wk(year, gwv_data.sig_wave_height, gwv_data.sea_surface_temperature, zoo.Total_Zooplankton_Abundance)
	
	# applying the timeseries function to plot the 3 variables over the spring bloom season for the desired year
	timeseries(comb_2012, comb_2012.sig_wave_height, comb_2012.sea_surface_temperature, comb_2012.Total_Zooplankton_Abundance, 'time-series_2012')
	
	
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
	
def spring_wk(year, column_1, column_2, column_3):
    '''For either of my two datasets, this function will average any 3 variables
     on a weekly basis for any spring between 2009-2012. The outputs of this munged data 
     is inserted into a new dataframe'''
    
    assert 2009 <= year <= 2012, 'Year should be between 2009 and 2012'
    assert len(column_1) > 1
    assert len(column_2) > 1
    assert len(column_3) > 1
    #assert dataset_1.index.name == 'DATE', 'index should be in terms of date and named DATE'
    #assert dataset_2.index.name == 'DATE', 'index should be in terms of date and named DATE'
    
    # Ensuring dataset_1 index (time) is in pandas datetime format
    #dataset_1.index = pd.to_datetime(dataset_1.index, unit='m')

    # Resampling the columns from dataset_1 into weekly averages
    column_1_weekly = column_1.resample('W', how=('mean'))
    column_2_weekly = column_2.resample('W', how=('mean'))
    
    # Subsetting the columns from dataset_1 for the spring plankton bloom in the specified year
    if year == 2009:
        first ='2009-02-24'
        last = '2009-07-05' 
    if year == 2010:
        first = '2010-03-03'
        last = '2010-6-28'   
    if year == 2011:
        first = '2011-03-07'
        last = '2011-07-03'
    if year == 2012:
        first ='2012-03-30'
        last = '2012-07-01'
    column_1_weekly_year = column_1_weekly[first:last]
    column_2_weekly_year = column_2_weekly[first:last]

    # dropping the rows where naN's are present in dataset_1
    column_1_weekly_year_new = column_1_weekly_year.dropna()
    column_2_weekly_year_new = column_2_weekly_year.dropna()
    
    # Ensuring dataset_2 index (time) in in pandas datetime format
    #dataset_2.index = pd.to_datetime(dataset_2.index, unit='d')
    
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
    combination_data = combination_data.dropna()
    
    return combination_data
	
def timeseries(dataset, variable_1, variable_2, variable_3, savename):
    '''Function plots any three varaibles into timeseries plot and saves plot. 
    Only required inputs are dataset name, 3 variables of interest in the format:
    dataset.column_name and the savename in quotations'''
    
    assert type(savename) == str, 'the output file name (savename) must be a string'
    assert len(dataset) > 1, 'dataset should have a length of more than 1 in order to plot'
    
    fig = plt.figure(figsize=(11, 8)) 
    
    # layering the three axes, which contain the three varaibles, on top of one another to create a single subplot
    # layering completed with twinx() method
    ax1 = plt.subplot()
    ax2 = ax1.twinx()
    ax3 = ax1.twinx()
    
    # plotting the 3 variables into the predetermined plot outlined above
    # Setting the color and width of lines on the graph
    ax1.plot(dataset.index, variable_1, 'k-', linewidth =2)
    ax2.plot(dataset.index, variable_2, 'grey', linewidth=2)
    ax3.plot(dataset.index, variable_3, 'g-', linewidth=4)
    
    # moving the spine that the zooplankton was plotted onto towards the right so it isnt on top of the second spine(ax2)
    variable_3_spine = ax3.spines['right']
    variable_3_spine.set_position(('axes', 1.2))

    # Adjusting the color of the axes ticks to match line color
    ax1.yaxis.set_tick_params(labelcolor='k')
    ax2.yaxis.set_tick_params(labelcolor='grey')
    ax3.yaxis.set_tick_params(labelcolor='green')
    
    # Making axes labels, selecting their color, and selecting their size
    ax1.set_xlabel(dataset.index.name, fontsize=14, y=0)
    ax1.set_ylabel(variable_1.name, fontsize = 13, color ='k')
    ax2.set_ylabel(variable_2.name + '($^o$C)', fontsize = 13, color='grey')
    ax3.set_ylabel(variable_3.name + '(m$^3$)', fontsize = 13, color='g')
    
    plt.savefig('../results/computational_experiments/'+savename+'.pdf')

main()
