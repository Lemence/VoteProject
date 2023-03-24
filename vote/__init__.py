from .celery import app as celery_app
import vote.signals

__all__ = ("celery_app",)