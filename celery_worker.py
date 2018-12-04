#!/usr/bin/env python
from config import Config
from app import celery, create_app

app = create_app(config_class=Config)
app.app_context().push()
