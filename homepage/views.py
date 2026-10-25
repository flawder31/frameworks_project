from django.http import HttpResponse


def page(title, content):
    """Общий HTML-каркас для всех страниц с подключением Bootstrap."""
    bootstrap = (
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3"
        "/dist/css/bootstrap.min.css"
    )
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <link rel="stylesheet" href="{bootstrap}">
</head>
<body class="bg-light">
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark mb-4">
        <div class="container">
            <a class="navbar-brand" href="/">Сервис счетчиков</a>
            <div class="navbar-nav">
                <a class="nav-link" href="/">Главная</a>
                <a class="nav-link" href="/meters/">Счетчики</a>
                <a class="nav-link" href="/readings/">Показания</a>
            </div>
        </div>
    </nav>
    <main class="container bg-white p-4 rounded shadow-sm">
        {content}
    </main>
</body>
</html>"""


def index(request):
    """Главная страница."""
    content = """
    <h1 class="display-4">Сервис учета показаний</h1>
    <p class="lead">Приложение для учета потребления ресурсов по счетчикам.</p>
    <hr class="my-4">
    <p>Выберите раздел:</p>
    <a href="/meters/" class="btn btn-primary me-2">Счетчики</a>
    <a href="/readings/" class="btn btn-secondary">Показания</a>
    """
    return HttpResponse(page("Главная - Сервис счетчиков", content))


def page_not_found(request, exception):
    """Обработчик ошибки 404."""
    content = """
    <h1 class="text-danger">404 - Страница не найдена</h1>
    <p>Проверьте адрес или вернитесь на главную.</p>
    <a href="/" class="btn btn-primary">На главную</a>
    """
    return HttpResponse(page("404 - Не найдено", content), status=404)
