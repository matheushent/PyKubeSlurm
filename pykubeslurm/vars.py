"""Core module for defining variables use accros the app"""
from datetime import datetime


# Record the time in which the APP has started to avoid duplicate resource creation on k8s
APP_STARTED_AT = datetime.now()