from web.backend.celery import app


@app.task
def print_hello():
    with open('something.txt', 'w', encoding='utf-8') as file:
        file.write('Hello everyone!')

