# Border Crossing Analysis

## Table of Contents
1. [Problem Statement](README.md#problem)
1. [Input Dataset Information](README.md#input)
1. [Required Output](README.md#Required Output)
1. [Repo directory structure](README.md#Repo directory structure)
1. [Source Code Details](README.md#Source Code Details)
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

The prepared program write the requested output data to a file named `report.csv` in the `output` directory of this repository.

A sample of the output file, `report.csv` is:

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

The column, `Average`, is for the running monthly average of total crossings for that border and means of crossing in all previous months. In this example, to calculate the `Average` for the first line (i.e., running monthly average of total pedestrians crossing the US-Mexico Border in all of the months preceding March), you'd take the average sum of total number of US-Mexico pedestrian crossings in February `172,163` and January `56,810`, and round it to the nearest whole number `round(228,973/2) = 114,487`


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



## Source Code Details

The main sourcecode is written in "border_analytics.py" file which is located in the 'src' folder of this repository. 
The main algorithm is as follows:
1. Read the input file line by line
2. Split the comma separated line into words or fields which will represent the eight different input fields
3. Only the fields of Border, Date, Measure, and Value are considered for further analysis
4. A python dictionary is created which has three level of keys: fist level of key is the Border, second level key is measure, and the third level key is the Date. Therefore, for the dictionary value is for a specific border, measure and date. 
5. If new Values are found for a specific key combination (e.g. border, measure, and date) then the new Value is summed up with the existing value. This will provide us the sum of the total number of crossings (`Value`) of each type of vehicle or equipment, or passengers or pedestrians, that crossed the border that month, regardless of what port was used.
6. Using the dictionary the running monthly average of total crossings is calculated
7. Later, all the dictionary data is saved into a multidimentional array in order to do the sorting. Each data point is saved as a specific class to make the sorting procedure easier. 
8. Finally, the sorted data is saved into the 'report.csv' file



# Questions?
Email me at: miqba005@fiu.edu
