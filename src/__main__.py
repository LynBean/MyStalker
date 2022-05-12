# Purpose : For Educational Purposes Only :/                                                                         Of course not, I'm going to stalk my haters muahahahaha
# Programmer : Asuna Yuuki
# Version : 2.2.0

import os
import sys
import json
import time
import datetime
import random
import shutil

from src.__retrieve__ import ClearScreen, _PlacesOfBirth, _Areas, _Schools, _Get


def ClearLastLine (GetWidthOnly = False) :
    global Width
    Width = shutil.get_terminal_size()[0]
    if not GetWidthOnly :
        print (" "*(Width), end = "\r", flush = True)

def ValidateDatetime(Date):
    try :
        datetime.datetime.strptime(Date, "%y%m%d")
        return True
    except ValueError:
        return False
    
    
def FileDumpWithSchools(Response) : 
    # Response return [True, IdentityCode, SchoolCodeReturn, SchoolNameReturn, StudentNameReturn, PlaceCodeReturn, PlaceNameReturn, AreaCodeReturn, AreaNameReturn]
    PlaceCode = Response[5]
    PlaceName = Response[6]
    AreaCode = Response[7]
    AreaName = Response[8]
    SchoolCode = Response[2]
    SchoolName = Response[3]
    IdentityCode = Response[1]
    StudentName = Response[4]

    try : # Retrieve Data first using "r" mode, if using "w" mode, it will truncate the data
        Data = json.load(open ("HereYouGo.json", "r", encoding ="utf8"))
    except :
        Data = {}
    
    # Write into a .txt file
    with open ("HereYouGo.txt", "a", encoding ="utf8") as TxTFile, open ("HereYouGo.json", "w", encoding ="utf8") as JsonFile :
        TxTFile.write( f"{IdentityCode}\t{StudentName}\t{SchoolCode}\t{SchoolName}\t{AreaName}\t{PlaceName}\n")
    
    # Write into a .json file
            
        '''
        Data[PlaceCode] = {
                            "PlaceName": PlaceName,
                            "Areas": {
                                AreaCode: {
                                    "AreaName": AreaName,
                                    "Schools": {
                                        SchoolCode: {
                                            "SchoolName": SchoolName,
                                            "Students": {
                                                IdentityCode: {
                                                    "StudentName": StudentName
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
        '''
        
        if PlaceCode not in Data.keys() :
            Data[PlaceCode] = {
                "PlaceName": PlaceName,
                "Areas": {
                    AreaCode: {
                        "AreaName": AreaName,
                        "Schools": {
                            SchoolCode: {
                                "SchoolName": SchoolName,
                                "Students": {
                                    IdentityCode: {
                                        "StudentName": StudentName
                                    }
                                }
                            }
                        }
                    }
                }
            }
            
        if AreaCode not in Data[PlaceCode]["Areas"].keys() :
            Data[PlaceCode]["Areas"][AreaCode] = {
                "AreaName": AreaName,
                "Schools": {
                    SchoolCode: {
                        "SchoolName": SchoolName,
                        "Students": {
                            IdentityCode: {
                                "StudentName": StudentName
                            }
                        }
                    }
                }
            }

        if SchoolCode not in Data[PlaceCode]["Areas"][AreaCode]["Schools"] :
            Data[PlaceCode]["Areas"][AreaCode]["Schools"][SchoolCode] = {
                "SchoolName": SchoolName,
                "Students": {
                    IdentityCode: {
                        "StudentName": StudentName
                    }
                }
            }

        if IdentityCode not in Data[PlaceCode]["Areas"][AreaCode]["Schools"][SchoolCode]["Students"] :
            Data[PlaceCode]["Areas"][AreaCode]["Schools"][SchoolCode]["Students"][IdentityCode] = {
                "StudentName": StudentName
            }
            
        json.dump (Data, JsonFile, indent = 4, ensure_ascii = False, sort_keys = False)
        
    
        
def main () :
    
    ClearScreen()
    print ("\tGenerating Database ... Please wait for a while ...")
    _Get.RetrieveData()
    
    if not os.path.exists("HereYouGo.json") :
        with open ("HereYouGo.json", "w+", encoding ="utf8") as f:
            pass
    if not os.path.exists("HereYouGo.txt") :
        with open ("HereYouGo.txt", "w+", encoding ="utf8") as f:
            pass
        
    while True:
        
        ClearScreen()
        print ( "\tOptions" )
        print ( "\t--------------------------------")
        print ( "\t1. Provide details of the user :" )
        print ( "\t    - Birth Date (Compulsary)" )
        print ( "\t    - Gender (Optional)" )
        print ( "\t    - Place of Birth Code (Optional)" )
        print ( "\t    - Area Code (Optional)" )
        print ( "\t    - School Code (Optional)" )
        print ( "\t   You will get the user **Full name**, **Identity Number in Malaysia**, **Place of Birth**, **Areas Stayed Before**, **Schools Studied Before**", end = "\n\n" )
        print ( "\t2. Provide details of the user :" )
        print ( "\t    - Identity Number in Malaysia" )
        print ( "\t   You will get the user **Full name**, **Areas Stayed Before**, **Schools Studied Before**", end = "\n\n" )
        print ( "\t--------------------------------")
        Option = input("\n\tChoose : ")
        
        global BirthDate, UserInputPlaceCode, Gender, UserInputSchoolCode, UserInputFourDigitsNumber
        
        match Option : # New Switch-case function only for Python Version >= 3.10
            
            case "1" :
                UserInputFourDigitsNumber = None
                
                while True :
                    ClearScreen()
                    BirthDate = str ( input( "\tPlease provide a valid birth date in the format of YYMMDD : (031231) "))
                    if ValidateDatetime(BirthDate) :
                        break
                    
                while True :
                    ClearScreen()
                    Gender = str ( input( "\tPlease provide sex : (Female)(If no just keep it blank) ")).upper()
                    if Gender in ("MALE", "FEMALE", "M", "F", "") :
                        break
                    
                while True :
                    ClearScreen()
                    UserInputPlaceCode = str ( input( "\tPlease provide a valid place of birth : (13)(If no just keep it blank) "))
                    if _Get.VerifyCode(UserInputPlaceCode) or UserInputPlaceCode in ("") :
                        break
                    
                while True :
                    ClearScreen()
                    UserInputAreaCode = str ( input( "\tPlease provide a valid area code : (Y040)(If no just keep it blank) ")).upper()
                    if _Get.VerifyCode(UserInputAreaCode) or UserInputAreaCode in ("") :
                        break
                    
                while True :
                    ClearScreen()
                    UserInputSchoolCode = str ( input( "\tPlease provide a valid school code : (YCC4102)(If no just keep it blank) ")).upper()
                    if _Get.VerifyCode(UserInputSchoolCode) or UserInputSchoolCode in ("") :
                        break
                break
            
            case "2" :
                while True :
                    ClearScreen()
                    
                    IdentityCode = input( "\tPlease provide a valid identity codes : (011231101234) ")
                    if len (IdentityCode) > 12 or not (IdentityCode).isdecimal() :
                        continue
                    
                    if not ValidateDatetime( IdentityCode[0:6] ) :
                        continue
                    BirthDate = IdentityCode[0:6]
                    
                    if not _Get.VerifyCode( IdentityCode[6:8]) :
                        continue
                    UserInputPlaceCode = IdentityCode[6:8]
                    
                    if int ( IdentityCode[8:12] ) not in range (10000) :
                        continue
                    UserInputFourDigitsNumber = IdentityCode[8:12]
                    
                    break
                break
            
            case default :
                continue
                
    
    ExistingList = []
    Output = True

    
    if Option == "1" :
        
        PlaceVerify = _Get.VerifyCode(UserInputPlaceCode)
        AreaVerify = _Get.VerifyCode(UserInputAreaCode)
        SchoolVerify = _Get.VerifyCode(UserInputSchoolCode)
        
        Places = _PlacesOfBirth.Response()
            
        if AreaVerify :
            PriorityPlaceCode = _PlacesOfBirth.RetrievePlaceFromDatabase(AreaCode = UserInputAreaCode)[0]
            Index = Places[0].index(PriorityPlaceCode)
            Places[0].insert(0, Places[0].pop( Index ))
            Places[1].insert(0, Places[1].pop( Index ))
            
        if SchoolVerify :
            PriorityPlaceCode = _PlacesOfBirth.RetrievePlaceFromDatabase(SchoolCode = UserInputSchoolCode)[0]
            Index = Places[0].index(PriorityPlaceCode)
            Places[0].insert(0, Places[0].pop( Index ))
            Places[1].insert(0, Places[1].pop( Index ))

        if PlaceVerify :
            Index = Places[0].index(UserInputPlaceCode)
            Places[0].insert(0, Places[0].pop( Index ))
            Places[1].insert(0, Places[1].pop( Index ))
            
        FirstLoop = True

        while FirstLoop :
            
            if not SchoolVerify :
                FirstLoop = False
                
            for PlaceCode in Places[0] :
                
                try :
                    
                    ClearScreen()
                    print ("\tGot'cha ------------\n")
                    
                    if not ExistingList :
                        print ("\tEmpty~~ :(\n")
                        
                    for Existing in ExistingList :
                        print ( f"\t{Existing}\n")
                        
                    print ("\t" + "-"*20, "\n")
                    print ( f"\tCurrent Place : { Places[1][(Places[0].index(PlaceCode))] }\n")
                    print ("You may press <CTRL + C> to skip finding in this place\n")
                    time.sleep(5)
                    
                    Areas = _Areas(PlaceCode).Response() # return (AreasCodeList, AreasNameList)
                    
                    if SchoolVerify :
                        PriorityAreaCode = _Areas.RetrieveAreaFromDatabase(SchoolCode = UserInputSchoolCode)[0]
                        if PriorityAreaCode in Areas[0] :
                            Index = Areas[0].index(PriorityAreaCode)
                            Areas[0].insert(0, Areas[0].pop( Index ))
                            Areas[1].insert(0, Areas[1].pop( Index ))
                    
                    if AreaVerify and ( UserInputAreaCode in Areas[0] ) :
                        Index = Areas[0].index(UserInputAreaCode)
                        Areas[0].insert(0, Areas[0].pop( Index ))
                        Areas[1].insert(0, Areas[1].pop( Index ))
                    
                    for i in range(0, 10000) : 
                        
                        if Output :
                            ClearScreen()
                            print ("\tGot'cha ------------\n")
                            
                            if not ExistingList :
                                print ("\tEmpty~~ :(\n")
                                
                            for Existing in ExistingList :
                                print ( f"\t{Existing}\n")
                                
                            print ("\t" + "-"*20, "\n")
                            print ( f"\tCurrent Place : { Places[1][(Places[0].index(PlaceCode))] }\n")
                            print ("You may press <CTRL + C> to skip finding in this place\n")
                            Output = False
                        
                        FourDigitsNumber = _Get.FourDigitsNumber(i, Gender)
                        if FourDigitsNumber == None :
                            continue
                        
                        InitResponse = _Get()
                        Response = InitResponse.Response(BirthDate, PlaceCode, FourDigitsNumber) 
                            # Response return [Bool, IdentityCode]
                        
                        if not Response[0] : 
                            
                            ProgressionPlaces = [Places[0].index(PlaceCode), len(Places[0])]
                            Progression = (i / 10000) * 100
                            ClearLastLine()
                            ProgressPrint = f"Current Progress (Places {ProgressionPlaces[0]}/{ProgressionPlaces[1]})({Progression:.1f}%) : {Response[1]}"
                            print ( ProgressPrint[0:Width], end = "\r", flush = True)
                            continue
                            
                        if SchoolVerify and FirstLoop :
                            
                            if Output :
                                ClearScreen()
                                print ("\tGot'cha ------------\n")
                                
                                if not ExistingList :
                                    print ("\tEmpty~~ :(\n")
                                    
                                for Existing in ExistingList :
                                    print ( f"\t{Existing}\n")
                                    
                                print ("\t" + "-"*20, "\n")
                                print ( f"\tCurrent Place : { Places[1][(Places[0].index(PlaceCode))] }\n")
                                print ("You may press <CTRL + C> to skip finding in this place\n")
                                Output = False
                                
                            InitResponseWithSchool = _Get(SchoolCode = UserInputSchoolCode)
                            ResponseWithSchool = InitResponseWithSchool.Response(BirthDate, PlaceCode, FourDigitsNumber)
                                # Response return [Bool, IdentityCode, SchoolCodeReturn, SchoolNameReturn, StudentNameReturn, PlaceCodeReturn, PlaceNameReturn, AreaCodeReturn, AreaNameReturn]
                            
                            Progression = (i / 10000) * 100
                            ProgressionPlaces = [Places[0].index(PlaceCode), len(Places[0])]
                            ClearLastLine()
                            ProgressPrint = f"Current Progress (Places {ProgressionPlaces[0]}/{ProgressionPlaces[1]})({Progression:.1f}%) : {ResponseWithSchool[1]}\t{ResponseWithSchool[2]}\t{ResponseWithSchool[3]}"
                            print ( ProgressPrint[0:Width-10], end = "\r", flush = True)
                            
                            if not ResponseWithSchool[0] : 
                                continue
                            
                            FileDumpWithSchools(ResponseWithSchool)
                            ExistingList.append( f"{ResponseWithSchool[1]}\t{ResponseWithSchool[4]}\t{ResponseWithSchool[2]}\t{ResponseWithSchool[3]}\t{ResponseWithSchool[8]}\t{ResponseWithSchool[6]}")
                            Output = True
                            continue
                                
                        try :
                                
                            ClearLastLine()
                            print ( f"You may press <CTRL + C> to skip finding user {Response[1]}\n")
                            Output = True
                            time.sleep(5)
                            
                            for AreaCode in Areas[0] :
                                
                                try :
                                    
                                    Schools = _Schools(PlaceCode, AreaCode).Response() # return (SchoolsCodeList, SchoolsNameList)
                                    
                                    for SchoolCode in Schools[0] :
                                        
                                        if Output :
                                            ClearScreen()
                                            print ("\tGot'cha ------------\n")
                                            
                                            if not ExistingList :
                                                print ("\tEmpty~~ :(\n")
                                                
                                            for Existing in ExistingList :
                                                print ( f"\t{Existing}\n")
                                                
                                            print ("\t" + "-"*20, "\n")
                                            print ( f"\tCurrent Place : { Places[1][(Places[0].index(PlaceCode))] }")
                                            print ( f"\tCurrent Area : { Areas[1][(Areas[0].index(AreaCode))] }\n")
                                            print ( f"You may press <CTRL + C> to skip finding user {Response[1]} in this area\n")
                                            Output = False
                                            
                                        InitResponseWithSchool = _Get(SchoolCode = SchoolCode)
                                        ResponseWithSchool = InitResponseWithSchool.Response(BirthDate, PlaceCode, FourDigitsNumber)
                                            # Response return [Bool, IdentityCode, SchoolCodeReturn, SchoolNameReturn, StudentNameReturn, PlaceCodeReturn, PlaceNameReturn, AreaCodeReturn, AreaNameReturn]
                                        
                                        ProgressionAreas = [Areas[0].index(AreaCode), len(Areas[0])]
                                        ProgressionSchools = [Schools[0].index(SchoolCode), len(Schools[0])]
                                        ClearLastLine()
                                        ProgressPrint = f"Current Progress (Areas {ProgressionAreas[0]}/{ProgressionAreas[1]})(Schools {ProgressionSchools[0]}/{ProgressionSchools[1]}) : {ResponseWithSchool[1]}\t{ResponseWithSchool[2]}\t{ResponseWithSchool[3]}"
                                        print ( ProgressPrint[0:Width-10], end = "\r", flush = True)
                                        
                                        if not ResponseWithSchool[0] : 
                                            continue
                                        
                                        FileDumpWithSchools(ResponseWithSchool)
                                        ExistingList.append( f"{ResponseWithSchool[1]}\t{ResponseWithSchool[4]}\t{ResponseWithSchool[2]}\t{ResponseWithSchool[3]}\t{ResponseWithSchool[8]}\t{ResponseWithSchool[6]}")
                                        Output = True
                                        
                                    else :
                                        Output = True
                                        
                                except KeyboardInterrupt :
                                    Output = True
                                    continue
                                        
                            else :
                                Output = True
                                
                        except KeyboardInterrupt :
                            Output = True
                            continue
                                
                    else :
                        Output = True
                    
                except KeyboardInterrupt :
                    Output = True
                    continue
                
            else :
                FirstLoop = False
    
    
    elif Option == "2" :
        
        Places = _PlacesOfBirth.Response()
        Index = Places[0].index(UserInputPlaceCode)
        Places[0].insert(0, Places[0].pop( Index )) # Move priority place code infront
        Places[1].insert(0, Places[1].pop( Index )) # Move priority place name infront
        
        FourDigitsNumber = UserInputFourDigitsNumber
        
        for PlaceCode in Places[0] :
            
            try :
                ClearScreen()
                print ("\tGot'cha ------------\n")
                
                if not ExistingList :
                    print ("\tEmpty~~ :(\n")
                    
                for Existing in ExistingList :
                    print ( f"\t{Existing}\n")
                    
                print ("\t" + "-"*20, "\n")
                print ( f"\tCurrent Place : { Places[1](Places[0].index(UserInputPlaceCode)) }\n")
                print ("You may press <CTRL + C> to skip finding in this place\n")
                time.sleep(5)
                    
                Areas = _Areas(PlaceCode).Response() # return (AreasCodeList, AreasNameList)
                for AreaCode in Areas[0] :
                    
                    try :
                        Schools = _Schools(PlaceCode, AreaCode).Response() # return (SchoolsCodeList, SchoolsNameList)
                        
                        for SchoolCode in Schools[0] :
                            if Output :
                                ClearScreen()
                                print ("\tGot'cha ------------\n")
                                
                                if not ExistingList :
                                    print ("\tEmpty~~ :(\n")
                                    
                                for Existing in ExistingList :
                                    print ( f"\t{Existing}\n")
                                    
                                print ("\t" + "-"*20, "\n")
                                print ( f"\tCurrent Place : { Places[1][(Places[0].index(UserInputPlaceCode))] }\n")
                                print ( f"\tCurrent Area : { Areas[1][(Areas[0].index(AreaCode))] }\n")
                                print ("You may press <CTRL + C> to skip finding in this area")
                                Output = False
                                
                            InitResponseWithSchool = _Get(SchoolCode = SchoolCode)
                            ResponseWithSchool = InitResponseWithSchool.Response(BirthDate, UserInputPlaceCode, FourDigitsNumber)
                                # Response return [Bool, IdentityCode, SchoolCodeReturn, SchoolNameReturn, StudentNameReturn, PlaceCodeReturn, PlaceNameReturn, AreaCodeReturn, AreaNameReturn]
                            
                            ProgressionPlaces = [Places[0].index(PlaceCode), len(Places[0])]
                            ProgressionAreas = [Areas[0].index(AreaCode), len(Areas[0])]
                            ProgressionSchools = (Schools[0].index(SchoolCode) / len(Schools[0])) * 100
                            ClearLastLine()
                            ProgressPrint = f"Current Progress ({ProgressionPlaces[0]}/{ProgressionPlaces[1]})({ProgressionAreas[0]}/{ProgressionAreas[1]})({ProgressionSchools:.1f}%) : {ResponseWithSchool[1]}\t{ResponseWithSchool[2]}\t{ResponseWithSchool[3]}\t{ResponseWithSchool[7]}\t{ResponseWithSchool[5]}"
                            print ( ProgressPrint[0:Width-50], end = "\r", flush = True)
                            
                            if not ResponseWithSchool[0] : 
                                continue
                            
                            FileDumpWithSchools(ResponseWithSchool)
                            ExistingList.append( f"{ResponseWithSchool[1]}\t{ResponseWithSchool[4]}\t{ResponseWithSchool[2]}\t{ResponseWithSchool[3]}\t{ResponseWithSchool[8]}\t{ResponseWithSchool[6]}")
                            Output = True
                            
                        else :
                            Output = True
                            
                    except KeyboardInterrupt :
                        Output = True
                        continue
                        
            except KeyboardInterrupt :
                continue
            
    
    
    ClearScreen()
    print ( f"\tThe Following Results had been saved in the following path :\n\t{os.getcwd()}\HereYouGo.txt\n\t{os.getcwd()}\HereYouGo.json\n")
    
    if not ExistingList :
        print ("\tEmpty~~ :(\n")
        
    for Existing in ExistingList :
        print ( f"\t{Existing}\n")
        
    print ("\t" + "-"*20, "\n")
    
    Quotes = [
        "I will run as fast as I can to wherever my customer desires. I am the Auto Memories Doll, Violet Evergarden.\n-Violet Evergarden\n\n",
        "Do I have any right after I killed so many people as a weapon? I must have prevented them from keeping promises of their own.\n-Violet Evergarden\n\n",
        "Live and be free.\n-Gilbert Bougainvillea\n\n"
    ]

    print ( random.choice (Quotes) )




if __name__ == "__main__" :
    main ()
    