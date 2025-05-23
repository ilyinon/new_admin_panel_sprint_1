# Greetings traveller

Мы рады, что вы приступили к выполнению 1 задания из курса Middle Python-разработчик.
 
Описание структуры и порядок выполнения проекта:
1. `schema_design` - раздел c материалами для архитектуры базы данных.
2. `movies_admin` - раздел с материалами для панели администратора.
3. `sqlite_to_postgres` - раздел с материалами по миграции данных.

Напоминаем, что все три части работы нужно сдавать на ревью одновременно.

Успехов!

-------
# Выполнение задания
-------
## 0. Подготовительный этап
Для начала необходимо иметь PostgreSQL на хосте. Его можно установить в докер следующей командой:

`
docker run -d \
  --name postgres \
  -p 5432:5432 \
  -v {CHOOSE_WHERE_TO_STORE_FILES}:/var/lib/postgresql/data \
  -e POSTGRES_PASSWORD=123qwe \
  -e POSTGRES_USER=app \
  -e POSTGRES_DB=movies_database  \
  postgres:16
  `

Также установить зависимости из requirements.txt

`
pip install -r requirements.txt
`

## 1. Проектное задание: SQL

Мигрируем схему командой:

`
psql -h 127.0.0.1 -U app -d movies_database -f schema_design/movies_database.ddl
`

## 2. Проектное задаине: панель администратора

Необходимо заполнить файл 

`
.env
`

Запустить django можно следующим способом

`
cd movies_admin/ && python manage.py migrate &&  python3 manage.py runserver
`

После этого django будет доступен на адресе localhost:8000

Не забываем добавить superuser

`
python manage.py createsuperuser
`

## 3. Проектное задание: перенос данных


Для загрузки данных из sqlite в postgresql нужно выполнить команду

`
python sqlite_to_postgres/main.py
`

Для проверки корреткности загрузки нужно запустить файл с тестами, например

`
python -m unittest sqlite_to_postgres/tests/check_consistency.py
`

результатом запуска должен быть вывод 

`
Ran 3 tests in 0.256s
OK
` 

с кодом ноль, что говорит о корректности загрузки данных.