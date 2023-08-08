import openpyxl
from openpyxl import Workbook
from openpyxl.drawing.image import Image

# Создаем новый документ Excel
workbook = openpyxl.load_workbook(f'TEST.xlsx')
sheet = workbook.active

# Путь к файлу изображения
image_path = 'загружено.jpeg'

# Создаем объект изображения
img = Image(image_path)

# Добавляем изображение в ячейку (например, B2)
sheet.add_image(img, 'B2')

# Сохраняем документ Excel
workbook.save('TEST.xlsx')