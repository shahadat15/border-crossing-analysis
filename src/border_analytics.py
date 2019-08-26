## Import sys library to get the command shell arguments (input and output file names)
import sys
input_file_location = sys.argv[1]
output_file_location = sys.argv[2]


### Define required functions

#  This function open the data file 'Border_Crossing_Entry_Data.csv' and read it line by line. Split the line and 
#  insert the data into a multidimentional dictionary. 

#  The dictionary keys are border, measure, and Date. The values of the dictionary are the Sum the total number of crossings 
#  (Value) of each type of vehicle or equipment, or passengers or pedestrians, that crossed the border that month, 
#  regardless of what port was used.

def read_lines(input_link):
    # Define an empty dictionary
    input_data_dictionary = {}
    
    with open(input_link) as myfile:
        # skip the first line which is a header
        line = next(myfile)
        # Read rest of the lines
        for line in myfile:
            # split the comma separated words
            words = line.strip().split(',')
            # Check wheather the dictionary key is already exists or not. If not exists then declare it. 
            # Otherwise, sum up the current value to the dictionary value
            if words[3] in input_data_dictionary.keys():
                if words[5] in input_data_dictionary[words[3]].keys():
                    if words[4] in input_data_dictionary[words[3]][words[5]].keys():
                        input_data_dictionary[words[3]][words[5]][words[4]] +=int(words[6])
                    else:
                        input_data_dictionary[words[3]][words[5]][words[4]] = int(words[6])
                else:
                    input_data_dictionary[words[3]][words[5]] ={}
                    if words[4] in input_data_dictionary[words[3]][words[5]].keys():
                        input_data_dictionary[words[3]][words[5]][words[4]] +=int(words[6])
                    else:
                        input_data_dictionary[words[3]][words[5]][words[4]] = int(words[6])
            else:
                input_data_dictionary[words[3]] = {}
                if words[5] in input_data_dictionary[words[3]].keys():
                    if words[4] in input_data_dictionary[words[3]][words[5]].keys():
                        input_data_dictionary[words[3]][words[5]][words[4]] +=int(words[6])
                    else:
                        input_data_dictionary[words[3]][words[5]][words[4]] = int(words[6]) 
                else:
                    input_data_dictionary[words[3]][words[5]] ={}
                    if words[4] in input_data_dictionary[words[3]][words[5]].keys():
                        input_data_dictionary[words[3]][words[5]][words[4]] +=int(words[6])
                    else:
                        input_data_dictionary[words[3]][words[5]][words[4]] = int(words[6])
    myfile.close() # Close the open file link
    return input_data_dictionary



# In order to sort the data, the dictionary data is saved as an array with each line as a data_point class.
# The class information is defined here
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
        return repr((self.border, self.date, self.measure, self.value,self.average,self.year,self.month))
    
    

# The final function is used to get the moving average of the value and saved the data into an multidimentional array
def data_process(input_data_dictionary):
    # define a new array 
    processed_data = []

    # Iterate over the dictionary keys
    for border_key in input_data_dictionary.keys():
        for measure_key in input_data_dictionary[border_key]:
            # For a spefic border type and measure, the value is stored to another dictionary. This dictionary has key of year. 
            # For each year it stores the twelve months crossing value
            value_months = {}
            for date_key in input_data_dictionary[border_key][measure_key]:
                yr = date_key.split(" ")[0].split("/")[2]
                mn = date_key.split(" ")[0].split("/")[0]
                if yr in value_months.keys():
                    value_months[yr][int(mn)-1]= int(input_data_dictionary[border_key][measure_key][date_key])
                else:
                    # If key is not present then declare the value with a list of 12 values.
                    # Each value of the list represnts the month in chronological order
                    value_months[yr] = [0,0,0,0,0,0,0,0,0,0,0,0] 

            # Now based on value_months dictionary data the moving average is calculated and saved it into processed_data array
            # the second value of the input_data_dictionary value list represents the moving average
            for date_key in input_data_dictionary[border_key][measure_key]:
                yr = date_key.split(" ")[0].split("/")[2]
                mn = int(date_key.split(" ")[0].split("/")[0])
                if mn == 1:
                    processed_data.append(data_point(border_key,date_key,measure_key,
                                                  (input_data_dictionary[border_key][measure_key][date_key]),
                                                  0,yr,mn))
                elif (mn == 2):
                    processed_data.append(data_point(border_key,date_key, measure_key,
                                                  (input_data_dictionary[border_key][measure_key][date_key]),
                                                  (value_months[yr][0]),yr,mn))
                else:
                    a = sum(value_months[yr][0:int(mn)-1])
                    b = (int(mn)-1)
                    processed_data.append(data_point(border_key,date_key, measure_key,
                                                  (input_data_dictionary[border_key][measure_key][date_key]),
                                                  (round(a/b)),yr,mn))
    return (processed_data)
	

###  Read the input data file and insert the data into a dictionary
## define the input file. Default locaiton with file name is './input/Border_Crossing_Entry_Data.csv'
# Read the data and get them as a Dictionary
input_data_dictionary = read_lines(input_file_location)


## Process the data, get moving average, and insert the data into a multidimentional array
processed_data = data_process(input_data_dictionary)


## The final step is to sort the data
processed_data_ordered = sorted(processed_data, key=lambda data_point: 
                       (data_point.year,data_point.month, data_point.value,data_point.measure, 
                        data_point.border) , reverse =True ) 
						
						


f1= open(output_file_location,"w+")
f1.write("Border,Date,Measure,Value,Average\n")
for row in processed_data_ordered:
    f1.write(str(row.border)+","+str(row.date)+","+str(row.measure)+","+str(row.value)+","+str(row.average)+"\n")
f1.close()
