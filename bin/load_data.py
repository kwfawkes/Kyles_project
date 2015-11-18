# importing packages
import sys
import pandas as pd


def main():
	script = sys.argv[0]
	filename_1 = sys.argv[1]
	filename_2 = sys.argv[2]
	data_name_1 = sys.argv[3]
	data_name_2 = sys.argv[4]




def data_load_2(filename_1, filename_2):
    '''For each dataset: Loads data in CSV format, produces pandas dataframe for data, 
    and converts index to datetime, only inputs required are 
    the file paths'''
    ''' input must have date column labeled 'DATE', and file path 
    must be in quotes'''
    
    # loading the first dataset and changing the index column to the date
    dataset_1 = pd.read_csv(filename_1, sep=',', index_col='DATE')
    # converting the date index to datetime
    dataset_1.index = pd.to_datetime(dataset_1.index)
    # Saving data to results and computational experiments folders
    dataset_1.save('../results/computational_experiments/'+ data_name_1)

    
    # loading the second dataset and changing the index column to the date
    dataset_2 = pd.read_csv(filename_2, sep=',', index_col='DATE')
    # converting the date index to datetime
    dataset_2.index = pd.to_datetime(dataset_2.index)
    # Saving data to results and computational experiments folders
    dataset_1.save('../results/computational_experiments/'+ data_name_2)
