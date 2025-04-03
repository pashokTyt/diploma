# pravo/tasks.py

from celery import shared_task
from celery.utils.log import get_task_logger
import sys
import os

logger = get_task_logger(__name__)

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from parser import parse_orel_npa, check_shit

@shared_task(name="run_parser_task")
def run_parser_task():
    logger.info("Парсер запущен")
    parse_orel_npa()
    check_shit()
    logger.info("Парсер завершил работу")


# celery -A diplom beat -l info

# celery -A diplom worker -l info

# sudo systemctl start redis-server



# git remote add origin https://github.com/pashokTyt/diploma.git
# git branch -M main
# git push -u origin main