import pandas as pd
import xmlschema
import lxml
import json
import matplotlib.pyplot as plt
from datetime import datetime
from pandas import json_normalize
from lxml import etree
import argparse


#filename = '/Users/audreyhoughton/Desktop/IMAT_techchallenge/test_data/input/people_data.xml'

#load in and validate XML file

def read_xml(filename):
    if is_xml_file(filename):

        df = generate_df(filename)
        dt_formatted_df = dt_format(df, 'dob')
        inferred_country_df = infer_country(dt_formatted_df)
        valid_df = drop_invalid_data(inferred_country_df)
           
    return valid_df

def is_xml_file(filename):
    return filename.lower().endswith('.xml')

def generate_df(filename):
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
    df[key] = pd.to_datetime(df[key], errors='coerce')
    return df

def infer_country(df):
    df['country'] = df.apply(
        lambda row: "USA" if row['country'] == "" and row['zipcode'].isdigit() and len(row['zipcode']) == 5 else row['country'],
        axis=1
    )
    return df    

def drop_invalid_data(df):
    filled_df = df.replace("", pd.NA)
    valid_df = filled_df.dropna()
    return valid_df

def get_todays_date():
    return datetime.today().strftime('%Y%m%d')

#summarize data

def child_or_adult(df):
    today = datetime.today()
    
    df['age'] = (today - df['dob']).dt.days // 365. 
    
    df['category'] = df['age'].apply(lambda x: "Adult" if x >= 18. else "Child")
    
    return df

def generate_report(df, path):
    categorized_df = child_or_adult(df)
    counts_summary = categorized_df['category'].value_counts().to_dict()
    
    
    print(f"Number of Adults (18+): {counts_summary.get('Adult', 0)}")
    print(f"Number of Children (<18): {counts_summary.get('Child', 0)}")
    
    with open(path + 'age_categorized_' + get_todays_date() + '.json', 'w') as json_file:
        json.dump(counts_summary, json_file, indent=4)
    
    return categorized_df

#output bar chart of average age by city

def average_age_by_city(df):

    avg_age_by_city = df.groupby('city')['age'].mean().round()
    
    return avg_age_by_city 

def create_bar_graph(df, path):
    
    df.plot(kind='bar', color='green', edgecolor='black')
    plt.title('Average Age by City')
    plt.xlabel('City')
    plt.ylabel('Average Age (Years)')
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(path + "average_age_by_city_" + get_todays_date() + ".png")


def main():
    
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