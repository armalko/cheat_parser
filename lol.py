from selenium import webdriver
import time
import urllib.request
from python_anticaptcha import AnticaptchaClient, ImageToTextTask
from io import BytesIO
from PIL import Image
from selenium.webdriver.common.action_chains import ActionChains
import random

def get_mail():
    email = mailDriver.find_element_by_class_name("opentip")
    email = email.get_attribute('value')
    print(email)
    return email


def getRegId():
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)
    regIdDriver = webdriver.Chrome(chrome_options=chrome_options)
    regIdDriver.get("https://www.mi.com/ru/")
    regId = regIdDriver.find_element_by_xpath("//*[contains(text(), 'Регистрация')]").get_attribute('href')
    print(regId)
    regIdDriver.quit()
    return regId


def solveCaptcha():    
    api_key = '0bb959acace0ae069bb6b33015b158df'
    captcha_fp = open('captcha.png', 'rb')
    client = AnticaptchaClient(api_key)
    task = ImageToTextTask(captcha_fp)
    job = client.createTask(task)
    job.join()
    return(job.get_captcha_text())


def mailConfirm():
    m = mailDriver.find_element_by_class_name("opentip").get_attribute('value')
    time.sleep(3)
    mailDriver.find_element_by_xpath('//*[@id="click-to-refresh"]/span').click()
    time.sleep(3)
    mailDriver.find_element_by_class_name('link').click()
    time.sleep(3)
    try:
        mail = mailDriver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div[1]/div[1]/div[3]/div/div/div/p[4]/a').get_attribute('href')
    except:
        time.sleep(3)
        mail = mailDriver.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div[1]/div[1]/div[3]/div/div/div/p[4]/a').get_attribute('href')
    mailDriver.get(mail)
    mailDriver.get("https://temp-mail.org/ru/")
    mailDriver.find_element_by_id("click-to-delete").click()
    return m


def register(regId):
    regDriver = webdriver.Chrome()
    try:
        regDriver.get(regId)
        mail = get_mail()
        regDriver.find_element_by_name("email").send_keys(mail)
        regDriver.find_elements_by_css_selector(".btn332.btn_reg_1.submit-step")[-1].click()
        time.sleep(1.5)
        try:
            regDriver.find_element_by_name("password").send_keys(password)
            regDriver.find_element_by_name("repassword").send_keys(password)
        except:
            time.sleep(3)
            regDriver.find_element_by_name("password").send_keys(password)
            regDriver.find_element_by_name("repassword").send_keys(password)
        
        try:
            image = regDriver.find_elements_by_tag_name('img')[-1]
            image = image.screenshot_as_png
            im = Image.open(BytesIO(image))
            im.save("captcha.png")
            time.sleep(0.5)
            captans = solveCaptcha()
        except Exception as e:
            print(str(e))
            time.sleep(5)
            image = regDriver.find_elements_by_tag_name('img')[-1]
            image = image.screenshot_as_png
            im = Image.open(BytesIO(image))
            im.save("captcha.png")
            captans = solveCaptcha()
        regDriver.find_element_by_name("inputcode").send_keys(captans)
        regDriver.find_elements_by_css_selector(".btn332.btn_reg_1.submit-step")[-1].click() 
        regDriver.quit()
        email = mailConfirm()
    except Exception as e:
        print("in register() :", str(e))
        email = 0
        regDriver.quit()
    
    return email


def vote(email):
    voteDriver = webdriver.Chrome()
    try:
        voteDriver.get("https://event.mi.com/us/photography2018")
        try:
            voteDriver.find_element_by_class_name("vote-start-button").click()
        except:
            time.sleep(3)
            voteDriver.find_element_by_class_name("vote-start-button").click()
        voteDriver.find_element_by_id("username").send_keys(email)
        voteDriver.find_element_by_id("pwd").send_keys(password)
        voteDriver.find_element_by_id("login-button").click()
        time.sleep(3)
        voteDriver.find_element_by_class_name("vote-start-button").click()
        time.sleep(1.5)
        try:
            for j in range(49):
                time.sleep(1)
                photos = voteDriver.find_elements_by_class_name("vertical")
                if len(photos) < 2:                      
                    voteDriver.find_element_by_xpath('//*[@id="global"]/div[2]/div[2]/div[2]/div[1]/button').click()
                    continue
                if photos[0].get_attribute("src") == "//u01.appmifile.com/518_huodong_ru/08/11/2018/9b24b36e-7f05-4407-8b69-29292f37ca33_1000_1000.jpg" or photos[1].get_attribute("src") == "http://u01.appmifile.com/467_huodong_en/02/11/2018/e6025c50-8e8f-4fd9-b2d9-470a25567886_1000_1000.jpg":
                    voteDriver.find_element_by_xpath('//*[@id="global"]/div[2]/div[2]/div[2]/div[1]/button').click()
                elif photos[1].get_attribute("src") == "//u01.appmifile.com/518_huodong_ru/08/11/2018/9b24b36e-7f05-4407-8b69-29292f37ca33_1000_1000.jpg" or photos[0].get_attribute("src") == "http://u01.appmifile.com/467_huodong_en/02/11/2018/e6025c50-8e8f-4fd9-b2d9-470a25567886_1000_1000.jpg":
                    voteDriver.find_element_by_xpath('//*[@id="global"]/div[2]/div[2]/div[3]/div[1]/button').click()
                else:
                    time.sleep(0.5)
                    i = random.randint(0, 1)
                    if i == 0:
                        voteDriver.find_element_by_xpath('//*[@id="global"]/div[2]/div[2]/div[2]/div[1]/button').click()
                    else:
                        voteDriver.find_element_by_xpath('//*[@id="global"]/div[2]/div[2]/div[3]/div[1]/button').click()
        except Exception as e:
            print("Exception in vote() function:", str(e))
    except:
        pass
    voteDriver.quit()
    


password = "LolKekArbidol123"

mailDriver = webdriver.Chrome()
mailDriver.get("https://temp-mail.org/ru/")

url = "//u01.appmifile.com/518_huodong_ru/08/11/2018/9b24b36e-7f05-4407-8b69-29292f37ca33_1000_1000.jpg"


while True:
    try:
        email = register(getRegId())
        vote(email)
    except Exception as e:
        print("main:" + str(e))









    
