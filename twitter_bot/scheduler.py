from celery import Celery
from celery.schedules import crontab
import os
from dotenv import load_dotenv
from loguru import logger
import sys
from tasks import generate_and_store_tweet_task, post_random_tweet_task

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

TWEET_GENERATION_INTERVAL_HOURS = int(os.getenv('TWEET_GENERATION_INTERVAL_HOURS', 1))
TWEET_POSTING_DELAY_SECONDS = int(os.getenv('TWEET_POSTING_DELAY_SECONDS', 10))
TWEET_POSTING_INTERVAL_HOURS = int(os.getenv('TWEET_POSTING_INTERVAL_HOURS', 24))

# Initialize Celery application
redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
logger.debug(f"Initializing Celery with broker: {redis_url}")
scheduler_app = Celery('tasks', broker=redis_url)

# Schedule tasks
scheduler_app.conf.beat_schedule = {
    'generate-and-store-tweet': {
        'task': 'tasks.generate_and_store_tweet_task',
        'schedule': crontab(hour=f'*/{TWEET_GENERATION_INTERVAL_HOURS}'),
    },
    'post-random-tweet': {
        # Add a delay to ensure generation happens first
        'task': 'tasks.post_random_tweet_task',
        'schedule': crontab(hour=f'*/{TWEET_POSTING_INTERVAL_HOURS}'),
        'options': {'countdown': TWEET_POSTING_DELAY_SECONDS},
    },
}

scheduler_app.conf.timezone = 'UTC'
scheduler_app.conf.broker_connection_retry_on_startup = True
scheduler_app.conf.worker_proc_alive_timeout = 60

# Optional immediate execution for development/testing
if os.getenv('TRIGGER_IMMEDIATE', 'false').lower() == 'true':
    try:
        logger.info("Triggering immediate execution of `generate_and_store_tweet_task`.")
        scheduler_app.send_task('tasks.generate_and_store_tweet_task')
        logger.info(f"Scheduling `post_random_tweet_task` with a {TWEET_POSTING_DELAY_SECONDS}s delay.")
        scheduler_app.send_task('tasks.post_random_tweet_task', countdown=TWEET_POSTING_DELAY_SECONDS)
    except Exception as e:
        logger.error(f"Failed to trigger immediate tasks: {e}")

if __name__ == '__main__':
    scheduler_app.start(['worker', '-B', '--loglevel=info'])
