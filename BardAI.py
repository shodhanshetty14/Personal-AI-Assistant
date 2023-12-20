import pyautogui
import webbrowser
from time import sleep
import pyperclip
import json
import keyboard
from bardapi import BardCookies
import datetime
import logging

logging.basicConfig(filename='./logs/error.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s')

url = "https://bard.google.com/chat"


def get_cookies():
    print("get_cookies")
    webbrowser.open(url)
    sleep(10)

    pyautogui.click(x=1679, y=98)  # cookie_button = Point(x=1679, y=98)
    sleep(10)
    pyautogui.click(x=1469, y=121) # Export button = Point(x=1469, y=121)
    sleep(5)
    keyboard.press_and_release('ctrl + w')

    cookies = json.loads(pyperclip.paste())
    
    cookie_dict = {
    "__Secure-1PSID" : "",
    "__Secure-1PSIDTS" : "",
    "__Secure-1PSIDCC" : ""
    }
    
    for data in cookies:
        if data['name'] == "__Secure-1PSID":
            cookie_dict["__Secure-1PSID"] = data['value']
        elif data['name'] == "__Secure-1PSIDTS":
            cookie_dict["__Secure-1PSIDTS"] = data['value']
        elif data['name'] == "__Secure-1PSIDCC":
            cookie_dict["__Secure-1PSIDCC"] = data['value']

    f = open("data.txt", "w")
    f.write(f"__Secure-1PSID,{cookie_dict["__Secure-1PSID"]}\n__Secure-1PSIDTS,{cookie_dict["__Secure-1PSIDTS"]}\n__Secure-1PSIDCC,{cookie_dict["__Secure-1PSIDCC"]}")
    f.close()
    
    return cookie_dict


def readCookies():
    print("readCookies from file")
    f = open('data.txt', 'r')
    cookie_dict = {
    "__Secure-1PSID" : "",
    "__Secure-1PSIDTS" : "",
    "__Secure-1PSIDCC" : ""
    }
    for line in f.readlines():
        line = line.strip().split(',')
        if line[0] == "__Secure-1PSID":
            cookie_dict["__Secure-1PSID"] = line[1]
        elif line[0] == "__Secure-1PSIDTS":
            cookie_dict["__Secure-1PSIDTS"] = line[1]
        elif line[0] == "__Secure-1PSIDCC":
            cookie_dict["__Secure-1PSIDCC"] = line[1]
    return cookie_dict
   

def split_and_save_paragraphs(data, filename):
    paragraphs = data.split('\n\n')
    with open(filename, 'w') as file:
        file.write(data)
    data = paragraphs[:3]
    separator = ', '
    joined_string = separator.join(data)
    return joined_string      


def Bard(command, name=None):
    # print(command, name)
    try:
        cookie_dict = readCookies()
        bard = BardCookies(cookie_dict =cookie_dict)
        
    except Exception as e:
        logging.error(e)
        cookie_dict = get_cookies()
        bard = BardCookies(cookie_dict =cookie_dict)
    
    try:
        Question = command
        if "write code" in Question:
            results = bard.get_answer(Question)['content']

            filenamedate = f"./DataBase/Codes/{name}.txt"
            f = open(filenamedate, "w")
            f.write(results)
            return f"Code saved successfully in DataBase as {name}.txt"
        
        results = bard.get_answer(Question)['content']
    
        current_datetime = datetime.datetime.now()
        formatted_time = current_datetime.strftime("%H%M%S")
        filenamedate = str(formatted_time) + str(".txt")
        filenamedate = f"./DataBase/chat/{filenamedate}"
        response_data = split_and_save_paragraphs(results, filename=filenamedate)
        return response_data
    except Exception as e:
        logging.error(e)
        return f"Face some probelm can you try again"
        

if __name__ == "__main__":
    Bard()