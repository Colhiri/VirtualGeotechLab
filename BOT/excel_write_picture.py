from PIL import Image as PILImage
import openpyxl
from openpyxl import Workbook
from openpyxl.drawing.image import Image
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from openpyxl import Workbook
from openpyxl.drawing.image import Image

# Создаем данные для графика (пример)
x = [1, 2, 3, 4, 5]
y = [10, 15, 7, 12, 9]
# Создаем график
fig, ax = plt.subplots(figsize=(10, 3.7))
ax.plot(x, y, label='График')
# Добавляем подписи
ax.set_xlabel('X-Ось')
ax.set_ylabel('Y-Ось')
# Добавляем легенду
ax.legend()
# Создаем объект для сохранения графика в виде изображения
canvas = FigureCanvas(fig)
canvas.draw()
# Сохраняем график как изображение
graph_image_path = 'график.png'
plt.savefig(graph_image_path, dpi=100)  # canvas.print_png(graph_image_path)

# Открываем исходное изображение с помощью PIL
image = PILImage.open(graph_image_path)
# Изменяем размер картинки (например, до 200x200 пикселей)
new_size = (1000, 370)
resized_image = image.resize(new_size)
# Сохраняем измененную картинку
resized_image.save(graph_image_path)

# Создаем новый документ Excel
workbook = openpyxl.load_workbook(f'TEST.xlsx')
sheet = workbook.active

# Создаем объект изображения на основе сохраненного графика
img = Image(graph_image_path)

# Добавляем изображение в ячейку (например, B2)
sheet.add_image(img, 'B2')

# Сохраняем документ Excel
output_excel_path = 'TEST.xlsx'
workbook.save(output_excel_path)
