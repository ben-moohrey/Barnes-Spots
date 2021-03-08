import json
import os
import sys


def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def pull_data():
    print(resource_path(".user.json"))
    if os.path.exists(resource_path(".user.json")):
        
        with open(resource_path(".user.json"), "r") as f:
            data = json.load(f)
            return (data["username"], data["password"], data["link"])
    else:
        push_data("","","")
        return ("", "", "")



    


def push_data(username, password, link):
    print(resource_path(".user.json"))
    with open(resource_path(".user.json"), "w") as f:
        
        data = {}
        data["username"] = username
        data["password"] = password
        data["link"]     = link
        json.dump(data, f, indent=1)


# push_data("adfadfadf", "benmoohr", "www.poop.com")
a,b,c = pull_data()
print(a, b, c)









