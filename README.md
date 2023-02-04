# API "YaMDb"
## Описание проекта
API для социальной сети блогеров YaMDb, где пользователи могут оставлять отзывы на произведения.
Произведения делятся на категории, такие как «Книги», «Фильмы», «Музыка».
Произведению может быть присвоен жанр из списка предустановленных.
Пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.


## Системные требования
- Python 3.7+
- Linux, Windows, macOS

## Технологии
- Python 3.7 
- Django 2.2.16
- DRF 3.12.4
- JWT

### Пользовательские роли

* **Аноним** — может просматривать описания произведений, читать отзывы и комментарии.
* **Аутентифицированный пользователь (user)**— может читать всё, как и Аноним, дополнительно может публиковать отзывы и ставить рейтинг произведениям (фильмам/книгам/песенкам), может комментировать чужие отзывы и ставить им оценки; может редактировать и удалять свои отзывы и комментарии.
* **Модератор (moderator)** — те же права, что и у Аутентифицированного пользователя плюс право удалять любые отзывы и комментарии.
* **Администратор (admin)** — полные права на управление проектом и всем его содержимым. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.
* **Администратор Django** — те же права, что и у роли Администратор.


## Возможности API
- Добавлять произведения, категории и жанры может только администратор.
- Авторизованным пользователям доступно:
  - создавать, редактировать и удалять записи в социальной сети Yatube
  - просматривать и комментировать записи других авторов
  - подписываться на других авторов
- Анонимным пользователям доступно:
  - чтение чужих записей и комментариев

### Ресурсы API YaMDb
* Ресурс AUTH: аутентификация.
* Ресурс USERS: пользователи.
* Ресурс TITLES: произведения, к которым пишут отзывы (определённый фильм, книга или песенка).
* Ресурс CATEGORIES: категории (типы) произведений («Фильмы», «Книги», «Музыка»).
* Ресурс GENRES: жанры произведений. Одно произведение может быть привязано к нескольким жанрам.
* Ресурс REVIEWS: отзывы на произведения. Отзыв привязан к определённому произведению.
* Ресурс COMMENTS: комментарии к отзывам. Комментарий привязан к определённому отзыву.


### Запуск приложения

Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```

```
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```

### Спецификация API будет доступна после запуска проекта по адресу
```
http://localhost:8000/redoc/
```

#### Авторы
Паутова Татьяна, Магомед Мулаев, Антов Андреев