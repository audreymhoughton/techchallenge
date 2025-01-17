#Audrey Houghton
#Created on: 1/16/2025
#Last Updated on: 1/17/2025

#load in python packages
import pandas as pd
import xmlschema
import lxml
import json
import matplotlib.pyplot as plt
from datetime import datetime
from pandas import json_normalize
from lxml import etree
import argparse

"""
This script processes and visualizes people data from an XML file.
It reads the file, formats data, generates a report, and optionally creates a bar graph of average age by city.
"""

def read_xml(filename):
    '''
    Read and process an XML file, returning a cleaned DataFrame.

    This function checks if the input file has an XML extension, parses the XML data, converts the date of birth 
    column to a datetime format, infers the country based on ZIP code when missing, and removes rows with invalid 
    or missing data.

    Args:
        filename: A string representing the path to the input XML file.

    Returns:
        A pandas DataFrame containing the cleaned and processed data from the XML file.
    '''
    if is_xml_file(filename):

        df = generate_df(filename)
        dt_formatted_df = dt_format(df, 'dob')
        inferred_country_df = infer_country(dt_formatted_df)
        valid_df = drop_invalid_data(inferred_country_df)
           
    return valid_df

def is_xml_file(filename):
    '''
    Check if the file has an XML extension (case-insensitive).
    
    Args:
        filename (str): The file path of the XML file provided by args.input_file.
        
    Returns:
        bool: True if the file has an XML extension, otherwise False.
    '''
    return filename.lower().endswith('.xml')

def generate_df(filename):
    '''
    Parse the provided XML file and generate a DataFrame containing people data.
    
    Args:
        filename (str): The path to the XML file to be parsed.
        
    Returns:
        pandas.DataFrame: A DataFrame containing information about each person 
                          (name, id, dob, address).
    '''
    tree = etree.parse(filename)
    people = tree.xpath("/people/person")
    data = []
        
    for person in people:
            
        name = person.findtext("name", default = "")
        id = person.findtext("id", default = "")
        dob = person.findtext("dob", default = "")
        street = person.findtext("address/street", default = "")
        city = person.findtext("address/city", default = "")
        state = person.findtext("address/state", default = "")
        zipcode = person.findtext("address/zipcode", default = "")
        country = person.findtext("address/country", default = "")
            
        data.append({
            "name": name,
            "id": id,
            "dob": dob,
            "street": street,
            "city": city,
            "state": state,
            "zipcode": zipcode,
            "country": country
        })
        
    df = pd.DataFrame(data)
    return df

def dt_format(df, key):
    '''
    Convert the specified column in the DataFrame to datetime format.
    
    Args:
        df (pandas.DataFrame): The DataFrame containing the data.
        key (str): The name of the column to be converted to datetime.
        
    Returns:
        pandas.DataFrame: The DataFrame with the specified column formatted as datetime.
    '''
    df[key] = pd.to_datetime(df[key], errors='coerce')
    return df

def infer_country(df):
    '''
    Infer the country based on the presence of a valid 5-digit zipcode.
    If the country field is empty and the zipcode is a 5-digit number, the country is set to "USA".
    
    Args:
        df (pandas.DataFrame): The DataFrame containing the data, including 'country' and 'zipcode' columns.
        
    Returns:
        pandas.DataFrame: The DataFrame with the 'country' column updated, if applicable.
    '''
    df['country'] = df.apply(
        lambda row: "USA" if row['country'] == "" and row['zipcode'].isdigit() and len(row['zipcode']) == 5 else row['country'],
        axis=1
    )
    return df    

def drop_invalid_data(df):
    '''
    Remove rows with missing or empty data from the DataFrame.
    Replaces empty strings with NaN and drops rows containing NaN values.
    
    Args:
        df (pandas.DataFrame): The DataFrame to clean, where rows with missing or empty data will be removed.
        
    Returns:
        pandas.DataFrame: The cleaned DataFrame with invalid data dropped.
    '''
    filled_df = df.replace("", pd.NA)
    valid_df = filled_df.dropna()
    return valid_df

def get_todays_date():
    '''
    Get today's date in the format YYYYMMDD.
    
    Returns:
        str: The current date formatted as a string in the format YYYYMMDD.
    '''
    return datetime.today().strftime('%Y%m%d')

def child_or_adult(df):
    '''
    Categorize individuals as "Adult" or "Child" based on their age (18 years or older is considered an adult).

    This function calculates the age of each person based on their date of birth and assigns them 
    to a category ("Adult" or "Child") depending on whether their age is 18 years or older.

    Args:
        df: A pandas DataFrame containing a 'dob' (date of birth) column.

    Returns:
        A pandas DataFrame with two new columns:
        - 'age': The age of each individual in years.
        - 'category': The category ('Adult' or 'Child') based on the age.
    '''
    today = datetime.today()
    
    df['age'] = (today - df['dob']).dt.days // 365. 
    
    df['category'] = df['age'].apply(lambda x: "Adult" if x >= 18. else "Child")
    
    return df

def generate_report(df, path):
    '''
    Generate a report summarizing the number of adults and children by city, and save the results in a JSON file.

    This function processes the input DataFrame to categorize individuals as "Adult" or "Child", groups 
    them by city, and counts the number of adults and children in each city. The summary is printed to 
    the console and saved as a JSON file with today's date appended to the file name.

    Args:
        df: A pandas DataFrame containing individual data with a 'dob' (date of birth) and 'city' column.
        path: A string representing the directory path where the JSON file will be saved.

    Returns:
        A pandas DataFrame with an additional 'category' column categorizing individuals as 'Adult' or 'Child'.
    '''
    categorized_df = child_or_adult(df)
    counts_by_city = categorized_df.groupby('city')['category'].value_counts().unstack(fill_value=0)
    counts_summary = counts_by_city.to_dict(orient='index')
    
    for city, counts in counts_summary.items():
        print(f"City: {city}, Adults: {counts.get('Adult', 0)}, Children: {counts.get('Child', 0)}")
    
    
    with open(path + 'age_categorized_by_city_' + get_todays_date() + '.json', 'w') as json_file:
        json.dump(counts_summary, json_file, indent=4)
    
    return categorized_df

def average_age_by_city(df):
    '''
    Calculate the average age of individuals in each city.

    This function groups the input DataFrame by city and calculates the mean age for each group. 
    The age values are rounded to the nearest whole number.

    Args:
        df: A pandas DataFrame containing individual data, including an 'age' and 'city' column.

    Returns:
        A pandas Series with the average age by city, where the index is the city name.
    '''
    avg_age_by_city = df.groupby('city')['age'].mean().round()
    
    return avg_age_by_city 

def create_bar_graph(series, path):
    '''
    Create and save a bar graph showing the average age by city.

    This function generates a bar graph with cities on the x-axis and the average age on the y-axis.
    The graph is styled with a green color for the bars and black edges, and is saved as a PNG file in 
    the specified directory.

    Args:
        series: A pandas Series containing the average age by city.
        path: A string representing the directory path where the graph will be saved.

    Returns:
        None
    '''
    df.plot(kind='bar', color='green', edgecolor='black')
    plt.title('Average Age by City')
    plt.xlabel('City')
    plt.ylabel('Average Age (Years)')
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(path + "average_age_by_city_" + get_todays_date() + ".png")


def main():
    '''
    Main function to parse arguments, read input data, generate a report, and optionally create a bar graph.

    This function sets up argument parsing, reads the input XML file, processes the data to generate a report 
    (with counts of adults and children by city), and optionally creates and saves a bar graph of the average age 
    by city.

    Args:
        None

    Returns:
        None
    '''
    parser = argparse.ArgumentParser(description='Process and visualize people data from an XML file.')
    parser.add_argument('input_file', type=str, help='Input XML file')
    parser.add_argument('output_path', type=str, help='Output JSON file for report')
    parser.add_argument('--output_graph', action='store_true', help='Flag to output an average age by city graph image file')

    args = parser.parse_args()
    
    valid_df = read_xml(args.input_file)
    categorized_df = generate_report(valid_df, args.output_path)
    
    if args.output_graph:
        avg_age_by_city = average_age_by_city(valid_df)
        create_bar_graph(avg_age_by_city, args.output_path)
    
    return print("reports generated")

if __name__ == "__main__":
    main()