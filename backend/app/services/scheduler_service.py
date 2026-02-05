from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
from app.core.config import settings
import pytz


class SchedulerService:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.fetch_job = None

    def start(self, fetch_callback):
        """Start the scheduler with fetch callback."""
        if self.scheduler.running:
            return

        eastern = pytz.timezone('US/Eastern')

        # Schedule for 5am and 5pm Eastern Time
        self.fetch_job = self.scheduler.add_job(
            fetch_callback,
            trigger=CronTrigger(hour='5,17', timezone=eastern),
            id='scheduled_fetch',
            name='Daily fetch at 5am and 5pm ET',
            replace_existing=True
        )

        self.scheduler.start()
        print("Scheduler started. Will fetch at 5am and 5pm Eastern Time.")

    def stop(self):
        """Stop the scheduler."""
        if self.scheduler.running:
            self.scheduler.shutdown()
            print("Scheduler stopped.")

    def trigger_manual_fetch(self, fetch_callback):
        """Trigger an immediate fetch."""
        try:
            fetch_callback()
            return True
        except Exception as e:
            print(f"Error triggering manual fetch: {e}")
            return False
