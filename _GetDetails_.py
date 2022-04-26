import os
import sys
import platform
import requests
import urllib3

from bs4 import BeautifulSoup
from urllib.request import urlopen

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def clear_screen() :
    try:
        if platform.uname().system in ("Linux","Darwin"):
            os.system("clear")
        elif platform.uname().system == "Windows":
            os.system("cls")
    except:
        pass


class GetPlacesOfBirth :
    
    def get_pb () :
        place_code = []
        place_name = []
        
        session = requests.Session()
        
        place_html = session.get("https://sapsnkra.moe.gov.my/ibubapa2/indexv2.php", verify = False)
        
        soup = BeautifulSoup(place_html.text, "lxml")
        
        for option in soup.find_all('option'):
            
            if option['value'] != "" :
                place_code.append(option["value"])
            if option.text not in ("-PILIH NEGERI-", "-PILIH DAERAH-", "-PILIH SEKOLAH-") :
                place_name.append(option.text)
        
        return (place_code, place_name)

class GetAreas :
    
    def get_area (pb) :
        area_code = []
        area_name = []
        
        session = requests.Session()
        
        area_html = session.get( f"https://sapsnkra.moe.gov.my/ajax/senarai_ppd.php?kodnegeri={pb}", verify = False)
        
        soup = BeautifulSoup(area_html.text, "lxml")
        
        for option in soup.find_all('option'):
            
            if option['value'] != "" :
                area_code.append(option["value"])
            if option.text != "-PILIH PPD-" :
                area_name.append(option.text)
        
        return (area_code, area_name)


class GetSchools :
    
    def get_school (pb, area_code) :
        school_code = []       
        school_name = []       
        session = requests.Session()
        
        school_html = session.get( f"https://sapsnkra.moe.gov.my/ajax/ddl_senarai_sekolah.php?kodnegeri={pb}&kodppd={area_code}", verify = False)
        
        soup = BeautifulSoup(school_html.text, "lxml")
        
        for option in soup.find_all('option'):
            
            if option['value'] != "" :
                school_code.append(option["value"])
            if option.text != "-PILIH SEKOLAH-" :
                school_name.append(option.text)
        
        return (school_code, school_name)


if __name__ == '__main__' :
    
    while True :
        
        clear_screen()
        places = GetPlacesOfBirth.get_pb()
        for place_name in places[1] :
            print (place_name)
            
        print( "-"*20)
        user_input_place_code = str (input("Please enter the place of birth : (13) "))
        clear_screen()
        
        if user_input_place_code in places[0] :
            
            areas = GetAreas.get_area(user_input_place_code)
            for area_name in areas[1] :
                print (area_name)
                
            print( "-"*20)
            print( f"Place of Birth : {places[1][places[0].index(user_input_place_code)]}")
            user_input_area_code = str (input("Please enter the area code : (Y040) "))
            clear_screen()
            
            if user_input_area_code in areas[0] :
                
                schools = GetSchools.get_school(user_input_place_code, user_input_area_code)
                for i in range(len(schools[0])) :
                    print ( f"{schools[0][i]}\t   {schools[1][i]}")
                
                print( "-"*20)
                print( f"Place of Birth : {places[1][places[0].index(user_input_place_code)]}")
                print( f"Area : {areas[1][areas[0].index(user_input_area_code)]}")
                user_input_school_code = str (input("Please enter the school code : (YCC4102) "))
                
                clear_screen()
                print( "-"*20)
                print( f"Place of Birth : {user_input_place_code}")
                print( f"Area : {user_input_area_code}")
                print( f"School : {user_input_school_code}")
                print( "Now key in all this details into the __main__.py file")
                
                break
            
        input ( "You had entered wrong code, please try again\nPress enter to continue...")
        