from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pprint import pprint
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--start-maximized")
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://orteil.dashnet.org/cookieclicker/")


time.sleep(1)
consent = driver.find_element(By.CSS_SELECTOR, ".fc-button")
consent.click()
time.sleep(1)
got_it = driver.find_element(By.CSS_SELECTOR, "body .cc_banner .cc_btn")
got_it.click()
time.sleep(0.2)
english = driver.find_element(By.XPATH, '//*[@id="langSelect-EN"]')
english.click()
time.sleep(4)
close = driver.find_element(By.CLASS_NAME, "close")
close.click()
time.sleep(0.1)

big_cookie = driver.find_element(By.ID, "bigCookie")
cookies_count = driver.find_element(By.ID, "cookies").text.split()[0]

bulk1 = driver.find_element(By.ID, "storeBulk1")

bulk10 = driver.find_element(By.ID, "storeBulk10")

# products = driver.find_elements(By.CLASS_NAME, "product")

# upgrades_list = upgrades.find_elements(By.TAG_NAME, "div")
# print(upgrades_list)


# print(products[0].find_element(By.CLASS_NAME, "price").text)

five_min = time.time() + 60 * 5  # 5 minutes
# i = 0
while time.time() < five_min:
    # i = (i + 1) % 100
    try:
        big_cookie.click()
    except:
       pass


    upgrades = driver.find_elements(By.CSS_SELECTOR, ".crate.upgrade.enabled")
    if upgrades:
        for upgrade in upgrades[::-1]:
            try:
                upgrade.click()
            except:
                continue


    products = driver.find_elements(By.CSS_SELECTOR, ".product.unlocked.enabled")
    if products:
        bulk10.click()
        for product in products[::-1]:
            try:
                product.click()
            except:
                continue
        bulk1.click()

    # After 5 minutes stop the bot and check the cookies per second count.
    if time.time() > five_min:
        cookie_per_s = driver.find_element(by=By.ID, value="cookiesPerSecond").text
        print(cookie_per_s)
        break

