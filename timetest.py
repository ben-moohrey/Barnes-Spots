import datetime
import time
import sys
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

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




#



def automate(timeSlot, username, password, link):
    
    # Print Time and set path for driver
    print("time: ", timeSlot)
    CHROME_DRIVER_PATH = "driver/chromedriver"
    driver = webdriver.Chrome(resource_path(CHROME_DRIVER_PATH))


    def reload_until_clickable(reload_times, xpath):
        while reload_times != 0:
            try:
                clickNext = driver.find_element_by_xpath(xpath)
                clickNext.click()
                return
            except:
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
                return
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



timeSlot = datetime.datetime.now()
timeSlot = timeSlot.replace(hour=16,minute = 30, second = 0)

automate(timeSlot, "bmurray@syr.edu", "ER4r9!RhDfm7vJG", "https://bewell.ese.syr.edu/Program/GetProgramDetails?courseId=21fb2e43-2d6f-4d22-9941-df5e95224734&semesterId=fb963dc4-ba57-4f69-b2dd-000111fcc3d5")