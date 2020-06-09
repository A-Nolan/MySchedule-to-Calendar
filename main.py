from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
import time
import datetime
from create_event import create_event, is_events_this_week

def ask_if_correct(info):
    for item in info:
        print('Date: {}'.format(str(item[2])))
        print('Start Time: {}'.format(item[0]))
        print('End Time: {}'.format(item[1]))
        print('\n')

    return input('Does this information look correct? (y/n) : ')

def get_shifts(current_date):
    shift_information = []

    all_shifts = driver.find_elements_by_class_name('schdnormal')
    for shift in all_shifts:
        if shift.text == ' ':
            current_date += datetime.timedelta(days=1)
        else:
            shift_information.append([shift.text[1:6], shift.text[-5:], current_date])
            current_date += datetime.timedelta(days=1)

    return shift_information

options = Options()
options.add_argument('headless')

# input users id and password
userid = input('User ID: ')
password = input('Password: ')

driver = webdriver.Chrome(options=options, executable_path='C:\Program Files (x86)\chromedriver')
driver.get('https://psschedule.reflexisinc.co.uk/wfmmcdirlprd/ModuleSelection.jsp')

# Log in
userid_input_box = driver.find_element_by_name("txtUserID")
password_input_box = driver.find_element_by_name('txtPassword')
userid_input_box.send_keys(userid)
password_input_box.send_keys(password)
login_button = driver.find_element_by_class_name('button-t')
login_button.click()

# Navigate to shifts page
driver.get('https://psschedule.reflexisinc.co.uk/wfmmcdirlprd/rws/ess/ess_notice_board.jsp?mm=ESS')

# Grab the starting date and convert to datetime
starting_date = driver.find_element_by_name('weekstarts').text[-10:]
current_date = datetime.datetime(int(starting_date[-4:]), int(starting_date[3:5]), int(starting_date[0:2]))

if not is_events_this_week(current_date):
    shift_information = get_shifts(current_date)

    proceed = ask_if_correct(shift_information)

    if proceed == 'y':
        for item in shift_information:
            create_event(item)

next_week = driver.find_element_by_id('rightImg')
if 'visible' in next_week.get_attribute('style'):
    next_week.click()

    current_date += datetime.timedelta(days=7)

    if not is_events_this_week(current_date):
        shift_information = get_shifts(current_date)

        proceed = ask_if_correct(shift_information)

        if proceed == 'y':
            for item in shift_information:
                create_event(item)