Feature: Пошук
    Щоб дізнатися більше
    Як той що шукає знання
    Я хочу знайти більше інформації

    Scenario: Знайти те що я шукаю
        Припустимо я на сторінці пошуку Google
        Коли я ввожу „42 Coffee Cups“
        І натискаю „Мені пощастить“
        Тоді маю перейти на 42coffeecups.com

    Scenario: Кількість результатів
        Припустимо я на сторінці пошуку Google
        Коли я шукаю "42 Coffee Cups"
        Тоді кількість результатів буде 1450000