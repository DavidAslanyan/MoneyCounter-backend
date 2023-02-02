from dotenv import load_dotenv
import os
import redis

class ApplicationConfig:
  SECRET_KEY = os.urandom(32)
  SQLALCHEMY_TRACK_MODIFICATONS = False
  SQLALCHEMY_ECHO = True
  SQLALCHEMY_DATABASE_URI = "MY-DATABASE-CREDENTIALS"

  SESSION_TYPE = "redis"
  SESSION_PERMANENT = False
  SESSION_USE_SIGNER = True
  SESSION_REDIS = redis.from_url("MY-REDIS-DATABASE-CREDENTIALS")