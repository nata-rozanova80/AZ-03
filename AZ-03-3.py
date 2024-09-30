import time
import csv
import sys
import pandas as pd
from selenium import webdriver
import matplotlib.pyplot as plt
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

url = "https://www.divan.ru/category/promo-dostavim-bystro-moscow?types%5B%5D=1"
driver.get(url)

# Задержка для загрузки страницы
time.sleep(10)

# Поиск цен на диваны
prices = []
parsed_data = []

products = driver.find_elements(By.CLASS_NAME, 'lsooF')
print("Найдено продуктов:", len(products))
if products == 0:
    sys.exit()

for product in products:
    try:
        price = product.find_element(By.CSS_SELECTOR, 'meta[itemprop="price"]').get_attribute('content')
        parsed_data.append([price])
    except Exception as e:
        print("Нет такого элемента:", e)
        continue

# Запись данных в CSV файл
with open("divans.csv", 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Цена'])  # Заголовок
    writer.writerows(parsed_data)

# Создание DataFrame из записанных данных
df = pd.DataFrame(parsed_data, columns=['Цена'])

# Извлечение числовых данных
df['Цена'] = df['Цена'].astype(int)

# Нахождение средней цены
average_price = df['Цена'].mean()
print(f'Средняя цена на диваны: {average_price} ₽')

# Построение гистограммы цен
plt.hist(df['Цена'], bins=20, alpha=0.7, color='blue', edgecolor='black')
plt.title('Гистограмма цен на диваны')
plt.xlabel('Цена (₽)')
plt.ylabel('Частота')
plt.grid(axis='y', alpha=0.75)
plt.show()

# Закрытие браузера
driver.quit()
