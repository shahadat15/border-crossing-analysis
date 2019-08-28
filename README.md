# Border Crossing Analysis Solution

## Table of Contents
1. [Problem Statement](README.md#problem)
1. [Input Dataset Information](README.md#input)
1. [Required Output](README.md#required)
1. [Repo directory structure](README.md#repo)
1. [Analysis Procedure](README.md#analysis)
1. [Source Code Details](README.md#source)
1. [Questions?](README.md#questions?)

## Problem Statement
The Bureau of Transportation Statistics regularly makes available data on the number of vehicles, equipment, passengers and pedestrians crossing into the United States by land.

**The main objective of this challenge is to calculate the total number of times vehicles, equipment, passengers and pedestrians cross the U.S.-Canadian and U.S.-Mexican borders each month and the running monthly average of total number of crossings for that type of crossing and border.**



## Input Dataset Information

The input file, `Border_Crossing_Entry_Data.csv`, is in the `input` directory of this repository.

The file contains data of the form:

```
Port Name,State,Port Code,Border,Date,Measure,Value,Location
Derby Line,Vermont,209,US-Canada Border,03/01/2019 12:00:00 AM,Truck Containers Full,6483,POINT (-72.09944 45.005)
Norton,Vermont,211,US-Canada Border,03/01/2019 12:00:00 AM,Trains,19,POINT (-71.79528000000002 45.01)
Calexico,California,2503,US-Mexico Border,03/01/2019 12:00:00 AM,Pedestrians,346158,POINT (-115.49806000000001 32.67889)
Hidalgo,Texas,2305,US-Mexico Border,02/01/2019 12:00:00 AM,Pedestrians,156891,POINT (-98.26278 26.1)
Frontier,Washington,3020,US-Canada Border,02/01/2019 12:00:00 AM,Truck Containers Empty,1319,POINT (-117.78134000000001 48.910160000000005)
Presidio,Texas,2403,US-Mexico Border,02/01/2019 12:00:00 AM,Pedestrians,15272,POINT (-104.37167 29.56056)
Eagle Pass,Texas,2303,US-Mexico Border,01/01/2019 12:00:00 AM,Pedestrians,56810,POINT (-100.49917 28.70889)
```
More information on each field are provided here: [notes from the Bureau of Transportation Statistics](https://data.transportation.gov/Research-and-Statistics/Border-Crossing-Entry-Data/keg4-3bc2).

To fulfill the challenge objective, the following fields are considered for further analysis:
* `Border`: Designates what border was crossed
* `Date`: Timestamp indicating month and year of crossing
* `Measure`: Indicates means, or type, of crossing being measured (e.g., vehicle, equipment, passenger or pedestrian)
* `Value`: Number of crossings

## Required Output
Using the input file, this challenge requires to write a program to 
* Sum the total number of crossings (`Value`) of each type of vehicle or equipment, or passengers or pedestrians, that crossed the border that month, regardless of what port was used. 
* Calculate the running monthly average of total crossings, rounded to the nearest whole number, for that combination of `Border` and `Measure`, or means of crossing.

The prepared program write the output data to a file named `report.csv` in the `output` directory of this repository. A sample output file is shown below:

```
Border,Date,Measure,Value,Average
US-Mexico Border,03/01/2019 12:00:00 AM,Pedestrians,346158,114487
US-Canada Border,03/01/2019 12:00:00 AM,Truck Containers Full,6483,0
US-Canada Border,03/01/2019 12:00:00 AM,Trains,19,0
US-Mexico Border,02/01/2019 12:00:00 AM,Pedestrians,172163,56810
US-Canada Border,02/01/2019 12:00:00 AM,Truck Containers Empty,1319,0
US-Mexico Border,01/01/2019 12:00:00 AM,Pedestrians,56810,0

```

The lines should be sorted in descending order by 
* `Date`
* `Value` (or number of crossings)
* `Measure`
* `Border`


## Repo directory structure

The directory structure for this reposatory is:

    ├── README.md
    ├── run.sh
    ├── src
    │   └── border_analytics.py
    ├── input
    │   └── Border_Crossing_Entry_Data.csv
    ├── output
    |   └── report.csv
    ├── insight_testsuite
        └── run_tests.sh
        └── tests
            └── test_1
            |   ├── input
            |   │   └── Border_Crossing_Entry_Data.csv
            |   |__ output
            |   │   └── report.csv
            ├── your-own-test_1
                ├── input
                │   └── Border_Crossing_Entry_Data.csv
                |── output
                    └── report.csv



## Analysis Procedure

The analysis procedure is described below:

1. Read the input file line by line
2. Split the comma separated line into words or fields which will represent the eight different input fields
3. Only the fields of Border, Date, Measure, and Value are considered for further analysis
4. A python dictionary is created which has three level of keys: fist level of key is the Border, second level key is measure, and the third level key is the Date. Therefore, for the dictionary value is for a specific border, measure and date. 
5. If new Values are found for a specific key combination (e.g. border, measure, and date) then the new Value is summed up with the existing value. This will provide us the sum of the total number of crossings (`Value`) of each type of vehicle or equipment, or passengers or pedestrians, that crossed the border that month, regardless of what port was used.
6. Using the dictionary the running monthly average of total crossings is calculated
7. Later, all the dictionary data is saved into a multidimentional array in order to do the sorting. Each data point is saved as a specific class to make the sorting procedure easier. 
8. Finally, the sorted data is saved into the 'report.csv' file


## Source Code Details

The main sourcecode is written in "border_analytics.py" file which is located in the 'src' folder of this repository. 

Firstly, "sys" package is imported to get the command shell arguments (input and output file names)

```
import sys
input_file_location = sys.argv[1]
output_file_location = sys.argv[2]
```

The first part of the codes defines all the required funcitons that are needed for this analysis. 
Although those functioned can be written in a separate file, for a short code like this the author prefer to put it together. 

This first function is 'read_input_file' which open the data file 'Border_Crossing_Entry_Data.csv' and 
read it line by line. Then it split the line and insert the data into a multidimentional dictionary.
The dictionary keys are border, measure, and Date. The values of the dictionary are the Sum the total 
number of crossings (Value) of each type of measures, that crossed the border that month, regardless of what port was used.

Several test checks are also included to find any problem/irregularities with input data. The code will 
return some Error message on such case. 

```
def read_input_file(input_file_location):
    # Define an empty dictionary
    input_data = {}
    
    try:
        with open(input_file_location) as _file:
            # Read the first line which is a header
            _line = next(_file)
            header_input_file = _line.strip().split(',')
            header_actual = ['Port Name','State','Port Code','Border','Date',
                             'Measure','Value','Location']
 
            if header_input_file != header_actual:
                return(print("ERROR: Check the input file: \nPossible causes:" +
                       "\n1. Either all variables are not present"+
                       "\n2. Variables are not in right order" + 
                       "\n3. Header is not present"))   
            
            # Read rest of the lines
            for _line in _file:
                # split the comma separated words
                _words = _line.strip().split(',')
                try: int(_words[6]) ## Check if any NA values are found
                except: return (print("Error: Unacceptable (or NA) values are Found"))
  
                   
                # Check wheather the dictionary key is already exists or not 
                # If not exists then declare it
                # Otherwise, sum up the current value to the dictionary value
                if _words[3] in input_data.keys():
                    if _words[5] in input_data[_words[3]].keys():
                        if _words[4] in input_data[_words[3]][_words[5]].keys():
                            input_data[_words[3]][_words[5]][_words[4]] +=int(_words[6])
                        else:
                            input_data[_words[3]][_words[5]][_words[4]] = int(_words[6])
                    else:
                        input_data[_words[3]][_words[5]] ={}
                        input_data[_words[3]][_words[5]][_words[4]] = int(_words[6])
                else:
                    input_data[_words[3]] = {}
                    input_data[_words[3]][_words[5]] ={}
                    input_data[_words[3]][_words[5]][_words[4]] = int(_words[6])
        _file.close() # Close the open file link
        return input_data
    
    except:
        return (print('ERROR: Check input file or file location'))
```

    
After importing the data, the data has been processed to get the moving average. The dictionary is iterated over border, 
and measure to get the number of crossing for differnt months and year. Later the montly data is utilized to get the 
moving average. This procedure is described in function named 'data_process_get_average'. This function also saves the data
in a array which has data point from class 'data_point'. Therefore, the details of the 'data_point' class is described first.
Point to be noted, the dictionary data is stored into a array considering a data class to make the sorting procedure easier. 

```
class data_point:
    def __init__(self, border,date, measure, value, average,year,month):
        self.border = border
        self.date = date
        self.measure = measure
        self.value = value
        self.average = average
        self.year = year
        self.month = month
    def __repr__(self):
        return repr((self.border, self.date, self.measure, 
                     self.value,self.average,self.year,self.month))
    
 

def data_process_get_average(input_data):
    # define a new array 
    processed_data = []

    # Iterate over the dictionary keys
    for border_key in input_data.keys():
        for measure_key in input_data[border_key]:
            # Another temporary dictionary is  created to store monthly value
            # The key of the dictionary is the year
            value_months = {}
            for date_key in input_data[border_key][measure_key]:
                try:
                    _year = date_key.split(" ")[0].split("/")[2] 
                    _month = date_key.split(" ")[0].split("/")[0]
                    if _year in value_months.keys():
                        value_months[_year][int(_month)-1]= int(input_data[border_key]
                                                                [measure_key][date_key])
                    else:
                    	# If key is not present then declare the value with a list of 12 values.
                    	# Each value of the list represnts the month in chronological order
                        value_months[_year] = [0,0,0,0,0,0,0,0,0,0,0,0]
                        value_months[_year][int(_month)-1]= int(input_data[border_key]
                                                                [measure_key][date_key])
                except:
                    return (print("Error: Date is not in right format"))
                
            # Now based on value_months dictionary data the moving average is calculated 
            # moving_average is saved into processed_data array
            for date_key in input_data[border_key][measure_key]:
                _year = date_key.split(" ")[0].split("/")[2]
                _month = int(date_key.split(" ")[0].split("/")[0])
                if _month > 1:
                    _sum_previous_months = sum(value_months[_year][0:(_month-1)])
                    _number_of_previous_months = (_month-1)
                    _moving_average = (_sum_previous_months/_number_of_previous_months)
                    
                    if float(str(_moving_average-int(_moving_average))[1:])<0.5:
                        _moving_average_round = int(_moving_average)
                    else:
                        _moving_average_round = int(_moving_average)+1
                    
                        
                    processed_data.append(data_point
                                          (border_key, date_key, measure_key,
                                                  (input_data[border_key]
                                                  [measure_key][date_key]),
                                                  _moving_average_round,_year,_month))
                else:
                    processed_data.append(data_point
                                          (border_key,date_key,measure_key,
                                                  (input_data[border_key]
                                                  [measure_key][date_key]),
                                                  0,_year,_month))
    return (processed_data)
    
```

The second part of the code process the data using the function mentioned above and 
finally save into the output file named provided by the command shell argument. 
    

```
# Read the input data file and insert the data into a dictionary
input_data = read_input_file(input_file_location)


# Process the data, get moving average, and insert the data into a multidimentional array
processed_data = data_process_get_average(input_data)


# Data sorting
processed_data_ordered = sorted(processed_data, key=lambda data_point: 
                       (data_point.year,data_point.month, 
                       data_point.value,data_point.measure, 
                        data_point.border) , reverse =True ) 
						
						
# Write the output file 
try:
    output_file= open(output_file_location,"w+")
    output_file.write("Border,Date,Measure,Value,Average\n")
    for row in processed_data_ordered:
        output_file.write(str(row.border)+","+str(row.date)+","+str(row.measure)+","
        +str(row.value)+","+str(row.average)+"\n")
    output_file.close()
except:
    print ("ERROR: Check output file or file location")
```

# Questions?
If you have any question please email me at: miqba005@fiu.edu
