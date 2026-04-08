# importing the module
import pandas as pd 
  
# making data frame from the csv file 
df = pd.read_csv("AddResource(AddResource).csv") 
  
# using the replace() method
df['Category (Dropdown)'].replace(to_replace ="College", 
                 value = 1, 
                  inplace = True)
df['Category (Dropdown)'].replace(to_replace ="Scholarships", 
                 value = 2, 
                  inplace = True)
df['Category (Dropdown)'].replace(to_replace ="Mental", 
                 value = 3, 
                  inplace = True)
df['Category (Dropdown)'].replace(to_replace ="Jobs", 
                 value = 4, 
                  inplace = True)
df['Category (Dropdown)'].replace(to_replace ="Activities", 
                 value = 5, 
                  inplace = True)
df['Category (Dropdown)'].replace(to_replace ="Other", 
                 value = 6, 
                  inplace = True)

# writing  the dataframe to another csv file
df.to_csv('outputfile.csv', 
                 index = False) 
