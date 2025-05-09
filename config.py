# -*- coding: utf-8 -*-
import os

MAIL_SERVER = os.environ.get("RER_NEWSLETTERDISPATCHER_MAIL_SERVER", default="")
MAIL_PORT = os.environ.get("RER_NEWSLETTERDISPATCHER_MAIL_PORT", default=25)
MAIL_USERNAME = os.environ.get("RER_NEWSLETTERDISPATCHER_MAIL_USERNAME", default="")
MAIL_PASSWORD = os.environ.get("RER_NEWSLETTERDISPATCHER_MAIL_PASSWORD", default="")
MAIL_TIMEOUT = os.environ.get("RER_NEWSLETTERDISPATCHER_MAIL_TIMEOUT", default=120)

SENTRY_DSN = os.environ.get("RER_NEWSLETTERDISPATCHER_SENTRY_DSN", default="")
# NOTE: Redis default port is 6379
REDIS_PORT = os.environ.get("RER_NEWSLETTERDISPATCHER_REDIS_PORT", default="6379")
