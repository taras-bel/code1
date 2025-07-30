"""
Celery configuration for background tasks
"""
import os
from celery import Celery
from celery.schedules import crontab

# Celery configuration
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/1")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/2")

# Create Celery app
celery_app = Celery(
    "noa_metrics",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
    include=[
        "tasks.analysis_tasks",
        "tasks.maintenance_tasks"
    ]
)

# Celery configuration
celery_app.conf.update(
    # Task serialization
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    
    # Task routing - используем очередь по умолчанию
    # task_routes={
    #     "tasks.analysis_tasks.*": {"queue": "analysis"},
    #     "tasks.maintenance_tasks.*": {"queue": "maintenance"}
    # },
    
    # Task execution
    task_always_eager=False,  # Set to True for testing
    task_eager_propagates=True,
    
    # Worker configuration
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
    worker_disable_rate_limits=False,
    
    # Result backend configuration
    result_expires=3600,  # 1 hour
    result_persistent=True,
    
    # Beat schedule for periodic tasks
    beat_schedule={
        "clean-expired-cache": {
            "task": "tasks.maintenance_tasks.clean_expired_cache",
            "schedule": crontab(minute="0", hour="*/6"),  # Every 6 hours
        },
        "reset-weekly-limits": {
            "task": "tasks.maintenance_tasks.reset_weekly_rate_limits",
            "schedule": crontab(minute="0", hour="0", day_of_week="1"),  # Every Monday at midnight
        },
        "health-check": {
            "task": "tasks.maintenance_tasks.health_check",
            "schedule": crontab(minute="*/15"),  # Every 15 minutes
        },
        "cleanup-old-files": {
            "task": "tasks.maintenance_tasks.cleanup_old_files",
            "schedule": crontab(minute="0", hour="2"),  # Daily at 2 AM
        },
    },
    
    # Task retry configuration
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    task_remote_tracebacks=True,
    
    # Monitoring
    worker_send_task_events=True,
    task_send_sent_event=True,
)

# Optional: Configure logging
celery_app.conf.update(
    worker_log_format="[%(asctime)s: %(levelname)s/%(processName)s] %(message)s",
    worker_task_log_format="[%(asctime)s: %(levelname)s/%(processName)s][%(task_name)s(%(task_id)s)] %(message)s",
)

if __name__ == "__main__":
    celery_app.start() 