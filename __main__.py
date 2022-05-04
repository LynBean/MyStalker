# Purpose : To get all my haters IC numbers
# Programmer : Asuna
# Version 1.9.5

import os
import sys
import time
import datetime

from _GetDetails_ import ClearScreen, _PlacesOfBirth, _Areas, _Schools, _Get


def ValidateDatetime(Date):
    try :
        datetime.datetime.strptime(Date, '%y%m%d')
        return True
    except ValueError:
        return False
    
def FileDump(Response) :
    if "Not Existing" not in Response :
        with open (os.path.join(sys.path[0], "Results.txt"), "a+", encoding = "utf-8") as f:
            f.write(Response + "\n")
        

if __name__ == "__main__" :
    
    ClearScreen()
    while True :
        BirthDate = str ( input( "Please enter the birth date : (031231) "))
        if ValidateDatetime(BirthDate) :
            break
    while True :
        UserInputPlaceCode = str ( input( "Please enter the place of birth : (13)(If no just keep it blank) "))
        if _Get.VerifyCode(UserInputPlaceCode) :
            break
    while True :
        Gender = str ( input( "Please enter the gender : (Female)(If no just keep it blank) ")).upper()
        if Gender in ("MALE", "FEMALE", "") :
            break
    while True :
        UserInputSchoolCode = str ( input( "Please enter the school code : (YCC4102)(If no just keep it blank) ")).upper()
        if _Get.VerifyCode(UserInputSchoolCode) or UserInputSchoolCode == "" :
            break
    
    ExistingList = []
    Output = True
    
    if _Get.VerifyCode(UserInputPlaceCode) : # If PlaceOfBirth Code entered by user is valid
        
        if _Get.VerifyCode(UserInputSchoolCode) : # If School Code entered by user is valid
            pass
        
        if not _Get.VerifyCode(UserInputSchoolCode) : # If School Code entered by user is invalid
            Areas = _Areas(UserInputPlaceCode).Response() # return (AreasCodeList, AreasNameList)
            
            for i in range(10000) : 
                if Output :
                    ClearScreen()
                    print ("\tGot'cha Response --\n")
                    
                    if not ExistingList :
                        print ("\tEmpty~~ :(\n")
                        
                    for Existing in ExistingList :
                        print ( f"\t{Existing}\n")
                        
                    print ("\t", "-"*20, "\n")
                    Output = False
                
                FourDigitsNumber = _Get.FourDigitsNumber(i, Gender)
                if FourDigitsNumber == None :
                    continue
                
                InitResponse = _Get()
                Response = InitResponse.Response(BirthDate, UserInputPlaceCode, FourDigitsNumber)
                if "Not Existing" in Response : 
                    
                    print ("  "*100, end = "\r") # Clear Last Line
                    print ( f"Current Progress : {Response}", end = "\r")
                    continue
                
                print ("  "*100, end = "\r") # Clear Last Line
                print ( f"Current Progress : {Response} is existing. Now will find this user name through finding user school", end = "\r")
                
                time.sleep(5)
            
                for AreaCode in Areas[0] :
                    Schools = _Schools(UserInputPlaceCode, AreaCode).Response() # return (SchoolsCodeList, SchoolsNameList)
                    
                    for SchoolCode in Schools[0] :
                        if Output :
                            ClearScreen()
                            print ("\tGot'cha Response --\n")
                            
                            if not ExistingList :
                                print ("\tEmpty~~ :(\n")
                                
                            for Existing in ExistingList :
                                print ( f"\t{Existing}\n")
                                
                            print ("\t", "-"*20, "\n")
                            Output = False
                            
                        InitResponseWithSchool = _Get(SchoolCode = SchoolCode)
                        ResponseWithSchool = InitResponseWithSchool.Response(BirthDate, UserInputPlaceCode, FourDigitsNumber)
                        
                        if "Not Existing" in ResponseWithSchool : 
                            
                            print ("  "*100, end = "\r") # Clear Last Line
                            print ( f"Current Progress : {ResponseWithSchool}", end = "\r")
                            continue
                        
                        print ("  "*100, end = "\r") # Clear Last Line
                        print ( f"Current Progress : {ResponseWithSchool}", end = "\r")
                        FileDump(ResponseWithSchool)
                        ExistingList.append(ResponseWithSchool)
                        Output = True
                        time.sleep(3)
                    
    if not _Get.VerifyCode(UserInputPlaceCode) : # If PlaceOfBirth Code entered by user is invalid
        
        if _Get.VerifyCode(UserInputSchoolCode) : # If School Code entered by user is valid
            pass
        if not _Get.VerifyCode(UserInputSchoolCode) : # If School Code entered by user is invalid
            pass
