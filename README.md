# People Data XML Processing and Report Generation
This Python script processes an XML file containing people's data, validates and cleans the data, categorizes individuals as "Adult" or "Child" based on age, generates a summary report, and optionally outputs a bar graph of the average age by city.

# Features
- XML Parsing: Reads the XML file and extracts relevant data (name, id, date of birth, address, etc.).
- Data Processing: Validates, formats dates, infers missing country data based on zip codes, and filters invalid records<sup>1</sup>.
- Age Categorization: Categorizes individuals as "Adult"<sup>2</sup> or "Child"<sup>3</sup> based on their age.
- Report Generation: Outputs a JSON report summarizing the number of Adults and Children.
- Graph Generation: Optionally generates a bar graph showing the average age by city<sup>4</sup> and saves it as a PNG file.
- File Dating: Outputs filenames with the current date (in the format `YYYYMMDD`)

# Requirements
This code was created utilizing `Python 3.12.8` and has been tested on that version alone. Make sure you have the required dependencies installed. You can install them by running:

```bash
pip install -r requirements.txt
```

# Usage
To use the script, run it with the following arguments:

```bash
python script.py <input_file> <output_path> [--output_graph]
```
## Arguments:
- `input_file`: 
    - Required. Path to the input XML file containing people data.
- `output_path`:
    - Required. Path to the output directory where the JSON report and the graph (if requested) will be saved.
- `--output_graph`: 
    - Optional flag. If specified, a bar graph of average age by city will be generated and saved as `average_age_by_city_YYYYMMDD.png` in the output directory.


# Example
```
python script.py people_data.xml ./output/
```
This will process the people_data.xml file and save the JSON report to `./output/age_categorized.json`.

To also generate the bar graph, run:
```bash
python script.py people_data.xml ./output/ --output_graph
```
This will also generate and save the bar graph as `average_age_by_city_YYYYMMDD.png` in the output directory.

# Input File
The path to the XML file containing the people data. This file should be structured in a way that each person is wrapped in a `<person>` element, and details like `name`, `dob`, `zipcode`, and `address` should be inside respective child elements. The script processes the data from this XML file for further operations.

# Outputs
- JSON Report: `age_categorized_YYYYMMDD.json` – Contains the summary of the number of Adults and Children.
- Bar Graph: `average_age_by_city_YYYYMMDD.png` (if `--output_graph` is provided) – A bar graph of the average age by city.

# Test Data
For your convenience, a testing input file and example outputs from that input data have been provided under `test_data` within this repository.

# Definitions
<sup>1</sup> An invalid record refers to any person with a blank or NaN record within one of the values; reports are only generated from people with complete data.<br>
<sup>2</sup> Over the age of 18, determined by their date of birth and today's date.<br>
<sup>3</sup> Under the age of 18, determined by their date of birth and today's date.<br>
<sup>4</sup> Rounded to the nearest whole number, as bar graphs prefer whole numbers.
