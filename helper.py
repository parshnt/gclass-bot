# a place to place all the helper funcitions :)
from config import THRESHOLD_PEOPLE as MAX_INT
import os, sys
from time import sleep
from datetime import datetime
from datetime import timedelta
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# DISABLE print()
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# RESTORE print()
def enablePrint():
    sys.stdout = sys.__stdout__

# CONVERT STRING TO DATE-TIME OBJECT
def timeParser(time):
    timeStr = datetime.now().strftime("%d/%m/%Y") + time
    return datetime.strptime(timeStr, "%d/%m/%Y%H:%M")


# TIMETABLE.TXT PARSER
def loadTimetable(today):

    try:

        schedule = []

        file = open("timetable.txt", "r")
        print("\n*** TODAY'S SCHEDULE ***\n")

        for line in file:

            line = line.rstrip("\n")

            if not line:  # line is blank
                continue

            if line.startswith("#"):  # comment line
                continue

            fields = line.split(";")

            className = fields[0]
            classTime = fields[1].split("-")
            classDays = fields[2].split(",")

            joinTime = timeParser(classTime[0])
            leaveTime = timeParser(classTime[1])

            for day in classDays:

                if day == today and joinTime < leaveTime:
                    print(className, ":", joinTime, "to", leaveTime)
                    schedule.append(
                        {"name": className, "start": joinTime, "end": leaveTime}
                    )

                elif joinTime > leaveTime:
                    print(
                        "ERROR: Ending time of",
                        className,
                        "on",
                        day,
                        "is earlier than Starting time\n",
                    )

                elif joinTime == leaveTime:
                    print(
                        "ERROR: Ending time of",
                        className,
                        "on",
                        day,
                        "is same as Starting time\n",
                    )

        file.close()

        return schedule

    except Exception as e:

        print("\nTimetable.txt not found or not properly formatted")
        return False

# SLEEP TILL NEXT CLASS
def sleepNow():

    schedule = False
    dayCount = 0
    thisDay = datetime.today()

    # LOADS NEXT WORKING DAY'S SCHEDULE FROM TIMETABLE
    while(not schedule):

        dayCount += 1
        nextdayName = (thisDay + timedelta(days=dayCount)).strftime("%A")

        blockPrint()
        schedule = loadTimetable(nextdayName)
        enablePrint()

    # SORT CLASSES BY JOIN TIME
    schedule.sort(key=lambda x: x["start"])

    ## SO SCHEDULE[0] WILL BE THE 1st CLASS ON NEXT WORKING DAY, WE'LL SLEEP TILL THEN (USEFUL IN VPS, CLOUD VM'S)

    # NEXT CLASS'S DATE-TIME OBJECT
    nextClass = timedelta(days=dayCount)+schedule[0]["start"]

    # SECONDS TILL NEXT CLASS
    sleepTime = int((nextClass-datetime.now()).total_seconds())

    # ONE LAST TIME, BEFORE THE LONG SLEEP
    print("sleeping till next class. Press 'Ctrl + C' anytime to wake & Quit.\n")

    try:
        # SLEEP, RETURN TRUE WHEN DONE!
        print("Good Night...zZZ")
        sleep(sleepTime-300)
        return True

    except KeyboardInterrupt:

        # RETURN FALSE, WHEN WOKE-UP
        print("Waking out of Sleep and Exiting....")
        return False


"""
loadTimetable() takes today's day as input arg. and returns a list of classes that are on today's timetable.
Each class in list is a dictionary with 3 keys: className, startTime & endTime.
"""

# BROWSER OPTIONS TO AID IN AUTOMATION
op = Options()

op.add_argument("start-maximized")

op.add_experimental_option("excludeSwitches", ["enable-automation"])
op.add_experimental_option(
    "prefs",
    {
        "profile.default_content_setting_values.media_stream_mic": 1,
        "profile.default_content_setting_values.media_stream_camera": 1,
        "profile.default_content_setting_values.geolocation": 1,
        "profile.default_content_setting_values.notifications": 1,
        "profile.password_manager_enabled": False,
        "credentials_enable_service": False,
    },
)


# SELENIUM FUNCTIONS
class webDriver:

    # START BROWSER WITH OP()
    def __init__(self):
        self.driver = webdriver.Chrome(options=op)

    ## COMMON CHECKS TO CONFIRM IF G-MEET SESSION EXISTS (BUT NOT JOIN YET!)

    # CHECK 1
    def notCreated(self):
        text = "You can't create a meeting yourself. Contact your system administrator for more information."
        if text in self.driver.page_source:
            return True
        return False

    # CHECK 2
    def alreadyEnded(self):
        text = "This meeting has already ended"
        if text in self.driver.page_source:
            return True
        return False

    # CHECK 3
    def notStarted(self):
        text = "This meeting hasn't started yet"
        if text in self.driver.page_source:
            return True
        return False

    # LOGIN INTO G-ACCOUNT
    def googleLogin(self, userid, passwd):

        driver = self.driver

        driver.get(
            "https://accounts.google.com/o/oauth2/v2/auth/oauthchooseaccount?redirect_uri=https://developers.google.com/oauthplayground&prompt=consent&response_type=code&client_id=407408718192.apps.googleusercontent.com&scope=email&access_type=offline&flowName=GeneralOAuthFlow"
        )

        sleep(3)

        try:

            try:
                driver.find_element_by_name("identifier").send_keys(userid)
                sleep(1)
            except:
                driver.find_element_by_name("Email").send_keys(userid)
                sleep(1)
            try:
                driver.find_element_by_id("identifierNext").click()
                sleep(4)
            except:
                driver.find_element_by_id("next").click()
                sleep(4)
            try:
                driver.find_element_by_name("password").send_keys(passwd)
                sleep(1)
            except:
                driver.find_element_by_name("Passwd").send_keys(passwd)
                sleep(1)
            try:
                driver.find_element_by_id("passwordNext").click()
                sleep(4)
            except:
                driver.find_element_by_id("trustDevice").click()
                driver.find_element_by_id("submit").click()
                sleep(4)
        except Exception as e:

            print("\nLogin failed, please open an issue on GitHub")
            print(e)

    # NAVIGATE TO G-MEET URL & JOIN
    def joinClass(self, url):

        driver = self.driver

        driver.get(url)

        driver.implicitly_wait(5)

        while(self.notCreated() or self.alreadyEnded() or self.notStarted()):
            print("Class not found/started, retrying again in 1 min.")
            sleep(60)
            driver.get(url)

        try:

            body = driver.find_element_by_xpath("//body")

            sleep(3)

            body.send_keys(Keys.CONTROL, "e")
            body.send_keys(Keys.CONTROL, "d")

            sleep(2)

            joinButton = driver.find_elements_by_xpath(
                "//*[contains(text(), 'Join now') or contains(text(), 'Ask to join')]"
            )
            joinButton[0].click()

            sleep(2)

        except Exception as e:

            print("\nSomething broke in joinClass(). Please open an issue on GitHub")
            print(e)
            return False

    # LEAVE G-MEET SESSION
    def leaveClass(self):

        driver = self.driver

        try:

            leaveButton = driver.find_elements_by_xpath(
                "//div[@aria-label='Leave call']"
            )

            menu = driver.find_elements_by_xpath(
                "//div[@aria-label='Show everyone']")

            menu[0].click()
            leaveButton[0].click()
        except Exception as e:

            print(e)
            print("\nEither you were Kicked Out of Class or Something broke!")

    # CONFIRM IF JOINED G-MEET SESSION SUCCESSFULLY
    def ifJoined(self):
        checks = ["Meeting details", "Turn on captions"]
        for text in checks:
            flag = text in self.driver.page_source
        return flag

    # CONFIRM IF LEFT G-MEET SESSION SUCCESSFULLY
    def ifLeft(self):
        checks = ["You left the meeting", "Rejoin", "Return to home screen"]
        for text in checks:
            flag = text in self.driver.page_source
        return flag

    # PEOPLE PRESENT IN CURRENT G-MEET SESSION
    def peopleNow(self):

        try:
            people = self.driver.find_element_by_xpath(
                "//div[@aria-label='Show everyone']"
            ).get_attribute("textContent")
            return int(people)

        except Exception as e:

            print("\nNot able to find number of people in meeting.")
            return MAX_INT+1

    # CLOSE BROWSER SESSION
    def closeBrowser(self):
        self.driver.quit()
        print("\nBrowser closed!")

    # NAVIGATE TO A DIFFERENT URL TO LEAVE THE MEETING (IF leaveClass() DOESN'T WORK)
    def navigateAway(self):
        self.driver.get("http://www.google.com")


## END-OF-FILE ##
