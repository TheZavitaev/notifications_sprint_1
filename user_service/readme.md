# Сервис, имитирующий работу AUTH и модуля UGC

Генерит события о регистрации нового юзера и шлет их в сервис нотификации.
Отдает по РЕСТу настройки и персонализированные данные юзера.

Оперирует объектами вида:
```
{
      "id": "39275483-d542-400a-bb7c-6aefa15fbee6",
      "first_name": "Jason",
      "last_name": "Meyer",
      "email": "jason.meyer@example.com",
      "promo_agree": true,
      "category": "active",
      "films_month_count": 4,
      "favourite_genre": "\u0431\u043e\u0435\u0432\u0438\u043a"
    },
```
