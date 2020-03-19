#######################################################################
# 
# Algorithm
#
#   Prompt for three different files, ip addresses for each country, 
#   attacks ip addresses to be searched, and the codes for each country name.
#   These files are parced and formed into lists converting the IP address to
#   12 digit numbers for easy comparison. For each attack IP if it sits between
#   the start IP and end Ip for the country it is a match and the country code
#   is returned. The end user is then prompted if they want to display data and
#   plot. Top ten countries by attack amounts is displayed. 
#
########################################################################

import csv
import pylab
import re
from operator import itemgetter

def open_file(message):
    
    """ Prompt for file name. Iterate until correct file name is entered """ 
    
    while True:
    
        try:
    
            filename = input(message)
            
            fp = open(filename)
            
            return fp
            
        except FileNotFoundError: 
            
            print("File is not found! Try Again!")
    
            
def read_ip_location(file):
    
    """ 
    Converts each IP to 12 digits and creates a list of tuples containing
    start IP, end IP and country code.
    
    """

    mast_list = []
    
    tup = ()
    
    #Split at commas for our three values - start_ip, end_ip, country_code
    
    for line in file:
        
        rem = line.strip().split(",")
        
        start_ip = rem[0]
        
        end = rem[1]
        
        country_code = rem[2]
        
        #Split at periods in each IP for 4 different numbers to be evaluated
        
        start = start_ip.split(".")
        
        end_ip = end.split(".")
        
        #If tree discerns length of each number in start and decides the amount
        #of zeros to append. 
        
        if len(start[0]) == 1:
            
            start[0] = "00" + str(start[0])
            
            
        elif len(start[0]) == 2:
            
            start[0] = "0" + str(start[0])
            
        if len(start[1]) == 1:
            
            start[1] = "00" + str(start[1])
            
        elif len(start[1]) == 2:
            
            start[1] = "0" + str(start[1])
            
        if len(start[2]) == 1:
        
            start[2] = "00" + str(start[2]) 
            
        if len(start[2]) == 2:
            
            start[2] = "0" + str(start[2])
            
        if len(start[3]) == 1:
            
            start[3] = "00" + str(start[3]) 
            
        if len(start[3]) == 2:
            
            start[3] = "0" + str(start[3])
            
        #################################
        #################################
        
        #If tree discerns length of each number in end and decides the amount
        #of zeros to append.
        
        if len(end_ip[0]) == 1:
            
            end_ip[0] = "00" + str(end_ip[0])
            
        elif len(end_ip[0]) == 2:
            
            end_ip[0] = "0" + str(end_ip[0])
            
        if len(end_ip[1]) == 1:
            
            end_ip[1] = "00" + str(end_ip[1])
            
        elif len(end_ip[1]) == 2:
            
            end_ip[1] = "0" + str(end_ip[1])
            
        if len(end_ip[2]) == 1:
            
            end_ip[2] = "00" + str(end_ip[2])
            
        elif len(end_ip[2]) == 2:
            
            end_ip[2] = "0" + str(end_ip[2])
            
        if len(end_ip[3]) == 1:
            
            end_ip[3] = "00" + str(end_ip[3])
            
        elif len(end_ip[3]) == 2:
            
            end_ip[3] = "0" + str(end_ip[3])
        
        #Items in start_ip and end_ip are joined together to form single nums
        #for each. 
            
        start_ip = ''.join(start)
        
        end_ip = ''.join(end_ip)
        
        #Tuple containing start_ip, end_ip, country_code formed and appended to
        #list
        
        tup = (int(start_ip),int(end_ip),country_code)
        
        mast_list.append(tup)
        
    return mast_list


def read_ip_attack(file):
    
    """
    Converts each IP to either 12 digits or 9 digits with xxx appended. Then
    creates a list of tuples containing one of each.
    
    """
    
    mast_list = []
    
    tup = ()
    
    #Split at periods in each IP for 3 different numbers to be evaluated
    
    for line in file:
        
        att = line.strip()
        
        attack = att.split(".")
        
        #If tree discerns length of each number in start and decides the amount
        #of zeros to append.
        
        if len(attack[0]) == 1:
            
            attack[0] = "00" + str(attack[0])   
            
        elif len(attack[0]) == 2:
            
            attack[0] = "0" + str(attack[0])
            
        if len(attack[1]) == 1:
            
            attack[1] = "00" + str(attack[1])
            
        elif len(attack[1]) == 2:
            
            attack[1] = "0" + str(attack[1])
            
        if len(attack[2]) == 1:
        
            attack[2] = "00" + str(attack[2]) 
            
        if len(attack[2]) == 2:
            
            attack[2] = "0" + str(attack[2])
            
        #Join items in list to form single number
            
        attack_ip = ''.join(attack)
        
        #Append string to first item "000"
        
        attack_ip = int(attack_ip + "000")
        
        #Append string to second item ".xxx"
        
        triple_x_ip = att + ".xxx"
        
        #Form tuple of two items and append
        
        tup = (attack_ip,triple_x_ip)
        
        mast_list.append(tup)
    
    return mast_list
        
def read_country_name(file):
    
    """
    Creates list of tuples containing country name and its corresponding 
    country code.
    
    """
    
    mast_list = []
    
    tup = ()
    
    for line in file:
        
        #Split at semi-colon
        
        new_line = line.strip().split(";")
        
        full_name = new_line[0]
        
        country_code = new_line[1]
        
        #Tuple of country code and fully corresponding country name then append
        
        tup = (country_code, full_name)
        
        mast_list.append(tup)
        
    return(mast_list)
    
def locate_address(ip_list, ip_attack):
    
    """
    Iterates through list of attack IP's. Returns country code if IP is 
    inbetween start_ip and end_ip for that country code.
    
    """

    for value in ip_list:
        
        start = value[0]
        end = value[1]
        code = value[2]
        
        #If ip_attack less than end but greater than start return corresponding
        #country code
        
        if int(start) <= int(ip_attack) <= int(end):
            
           return code

def get_country_name(country_list, code):
    
    """
    Returns country name for country code passed to it.
    
    """
    
    for item in country_list:
    
        if code == item[0]:
        
            return item[1]

def bar_plot(count_list, countries):
    
    """
    Function for plotting top ten data
    """
    
    pylab.figure(figsize=(10,6))
    pylab.bar(list(range(len(count_list))), count_list, tick_label = countries)
    pylab.title("Countries with highest number of attacks")
    pylab.xlabel("Countries")
    pylab.ylabel("Number of attacks")
    
def get_country_code(country_list, country):
    
    """
    Returns country code for country name passed to it. 
    
    """

    for item in country_list:
        
        if country == item[1]:
            
            return item[0]
    
def main():
    
    """
    Main driver of the program. Calls other functions. Prompts user for file 
    input iterates through IP attacks file - calling proper functions. Handles
    data display and data prompts.
    """
    
    display_list = []
    
    tup = ()
    
    file = open_file("Enter the filename for the IP Address location list: ")
    ip_data = read_ip_location(file)
    
    file = open_file("Enter the filename for the IP Address attacks: ")
    attack_data = read_ip_attack(file)
    
    file = open_file("Enter the filename for the country codes: ")
    country_data = read_country_name(file)
    
    #MIRMIR
    
    print()
    
    #Calls requred functions for each item in attack_data and creates a list
    #of tuples with country_name and private_ip
    
    for item in attack_data:
        
        ip_attack = item[0]
        
        private_ip = item[1]
    
        country_code = locate_address(ip_data, ip_attack)
        
        country_name = get_country_name(country_data, country_code)
        
        tup = (private_ip, country_name)
        
        display_list.append(tup)
        
    disp_inp = input("Do you want to display all data? ")
    
    if disp_inp.lower() == "yes":
        
        for item in display_list:
            
            print("The IP Address: {:<19s}originated from {:<}"
                  .format(str(item[0]), str(item[1])))
            
    top_ten = []
    
    #Iterator to find highest attack count for country codes
            
    for item in display_list:
        
        name = item[1]
        
        count = 0
        
        code = get_country_code(country_data,name)
        
        for item in display_list:
           
           if name == item[1]:
            
               count += 1
               
        tup = (code, count)
        
        if tup not in top_ten:
        
            top_ten.append(tup)
            
    #Sort by alpha and then by number
        
    top_ten.sort(reverse = True)
    top_ten.sort(key=itemgetter(1), reverse = True )
    
    #Trim list to just top ten entries
    
    top_ten_new = top_ten[0:10]
    
    print()
    print("Top 10 Attack Countries")
    print("Country  Count")
         
    codes = []
    
    counts = []
    
    #Display for top ten 
    
    for item in top_ten_new:
        
        count = item[1]
        
        code = item[0]
        
        codes.append(code)
        
        counts.append(count)
        
        print("{:<10} {:>3}".format(code,item[1]))
        
    #Prompt for plot and function call 
            
    answer = input("\nDo you want to plot? ")
    
    if answer.lower() == "yes":
        
        bar_plot(counts,codes)
        
        
    
if __name__ == "__main__":
    
      main()
    
