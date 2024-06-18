# Дипломный проект. Задание 2: API-тесты

## Описание
API-тесты функциональности сайта [**Яндекс Самокат**](https://qa-scooter.praktikum-services.ru/)    

### Технологии (stack)
- Python 3.11
- PyTest
- RestAPI
- Allure

### Запуск тестов

1. Клонировать репозиторий с проектом

2. Перейти в корень проекта

3. Настроить виртуальную среду (virtual environment):
   > `$ python -m venv .venv

4. Запустить virtual environment:
   - Windows
   > `$ .venv\Scripts\activate
   - MacOS/Linux:
   > `$ source .venv/bin/activate
5. Установить зависимости:
    > `$ pip install -r requirements.txt

6. Запуск тестов:
    > `$ python -m pytest .\tests\
   
7. Allure отчеты:
    7.1 Сформировать .json отчёт:
    > `$ python -m pytest .\tests\ --alluredir=allure_results
    7.2 Сформировать .html отчёт:
    > `$ allure serve allure_results

### Покрытие автотестами

***Создание пользователя:***
- [x] создать уникального пользователя;
- [x] создать пользователя, который уже зарегистрирован;
- [x] создать пользователя и не заполнить одно из обязательных полей.

***Логин пользователя:***
- [ ] логин под существующим пользователем,
- [ ] логин с неверным логином и паролем.

***Изменение данных пользователя:***
- [ ] с авторизацией,
- [ ] без авторизации.

***Создание заказа:***
- [ ] с авторизацией,
- [ ] без авторизации,
- [ ] с ингредиентами,
- [ ] без ингредиентов,
- [ ] с неверным хешем ингредиентов.

***Получение заказов конкретного пользователя:***
- [ ] авторизованный пользователь,
- [ ] неавторизованный пользователь.
