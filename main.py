import subprocess
from selenium import webdriver
import time
import zipfile
import requests
from numpy import random
import threading
import names
import json
import random
import datetime
from discord_webhook import DiscordWebhook, DiscordEmbed
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

stop = False

API_KEY = 'pk_HR4eQXNHA1yYaJAAx2Yeq9pVsaL0uAks'


def get_random_time():
    picker = random.randint(1, 3)
    if picker == 1:
        rand_time = random.uniform(2, 4)
    else:
        rand_time = random.uniform(4, 8)
    return rand_time


def get_random_time_text():
    rand_time_text = random.uniform(0.5, 1.5)
    return rand_time_text


def update_license(license_key, hardware_id):
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }

    payload = {
        'metadata': {
            'hwid': hardware_id
        }
    }

    req = requests.patch(f'https://api.hyper.co/v6/licenses/{license_key}/metadata', headers=headers, json=payload)
    if req.status_code == 200:
        return True

    return None


def get_license(license_key):
    headers = {
        'Authorization': f'Bearer {API_KEY}'
    }

    req = requests.get(f'https://api.hyper.co/v6/licenses/{license_key}', headers=headers)
    if req.status_code == 200:
        return req.json()

    return None


license_authenticated = True
key = input('Please Enter Your License Key: ')
license_data = get_license(key)
if license_data:
    if license_data.get('metadata') != {}:
        print('License is already in use on another machine!')
        input('Press Any Key to Continue...')
    else:
        hwid = str(subprocess.check_output(
            'wmic csproduct get uuid')).split('\\r\\n')[1].strip('\\r').strip()
        if update_license(key, hwid):
            license_authenticated = True
            print('License is good to go!')
else:
    print('License not found!')
    input('Press any key to continue...')


def gen_google(task, tasks_to_run, concurrent_tasks, proxies_available):

    with open('proxies.txt', 'r') as f:
        proxies = [line.strip() for line in f]

    if len(proxies) == 0:
        print('Please Insert Proxies into proxies.txt...')
        input('Press Any Key to Continue...')
        return
    elif proxies[0] == '---Insert Proxies Here---':
        print('Please Insert Proxies into proxies.txt...')
        input('Press Any Key to Continue...')
        return

    with open('settings.json', 'r') as f:
        data = json.load(f)

    API_KEY = data['API_KEY']
    CATCHALL = data['CATCHALL']
    WEBHOOK = data['DISCORD_WEBHOOK']
    if API_KEY == 'Insert sms-gen API Key Here':
        print('Please enter sms-gen api key. If you do not have an account or funds, please visit https://sms-gen.com/')
        input('Press any key to continue...')
        return

    if CATCHALL == 'Insert Catchall Here' or CATCHALL == '':
        yn = input('Are you sure you want to generate without adding a recovery email? (y/n)')
        if yn != 'y':
            return

    if WEBHOOK == '':
        yn = input('Are you sure you want to generate without using your discord webhook? (y/n)')
        if yn != 'y':
            return

    with open('settings.json', 'r') as f:
        data = json.load(f)

    api_key = data['API_KEY']
    catchall = data['CATCHALL']
    webhook_url = data["DISCORD_WEBHOOK"]

    def send_webhook(email, password, recovery, phone, gen_proxy):
        webhook = DiscordWebhook(
            url=webhook_url,
            username="Genned Mails")

        embed = DiscordEmbed(title="Account Created :tada:", color=242424)

        embed.add_embed_field(name="Email", value=f"|| {email} ||", inline=True)
        embed.add_embed_field(name="Password", value=f"|| {password} ||", inline=True)
        embed.add_embed_field(name="Recovery", value=f"|| {recovery} ||", inline=True)
        embed.add_embed_field(name="Proxy", value=f"|| {gen_proxy} ||", inline=True)
        embed.add_embed_field(name="Phone", value=f"|| {phone} ||", inline=True)

        embed.set_image(file='gmail_logo.png')

        date_and_time = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        embed.set_footer(text=f"BOUNDLESS GENS {date_and_time}")

        webhook.add_embed(embed)

        response = webhook.execute()
        if response.ok:
            print('Webhook Sent!')
        else:
            print('Webhook Failed to Send.')

    def send_webhook_public():
        webhook = DiscordWebhook(
            url='https://discordapp.com/api/webhooks/960231662959067246/UehgCp_BHs0caE9AW0WVDkOuwCnbV6ADAew5yDUjTO5Dah8Z_EXHpZebNbGtykrKl2qX',
            username="Google Gen")

        embed = DiscordEmbed(title="Account Created :tada:", color=242424)

        embed.add_embed_field(name="Type", value=f"Gmail", inline=True)
        embed.add_embed_field(name="Verification", value=f"PVA + Recovery", inline=True)

        embed.set_image(file='gmail_logo.png')

        date_and_time = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        embed.set_footer(text=f"BOUNDLESS GENS {date_and_time}")

        webhook.add_embed(embed)

        response = webhook.execute()
        if response.ok:
            print('Webhook Sent!')
        else:
            print('Webhook Failed to Send.')

    if int(concurrent_tasks) > 1:
        proxies_available = proxies_available.split(',')
        start = 0
        finish = 0
        total = 0

        for i in range(task - 1):
            total = total + int(proxies_available[i])

        start = total
        finish = (total + int(proxies_available[task - 1])) - 1
    else:
        proxies_available = int(proxies_available)
        start = 0
        finish = proxies_available - 1

    with open('proxies.txt', 'r') as f:
        proxies = [line.strip() for line in f]

    number_of_proxies = len(proxies)

    ip = []
    port = []
    user = []
    passwords = []

    for p in range(start, finish + 1):
        proxy = proxies[p].split(':')
        ip.append(proxy[0])
        port.append(proxy[1])
        user.append(proxy[2])
        passwords.append(proxy[3])

    def gen_account(task_num):
        f_name = names.get_first_name('male')
        l_name = names.get_last_name()
        rand_pass = ''
        for k in range(8):
            letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
            index = random.randrange(len(letters))
            rand_pass += letters[index]
        for t in range(2):
            numbers = '1234567890'
            index = random.randrange(len(numbers))
            rand_pass += numbers[index]

        email_name = f_name + l_name

        PROXY_HOST = ip[task_num]  # rotating proxy or host
        PROXY_PORT = port[task_num]  # port
        PROXY_USER = user[task_num]  # username
        PROXY_PASS = passwords[task_num]  # password

        def send_input(text, element):
            for m in range(len(text)):
                element.send_keys(text[m])
                time.sleep(get_random_time_text())

        manifest_json = """
        {
            "version": "1.0.0",
            "manifest_version": 2,
            "name": "Chrome Proxy",
            "permissions": [
                "proxy",
                "tabs",
                "unlimitedStorage",
                "storage",
                "<all_urls>",
                "webRequest",
                "webRequestBlocking"
            ],
            "background": {
                "scripts": ["background.js"]
            },
            "minimum_chrome_version":"22.0.0"
        }
        """

        background_js = """
        var config = {
                mode: "fixed_servers",
                rules: {
                singleProxy: {
                    scheme: "http",
                    host: "%s",
                    port: parseInt(%s)
                },
                bypassList: ["localhost"]
                }
            };
        chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
        function callbackFn(details) {
            return {
                authCredentials: {
                    username: "%s",
                    password: "%s"
                }
            };
        }
        chrome.webRequest.onAuthRequired.addListener(
                    callbackFn,
                    {urls: ["<all_urls>"]},
                    ['blocking']
        );
        """ % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)

        def get_chromedriver(use_proxy=False):
            chrome_options = webdriver.ChromeOptions()
            if use_proxy:
                pluginfile = 'proxy_auth_plugin.zip'

                with zipfile.ZipFile(pluginfile, 'w') as zp:
                    zp.writestr("manifest.json", manifest_json)
                    zp.writestr("background.js", background_js)
                chrome_options.add_extension(pluginfile)
            chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_argument("window-size=1280,800")
            chrome_options.add_experimental_option('useAutomationExtension', False)
            driver = webdriver.Chrome(executable_path='chromedriver.exe', options=chrome_options)
            return driver

        browser = get_chromedriver(use_proxy=True)

        print('Generation Started...')

        browser.get('https://google.com')

        time.sleep(get_random_time())

        print(f"thread[{task}] task[{task_num + 1}] Looking for popup...")

        try:
            elem = browser.find_element(By.XPATH, '//*[@id="vc3jof"]')
            print(f"thread[{task}] task[{task_num + 1}] Popup Found...")
            elem.click()

            time.sleep(get_random_time())

            elem = browser.find_element(By.XPATH, '//*[@id="tbTubd"]/div/li[12]')
            elem.click()

            time.sleep(get_random_time())

            elem = browser.find_element(By.ID, 'L2AGLb')
            elem.click()

            time.sleep(get_random_time())
        except:
            print(f"thread[{task}] task[{task_num + 1}] No popup found...")

        elem = browser.find_element(By.XPATH, '//*[@id="gb"]/div/div[2]/a')
        elem.click()

        time.sleep(get_random_time())

        create_elem_count = 0
        create_elem_found = False
        while not create_elem_found:
            try:
                create_acc_btn = browser.find_element(By.CSS_SELECTOR,
                                                      '.VfPpkd-LgbsSe.VfPpkd-LgbsSe-OWXEXe-dgl2Hf.ksBjEc.lKxP2d.qfvgSe.FliLIb.uRo0Xe.TrZEUc.t29vte')
                create_acc_btn.click()

                time.sleep(get_random_time())

                for_myself = browser.find_element(By.XPATH,
                                                  '//*[@id="view_container"]/div/div/div[2]/div/div[2]/div/div[2]/div/div/div[2]/div/ul/li[1]')
                for_myself.click()

                time.sleep(get_random_time())
                create_elem_found = True
                break
            except:
                print(f"thread[{task}] task[{task_num}]Waiting for page to load...")
                time.sleep(get_random_time())
                if create_elem_count > 5:
                    print(f"thread[{task}] task[{task_num}] page took too long to load (potential proxy issue), terminating task...")
                    return
                create_elem_count = create_elem_count + 1

        info_elem_count = 0
        elem_info_found = False
        while not elem_info_found:
            try:
                print(f"thread[{task}] task[{task_num + 1}]: Entering First Name...")
                first_name = browser.find_element(By.XPATH, '//*[@id="firstName"]')
                send_input(f_name, first_name)

                time.sleep(get_random_time())
                elem_info_found = True
                break
            except:
                if info_elem_count > 5:
                    print(f"thread[{task}] task[{task_num + 1}] page took too long to load (potential proxy issue), terminating task...")
                    return
                info_elem_count = info_elem_count + 1
                print(f"thread[{task}] task[{task_num + 1}] Waiting for page to load...")
                time.sleep(get_random_time())

        print(f"thread[{task}] task[{task_num + 1}]: Entering Last Name...")
        last_name = browser.find_element(By.XPATH, '//*[@id="lastName"]')
        send_input(l_name, last_name)

        time.sleep(get_random_time())

        print(f"thread[{task}] task[{task_num + 1}]: Entering Email...")
        email = browser.find_element(By.XPATH, '//*[@id="username"]')
        if email.get_attribute('value') == "":
            send_input(email_name, email)

        time.sleep(get_random_time())

        print(f"thread[{task}] task[{task_num + 1}]: Entering Password...")
        password = browser.find_element(By.XPATH, '//*[@id="passwd"]/div[1]/div/div[1]/input')
        send_input(rand_pass, password)

        time.sleep(get_random_time())

        print(f"thread[{task}] task[{task_num + 1}]: Entering Password(2)...")
        confirm_password = browser.find_element(By.XPATH, '//*[@id="confirm-passwd"]/div[1]/div/div[1]/input')
        send_input(rand_pass, confirm_password)

        time.sleep(get_random_time())
        genned_mail_address = ''
        found_suggestion = False
        name_taken = True
        while name_taken:
            try:
                message = browser.find_element(By.XPATH,
                                               '//*[@id="view_container"]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[2]/div[1]/div/div[2]/div[2]/div')
                if message.is_displayed():
                    name_taken = True
            except:
                name_taken = False

            if name_taken:
                try:
                    suggested_name = browser.find_element(By.XPATH,
                                                          '//*[@id="view_container"]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[2]/div[2]/div/ul/li[2]/button')
                    found_suggestion = True
                except:
                    found_suggestion = False

                if found_suggestion:
                    print(f"thread[{task}] task[{task_num + 1}] Email Taken, Trying Suggested Option...")
                    genned_mail_address = suggested_name.text
                    suggested_name.click()
                    time.sleep(get_random_time())
                    print(genned_mail_address)
                    time.sleep(get_random_time())
                else:
                    print(f"thread[{task}] task[{task_num}] No Suggestion Found, Adding Numbers...")
                    email_num1 = random.randrange(1, 10)
                    email_num2 = random.randrange(1, 10)
                    email_num3 = random.randrange(1, 10)
                    send_input(str(email_num1) + str(email_num2) + str(email_num3), email)
                    time.sleep(get_random_time())
                    next_button = browser.find_element(By.XPATH, '//*[@id="accountDetailsNext"]/div/button')
                    next_button.click()
                    time.sleep(get_random_time())
                    try:
                        message = browser.find_element(By.XPATH,
                                                       '//*[@id="view_container"]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[2]/div[1]/div/div[2]/div[2]/div')
                        if message.is_displayed():
                            name_taken = True
                        else:
                            name_taken = False
                            genned_mail_address = email.get_attribute('value')
                            break
                    except:
                        name_taken = False
                        genned_mail_address = email.get_attribute('value')
                        break
            else:
                genned_mail_address = email.get_attribute('value')
                next_button = browser.find_element(By.XPATH, '//*[@id="accountDetailsNext"]/div/button')
                next_button.click()
                time.sleep(get_random_time())
                break

        time.sleep(get_random_time())

        phone_session = requests.session()

        get_phone_count = 0
        is_error = True
        while is_error:
            if get_phone_count > 3:
                print(f"thread[{task}] task[{task_num + 1}] Max Retry Reached, Stopping Task...")
                return
            print(f"thread[{task}] task[{task_num + 1}] Getting Phone Number...")
            res = phone_session.post(
                f"https://public.sms-gen.com/v1/sms/number?country=US&service=Google&channel=1&apikey={api_key}&ref=3929432")
            error_get = res.json()['isError']
            if not error_get:
                print(f"thread[{task}] task[{task_num + 1}]Phone Number Found!")
                phone_number = res.json()['number']
                phone_id = res.json()['id']
                print(f"thread[{task}] task[{task_num + 1}] Phone Number: {phone_number}")
                if '+' in phone_number:
                    phone_num = phone_number[2:len(phone_number)]
                else:
                    phone_num = phone_number[1:len(phone_number)]

                phone_page_count = 0
                phone_page_loaded = False
                while not phone_page_loaded:
                    try:
                        country_btn = browser.find_element(By.XPATH, '//*[@id="countryList"]/div/div[1]')
                        country_btn.click()

                        time.sleep(get_random_time())

                        country_code = browser.find_element(By.XPATH, '//*[@id="countryList"]/div/div[2]/ul/li[227]')
                        country_code.click()

                        time.sleep(get_random_time())

                        phone_page_loaded = True
                        break
                    except:
                        if phone_page_count > 5:
                            print(
                                f"thread[{task}] task[{task_num + 1}] page took too long to load (potential proxy issue), terminating task...")
                            return
                        phone_page_count = phone_page_count + 1
                        print(f"thread[{task}] task[{task_num + 1}] Waiting for page to load...")
                        time.sleep(2)

                print(f"thread[{task}] task[{task_num + 1}] Inserting Phone Number...")
                phone_input = browser.find_element(By.XPATH, '//*[@id="phoneNumberId"]')
                send_input(phone_num, phone_input)

                time.sleep(get_random_time())

                next_button = browser.find_element(By.XPATH,
                                                   '//*[@id="view_container"]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button')
                next_button.click()

                time.sleep(get_random_time())

                try:
                    error_message = browser.find_element(By.XPATH,
                                                         '//*[@id="view_container"]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[2]/div/div[2]/div[2]/div')
                    if error_message.is_displayed():
                        print(f"thread[{task}] task[{task_num + 1}] Phone Number Cant Be Used... Retry")
                        ban_res = phone_session.post(
                            f"https://public.sms-gen.com/v1/sms/bannumber?id={phone_id}&apikey={api_key}&ref=3929432")
                        phone_input.clear()
                        is_error = True
                    else:
                        print(f"thread[{task}] task[{task_num + 1}] Phone Number Valid!")
                        is_error = False
                        break
                except:
                    print(f"thread[{task}] task[{task_num + 1}] Phone Number Valid!")
                    is_error = False
                    break
            else:
                print(f"thread[{task}] task[{task_num + 1}] Phone Number Request Failed, Retry")
                get_phone_count = get_phone_count + 1

        time.sleep(get_random_time())

        retry = True
        time_count = 0
        while retry:
            print(f"thread[{task}] task[{task_num + 1}] Getting Code...")
            code_res = phone_session.get(
                f"https://public.sms-gen.com/v1/sms/code?id={phone_id}&apikey={api_key}&ref=3929432")
            retry = code_res.json()['retry']
            if not retry:
                print(f"thread[{task}] task[{task_num + 1}] Code found!")
                phone_code = code_res.json()['sms']
            else:
                print(f"thread[{task}] task[{task_num + 1}] Still waiting for code")
                time.sleep(8)
                time_count = time_count + 1
                if time_count > 8:
                    cancel_res = phone_session.post(
                        f"https://public.sms-gen.com/v1/sms/cancelnumber?id={phone_id}&apikey={api_key}&ref=3929432")
                    print(f"thread[{task}] task[{task_num + 1}] Code took too long to receive, terminating task & canceling number...")
                    return

        code_page_found = False
        code_page_count = 0
        while not code_page_found:
            try:
                print(f"thread[{task}] task[{task_num + 1}] Inserting Code...")
                code_input = browser.find_element(By.XPATH, '//*[@id="code"]')
                send_input(phone_code, code_input)

                time.sleep(get_random_time())
                code_page_found = True
                break
            except:
                if code_page_count > 5:
                    print(
                        f"thread[{task}] task[{task_num + 1}] page took too long to load (potential proxy issue), terminating task...")
                    return
                code_page_count = code_page_count + 1
                print(f"thread[{task}] task[{task_num + 1}] Waiting for page to load...")
                time.sleep(get_random_time())

        verify_button = browser.find_element(By.XPATH,
                                             '//*[@id="view_container"]/div/div/div[2]/div/div[2]/div[2]/div[1]/div/div/button')
        verify_button.click()

        time.sleep(get_random_time())

        personal_page_found = False
        personal_page_count = 0
        while not personal_page_found:
            try:
                print(f"thread[{task}] task[{task_num + 1}] Entering Personal Information")
                email_nums = random.randint(1, 10)
                email_nums2 = random.randint(1, 10)
                email_nums3 = random.randint(1, 10)
                if '@' in catchall:
                    recovery_email = f_name + l_name + str(email_nums) + str(email_nums2) + str(
                        email_nums3) + catchall
                else:
                    recovery_email = f_name + l_name + str(email_nums) + str(email_nums2) + str(
                        email_nums3) + '@' + catchall


                recovery_email_input = browser.find_element(By.XPATH,
                                                            '//*[@id="view_container"]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[2]/div[1]/div/div[1]/div/div[1]/input')
                send_input(recovery_email, recovery_email_input)

                personal_page_found = True
                break
            except:
                if personal_page_count > 5:
                    print(
                        f"thread[{task}] task[{task_num + 1}] page took too long to load (potential proxy issue), terminating task...")
                    return
                personal_page_count = personal_page_count + 1
                print(f"thread[{task}] task[{task_num + 1}] Waiting for page to load...")
                time.sleep(get_random_time())

        time.sleep(get_random_time())
        birth_month_dd = browser.find_element(By.XPATH, '//*[@id="month"]')
        birth_month_dd.click()

        time.sleep(get_random_time())

        month = random.randint(2, 12)
        birth_month = browser.find_element(By.XPATH, f"//*[@id='month']/option[{month}]")
        birth_month.click()

        time.sleep(get_random_time())

        birth_day_input = browser.find_element(By.XPATH, '//*[@id="day"]')
        birth_day_input.send_keys(random.randint(1, 2))
        time.sleep(get_random_time())
        birth_day_input.send_keys(random.randint(1, 8))

        time.sleep(get_random_time())

        birth_year_input = browser.find_element(By.XPATH, '//*[@id="year"]')
        first_num = random.randint(1, 2)
        birth_year_input.send_keys(first_num)
        time.sleep(get_random_time())
        if first_num == 1:
            birth_year_input.send_keys('9')
            time.sleep(get_random_time_text())
            birth_year_input.send_keys(random.randint(7, 9))
            time.sleep(get_random_time_text())
            birth_year_input.send_keys(random.randint(1, 9))
        elif first_num == 2:
            birth_year_input.send_keys('0')
            time.sleep(get_random_time_text())
            birth_year_input.send_keys('0')
            time.sleep(get_random_time_text())
            birth_year_input.send_keys(0, 4)

        time.sleep(get_random_time())

        gender_dd = browser.find_element(By.XPATH, '//*[@id="gender"]')
        gender_dd.click()

        time.sleep(get_random_time())

        gender = browser.find_element(By.XPATH, '//*[@id="gender"]/option[3]')
        gender.click()

        time.sleep(get_random_time())

        next_button = browser.find_element(By.XPATH,
                                           '//*[@id="view_container"]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button')
        next_button.click()

        time.sleep(get_random_time())

        preferences_page_found = False
        preferences_count = 0
        while not preferences_page_found:
            try:
                print(f"thread[{task}] task[{task_num + 1}] Selecting Preferences...")
                yes_im_in = browser.find_element(By.XPATH,
                                                 '//*[@id="view_container"]/div/div/div[2]/div/div[2]/div[2]/div[1]/div/div/button')
                yes_im_in.click()

                preferences_page_found = True
                break
            except:
                if preferences_count > 5:
                    print(
                        f"thread[{task}] task[{task_num + 1}] page took too long to load (potential proxy issue), terminating task...")
                    return
                preferences_count = preferences_count + 1
                print(f"thread[{task}] task[{task_num + 1}] Waiting for page to load...")
                time.sleep(2)

        time.sleep(get_random_time())
        personalization_page_found = False
        personalization_count = 0
        while not personalization_page_found:
            try:
                print(f"thread[{task}] task[{task_num + 1}] Selecting Preferences [2]...")
                personalization_settings = browser.find_element(By.XPATH,
                                                                '//*[@id="view_container"]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div/div/div[1]/div/span/div[1]/div/div[1]')
                personalization_settings.click()

                personalization_page_found = True
                break
            except:
                if personalization_count > 5:
                    print(
                        f"thread[{task}] task[{task_num + 1}] personalization button not found, moving on...")
                    break
                personalization_count = personalization_count + 1
                print(f"thread[{task}]task[{task_num + 1}] Finding Personalization Settings...")
                time.sleep(2)

        time.sleep(get_random_time())
        next_button_found = False
        next_button_count = 0
        while not next_button_found:
            try:
                next_button = browser.find_element(By.XPATH,
                                                   '//*[@id="view_container"]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button')
                next_button.click()

                next_button_found = True
                break
            except:
                if next_button_count > 5:
                    print(
                        f"thread[{task}] task[{task_num + 1}] page took too long to load (potential proxy issue), terminating task...")
                    return
                next_button_count = next_button_count + 1
                print(f"thread[{task}] task[{task_num + 1}] Trying to find personalization settings...")
                time.sleep(2)

        time.sleep(get_random_time())
        confirm_found = False
        confirm_count = 0
        while not confirm_found:
            try:
                confirm_button = browser.find_element(By.XPATH,
                                                      '//*[@id="view_container"]/div/div/div[2]/div/div[2]/div/div[1]/div[2]/div/div/button')
                confirm_button.click()

                confirm_found = True
                break
            except:
                if confirm_count > 5:
                    print(
                        f"thread[{task}] task[{task_num + 1}] no personalization pages found, moving on...")
                    break
                confirm_count = confirm_count + 1
                print(f"thread[{task}] task[{task_num + 1}] Trying to find personalization settings...")
                time.sleep(2)

        time.sleep(get_random_time())
        agree_found = False
        agree_count = 0
        while not agree_found:
            try:
                agree_button = browser.find_element(By.XPATH,
                                                    '//*[@id="view_container"]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button')
                agree_button.click()

                agree_found = True
                break
            except:
                if agree_count > 5:
                    print(
                        f"thread[{task}] task[{task_num + 1}] no personalization pages found, moving on...")
                    break
                agree_count = agree_count + 1
                print(f"thread[{task}] task[{task_num + 1}] Trying to find personalization settings...")
                time.sleep(get_random_time())

        time.sleep(get_random_time())
        gm = open('gennedmails.txt', 'a')
        gm.write(
            f"\n{genned_mail_address}@gmail.com:{rand_pass}:{f_name}:{l_name}:{recovery_email}-{PROXY_HOST}:{PROXY_PORT}:{PROXY_USER}:{PROXY_PASS}")
        print(f"thread[{task}] task[{task_num + 1}] Gmail Account Successfully Created.")
        format_proxy = PROXY_HOST + ":" + PROXY_PORT + ":" + PROXY_USER + ":" + PROXY_PASS
        send_webhook(genned_mail_address + '@gmail.com', rand_pass, recovery_email, phone_number, format_proxy)
        send_webhook_public()

    for s in range(tasks_to_run):
        t1 = threading.Thread(target=gen_account, args=[s])
        t1.start()
        t1.join()


while not stop and license_authenticated:

    with open('proxies.txt', 'r') as f:
        proxies = [line.strip() for line in f]

    amount_of_proxies = len(proxies)

    print('Welcome to Account Gen. Please Select a Module from the List Below.')
    print('1) Google Gen')
    print('0) Exit')
    correct = False
    while not correct:
        option = input('Option: ')
        if option != '1' and option != '0':
            correct = False
        else:
            correct = True
            break

    if option == '0':
        exit(0)

    with open('settings.json', 'r') as f:
        data = json.load(f)

    API_KEY = data['API_KEY']
    CATCHALL = data['CATCHALL']
    WEBHOOK = data['DISCORD_WEBHOOK']

    concurrent_tasks = int(input('Enter the amount of tasks you would like to run concurrently (Max 10): '))
    number_of_accounts = int(input('How many accounts would you like to create? '))

    accs_to_gen = []

    if concurrent_tasks > 10:
        print()

    if number_of_accounts % concurrent_tasks != 0:
        remainder = number_of_accounts % concurrent_tasks
        divisible_num = (number_of_accounts - remainder) // concurrent_tasks
        for i in range(concurrent_tasks):
            accs_to_gen.append(int(divisible_num))

        for i in range(remainder):
            accs_to_gen[i] = accs_to_gen[i] + 1
    else:
        for m in range(concurrent_tasks):
            accs_to_gen.append(int(number_of_accounts // concurrent_tasks))

    proxies_available = []

    if amount_of_proxies % concurrent_tasks != 0:
        remainder = amount_of_proxies % concurrent_tasks
        divisible_num = (amount_of_proxies - remainder) // concurrent_tasks
        for l in range(concurrent_tasks):
            proxies_available.append(divisible_num)

        for z in range(remainder):
            proxies_available[z] = proxies_available[z] + 1
    else:
        for s in range(concurrent_tasks):
            proxies_available.append(int(amount_of_proxies // concurrent_tasks))

    proxies_available_string = ''
    for l in range(len(proxies_available)):
        if l != len(proxies_available) - 1:
            proxies_available_string = proxies_available_string + str(proxies_available[l]) + ','
        else:
            proxies_available_string = proxies_available_string + str(proxies_available[l])

    def run_task(task, number_of_accs):
        gen_google(task=task, tasks_to_run=number_of_accs, concurrent_tasks=concurrent_tasks, proxies_available=proxies_available_string)


    if concurrent_tasks == 1:
        t1 = threading.Thread(target=run_task, args=[1, accs_to_gen[0]])
        t1.start()
        t1.join()
        print('Generation Complete...')

    if concurrent_tasks == 2:
        t1 = threading.Thread(target=run_task, args=[1, accs_to_gen[0]])
        t2 = threading.Thread(target=run_task, args=[2, accs_to_gen[1]])
        t1.start()
        time.sleep(get_random_time())
        t2.start()
        t1.join()
        t2.join()
        print('Generation Complete...')

    if concurrent_tasks == 3:
        t1 = threading.Thread(target=run_task, args=[1, accs_to_gen[0]])
        t2 = threading.Thread(target=run_task, args=[2, accs_to_gen[1]])
        t3 = threading.Thread(target=run_task, args=[3, accs_to_gen[2]])
        t1.start()
        time.sleep(get_random_time())
        t2.start()
        time.sleep(get_random_time())
        t3.start()
        t1.join()
        t2.join()
        t3.join()
        print('Generation Complete...')

    if concurrent_tasks == 4:
        t1 = threading.Thread(target=run_task, args=[1, accs_to_gen[0]])
        t2 = threading.Thread(target=run_task, args=[2, accs_to_gen[1]])
        t3 = threading.Thread(target=run_task, args=[3, accs_to_gen[2]])
        t4 = threading.Thread(target=run_task, args=[4, accs_to_gen[3]])
        t1.start()
        time.sleep(get_random_time())
        t2.start()
        time.sleep(get_random_time())
        t3.start()
        time.sleep(get_random_time())
        t4.start()
        t1.join()
        t2.join()
        t3.join()
        t4.join()
        print('Generation Complete...')

    if concurrent_tasks == 5:
        t1 = threading.Thread(target=run_task, args=[1, accs_to_gen[0]])
        t2 = threading.Thread(target=run_task, args=[2, accs_to_gen[1]])
        t3 = threading.Thread(target=run_task, args=[3, accs_to_gen[2]])
        t4 = threading.Thread(target=run_task, args=[4, accs_to_gen[3]])
        t5 = threading.Thread(target=run_task, args=[5, accs_to_gen[4]])
        t1.start()
        time.sleep(get_random_time())
        t2.start()
        time.sleep(get_random_time())
        t3.start()
        time.sleep(get_random_time())
        t4.start()
        time.sleep(get_random_time())
        t5.start()
        t1.join()
        t2.join()
        t3.join()
        t4.join()
        t5.join()
        print('Generation Complete...')

    if concurrent_tasks == 6:
        t1 = threading.Thread(target=run_task, args=[1, accs_to_gen[0]])
        t2 = threading.Thread(target=run_task, args=[2, accs_to_gen[1]])
        t3 = threading.Thread(target=run_task, args=[3, accs_to_gen[2]])
        t4 = threading.Thread(target=run_task, args=[4, accs_to_gen[3]])
        t5 = threading.Thread(target=run_task, args=[5, accs_to_gen[4]])
        t6 = threading.Thread(target=run_task, args=[6, accs_to_gen[5]])
        t1.start()
        time.sleep(get_random_time())
        t2.start()
        time.sleep(get_random_time())
        t3.start()
        time.sleep(get_random_time())
        t4.start()
        time.sleep(get_random_time())
        t5.start()
        time.sleep(get_random_time())
        t6.start()
        t1.join()
        t2.join()
        t3.join()
        t4.join()
        t5.join()
        t6.join()
        print('Generation Complete...')

    if concurrent_tasks == 7:
        t1 = threading.Thread(target=run_task, args=[1, accs_to_gen[0]])
        t2 = threading.Thread(target=run_task, args=[2, accs_to_gen[1]])
        t3 = threading.Thread(target=run_task, args=[3, accs_to_gen[2]])
        t4 = threading.Thread(target=run_task, args=[4, accs_to_gen[3]])
        t5 = threading.Thread(target=run_task, args=[5, accs_to_gen[4]])
        t6 = threading.Thread(target=run_task, args=[6, accs_to_gen[5]])
        t7 = threading.Thread(target=run_task, args=[7, accs_to_gen[6]])
        t1.start()
        time.sleep(get_random_time())
        t2.start()
        time.sleep(get_random_time())
        t3.start()
        time.sleep(get_random_time())
        t4.start()
        time.sleep(get_random_time())
        t5.start()
        time.sleep(get_random_time())
        t6.start()
        time.sleep(get_random_time())
        t7.start()
        t1.join()
        t2.join()
        t3.join()
        t4.join()
        t5.join()
        t6.join()
        t7.join()
        print('Generation Complete...')

    if concurrent_tasks == 8:
        t1 = threading.Thread(target=run_task, args=[1, accs_to_gen[0]])
        t2 = threading.Thread(target=run_task, args=[2, accs_to_gen[1]])
        t3 = threading.Thread(target=run_task, args=[3, accs_to_gen[2]])
        t4 = threading.Thread(target=run_task, args=[4, accs_to_gen[3]])
        t5 = threading.Thread(target=run_task, args=[5, accs_to_gen[4]])
        t6 = threading.Thread(target=run_task, args=[6, accs_to_gen[5]])
        t7 = threading.Thread(target=run_task, args=[7, accs_to_gen[6]])
        t8 = threading.Thread(target=run_task, args=[8, accs_to_gen[7]])
        t1.start()
        time.sleep(get_random_time())
        t2.start()
        time.sleep(get_random_time())
        t3.start()
        time.sleep(get_random_time())
        t4.start()
        time.sleep(get_random_time())
        t5.start()
        time.sleep(get_random_time())
        t6.start()
        time.sleep(get_random_time())
        t7.start()
        time.sleep(get_random_time())
        t8.start()
        t1.join()
        t2.join()
        t3.join()
        t4.join()
        t5.join()
        t6.join()
        t7.join()
        t8.join()
        print('Generation Complete...')

    if concurrent_tasks == 9:
        t1 = threading.Thread(target=run_task, args=[1, accs_to_gen[0]])
        t2 = threading.Thread(target=run_task, args=[2, accs_to_gen[1]])
        t3 = threading.Thread(target=run_task, args=[3, accs_to_gen[2]])
        t4 = threading.Thread(target=run_task, args=[4, accs_to_gen[3]])
        t5 = threading.Thread(target=run_task, args=[5, accs_to_gen[4]])
        t6 = threading.Thread(target=run_task, args=[6, accs_to_gen[5]])
        t7 = threading.Thread(target=run_task, args=[7, accs_to_gen[6]])
        t8 = threading.Thread(target=run_task, args=[8, accs_to_gen[7]])
        t9 = threading.Thread(target=run_task, args=[9, accs_to_gen[8]])
        t1.start()
        time.sleep(get_random_time())
        t2.start()
        time.sleep(get_random_time())
        t3.start()
        time.sleep(get_random_time())
        t4.start()
        time.sleep(get_random_time())
        t5.start()
        time.sleep(get_random_time())
        t6.start()
        time.sleep(get_random_time())
        t7.start()
        time.sleep(get_random_time())
        t8.start()
        time.sleep(get_random_time())
        t9.start()
        t1.join()
        t2.join()
        t3.join()
        t4.join()
        t5.join()
        t6.join()
        t7.join()
        t8.join()
        t9.join()
        print('Generation Complete...')

    if concurrent_tasks == 10:
        t1 = threading.Thread(target=run_task, args=[1, accs_to_gen[0]])
        t2 = threading.Thread(target=run_task, args=[2, accs_to_gen[1]])
        t3 = threading.Thread(target=run_task, args=[3, accs_to_gen[2]])
        t4 = threading.Thread(target=run_task, args=[4, accs_to_gen[3]])
        t5 = threading.Thread(target=run_task, args=[5, accs_to_gen[4]])
        t6 = threading.Thread(target=run_task, args=[6, accs_to_gen[5]])
        t7 = threading.Thread(target=run_task, args=[7, accs_to_gen[6]])
        t8 = threading.Thread(target=run_task, args=[8, accs_to_gen[7]])
        t9 = threading.Thread(target=run_task, args=[9, accs_to_gen[8]])
        t10 = threading.Thread(target=run_task, args=[10, accs_to_gen[9]])
        t1.start()
        time.sleep(get_random_time())
        t2.start()
        time.sleep(get_random_time())
        t3.start()
        time.sleep(get_random_time())
        t4.start()
        time.sleep(get_random_time())
        t5.start()
        time.sleep(get_random_time())
        t6.start()
        time.sleep(get_random_time())
        t7.start()
        time.sleep(get_random_time())
        t8.start()
        time.sleep(get_random_time())
        t9.start()
        time.sleep(get_random_time())
        t10.start()
        t1.join()
        t2.join()
        t3.join()
        t4.join()
        t5.join()
        t6.join()
        t7.join()
        t8.join()
        t9.join()
        t10.join()
        print('Generation Complete...')