from celery import Celery
from celery.schedules import crontab
from datetime import datetime
from config.logging import setup_logging
from app.core.common.commands.console.process_data_command import ProcessDataConsole
import config.enviroment as env

logger = setup_logging()

app = Celery('tasks', backend=env.CELERY_BROKER_URL, broker=None)


@app.task
def my_task():
    try:
        fecha_actual = datetime.now()
        now_str = fecha_actual.strftime("%Y-%m-%d")
        ProcessDataConsole.process_data(now_str)
        logger.info(f"Celery - Message: {now_str} done!")
    except Exception as e:
        logger.error(f"Celery - Message: {e}")
        print(e)   


# Set the schedule to run the task every day at 1:00 AM.
app.conf.beat_schedule = {
    'ejecutar-tarea-diaria': {
        'task': 'tasks.my_task',
        'schedule': crontab(hour=1, minute=0),
    },
}
