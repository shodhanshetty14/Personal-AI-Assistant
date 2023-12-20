from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pathlib
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import logging

# from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.firefox.service import Service
# from webdriver_manager.firefox import GeckoDriverManager

logging.basicConfig(filename='./logs/error.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s')
ScriptPath = pathlib.Path().absolute()

option = Options()
user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/22.0.1216.0 Safari/537.2'
option.add_argument(f'user-agent={user_agent}')
option.add_argument("--profile-directory=Default")
option.add_argument(f"user-data-dir={ScriptPath}\\chromedata")
# option.add_argument('--headless')

service = Service(ChromeDriverManager().install())

   
def WhatsApp(name, message):
    driver = webdriver.Chrome(service=service, options=option)
    driver.maximize_window()

    url = "https://web.whatsapp.com/"
    driver.get(url)
    driver.implicitly_wait(10)
    sleep(10)
    try:
        # finding the Search bar with Xpath
        search_bar_path = '/html/body/div[1]/div/div[2]/div[3]/div/div[1]/div/div[2]/div[2]/div/div/p'
        
        input_box = WebDriverWait(driver, 60).until(
        expected_conditions.presence_of_element_located((By.XPATH, search_bar_path))
        )
        
        driver.find_element(By.XPATH, search_bar_path).send_keys(name, Keys.ENTER)
        
        sleep(5)
        
        # finding the Text Box
        text_box_path = '/html/body/div[1]/div/div[2]/div[4]/div/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p'
        driver.find_element(By.XPATH, text_box_path).send_keys(message, Keys.ENTER)
        
        sleep(5)

    except Exception as e:
        logging.error("Unable to locate elements based on Xpath: ", e)
        
        # finding the Search bar
        search_bar_css = '.qh0vvdkp > p:nth-child(1)'
        input_box = WebDriverWait(driver, 60).until(
        expected_conditions.presence_of_element_located((By.CSS_SELECTOR, search_bar_css))
        )
        driver.find_element(By.CSS_SELECTOR, search_bar_css).send_keys(name, Keys.ENTER)
        sleep(2)
        
        # finding the Text Box
        text_box_css = '._3Uu1_ > div:nth-child(1) > div:nth-child(1) > p:nth-child(1)'
        driver.find_element(By.CSS_SELECTOR, text_box_css).send_keys(message, Keys.ENTER)
        
        sleep(5)
    
    driver.close()
    
   
   
if __name__ == "__main__":
    WhatsApp()
