from PIL import Image
from selenium import webdriver
from PIL import Image, ImageFilter
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\\Users\\MSI GP66\\PycharmProjects\\dj_project\\tesseract\\tesseract.exe"

def get_captcha(driver, element, path):
    # now that we have the preliminary stuff out of the way time to get that image :D
    # location = element.location
    # size = element.size
    # saves screenshot of entire page
    driver.save_screenshot(path)

    # uses PIL library to open image in memory
    image = Image.open(path)

    crop_width = 220 # 300
    crop_height = 60 # 80

    # Вычисляем координаты для обрезки по центру
    left = (image.width - crop_width) // 2
    top = (image.height - crop_height) // 3.2
    right = left + crop_width
    bottom = top + crop_height

    image = image.crop((left, top, right, bottom))  # defines crop points
    image.save(path, 'png')  # saves new cropped image

    captcha = pytesseract.image_to_string(image)
    captcha = captcha.replace(" ", "").strip()
    print(captcha)


# get_captcha(1, 1, path='captcha — копия (3) — копия.png')

