# D7. Работа с асинхронными задачами через Celery

Установлены и настроены Celery и Redis.

Файл signals.py переработан таким образом, чтобы он только вызывал задачу celery для рассылки подписчикам уведомлений о новых только что созданных статьях

Создан файл tasks.py, в котором прописана логика двух задач:
1) post_created, что позволяет осуществлять рассылку после создания записи
2) new_posts_for_a_week - осуществляет еженедельную рассылку в понедельник в 8 утра



# D6. Работа с почтой и выполнение задач по расписанию

в settings.py добавлен EMAIL_BACKEND для отображения email РАССЫЛКИ В КОНСОЛИ, а не на реальный почтовый ящик

в настойках яндекс создан пароль приложения eejtdteiyqaapsim

EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_USE_TLS, EMAIL_USE_SSL, DEFAULT_FROM_EMAIL

в accounts/forms.py обновлен код формы отправкой HTML-версии письма

в project/settings.py добавлен SERVER_EMAIL и коллекция ADMINS

accounts/forms.py добавлен код, реализующий рассылку для администратора о регистрации новых пользователей

в settings.py параметру ACCOUNT_EMAIL_VERIFICATION присвоено значение 'mandatory', после регистрации нового пользователя в консоли отображаются 3 письма:

    для администратора о регистрации нового пользователя
    на почту нового пользователя с приветствием
    на почту нового пользователя с просьбой подтвердить почтовый адрес

добавлены и отредактированы шаблоны для писем из рассылки при регистрации base_message.txt и email_confirmation_message.txt

в news/models.py добавлена модель Subscriptions

в views.py добавлена функция представления subscriptions

в news/urls.py добавлен маршрут для функции представления subscriptions

создан файл news/signals.py

в файле news/apps.py добавлен метод ready

в models.py в модели Post поле category переделано под ForeignKey, убрана промежуточная таблица PostCategory для связи ManyToMany

установлен пакет django-apscheduler

в settings.py добавлен "django_apscheduler" в INSTALLED_APPS

создан файл news/management/commands/runapscheduler.py

создан шаблон daily_post.html

# D5. Авторизация и регистрация

в views.py добавлен LoginRequiredMixin и raise_exception = True в классы представлений PostCreate, PostUpdate и PostDelete

создан шаблон 403.html, чтобы отображать страницу 403 для незарегистрированных пользователей

в urls.py пакета конфигураций сайта добавлен маршрут path('accounts/', include('django.contrib.auth.urls'))

создан шаблон templates/registration/login.html

добавлен LOGIN_REDIRECT_URL = "/news" , который позволяет перенаправить авторизованного пользователя на страницу со всеми новостями

для регистрации пользователей создано новое приложение accounts

приложение accounts зарегистрировано в settings.py c помощью 'accounts.apps.AccountsConfig'

в приложении accounts создан файл forms.py

в accounts/views.py создан класс представления SignUp для регистрации пользователей

создан шаблон templates/registration/signup.html

подключены urls приложения accounts в пакете конфигураций сайта newsportal/urls.py

установлен пакет allauth

в settings.py внесены изменения в TEMPLATES, AUTHENTICATION_BACKENDS, INSTALLED_APPS

settings.py внесены ACCOUNT_EMAIL_REQUIRED, ACCOUNT_UNIQUE_EMAIL, ACCOUNT_USERNAME_REQUIRED, ACCOUNT_AUTHENTICATION_METHOD, ACCOUNT_EMAIL_VERIFICATION

в пакете конфигураций сайта в urls.py все маршруты с accounts/ заменены на path("accounts/", include("allauth.urls"))

на сайте в панели администратора изменено Domain name на 127.0.0.1

в админ-панели добавлено социальное приложение YandexApp, через него авторизован новый пользователь novikova-box

в проекте в accounts/forms.py описан класс формы CustomSignupForm

в project/settings.py добавлен ACCOUNT_FORMS

в news/views.py добавлен миксин PermissionRequiredMixin для классов представлений PostCreate, PostUpdate, PostDelete

в шаблоне posts.html (страница со всеми статьями) сделаны ссылки на редактирование и удаление статей для зарегистрированных пользователей

# D4. Фильтры и формы

в views.py в класс представлений PostList(ListView) добавлена строка paginate_by = 10 (отображение не более 10 записей)

в templates/posts.html в блоке контента добавлена постраничная навигация + переход на первую и последнюю страницу

установлен django-filter для фильтрации данных

в INSTALLED_APPS добавлен django_filters

создан файл news/filters.py

создан класс PostFilter, в котором указано, как можно фильтровать данные модели Post

в views.py добавлен класс PostSearch для поиска статей

в news/urls.py связан класс представлений с маршрутом search/

создан шаблон postsearch.html

класс PostFilter из news/filters.py использован в классе представления PostSearch для фильтрации списка статей (по категориям Музыка и Образование можно фильтровать вместе, маршрут http://127.0.0.1:8000/news/search/)

создан файл news/forms.py

описан класс PostForm

создан шаблон post_edit.html

в views.py добавлен новый класс представления PostCreate

в news/urls.py добавлен маршрут 'create/', связанный с классом представления PostCreate (по маршруту http://127.0.0.1:8000/news/create/ можно создать новую статью)

в views.py добавлен класс PostUpdate для редактирования статей

в urls.py добавлен маршрут, связывающий класс PostUpdate c int:pk/update/ (по маршруту http://127.0.0.1:8000/news/25/update/ можно редактировать статью с id=25)

создан шаблон post_delete.html

создан класс представлений PostDelete для удаления статей

в urls.py прописан маршрут int:pk/delete/ (по маршруту http://127.0.0.1:8000/news/25/delete/ можно удалить статью с id=25)

# D3. Представления и шаблоны

в файле admin.py зарегистрированы модели Post и Category для работы в админ панели

в файле views.py прописано представление PostList, которое выводит список статей

создан файл для настройки путей к приложениям news/urls.py

в news/urls.py прописан путь к PostList

в пакете кнфигураций в файле urls.py прописан путь, который автоматически включает все адреса из приложения и добавляет к нему префикс news/

в news/templates создан файл шаблона страницы posts.html

в posts.html прописан код страницы

в news/views.py добавлен класс представлений PostText, сделан импорт DetailView

в news/urls.py добавлен маршрут к классу представлений PostText

создан новый шаблон страницы templates/posttext.html

в шаблоне posts.html в блоке контента создана таблица

в шаблоне posts.html выведен список статей

в базу данных добавлены новые статья и новость

изменен шаблон posttext.html

из модели Post удален метод str

добавлен файл news/templatetags/custom_filters.py

в custom_filters.py записан код фильтра цензур

в posttext.html добавлен фильтр цензуры

# D2. Модели

в models.py oпределены будущие модели Author, Category, Post, PostCategory, Comment

в модели Author определены поля user, user_rating, добавлен импорт User

в модели Category определено поле category_name

в модели Post определены поля author, post_category, time_create, category, title, text, post_rating

в модели PostCategory определены поля для связи с моделями Post и Category

в модели Comment определены поля post, user, text, time_create, comment_rating

в моделях Post и Comment добавлены методы like, dislike

в модели Post добавлен метод preview

в модели Author добавлен метод update_rating, cделан импорт Coalesce и Sum

добавлен метод str в модель Post

добавлен метод str в модель Category

# D1. Знакомство с Django

в settings.py изменен язык админ-панели на русский

в settings.py в INSTALLED_APPS добавлено приложение news.apps.NewsConfig

в settings.py в INSTALLED_APPS добавлены приложения sites и flatpages

определена переменная SITE_ID

в urls.py добавлена ссылка для доступа к плоским страницам, добавлен импорт include

в settings.py дополнен список MIDDLEWARE

создан файл шаблона newsportal/templates/flatpages/default.html

в settings.py отредактирована коллекция TEMPLATES, добавлен импорт os

добавлена дирректория newsportal/static, в нее добавлен файл css/styles.css

в default.html добавлен код страницы

в settings.py добавлен STATICFILES_DIRS

в default.html подгружены стили с помощью {% load static %}

в default.html удалена строка, отвечающая за иконку

в default.html изменена строка, отвечающая за подгрузку стилей

в default.html заменен блок Page content, в строках с "Start Bootstrap" сделана замена на "Новостной портал"

в default.html отредактирован блок Responsive navbar
