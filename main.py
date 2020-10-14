from datetime import datetime
from helper import *
from config import *

# EVENT LOOP FOR EACH CLASS IN SCHEDULE
def classLoop(event,web):

    # COPY VALUES
    startTime = event["start"]
    endTime = event["end"]
    className = event["name"]

    nowTime = datetime.now()

    while True:

        # FIND TIME LEFT/PASSED FROM STARTING TIME OF CLASS
        nowTime = datetime.now()
        timeDiff = startTime - nowTime
        minutes = int((timeDiff.total_seconds()) / 60)

        # MORE THAN 1 MIN. LEFT : SLEEP AND CHECK AGAIN
        if minutes > 1:
            print("Waiting for {} to start in {} minutes...".format(
                className, minutes))
            sleep(60)

        # 0 MIN. LEFT : JOIN CLASS
        elif minutes == 0:
            web.joinClass(CLASSROOM_URL)
            break

        # 1 MIN. OR MORE PASSED AND CLASS NOT ENDED : ASK USER WHAT TO DO?
        elif minutes <= 0 and nowTime < endTime:

            print(
                "{} has already started, you are {} minutes late. Joining by default in 60 seconds. Press 'Ctrl + C' to cancel & skip to next class.\n".format(
                    className, abs(minutes)
                )
            )

            try:
                sleep(60)
                web.joinClass(CLASSROOM_URL)
                break

            except KeyboardInterrupt:
                print("Skipping to next class...")
                return None

        # IF CLASS ENDED : SKIP TO NEXT CLASS
        else:
            print("{} has ended, skipping to next class.".format(className))
            return None

    # ADD MORE DELAY HERE IF YOUR TEACHER MANUALLY ACCEPTS JOIN REQUEST(S)
    sleep(10)

    # CHECK IF REALLY JOIN AND PRINT CONFORMATION OR TRY AGAIN!
    if web.ifJoined():
        print(
            "{} successfully joined @{}".format(
                className, datetime.now().strftime("%H:%M")
            )
        )

    else:

        print("Class not Joined, some error occurred. Retrying again...")
        web.joinClass(CLASSROOM_URL)

        if not web.ifJoined():
            print("Retry failed, something is wrong. Can't join {}".format(className))
            return None

    # TIME WHEN CLASS WILL BE LEFT
    print("{} will be auto-left @ {}".format(className, endTime))

    while True:

        nowTime = datetime.now()

        # IF DEFINED PEOPLE LIMIT > 0 AND CURRENT PEOPLE IN MEETING < DEFINED LIMIT, THEN LEAVE CLASS
        if THRESHOLD_PEOPLE > 0 and web.peopleNow() < THRESHOLD_PEOPLE:
            print(
                "Number of people are less than {}. Leaving {}...".format(
                    THRESHOLD_PEOPLE, className
                )
            )
            web.leaveClass()
            break

        # IF CURRENT TIME >= CLASS END TIME, THEN LEAVE CLASS
        elif nowTime >= endTime:
            print("{} ended @ {}. Leaving...".format(className, endTime))
            web.leaveClass()
            break

        # ELSE, SLEEP FOR 10 SEC. AND CHECK AGAIN!
        else:
            sleep(10)

    sleep(2)

    # CHECK IF REALLY LEFT AND PRINT CONFORMATION OR NAVIGATE TO DIFFERENT PAGE TO LEAVE MEETING!
    if web.ifLeft():
        print("{} left @ {}".format(className, datetime.now().strftime("%H:%M")))

    else:
        print(
            "Class not Left, some error occurred. Closing Tab to ensure Uniformity :)"
        )
        web.navigateAway()
        print("{} left @ {}\n".format(
            className, datetime.now().strftime("%H:%M")))

    ### END OF EVENT LOOP ###

# ENTIRE PROGRAM
def main():

    # FIND TODAY
    dayToday = datetime.now().strftime("%A")

    # FETCH TODAY'S SCHEDULE FROM TIMETABLE.TXT
    schedule = loadTimetable(dayToday)

    # SORT CLASSES BY JOIN TIME
    schedule.sort(key=lambda x: x["start"])

    # IF SCHEDULE ISN'T EMPTY
    if schedule:

        # CREATE OBJECT OF WEBDRIVER CLASS
        webDr = webDriver()

        # LOGIN INT0 G-ACCOUNT
        webDr.googleLogin(EMAIL, PASS)

        # LOOP FOR EACH CLASS IN SCHEDULE
        for classes in schedule:
            classLoop(classes,webDr)

        # CLOSE BROWSER
        webDr.closeBrowser()

        # YAY, ALL CLASSES ENDED!
        print("\nBEEP BEEP. You're done for Today :)")

    # ELSE, PRINT NO CLASSES
    else:
        print("\nNo classes Today. ENJOY :)")

# RUN EVENT-LOOP FOR TODAY
main()

# IF sleepNow(), THEN RUN THE PROGRAM AGAIN FOR NEXT WORKING DAY. ELSE QUIT AWAY.
while(sleepNow()):
    main()
