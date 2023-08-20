from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from captha import get_captcha

# Путь к веб-драйверу (например, Chrome)
webdriver_path = 'path/to/chromedriver'

# URL сайта, на котором нужно загрузить файл
site_url = 'https://dropmefiles.com'

# Путь к загружаемому файлу
file_path = r'C:\Users\MSI GP66\PycharmProjects\dj_project\GEOF\BOT\temp.rar'


# Инициализация веб-драйвера
driver = webdriver.Chrome()
driver.get("https://www.selenium.dev/selenium/web/web-form.html")
title = driver.title

# Открытие сайта
driver.get(site_url)


# img = driver.find_element(By.XPATH, '//img[@src="file"]')
# img = driver.find_element()
# print(img)
# print(img.text)
get_captcha(driver, 1, "captcha.png")


# Находим область для загрузки файла (пример на основе HTML-кода)
upload_area = driver.find_element(By.ID, 'upload_container')


# Перетаскиваем файл в область загрузки
file_input = driver.find_element(By.XPATH, '//input[@type="file"]')
file_input.send_keys(file_path)



# Ждем некоторое время, чтобы загрузка завершилась
while True:
    check = driver.find_element(By.CLASS_NAME, 'progress').text

    print(check)
    # change frame


    if check != 'загружено':
        time.sleep(1)
    else:
        break

time.sleep(60)

ref_area1 = driver.find_element(By.CLASS_NAME, 'url')

print(ref_area1.text)

# Закрываем веб-драйвер
driver.quit()
