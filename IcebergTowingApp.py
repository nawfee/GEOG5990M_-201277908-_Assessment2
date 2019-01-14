# -*- coding: utf-8 -*-
"""
Application to find icebergs and their towing ability

Author: Shahreen Muntaha Nawfee
Created on Wed Jan  9 00:01:25 2019
Version used: Pythn 3.7
"""


#Modules imported for the application
import csv  # to read radar and lidar data
import matplotlib.pyplot as plt  #to display radar and lidar data
import numpy as np  #to convert list to array
import tkinter as tk  #to create a GUI



"""Extract Radar data

radar data exists as a text file. It is extracted to an empty list named sea
using csv reader code 
"""

sea = []  #create an empty list for creating sea environment    
with open ('white1.radar.txt') as rdr:
    radar = csv.reader(rdr, quoting=csv.QUOTE_NONNUMERIC)#convert values to float
    for row in radar:  #Create loop to fetch data from reader, i.e, the csv file
        rowlist = []  #list of rows
        for value in row:  #list of values in rows
            rowlist.append(value)  #add values to rowlist
        sea.append(rowlist)  #creates a 2D list with radar pixel values
#print(sea)



""" Finding icebergs

each iceberg is identified based on their star and end row and column indexes
A value of 100 or above is assigned to be iceberg. To prevent edge effects the
indexes start from 1 and stops at a value before the length of the area
"""

# extract each iceberg
iceberg= []

icebergStartCol = []
icebergEndCol = []
icebergStartRow = []
icebergEndCol = []

value0 = 0.0
onBergLeft = False
onBergRight = False
onBergAbove = False
onBergBelow = False
onBerg = False


for rowindex in range(1, len(sea) - 1): #index value for rows within range 1 to 299
    rowabove = sea[rowindex - 1]  #rows above iceberg
    row = sea[rowindex]
    rowbelow = sea[rowindex + 1]  #rows below iceberg
    for colindex in range(1, len(row) - 1):  #index value for columns
        value = row[colindex - 1]
        if (100 <= value <= 256):
            onBergLeft = True  
        else:
            onBergLeft = False      
        #Right of iceberg
        value = row[colindex + 1]
        if (100 <= value <= 256):
            onBergRight = True
        else:
            onBergRight = False
        #Above iceberg
        value = rowabove[colindex]
        if (100 <= value <= 256):
            onBergAbove = True
        else:
            onBergAbove = False
        #Below iceberg
        value = rowbelow[colindex]
        if (100 <= value <= 256):
            onBergBelow = True
        else:
            onBergBelow = False
        #Cell value for iceberg
        value = row[colindex]
        if (100 <= value <= 256):
            onBerg = True
        else:
            onBerg = False
        if (onBerg):
            if (onBergRight == False):
                icebergendcolindex = colindex
            if (onBergLeft == False):
                icebergstartcolindex = colindex
            if (onBergAbove == False):
                icebergstartrowindex = rowindex
            if (onBergBelow == False):
                icebergendrowindex = rowindex

#prints the vstarting and ending row and column jndexes for icebergs       
print("icebergstartrowindex:",icebergstartrowindex)                
print("icebergstartcolindex:",icebergstartcolindex)                
print("icebergendrowindex:", icebergendrowindex)                
print("icebergendcolindex:", icebergendcolindex)



"""Extract lidar data
 
using csv reader code Lidar data is also extracted as a 2D list ino a file 
named, lidar_sea
"""

with open('white1.lidar.txt') as ldr: #extracting lidar file
    lidar = csv.reader(ldr, quoting=csv.QUOTE_NONNUMERIC)
    lidar_sea = []  #an empty list to take lidar data
    for row in lidar: 
        list_row = []  #list of row
        for value in row:  #values in row
            list_row.append(value)  #add values to list of rows
        lidar_sea.append(list_row)  #add list of rows to the empty list
#print(lidar_sea)



""" Display the radar and lidar data as images

The radar and lidar data imported above are displayed using matplotlib.pyplot
module. They are displayed as images and icebergs are marked in them
"""        
#plot an image of sea with iceberg using radar data
plt.subplot(1,2,1)  #making 1X2 subplot
plt.ylim(0,300)  #set the y axis in plot
plt.xlim(0,300)  #set the x axis in plot
plt.text(200,220, 'Sea',fontsize=12)
#annotate for showing the iceberg with an arrow
plt.annotate("Iceberg", xy=(155,145), xytext=(180,100), arrowprops=dict(facecolor="red" ))
plt.title('Radar image of a sea with iceberg',fontsize=12,fontname='Times New Roman')
plt.imshow(sea, 'Blues_r')  #display an image of sea using blue and white colour


#plot an image of a sea with iceberg using lidar data
plt.subplot(1,2,2)  #he second subplot
plt.ylim(0,300)  #set the y axis in plot
plt.xlim(0,300)  #set the x axis in plot
plt.text(200,220, 'Sea',fontsize=12)
plt.annotate("Iceberg", xy=(155,145), xytext=(180,100), arrowprops=dict(facecolor="red" ))
plt.title('Lidar image of a sea with iceberg',fontsize=12,fontname='Times New Roman')
plt.imshow(lidar_sea, 'Blues_r')#display an image of sea using blue and white colour

plt.tight_layout()
plt.show() #prints the images



"""Pulling out the height of iceberg from lidar data

By using index values of icebergs from radar data, the height values of the 
iceberg is pulled out of the lidar data for future calculation
"""  
 
#convert the lidar data to a 2D array
np_lidar_sea = np.array(lidar_sea,dtype=int)

#mask iceberg from the np_array
iceberg = np_lidar_sea[icebergstartrowindex:icebergendrowindex+1, icebergstartcolindex:icebergendcolindex+1]
#print(iceberg) #show only the pixel values of the iceberg



""" Construct a tkinter window for GUI output"""

root = tk.Tk()  #create a blank window 
root.wm_title("Iceberg Towing Application")  #setting the title of the window
root.geometry("300x300")  #setting the size of the window



class Iceberg_Towing():
    """Create a class named Iceberg Towing """
       
    def __init__(self):
        """Define methods for initializing objects within the class """

        
    total_iceberg_vol = 0.0  #define a global variable for total iceberg volume  
    def totalvol():
        """ Method for total volume of iceberg calculation
        
        10 units of lidar value,represent 1m in height. So the pixel values are
        multiplied by 0.1, to get height in meter. 
        The area of iceberg is 1 m2 (lengthxbreadth of pixels)
        The volume is calculated from area multiplied by height. 
        The total volume of iceberg is obtained from adding up individual 
        element from the iceberg volume list
        """  
        
        iceberg_vol_m3 = []  #empty list of iceberg volume in m3
        for i in iceberg:  #looping through each rows in iceberg list
            rowlist = []  #create an empty rowlist
            for j in i:   #looping through each values in the row
#multiplying each values in iceberg list with 0.1 to convert to m and multiplying with area
                rowlist.append(j*0.1*1) #volume = heightXarea
            iceberg_vol_m3.append(rowlist)  #add volume values to the volume list
        
    
        global total_iceberg_vol  #pass global variable
        total_iceberg_vol = 0.0
        for row in iceberg_vol_m3: #loop through each row in iceberg volume list
            for element in row:
            #add the values in iceberg volume list to get the total volume of iceberg
                total_iceberg_vol += element 
                    
 
        print("Total iceberg volume:", total_iceberg_vol,"m3") 

# add button to the tkinter window and bind it to the totalvol function            
#pressing it prints out the Total iceberg volume
    button1 = tk.Button(root, text = "Total iceberg volume",command=totalvol, fg = "blue")
    button1.pack(side = "top")


    total_iceberg_mass = 0.0   #create a global variable for iceberg mass        
    def totalmass():
        """Method defined for iceberg total mass calculation
        
        the equation used is mass = density x volume
        The density of iceberg is 900kg/m3. Total iceberg mass is calculated 
        assuming only 10% of the ice is above sea level
        """
        
        global total_iceberg_mass  #global variable passed
        iceberg_mass = total_iceberg_vol*900  #iceberg mass above water level
        total_iceberg_mass = iceberg_mass * 10 #considering 10% mass above water
        
        print("Total iceberg mass:", total_iceberg_mass,"kg")
    
#add button to the tkinter window and bind it to total mass function 
#pressing it prints out total mass of iceberg
    button2 = tk.Button(root, text = "Total iceberg mass",command=totalmass, fg = "blue")
    button2.pack(side = "top")
    
    
    def towingability():
        """ Assessing iceberg towing ability
        
        condition is set that, iceberg can be drag out in time if its total mass
        is below 36 million kg
        """    
        
        if total_iceberg_mass >= 36000000:
            print("Pulling iceberg is not possible")
        else:
            print("Pulling iceberg is possible")

# add button to the tkinter window and ind it to towing abilityfunction            
# pressing it prints out the iceberg towing ability based on its mass
    button3 = tk.Button(root, text = "Towing ability",command=towingability, fg = "blue")
    button3.pack(side = "top")
                
root.mainloop() #retains the tkinter window until closed  