import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) #in order to find main.py

import pytest
import pandas as pd
from main import *

@pytest.fixture
def input_file():
    return os.path.join(os.path.dirname(__file__), '..', 'example_data', 'input', "people_data.xml")


def test_generate_df(input_file):
    
    # Assuming 'input_file.xml' exists and has valid XML data
    df = generate_df(input_file)
    
    # Check if the returned dataframe is a pandas DataFrame
    assert isinstance(df, pd.DataFrame)
    
    # Check if expected columns exist
    assert 'name' in df.columns
    assert 'dob' in df.columns
    assert 'city' in df.columns

    
def test_dt_format():

    # Simulating sample data for testing dt_format function
    data = {'dob':['2000-01-01', '1990-05-15']}
    df = pd.DataFrame(data)
    
    # Apply the dt_format function
    dt_formatted_df = dt_format(df, 'dob')
    
    # Check if the 'dob' column is converted to datetime type
    assert pd.api.types.is_datetime64_any_dtype(dt_formatted_df['dob'])
    
    
    
def test_infer_country():
    
    # Simulating sample data for testing infer_country function
    data = {'zipcode': ['12345','12345','1234',''], 'country': ['USA','','','']}
    df = pd.DataFrame(data)
    
    # Apply the infer_country function
    df_w_countries_cleaned = infer_country(df)
    
    # Check if the 'country' column has properly inferred the country if and only if that country is the USA
    assert df_w_countries_cleaned['country'][0] == 'USA'
    assert df_w_countries_cleaned['country'][1] == 'USA'
    assert df_w_countries_cleaned['country'][2] == ''
    assert df_w_countries_cleaned['country'][3] == ''



def test_is_xml_file():
    filenames = ['test','test.png','test.xml','']
    
    assert is_xml_file(filenames[0]) == False
    assert is_xml_file(filenames[1]) == False
    assert is_xml_file(filenames[2]) == True
    assert is_xml_file(filenames[3]) == False