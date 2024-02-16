from celery import Celery
from celery.schedules import crontab
from datetime import datetime
from app.core.common.commands.console.process_data_command import ProcessData
import config.enviroment as env


app = Celery('tasks', backend=env.CELERY_BROKER_URL, broker=None)


@app.task
def my_task():
    try:
        fecha_actual = datetime.now()
        ProcessData.process_data(fecha_actual.strftime("%Y-%m-%d"))
        print("se ejecutó")
    except Exception as e:
        print(e)

# Set the schedule to run the task every day at 1:00 AM.
app.conf.beat_schedule = {
    'ejecutar-tarea-diaria': {
        'task': 'tasks.my_task',
        'schedule': crontab(hour=1, minute=0),
    },
}
