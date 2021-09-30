# Лабораторна робота №4

## Виконана робота
- Створено репозиторій та склоновано його
- Встановлено конкретну версію __Python__ `3.8.*` за допомогою утиліти [`pyenv`](https://github.com/pyenv/pyenv)
- Створене віртуальне середовище poetry
- Додано `Flask`
- Реалізовано адресу `api/v1/hello-world-15`, яка відповідає текстом `Hello World 15`
- Запущено проект через WSGI сервер
- Перевірено за допомогою `curl`:
    ```bash
    $ curl -v -XGET http://localhost:5000/api/v1/hello-world-15
    *   Trying 127.0.0.1:5000...
    * TCP_NODELAY set
    * Connected to localhost (127.0.0.1) port 5000 (#0)
    > GET /api/v1/hello-world-15 HTTP/1.1
    > Host: localhost:5000
    > User-Agent: curl/7.68.0
    > Accept: */*
    > 
    * Mark bundle as not supporting multiuse
    < HTTP/1.1 200 OK
    < Date: Tue, 28 Sep 2021 18:34:36 GMT
    < Connection: close
    < Content-Type: text/html; charset=utf-8
    < Content-Length: 19
    < 
    * Closing connection 0
    ```
