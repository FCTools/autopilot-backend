from web.backend.celery import app
from bot_manager.services.helpers.condition_parser import ConditionParser


@app.task
def print_hello():
    with open('something.txt', 'w', encoding='utf-8') as file:
        file.write(str(ConditionParser.check_sites('(((revenue < 50) AND (profit < 0)) OR (cost > 100))',
                                                   1379)))

