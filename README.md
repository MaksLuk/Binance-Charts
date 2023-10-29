# Отображение графиков криптовалют с Binance

### V1
Автоматически сортирует графики по убыванию изменения цены (за 24 часа). Можно изменять таймфрейм графиков.

## Запуск:

1. Запуск сервера на Flask:

    ```sh
    $ cd server
    $ python3 -m venv env
    $ source env/bin/activate
    (env)$ pip install -r requirements.txt
    (env)$ flask run --port=5001 --debug
    ```

    Сервер запустится на [http://localhost:5001](http://localhost:5001)

1. Запуск клиентской части:

    ```sh
    $ cd client
    $ npm install
    $ npm run dev
    ```

    Веб-приложение запустится на [http://localhost:5173](http://localhost:5173)
