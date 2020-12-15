from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy
import redis
from flask_redis import FlaskRedis

db = SQLAlchemy()
# cache = Cache(config={''})
# redis_db = redis.Redis(host='127.0.0.1', port=6379)
redis_db = FlaskRedis()

