import os
import sys
import time
import json
import platform
import requests
import urllib3

from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from urllib.request import urlopen

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def ClearScreen(Art = True, TextArt = open ("MYScraper\\ASCII_Text_Art", "r", encoding = "UTF-8").readlines()) :
    try:
        if platform.uname().system in ("Linux", "Darwin"):
            os.system("clear")
        elif platform.uname().system == "Windows":
            os.system("cls")
    
    except:
        pass
            
    finally :
        if Art :
            for art in TextArt :
                print ( f"\t{art}", end = "", flush = True )
                


class _PlacesOfBirth :
    
    def __init__(self) :
        pass
    
    def Response () :
        while True :
            try :
                PlacesCodeList = []
                PlacesNameList = []
                
                Session = requests.Session()
                
                PlacesHTML = Session.get("https://sapsnkra.moe.gov.my/ibubapa2/indexv2.php", verify = False)
                
                Locater = BeautifulSoup(PlacesHTML.text, "lxml")
                
                for Options in Locater.find_all("option") :
                    
                    if Options["value"] != "" :
                        PlacesCodeList.append(Options["value"])
                    if Options.text not in ("-PILIH NEGERI-", "-PILIH DAERAH-", "-PILIH SEKOLAH-") :
                        PlacesNameList.append(Options.text)
                
                return (PlacesCodeList, PlacesNameList)
            
            except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout, urllib3.exceptions.ConnectTimeoutError, urllib3.exceptions.ReadTimeoutError, urllib3.exceptions.MaxRetryError, TimeoutError) :
                time.sleep(5)
                continue
            
    def RetrievePlaceFromDatabase (PlaceCode = None, AreaCode = None, SchoolCode = None) :
        if all(Para is None for Para in {PlaceCode, AreaCode, SchoolCode}) :
            raise ValueError("Expected either PlaceCode, AreaCode or SchoolCode")
    
        Data = _Get.RetrieveData() 
        ReturnCode = []
        ReturnName = []
        
        try :
            
            if PlaceCode is not None :
                Index = list( Data["Code"] ).index(PlaceCode)
                ReturnsCode.append(PlaceCode)
                ReturnsName.append(list(Data["Name"])[CodeIndex])
            
            if AreaCode is not None :
                for _PlaceCode in Data["Code"] :
                    if AreaCode in list( Data["Code"][_PlaceCode] ) :
                        Index = list( Data["Code"] ).index(_PlaceCode)
                        ReturnCode.append(_PlaceCode)
                        ReturnName.append( list(Data["Name"])[Index] )
                        break
                
            if SchoolCode is not None :
                for _PlaceCode in Data["Code"] :
                    for _AreaCode in Data["Code"][_PlaceCode] :
                        if SchoolCode in list( Data["Code"][_PlaceCode][_AreaCode] ) :
                            Index = list( Data["Code"] ).index(_PlaceCode)
                            ReturnCode.append(_PlaceCode)
                            ReturnName.append( list(Data["Name"])[Index] )
                            break
                    else :
                        continue
                    break
                        
            AllSameCode = all(Code == ReturnCode[0] for Code in ReturnCode)
            AllSameName = all(Name == ReturnName[0] for Name in ReturnName)
            
            if AllSameCode and AllSameName :
                return [ReturnCode[0], ReturnName[0]]
            
            else :
                raise ValueError
                       
        except (KeyError, ValueError) :
            raise Exception("You might had input the code outside of our database, if the error is still occuring, you can remove the <Database.json> file and try again.")


class _Areas :
    
    def __init__(self, PlaceOfBirthCode) :
        self.PlaceOfBirthCode = PlaceOfBirthCode
    
    def Response (self) :
        while True :
            try :
                AreasCodeList = []
                AreasNameList = []
                
                Session = requests.Session()
                
                AreasHTML = Session.get( f"https://sapsnkra.moe.gov.my/ajax/senarai_ppd.php?kodnegeri={self.PlaceOfBirthCode}", verify = False)
                
                Locater = BeautifulSoup(AreasHTML.text, "lxml")
                
                for Options in Locater.find_all("option"):
                    
                    if Options["value"] != "" :
                        AreasCodeList.append(Options["value"])
                    if Options.text not in ("-PILIH PPD-") :
                        AreasNameList.append(Options.text)
                
                return (AreasCodeList, AreasNameList)
            
            except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout, urllib3.exceptions.ConnectTimeoutError, urllib3.exceptions.ReadTimeoutError, urllib3.exceptions.MaxRetryError, TimeoutError) :
                time.sleep(5)
                continue
            
    def RetrieveAreaFromDatabase (AreaCode = None, SchoolCode = None) :
        if all(Para is None for Para in {AreaCode, SchoolCode}) :
            raise ValueError("Expected either AreaCode or SchoolCode")
            
        Data = _Get.RetrieveData() 
        ReturnCode = []
        ReturnName = [] 
        
        try :
            
            if AreaCode is not None :
                for _PlaceCode in Data["Code"] :
                    if AreaCode in list( Data["Code"][_PlaceCode] ) :
                        Index = list( Data["Code"][_PlaceCode] ).index(AreaCode)
                        ReturnCode.append(AreaCode)
                        PlaceName = _PlacesOfBirth.RetrievePlaceFromDatabase(AreaCode = AreaCode)[1]
                        ReturnName.append( list( Data["Name"][PlaceName] )[Index] )
                        break
                
            if SchoolCode is not None :
                for _PlaceCode in Data["Code"] :
                    for _AreaCode in Data["Code"][_PlaceCode] :
                        if SchoolCode in list( Data["Code"][_PlaceCode][_AreaCode] ) :
                            Index = list( Data["Code"][_PlaceCode] ).index(_AreaCode)
                            ReturnCode.append(_AreaCode)
                            PlaceName = _PlacesOfBirth.RetrievePlaceFromDatabase(SchoolCode = SchoolCode)[1]
                            ReturnName.append( list( Data["Name"][PlaceName] )[Index] )
                            break
                    else :
                        continue
                    break
                        
            AllSameCode = all(Code == ReturnCode[0] for Code in ReturnCode)
            AllSameName = all(Name == ReturnName[0] for Name in ReturnName)
            
            if AllSameCode and AllSameName :
                return [ReturnCode[0], ReturnName[0]]
            
            else :
                raise ValueError
                       
        except (KeyError, ValueError) :
            raise Exception("You might had input the code outside of our database, if the error is still occuring, you can remove the <Database.json> file and try again.")


class _Schools :
    
    def __init__(self, PlaceOfBirthCode, AreaCode) :
        self.PlaceOfBirthCode = PlaceOfBirthCode
        self.AreaCode = AreaCode
        
    def Response (self) :
        while True :
            try :
                SchoolsCodeList = []
                SchoolsNameList = []
                Session = requests.Session()
                
                school_html = Session.get( f"https://sapsnkra.moe.gov.my/ajax/ddl_senarai_sekolah.php?kodnegeri={self.PlaceOfBirthCode}&kodppd={self.AreaCode}", verify = False)
                
                Locater = BeautifulSoup(school_html.text, "lxml")
                
                for Options in Locater.find_all("option"):
                    
                    if Options["value"] != "" :
                        SchoolsCodeList.append(Options["value"])
                    if Options.text not in ("-PILIH SEKOLAH-") :
                        SchoolsNameList.append(Options.text)
                
                return (SchoolsCodeList, SchoolsNameList)
            
            except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout, urllib3.exceptions.ConnectTimeoutError, urllib3.exceptions.ReadTimeoutError, urllib3.exceptions.MaxRetryError, TimeoutError) :
                time.sleep(5)
                continue

    def RetrieveSchoolFromDatabase (SchoolCode) :
        Data = _Get.RetrieveData() 
        
        try :
                
            for _PlaceCode in Data["Code"] :
                for _AreaCode in Data["Code"][_PlaceCode] :
                    if SchoolCode in list( Data["Code"][_PlaceCode][_AreaCode] ) :
                        Index = list( Data["Code"][_PlaceCode][_AreaCode] ).index(SchoolCode)
                        ReturnCode = SchoolCode
                        PlaceName = _PlacesOfBirth.RetrievePlaceFromDatabase(SchoolCode = SchoolCode)[1]
                        AreaName = _Areas.RetrieveAreaFromDatabase(SchoolCode = SchoolCode)[1]
                        ReturnName = list( Data["Name"][PlaceName][AreaName] )[Index]
                        
                        return [ReturnCode, ReturnName]
                    
            else :
                raise ValueError
                       
        except (KeyError, ValueError) as e :
            
            raise Exception( f"{e}\nYou might had input the code outside of our database, if the error is still occuring, you can remove the <Database.json> file and try again.")
        

class _Get :
    
    def __init__(self, SchoolCode = None) :
        self.SchoolCode = SchoolCode
        
    def Response (self, BirthDate, PlaceOfBirth, FourDigitsNumber) :
        while True :
            try :
                Session = requests.Session()
                
                if FourDigitsNumber != None : # Run if Four Digits Number has been generated
                    
                    if self.SchoolCode == None : # If user didn't provided School Code
                        Response = Session.get( f"https://sapsnkra.moe.gov.my/ajax/papar_carian.php?nokp={BirthDate}{PlaceOfBirth}{FourDigitsNumber}", verify = False)
                        
                        if ("Tidak Wujud" not in Response.text) : 
                            IdentityCode = str ( f"{BirthDate}{PlaceOfBirth}{FourDigitsNumber}")
                            return [True, IdentityCode]
                            
                        elif ("Tidak Wujud" in Response.text) :
                            IdentityCode = str ( f"{BirthDate}{PlaceOfBirth}{FourDigitsNumber}")
                            return [False, IdentityCode]
                    
                    
                    elif self.SchoolCode != None : # If user provided School Code
                        Response = Session.get( f"https://sapsnkra.moe.gov.my/ajax/papar_carianpelajar.php?nokp={BirthDate}{PlaceOfBirth}{FourDigitsNumber}&kodsek={self.SchoolCode}", verify = False)
                        
                        if ("Tidak Wujud" not in Response.text) : 
                            
                            SchoolsNameHTML = Session.get("https://sapsnkra.moe.gov.my/ibubapa2/semak.php", verify = False)
                            
                            Locater = BeautifulSoup(SchoolsNameHTML.text, "lxml")
                            StudentName = ((Locater.find(lambda t: t.text.strip() == "NAMA MURID")).find_next("td")).find_next("td")
                            
                            Place = _PlacesOfBirth.RetrievePlaceFromDatabase(SchoolCode = self.SchoolCode)
                            PlaceCodeReturn = Place[0]
                            PlaceNameReturn = Place[1]
                            Area = _Areas.RetrieveAreaFromDatabase(SchoolCode = self.SchoolCode)
                            AreaCodeReturn = Area[0]
                            AreaNameReturn = Area[1]
                            School = _Schools.RetrieveSchoolFromDatabase(SchoolCode = self.SchoolCode)
                            SchoolCodeReturn = School[0]
                            SchoolNameReturn = School[1]
                            IdentityCode =  f"{BirthDate}{PlaceOfBirth}{FourDigitsNumber}"
                            StudentNameReturn = StudentName.text
                            
                            return [True, IdentityCode, SchoolCodeReturn, SchoolNameReturn, StudentNameReturn, PlaceCodeReturn, PlaceNameReturn, AreaCodeReturn, AreaNameReturn]
                            
                        elif ("Tidak Wujud" in Response.text) :
                            
                            Place = _PlacesOfBirth.RetrievePlaceFromDatabase(SchoolCode = self.SchoolCode)
                            PlaceCodeReturn = Place[0]
                            PlaceNameReturn = Place[1]
                            Area = _Areas.RetrieveAreaFromDatabase(SchoolCode = self.SchoolCode)
                            AreaCodeReturn = Area[0]
                            AreaNameReturn = Area[1]
                            School = _Schools.RetrieveSchoolFromDatabase(SchoolCode = self.SchoolCode)
                            SchoolCodeReturn = School[0]
                            SchoolNameReturn = School[1]
                            IdentityCode = str ( f"{BirthDate}{PlaceOfBirth}{FourDigitsNumber}")
                            
                            return [False, IdentityCode, SchoolCodeReturn, SchoolNameReturn, PlaceCodeReturn, PlaceNameReturn, AreaCodeReturn, AreaNameReturn]
                        
                return None
            
            except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectTimeout, urllib3.exceptions.ConnectTimeoutError, urllib3.exceptions.ReadTimeoutError, urllib3.exceptions.MaxRetryError, TimeoutError) :
                time.sleep(5)
                continue
    
    def FourDigitsNumber(i, Gender) :
        if Gender in ("MALE", "FEMALE", "M", "F") :
            if Gender in ("MALE", "M") :
                if i%2 != 0 or i == 0 :
                    return f'{i:04}'
        
            elif Gender in ("FEMALE", "F") :
                if i%2 == 0 or i == 0 :
                    return f'{i:04}'
                
            return None
                
        else :
            return f'{i:04}'
        
    def RetrieveData() :
        if ( datetime.utcfromtimestamp(os.path.getmtime("Database.json")) >= datetime.utcnow() - timedelta(days = 1) ) : # If last file modified time not more than 1 day
            if os.stat("Database.json").st_size != 0 : # If the file is not empty
                with open("Database.json", "r", encoding = "utf-8") as f :
                    return json.load(f)
            
        Data = {}
        Data["Code"] = {}
        Data["Name"] = {}
        
        Places = _PlacesOfBirth.Response()
        for PlaceCode, PlaceName in zip(Places[0], Places[1]) :
            Data["Code"][PlaceCode] = {}
            Data["Name"][PlaceName] = {}
            
            Areas = _Areas(PlaceCode).Response()
            for AreaCode, AreaName in zip(Areas[0], Areas[1]) :
                Data["Code"][PlaceCode][AreaCode] = []
                Data["Name"][PlaceName][AreaName] = []
                
                Schools = _Schools(PlaceCode, AreaCode).Response()
                for SchoolCode, SchoolName in zip(Schools[0], Schools[1]) :
                    Data["Code"][PlaceCode][AreaCode].append(SchoolCode)
                    Data["Name"][PlaceName][AreaName].append(SchoolName)        
                    
        with open ("Database.json", "w", encoding = "utf-8") as f :
            json.dump(Data, f, indent = 4, ensure_ascii = False, sort_keys = False)

        return Data
    
    def VerifyCode(Code) :
        Data = _Get.RetrieveData()
        
        for PlaceCode in Data["Code"] :
            if Code == PlaceCode :
                return True
            
            for AreaCode in Data["Code"][PlaceCode] :
                if Code == AreaCode :
                    return True
                
                for SchoolCode in Data["Code"][PlaceCode][AreaCode] :
                    if Code == SchoolCode :
                        return True

        return False


def __init__ () :
    try:
        with open ("Database.json", "r", encoding = "utf8") as f:
            pass
    except FileNotFoundError :
        with open ("Database.json", "w+", encoding = "utf8") as f:
            pass

__init__ ()

if __name__ == "__main__" : # A program to get All the Code Listing including Places of Birth Code, Area Code, School Code that available
    
    _Get.RetrieveData()
    
    while True :
        
        ClearScreen()
        Places = _PlacesOfBirth.Response()
        for PlacesName in Places[1] :
            print (PlacesName)
            
        print( "-"*20)
        UserInputPlaceCode = str (input("Please enter the place of birth : (13) "))
        ClearScreen()
        
        if UserInputPlaceCode in Places[0] :
            
            
            Areas = _Areas(UserInputPlaceCode).Response()
            for AreasName in Areas[1] :
                print (AreasName)
                
            print( "-"*20)
            print( f"Place of Birth : {Places[1][Places[0].index(UserInputPlaceCode)]}")
            print( "-"*20)
            UserInputAreaCode = str (input("Please enter the area code : (Y040) "))
            ClearScreen()
            
            if UserInputAreaCode in Areas[0] :
                
                Schools = _Schools(UserInputPlaceCode, UserInputAreaCode).Response()
                for i in range(len(Schools[0])) :
                    print ( f"{Schools[0][i]}\t   {Schools[1][i]}")
                
                print( "-"*20)
                print( f"Place of Birth : {Places[1][Places[0].index(UserInputPlaceCode)]}")
                print( f"Area : {Areas[1][Areas[0].index(UserInputAreaCode)]}")
                print( "-"*20)
                UserInputSchoolCode = str (input("Please enter the school code : (YCC4102) "))
                ClearScreen()
                
                if UserInputSchoolCode in Schools[0] :
                    print( "-"*20)
                    print( f"Place of Birth Code : {UserInputPlaceCode}")
                    print( f"Area Code : {UserInputAreaCode}")
                    print( f"School Code : {UserInputSchoolCode}")
                    print( "-"*20)
                    print( "And that's all you need, you might use these information")
                    print( "on the __main__.py script, or you may re-run this script")
                    print( "to get more information\n")
                
                    break
            
        input ( "You had entered wrong code, please try again\nPress enter to continue...")
        