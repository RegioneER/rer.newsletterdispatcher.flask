import os

MAIL_SERVER = os.environ.get("RER_NEWSLETTERDISPATCHER_MAIL_SERVER", default="")
SENTRY_DSN = os.environ.get("RER_NEWSLETTERDISPATCHER_SENTRY_DSN", default="")

# NOTE: Redis default port is 6379
REDIS_PORT = os.environ.get("RER_NEWSLETTERDISPATCHER_REDIS_PORT", default=6379)
