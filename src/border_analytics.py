## Import sys library to get the command shell arguments (input and output file names)
import sys
input_file_location = sys.argv[1]
output_file_location = sys.argv[2]


### Define required functions

#  This function open the data file 'Border_Crossing_Entry_Data.csv' and 
#  read it line by line. Split the line and insert the data 
#  into a multidimentional dictionary. 

#  The dictionary keys are border, measure, and Date. The values of the dictionary 
#  are the Sum the total number of crossings (Value) of each type of measures, 
#  that crossed the border that month, regardless of what port was used.

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



    
# In order to sort the data, the dictionary data is saved as an array 
# with each line as a data_point class.

# The class information is defined here:
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
    
  

 
# The final function is used to get the moving average of the value and 
# saved the data into an multidimentional array

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
                if _month > 2:
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
                elif _month == 2:
                    processed_data.append(data_point
                                          (border_key,date_key,measure_key, 
                                                  (input_data[border_key]
                                                  [measure_key][date_key]),
                                                  (value_months[_year][0]),_year,_month))
                else:
                    processed_data.append(data_point
                                          (border_key,date_key,measure_key,
                                                  (input_data[border_key]
                                                  [measure_key][date_key]),
                                                  0,_year,_month))
    return (processed_data)
    
    
    
#### Data Analysis #########

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
