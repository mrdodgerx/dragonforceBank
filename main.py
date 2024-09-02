import requests
import time
import re
from colorama import Fore, Style, init
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import configparser

# Load configuration
config = configparser.ConfigParser()
config.read('setting.ini')
username = config.get('LOGIN', 'username')
password = config.get('LOGIN', 'password')



def login():
    chrome_options = Options()
    # chrome_options.binary_location = "/opt/google/chrome/chrome"  # Adjust if necessary
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=chrome_options
    )
    # # Setup WebDriver
    # driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    obj_browser = {
        "data_csrf": None,
        "xf_csrf": None,
        "xf_session": None,
        "cf_clearance": None,
        "xf_user": None
    }

    # Open the login page
    driver.get('https://www.dragonforce.io/dbtech-shop/bank/')
    driver.implicitly_wait(10)  # Wait for elements to load

    try:
        # Find the username and password fields and input the credentials
        username_field = driver.find_element(By.NAME, 'login')
        password_field = driver.find_element(By.NAME, 'password')
        username_field.send_keys(username)
        password_field.send_keys(password)

        # Find and click the login button
        login_button = driver.find_element(By.XPATH, '//button[contains(@class, "button--primary") and .//span[text()="Log in"]]') 
        login_button.click()

        # Wait for the page to load after login
        time.sleep(5)

        # Extract the `data-csrf` attribute value
        csrf_element = driver.find_element(By.XPATH, '//input[@name="_xfToken"]')
        data_csrf = csrf_element.get_attribute('value')
        obj_browser["data_csrf"] = data_csrf

        print(f"data-csrf: {data_csrf}")

        # Extract cookies
        cookies = driver.get_cookies()
        for cookie in cookies:
            obj_browser[cookie['name']] = cookie['value']

    finally:
        driver.quit()
        return obj_browser


class DC_SHOP:
    def __init__(self,obj_cookies=None):
        init(autoreset=True)
        self.web_form = 'WebKitFormBoundary9eD6TiUtbcBsRSPm'
        # if not obj_cookies:
        self.obj =obj_cookies # login()
        #     obj_cookies = self.obj
            
        self.cookies = self.obj

        self.headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': f'multipart/form-data; boundary=----{self.web_form}',
            'origin': 'https://www.dragonforce.io',
            'referer': 'https://www.dragonforce.io/dbtech-shop/steal/',
            'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Brave";v="128"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Linux"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }

        self.top5 = None

    def withdraw(self,value):
        data = f'------{self.web_form}\r\nContent-Disposition: form-data; name="_xfToken"\r\n\r\n{self.obj["data_csrf"]}\r\n------{self.web_form}\r\nContent-Disposition: form-data; name="points"\r\n\r\n{value}\r\n------{self.web_form}\r\nContent-Disposition: form-data; name="_xfRequestUri"\r\n\r\n/dbtech-shop/bank/\r\n------{self.web_form}\r\nContent-Disposition: form-data; name="_xfWithData"\r\n\r\n1\r\n------{self.web_form}\r\nContent-Disposition: form-data; name="_xfToken"\r\n\r\n{self.obj["data_csrf"]}\r\n------{self.web_form}\r\nContent-Disposition: form-data; name="_xfResponseType"\r\n\r\njson\r\n------{self.web_form}--\r\n'

        response = requests.post(
            'https://www.dragonforce.io/dbtech-shop/bank/dragoncoin.2/withdraw',
            cookies=self.cookies,
            headers=self.headers,
            data=data,
        )

        if response.status_code == 200:
            return f"{Fore.BLUE}Withdraw {value} Success{Style.RESET_ALL}"
        else:
            return f"{Fore.MAGENTA}Something error cannot withdraw {value}{Style.RESET_ALL}"

    def deposit(self,value):
        data = f'------{self.web_form}\r\nContent-Disposition: form-data; name="_xfToken"\r\n\r\n{self.obj["data_csrf"]}\r\n------{self.web_form}\r\nContent-Disposition: form-data; name="points"\r\n\r\n{value}\r\n------{self.web_form}\r\nContent-Disposition: form-data; name="_xfRequestUri"\r\n\r\n/dbtech-shop/bank/\r\n------{self.web_form}\r\nContent-Disposition: form-data; name="_xfWithData"\r\n\r\n1\r\n------{self.web_form}\r\nContent-Disposition: form-data; name="_xfToken"\r\n\r\n{self.obj["data_csrf"]}\r\n------{self.web_form}\r\nContent-Disposition: form-data; name="_xfResponseType"\r\n\r\njson\r\n------{self.web_form}--\r\n'

        response = requests.post(
            'https://www.dragonforce.io/dbtech-shop/bank/dragoncoin.2/deposit',
            cookies=self.cookies,
            headers=self.headers,
            data=data,
        )
        if response.status_code == 200:
            r = response.json()
            # print(r)
            if r['status'] == 'error':
                money_str = r['errors'][0]
                
                money =re.search(r'[\d,]+\.\d+', money_str).group()
                money = money.replace(',', '')

                # print(money)
                x = str(float(money)- 205.80)
                # print(x)
                return self.deposit(value=str(x))
            return f"{Fore.YELLOW}Transfer to bank {value}{Style.RESET_ALL}"
        else:
            r = response.json()
            return r
        
    def mark_read(self):
        headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',   
        }
            
        data = {
            '_xfRequestUri': '/dbtech-shop/bank/',
            '_xfWithData': '1',
            '_xfToken': self.obj['data_csrf'],
            '_xfResponseType': 'json',
        }

        response = requests.post('https://www.dragonforce.io/account/alerts/mark-read', cookies=self.cookies, headers=headers, data=data)
        if response.status_code == 200:
            return f"{Fore.YELLOW}All Message Read{Style.RESET_ALL}"
        return f"{Fore.RED}Error In read Message{Style.RESET_ALL}"
    
    def curi(self,username=''):
        data = f'------{self.web_form}\r\nContent-Disposition: form-data; name="_xfToken"\r\n\r\n{self.obj["data_csrf"]}\r\n------{self.web_form}\r\nContent-Disposition: form-data; name="username"\r\n\r\n{username}\r\n------{self.web_form}\r\nContent-Disposition: form-data; name="currency_id"\r\n\r\n2\r\n------{self.web_form}\r\nContent-Disposition: form-data; name="_xfRequestUri"\r\n\r\n/dbtech-shop/steal/\r\n------{self.web_form}\r\nContent-Disposition: form-data; name="_xfWithData"\r\n\r\n1\r\n------{self.web_form}\r\nContent-Disposition: form-data; name="_xfToken"\r\n\r\n{self.obj["data_csrf"]}\r\n------{self.web_form}\r\nContent-Disposition: form-data; name="_xfResponseType"\r\n\r\njson\r\n------{self.web_form}--\r\n'

        response = requests.post('https://www.dragonforce.io/dbtech-shop/steal/', cookies=self.cookies, headers=self.headers, data=data)
        if response.status_code == 200:
            # print(response.text)
            r = response.json()
            if r['message'] != 'You failed to steal any funds from the target.':
                return f"{Fore.GREEN}You got money from {username}{Style.RESET_ALL}"
            else:
                return f"{Fore.RED}Steal from {username} not success{Style.RESET_ALL}"
        return response
    
    def get_top5(self):
        params = {
            # 'user_id': '34520',
            '_xfRequestUri': '/',
            '_xfWithData': '1',
            '_xfToken': self.obj['data_csrf'],
            '_xfResponseType': 'json',
        }

        response = requests.get(
            'https://www.dragonforce.io/dbtech-credits/currency/dragoncoin.1/',
            params=params,
            cookies=self.cookies,
            headers=self.headers,
        )
        list_user = []
        if response.status_code == 200:
            data = response.json()
            
            # Regular expression pattern to match usernames
            pattern = r'class="username.*?>(.*?)<'

            # Find all matches in the HTML content
            usernames = re.findall(pattern, data['html']['content'])

            # Print the extracted usernames
            for name in usernames:
                # print(name)
                list_user.append(name)
                
        list_user = [name for name in list_user if name]

        self.top5 = list_user
    
    def run(self):
        self.get_top5()
        if not self.top5:
            print(self.top5)
            self.obj = login()
        if 'Nizar' in self.top5:
            self.top5.remove('Nizar')
        print(self.top5)
        for user in self.top5:
            print(self.withdraw(value=210))
            print(self.curi(username=user))
            print(self.deposit(value='108029800000.00'))
            print(self.mark_read())

    
if __name__ == "__main__":
    obj_cookies = login()

    while True:
        try:
            df = DC_SHOP(obj_cookies)
            df.run()
        except Exception as err:
            print(err)
        time.sleep(0.5)