import os
import sys
import time
import json
import datetime
import tkinter as tk 
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

###############################################
# Author - Ben Murray - 2/17/21               #
#                                             #
# Automates Barnes Center Reservations        #
# Uses Selenium and Chromedriver              #
###############################################

# Excutable Generation
# pyi-makespec main.py --onefile --noconsole --add-binary "driver/chromedriver:.driver/" --icon=su.ico --name "Barnes"
# pyinstaller --clean barnes.spec

COLOR = "orange"
BORDER = 0
class BarnesGUI:
    def __init__(self, parent):
        

        # label displaying Outputs
        self.label = tk.Label(parent, text="", font="Arial 30", width=40, bg=COLOR, bd = BORDER)
        self.label.pack()

        # Entry for link
        self.linkLabel = tk.Label(parent, text="Page Link", font="Airal 20", width=20, bg=COLOR, bd = BORDER)
        self.linkEntry = tk.Entry(parent, bg=COLOR, bd = BORDER)
        self.linkEntry.insert(0, pull_data("link"))
        self.linkLabel.pack()
        self.linkEntry.pack()

        # Entry for username
        self.usernameLabel = tk.Label(parent, text="SUID Username", font="Airal 20", width=20, bg=COLOR, bd = BORDER)
        self.usernameEntry = tk.Entry(parent, bg=COLOR, bd = BORDER)
        self.usernameEntry.insert(0, pull_data("username"))
        self.usernameLabel.pack()
        self.usernameEntry.pack()

        # Entry for password
        self.passwordLabel = tk.Label(parent, text="SUID Password", font="Airal 20", width=20, bg=COLOR, bd = BORDER)
        self.passwordEntry = tk.Entry(parent, show="*", bg=COLOR, bd = BORDER)
        self.passwordEntry.insert(0, pull_data("password"))
        self.passwordLabel.pack()
        self.passwordEntry.pack()

        # Button for saving user data
        self.saveButton = tk.Button(parent, command=self.save, text="Save INFO", bg=COLOR, bd = BORDER)
        self.saveButton.pack()

        # Entry for day
        self.dayLabel = tk.Label(parent, text="Day (ex. 21)", font="Airal 20", width=20, bg=COLOR, bd = BORDER)
        self.dayLabel.pack()
        self.dayEntry = tk.Entry(parent, bg=COLOR, bd = BORDER)
        self.dayLabel.pack()
        self.dayEntry.pack()
        
        # Entry for Hours
        self.hourLabel = tk.Label(parent, text="Hour (24hr)", font="Airal 20", width=20, bg=COLOR, bd = BORDER)
        self.hourLabel.pack()
        self.hourEntry = tk.Entry(parent, bg=COLOR, bd = BORDER)
        self.hourLabel.pack()
        self.hourEntry.pack()

        # Entry for Mins
        self.minuteLabel = tk.Label(parent, text="Min", font="Arial 20", width=10, bg=COLOR, bd = BORDER)
        self.minuteEntry = tk.Entry(parent, bg=COLOR, bd = BORDER)
        self.minuteLabel.pack()
        self.minuteEntry.pack()

        # Initializes timeSlot
        self.timeSlot = datetime.datetime.now()
        self.timeSlot = self.timeSlot.replace(minute = 0, second = 0)
        
        # Button for starting the time check loop
        self.submitButton = tk.Button(parent, command=self.submit, text="Start", bg=COLOR, bd = BORDER)
        self.submitButton.pack()


    # Pushes user data to .user.json
    def save(self):
        push_data(self.usernameEntry.get(), self.passwordEntry.get(), self.linkEntry.get())
        print("Data Saved")


    # Sets the timeSlot datetime object to the time selected, Adds the selected time to the display, Starts check_time() loop
    def submit(self):    
        if self.check_feilds():
            self.timeSlot = self.timeSlot.replace(day=int(self.dayEntry.get()), hour=int(self.hourEntry.get()), minute=int(self.minuteEntry.get()), second=0, microsecond=0)
            self.label.configure(text=str(self.timeSlot.strftime("%-m/%d - %-I:%M %p")))
            self.label.after(0, self.check_time)


    # Checks entries for valid inputs
    def check_feilds(self):
        if self.minuteEntry.get().isdigit() & self.hourEntry.get().isdigit() & self.dayEntry.get().isdigit():
            if (int(self.minuteEntry.get()) < 60) & (int(self.hourEntry.get()) < 25) & (int(self.dayEntry.get()) < 32):
                if (int(self.minuteEntry.get()) >= 0) & (int(self.hourEntry.get()) >= 0) & (int(self.dayEntry.get()) >= 1):
                    if (self.usernameEntry.get() != "") & (self.passwordEntry.get() != "") & (self.linkEntry.get() != ""):
                        print("Feild Entries Pass")
                        return True


    # Loop for comparing current time to the set time by user
    def check_time(self):
        # Update Time
        self.currtime = datetime.datetime.now()

        print("Waiting")
        print("current time: ", self.currtime.strftime("%-m/%-d/%Y %-I:%M:%S %p"))
        print("Set time: ", self.timeSlot.strftime("%-m/%-d/%Y %-I:%M:%S %p"))

        # Check if current time is valid
        if (self.currtime >= (self.timeSlot - datetime.timedelta(hours=6, seconds=10))):
            if (self.check_feilds()):
                self.out = automate(self.timeSlot, self.usernameEntry.get(), self.passwordEntry.get(), self.linkEntry.get())
                self.label.configure(text=self.out)
        else:
            # request tkinter to call self.refresh after 1s (the delay is given in ms)
            self.label.after(1000, self.check_time)


def push_data(username, password, link):
    print("Pushing to: "+ userdata_path(".user.json"))
    with open(userdata_path(".user.json"), "w") as f:
        data = {}
        data["username"] = username
        data["password"] = password
        data["link"]     = link
        json.dump(data, f, indent=1)


def pull_data(toPull):
    print("Pulling from: " + userdata_path(".user.json"))
    if os.path.exists(userdata_path(".user.json")):
        with open(userdata_path(".user.json"), "r") as f:
            data = json.load(f)
            return data[toPull]
    else:
        push_data("","","")
        return ""


# Old - *Remove in Build*
# Puts .user.json in the directory where the 
# def pull_data(toPull):
#     if os.path.exists(".user.json"):
#         with open(resource_path_2(".user.json"), "r") as f:
#             data = json.load(f)
#             return data[toPull]
#     else:
#         print("File did not exist: creating new .user.json at ", os.getcwd())
#         push_data("","","")
#         return ""
#
# def push_data(username, password, link):
#     print(resource_path_2(".user.json"))
#   
#     with open(resource_path_2(".user.json"), "w") as f:
#         data = {}
#         data["username"] = username
#         data["password"] = password
#         data["link"]     = link
#         json.dump(data, f, indent=1)

def userdata_path(relative_path):
    # Application Runtime - User Directory
    # Debug Runtime       - Local Directory
    home = os.path.expanduser("~")
    return os.path.join(home, relative_path)

def resource_path_2(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    elif __file__:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)

def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Wait function for when
def wait_until_FAST(jump_time):
    currTime = datetime.datetime.now()
    while (currTime <= jump_time):
        time.sleep(.15)
        print("Waiting at ", currTime.strftime("%-m/%-d/%Y %-I:%M:%S %p"))
        currTime = datetime.datetime.now()
    time.sleep(.2)


def automate(timeSlot, username, password, link):
    
    # Print Time and set path for driver
    print("time: ", timeSlot)
    CHROME_DRIVER_PATH = ".driver/chromedriver"
    driver = webdriver.Chrome(resource_path(CHROME_DRIVER_PATH))


    def reload_until_clickable(reload_times, xpath):
        while reload_times != 0:
            try:
                clickNext = driver.find_element_by_xpath(xpath)
                clickNext.click()
                return 0
            except:
                driver.refresh()
                time.sleep(.5)
                reload_times -= 1
        print("Chosen Time Spot Not Available")
        return -1
        

    def wait_until_clickable(timeout, xpath):
        while (timeout > 0):
            try:
                click = driver.find_element_by_xpath(xpath)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                click.click()
                return 0
            except:
                time.sleep(.5)
                timeout -= .5
        print ("Timeout! Waiting for click at: " + xpath)
        return -1
        


    # Login
    driver.get('https://bewell.ese.syr.edu')
    loginButton = driver.find_element_by_id('loginLink')
    loginButton.click()
    time.sleep(1)
    driver.execute_script("submitExternalLoginForm(\'Shibboleth\')")
    time.sleep(.5)
    usernameBox = driver.find_element_by_xpath("//*[@id='username']")
    passwordBox = driver.find_element_by_xpath("//*[@id='password']")
    loginButtonFinal = driver.find_element_by_xpath("/html/body/div/div/div/div/form/div[4]/button")
    usernameBox.send_keys(username)
    passwordBox.send_keys(password)
    loginButtonFinal.click()
    cookieClick = driver.find_element_by_xpath("//*[@id='gdpr-cookie-accept']")
    cookieClick.click()
    
    # Reservation 
    wait_until_FAST(timeSlot - datetime.timedelta(hours=6, seconds=10))
    try: 
        driver.get(link)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    except:
        print("Failed to Load: Wrong Username or Password")
        driver.close()
        return "Login Failed"

    # Tries to get the xpath element required (user's time slot) 4 times 
    if (reload_until_clickable(6, ".//button[contains(@onclick, '" + timeSlot.strftime("%-m/%-d/%Y %-I:%M:%S %p") + "')]")) == -1:
        driver.close()
        return "Time Unavailable"

    # Accept waver, complete and close
    wait_until_clickable(10, "/html/body/div[3]/div[1]/div[2]/div[3]/div[1]/div/form/button")  

    try:
        time.sleep(1)
        clickNext = driver.find_element_by_xpath("//*[@id='mainContent']/div[2]/div[2]/a")
        clickNext.click()
        clickNext = driver.find_element_by_xpath("//*[@id='btnAccept']")
        clickNext.click()
    except:
        print("No seccond waiver")

    # New Review Saftey
    wait_until_clickable(3, "//*[@id='mainContent']/div[2]/form[2]/div[2]/button[2]")

    # Checkout 1
    if (-1 == wait_until_clickable(6, "//*[@id='checkoutButton']")):
        return "Checkout Failed"
    
    # Checkout 2
    if (-1 == wait_until_clickable(6, "//*[@id='CheckoutModal']/div/div[2]/button[2]")):
        return "Checkout 2 Failed"

    driver.close()
    return "Done!"


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Barnes Grabber")
    root.configure(bg='orange')
    barnesApp = BarnesGUI(root)
    root.mainloop()