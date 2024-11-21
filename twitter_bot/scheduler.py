from celery import Celery
from celery.schedules import crontab
import os
from dotenv import load_dotenv
from loguru import logger
import sys

load_dotenv()

logger.remove()
logger.add(
    "../logs/scheduler.log",
    rotation="500 MB",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
)
logger.add(
    sys.stdout,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    level="DEBUG"
)

CALLER_INTERVAL_MINUTES = int(os.getenv('CALLER_INTERVAL_MINUTES', 7))

# Initialize Celery application
redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
logger.debug(f"Initializing Celery with broker: {redis_url}")
scheduler_app = Celery('tasks', broker=redis_url)

from tasks import post_tweet_task

scheduler_app.conf.beat_schedule = {
    'post-tweet-every-x-minutes': {
        'task': 'tasks.post_tweet_task',
        'schedule': crontab(minute=f'*/{CALLER_INTERVAL_MINUTES}'),
    },
}

scheduler_app.conf.timezone = 'UTC'
scheduler_app.conf.broker_connection_retry_on_startup = True
scheduler_app.conf.worker_proc_alive_timeout = 60

if os.getenv('TRIGGER_IMMEDIATE', 'false').lower() == 'true':
    try:
        logger.info("Triggering immediate execution of `post_tweet_task`.")
        scheduler_app.send_task('tasks.post_tweet_task')
    except Exception as e:
        logger.error(f"Failed to trigger immediate task: {e}")

if __name__ == '__main__':
    scheduler_app.start(['worker', '-B', '--loglevel=info'])
