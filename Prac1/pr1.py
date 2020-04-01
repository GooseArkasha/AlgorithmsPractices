import requests
from bs4 import BeautifulSoup
from datetime import datetime
from decimal import Decimal
from tkinter import *
import numpy as np
import matplotlib.pyplot as plt

# Задаем URL странички, с которой будем брать данные
url = 'https://cbr.ru/currency_base/dynamics/?UniDbQuery.Posted=True&UniDbQuery.mode=1&UniDbQuery.date_req1=&UniDbQuery.date_req2=&UniDbQuery.VAL_NM_RQ=R01090&UniDbQuery.From=28.03.2010&UniDbQuery.To=28.03.2020'

# Делаем запрос по данному URL
response = requests.get(url)

# Проверяем, получены ли данные
if response.status_code == 200:

    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    # В документе находим табличку, в которой хранятся данные
    table = soup.find('table')
    # В табличке через тег tr получаем все строки
    trs = table.find_all('tr')

    valCurrency = list()

    for i, tr in enumerate(trs):
        if i < 2:
            continue    # В первых двух строках хранятся название и шапка таблицы
        tds = tr.find_all('td')     # Формируем массив из всех данных строки [Дата][Единица][Курс]

        # Класс datetime удобен для работы с датами
        date = datetime.strptime(tds[0].text, "%d.%m.%Y")
        # Класс Decimal используем для точного представления вещественных чисел
        currencyRate = Decimal(tds[len(tds) - 1].text.replace(',', '.'))
        valCurrency.append((date, currencyRate))

else:
    print('Ошибка подключения к сайту')


def show_chart():
    x = list()
    y = list()
    for i, element in enumerate(valCurrency):
        if i % 365 == 0:
            x.append(element[0].strftime("%d.%m.%Y"))
            y.append(float(element[1]))

    x = np.array(x)
    y = np.array(y)

    fig, ax = plt.subplots()
    ax.bar(x, y)
    ax.set_title('Динамика курса валюты Белорусский рубль')
    ax.set_ylabel('Курс')
    ax.set_xlim(xmin=x[0], xmax=x[-1])
    plt.xticks(rotation=90)
    fig.tight_layout()

    plt.show()


# Создаем графику приложения
root = Tk()
root.title("Динамика курса валюты Белорусский рубль")
root.geometry("375x300")

showChartButton = Button(root, text="Посмотреть график", command=show_chart)

firstHeader = Label(root, text='Начальная дата')
secondHeader = Label(root, text='Конечная дата')
thirdHeader = Label(root, text='Шаг')

dateList = list()
for element in valCurrency:
    dateList.append(element[0].strftime("%d.%m.%Y"))    # Формируем список всех дат

firstDateListbox = Listbox()
secondDateListbox = Listbox()

for element in dateList:
    firstDateListbox.insert(END, element)   # Загружаем в первый лист бокс список всех дат
    secondDateListbox.insert(END, element)  # Загружаем во второй лист бокс список всех дат

stepsListbox = Listbox()
steps = ['День', 'Неделя', 'Месяц', 'Год']

for element in steps:
    stepsListbox.insert(END, element)


def accept_first_date():
    select = list(firstDateListbox.curselection())
    if len(select):
        select = select[len(select) - 1]
        text1.set(initialText + firstDateListbox.get(select))


acceptFirstDateButton = Button(root, text="Применить", command=accept_first_date)


def accept_second_date():
    select = list(secondDateListbox.curselection())
    if len(select):
        select = select[len(select) - 1]
        text2.set(initialText + secondDateListbox.get(select))


acceptSecondDateButton = Button(root, text="Применить", command=accept_second_date)


def accept_step():
    select = list(stepsListbox.curselection())
    if len(select):
        select = select[len(select) - 1]
        text3.set(initialText + stepsListbox.get(select))


acceptStepButton = Button(root, text="Применить", command=accept_step)

initialText = 'Ваш выбор:\n'
text1 = StringVar()
text1.set(initialText)
text2 = StringVar()
text2.set(initialText)
text3 = StringVar()
text3.set(initialText)
selectedFirstDateLabel = Label(root, textvariable=text1)
selectedSecondDateLabel = Label(root, textvariable=text2)
selectedStepLabel = Label(root, textvariable=text3)

firstHeader.grid(row=0, column=0)
secondHeader.grid(row=0, column=1)
thirdHeader.grid(row=0, column=2)
firstDateListbox.grid(row=1, column=0)
secondDateListbox.grid(row=1, column=1)
stepsListbox.grid(row=1, column=2)
acceptFirstDateButton.grid(row=2, column=0, padx=10, pady=10)
acceptSecondDateButton.grid(row=2, column=1, padx=10, pady=10)
acceptStepButton.grid(row=2, column=2, padx=10, pady=10)
selectedFirstDateLabel.grid(row=3, column=0)
selectedSecondDateLabel.grid(row=3, column=1)
selectedStepLabel.grid(row=3, column=2)
showChartButton.grid(row=4, column=0, columnspan=3)
root.mainloop()






