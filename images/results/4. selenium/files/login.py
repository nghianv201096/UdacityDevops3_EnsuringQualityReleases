from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
import datetime


def timestamp():
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return (ts + '\t')

# Start the browser and login with standard_user
def login(user, password):
    
    # go to login page.
    print(timestamp() + 'Starting the browser...')
    options = ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument("--headless") 
    options.add_argument("--remote-debugging-port=9230")
    driver = webdriver.Chrome(options=options, executable_path="./chromedriver")
    print(timestamp() + 'Browser started successfully. Navigating to the demo page to login.')
    driver.get('https://www.saucedemo.com/')
    
    # login to the website.
    driver.find_element(By.CSS_SELECTOR, "input[id='user-name']").send_keys(user)
    driver.find_element(By.CSS_SELECTOR, "input[id='password']").send_keys(password)
    driver.find_element(By.ID, "login-button").click()
    product_label = driver.find_element(By.CSS_SELECTOR, "div[class='inventory_item_name']").text
    assert "Sauce Labs Backpack" in product_label
    print(timestamp() + 'Login successfully with username {:s} and password {:s}.'.format(user, password))
    
    return driver

def add_cart(driver, n_items):
    for i in range(n_items):
        element = "a[id='item_" + str(i) + "_title_link']"  
        driver.find_element(By.CSS_SELECTOR, element).click()  
        driver.find_element(By.CSS_SELECTOR,"button.btn_primary.btn_inventory").click()  
        product = driver.find_element(By.CSS_SELECTOR,"div[class='inventory_details_name large_size']").text  
        print(timestamp() + product + " is added to the shopping cart.")  
        driver.find_element(By.CSS_SELECTOR,"button.inventory_details_back_button").click()

    print(timestamp() + '{:d} items are all added to the shopping cart successfully.'.format(n_items))

def remove_cart(driver, n_items):
    for i in range(n_items):
        element = "a[id='item_" + str(i) + "_title_link']"
        driver.find_element(By.CSS_SELECTOR,element).click()
        driver.find_element(By.CSS_SELECTOR,"button.btn_secondary.btn_inventory").click()
        product = driver.find_element(By.CSS_SELECTOR,"div[class='inventory_details_name large_size']").text
        print(timestamp() + product + " is removed from the shopping cart.")
        driver.find_element(By.CSS_SELECTOR,"button.inventory_details_back_button").click()
    print(timestamp() + '{:d} items are removed from the shopping cart successfully.'.format(n_items))


if __name__ == "__main__":
    N_ITEMS = 6
    TEST_USERNAME = 'standard_user'
    TEST_PASSWORD = 'secret_sauce'
    driver = login(TEST_USERNAME, TEST_PASSWORD)
    add_cart(driver, N_ITEMS)
    print(timestamp() + 'Test adding items done!')
    
    remove_cart(driver, N_ITEMS)
    print(timestamp() + 'Test removing items done!')
    
    driver.stop_client()
    driver.close()
    driver.quit()
    print('Clean the client done!');