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
StatusCode        : 200
StatusDescription : OK
Content           : <h1>Hello  15!</h1>
RawContent        : HTTP/1.0 200 OK
                    Content-Length: 19
                    Content-Type: text/html; charset=utf-8
                    Date: Thu, 30 Sep 2021 20:24:03 GMT
                    Server: Werkzeug/2.0.1 Python/3.8.11

                    <h1>Hello  15!</h1>
Forms             : {}
Headers           : {[Content-Length, 19], [Content-Type, text/html; charset=utf-8], [Date, Thu, 30 Sep 20
                    21 20:24:03 GMT], [Server, Werkzeug/2.0.1 Python/3.8.11]}
Images            : {}
InputFields       : {}
Links             : {}
ParsedHtml        : mshtml.HTMLDocumentClass
RawContentLength  : 19
