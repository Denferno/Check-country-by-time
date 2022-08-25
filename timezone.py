from bs4 import BeautifulSoup
import requests
import sys

time_url = 'https://www.timeanddate.com/worldclock/?sort=2'

def main():
    inputted_country_time = test_input() #  Example: you typed in 23:01 this will become 2301 since that's easier to work with
    response_time = requests.get(time_url) 
    html_text_time = BeautifulSoup(response_time.text, 'html.parser')
    times = html_text_time.find_all(class_='rbi')  # class rbi is used for all the different times
    all_times = []  
    for time in times:
        time = time.text.split()[-1]  # removing the day (example Fri 19:38 = 19:38)
        time = time.replace(':', "")  # removing the double dots (example 19:38 = 1938)
        all_times.append(int(time)) 
    

    index = [i for i, x in enumerate(all_times) if x == inputted_country_time]  # removing the double dots in the input
    index = []
    last_two_digits = [] #  This is for when you type the last two digits wrong or just too late
    run_once = False  
    # The website im scraping only has three different minutes counter. 
    # Example: In Western Australia, Eucla its currently:   05:46
    #           In Europe, France its currently:            23:01
    #           And in India, Delhi its currently:          02:31
    # No country has a different minute counter other than these three on this website
    # The program always starts with an American city that has the same minute counter as Europeans and most countries (Example: the France minutes counter (23:01)
    for i, x in enumerate(all_times):  # x[-2:] are the last two digits (the minutes ), I only need two numbers
        if run_once is False:
            x = str(x)  # It needs to be temporarily string again so that I can use slices in the code here below 
            inputted_country_time = str(inputted_country_time)
            last_two_digits.append(int(x[-2:])) # Example: '2301' will become '01' because of slices and the int will make it 1 and then it will add 1 to the list
            # Now we have to get the other minutes
            last_two_digits.append((last_two_digits[-1] + 30) % 60) #  1 + 30 %  60 = 31 
            last_two_digits.append((last_two_digits[-1] + 45) % 60) #  1 + 45 % 60 = 46
            difference = max(last_two_digits)
            for minute in (last_two_digits):  # Example: (0, 46), (1, 1), (2, 31)
                number = abs(int(inputted_country_time[-2:]) - minute)  # Example: input = 02:29 becomes 29 - 46 = *17*     or 29 - 1 = *28* or 29 - 31 = *2*
                # There is still a problem. If we type in 22:59 even though it's already 23:01 it won't see that the difference is only 2 minutes because 59 - 1 = 58
                # But if we use this line below it will fix the problem 
                number2 = 60 % int(inputted_country_time[-2:]) + minute #  60 % 59 + 1 = 2   
                if min(number, number2) < difference:  # Example: 17 < 46 = yes               29 < 17 = no            2 < 17 = yes                   / I only need the index
                    difference = min(number, number2)
                    closest_minute = minute  # 17 becomes the closest_number        Nothing changes         2 becomes the closest_number   / so that I can use this number
            # Now I'm combining the first two numbers I entered and using the number thats closest to the number I typed in
            inputted_country_time = int(str(inputted_country_time[:-2]) + str(closest_minute))
            # Example: input = 22:59 but the actual time I wanted was 23:017
            # The first part will use the 23 I typed in 
            run_once = True
        if x == inputted_country_time:
            index.append(i)
        
    countries = []
    table_rows = html_text_time.find_all('td')
    for table_row in table_rows:
        href_link = table_row.find('a', href=True)
        href_link = str(href_link)
        if href_link != 'None':
            href_link = href_link.split('/')[2]
            countries.append(href_link)
    possible_countries = []
    for i in index:
        if countries[i].capitalize() not in possible_countries:  # This is for removing duplicates
            possible_countries.append(countries[i].capitalize())
    
    print(*possible_countries, sep='\n')
    # The current input is in formatted without the double dots in the middle, so it's formatted like this (2301)
    # To format it with the double dots I'm gonna use slices again
    inputted_country_time = str(inputted_country_time) 
    if len(inputted_country_time) == 2:  #
        inputted_country_time =  '00' + inputted_country_time
    elif len(inputted_country_time) == 1:
        inputted_country_time == '000' + inputted_country_time
    correct_time_format = inputted_country_time[:-2] + ':' + inputted_country_time[-2:]

        
    if difference == 0:
       print(f'There are {len(possible_countries)} possible countries with the time {correct_time_format}')
    else:
        print(f'\nDid you meant to type in {correct_time_format}?')
        print(f'If you did, then there are {len(possible_countries)} possible countries with the time: {correct_time_format}')
    
    print('\nClick on ENTER to close the program')
    if input('\nIf you would like to restart the program, type in R and press ENTER: ').lower() == 'r':
        main()
    else:
        sys.exit()
 
def test_input():
    print("Type in the time and to find out where they're from")
    print("Example: 20:09, it also works if you have it in without the double dots.") 
    print("It can be a couple minutes off")    
    while True:   
        typed_time = input("You can type here: ")
        typed_time = typed_time.replace(':', '')
        try:
            if len(typed_time) > 4:
                print('\nInvalid Time, there are no times with more than 5 numbers\n')
                continue
            elif 0 > int(typed_time[-2:]) or int(typed_time[-2:])  > 59 :
                print('\nInvalid Time, the minutes should be between 0 and 59\n')
                print('\nInvalid Time, the hours should be between 0 and 23\n')
                continue
            elif 0 > int(typed_time[:-2]) or int(typed_time[:-2]) > 23:
                print('\nInvalid Time,the minutes should be between 0 and 59\n')
                print('\nInvalid Time, the hours should be between 0 and 23\n')
                continue
            return int(typed_time)
        except ValueError:
            print ('\nValid number, please\n')
            continue

if __name__ == '__main__':
     main()

#  type in the the possible cities you want from the country.