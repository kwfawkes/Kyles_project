#!/bin/bash
# Kyle Fawkes, November 17, 2015


# Shell script for 'On the Edge of Discovery': Zooplankton Abundance in the Discovery Passage


# Plots time-series of sea surface temperature, significant wave height, and Zooplankton Abundance for spring blooms 
python p_tseries.py 2012 '../data/c46131.csv' '../data/Zooplankton_2009-2012.csv' 'plankton_timeseries_2012'
python p_tseries.py 2011 '../data/c46131.csv' '../data/Zooplankton_2009-2012.csv' 'plankton_timeseries_2011'
python p_tseries.py 2010 '../data/c46131.csv' '../data/Zooplankton_2009-2012.csv' 'plankton_timeseries_2010'
python p_tseries.py 2009 '../data/c46131.csv' '../data/Zooplankton_2009-2012.csv' 'plankton_timeseries_2009'

# Makes a linear regression plot of sea surface temperature and significant wave height
python linear_regression.py '../data/c46131.csv' 'wave_temp_plot'

# Makes a linear model of relationship between sea surface temperature and significant wave height
# Extracts p-values and r-squared value in a dataframe
python linear_model.py '../data/c46131.csv' 'wave_temp'

# Makes a multivariate linear model for sea surface temperature, significant wave height, and Zooplankton Abundance 
# Extracts p-values in a dataframe for spring blooms between 2009 and 2012
python p_values.py '../data/c46131.csv' '../data/Zooplankton_2009-2012.csv' 'p_value' 

# Makes a multivariate linear model for sea surface temperature, significant wave height, and Zooplankton Abundance 
# Extracts r-squared values in a dataframe for spring blooms between 2009 and 2012
python r_squared.py '../data/c46131.csv' '../data/Zooplankton_2009-2012.csv' 'r_squared' 