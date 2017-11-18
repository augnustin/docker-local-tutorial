import os
from flask import Flask, request, render_template
from flask_redis import FlaskRedis

app = Flask(__name__)

app.config.update(
  # DB_1_PORT_6379_TCP=tcp://172.17.0.3:6379
  REDIS_URL=os.environ['DB_1_PORT_6379_TCP'].replace('tcp://', 'redis://')
)

redisStore = FlaskRedis(app)

def increment_user_agent_details(key, user_agent):
  namespace = 'hello-'
  value = getattr(user_agent, key)
  counterDict = redisStore.hgetall(namespace+key) or {}
  if value:
    counterDict[value] = int(counterDict.get(value, 0)) + 1
    redisStore.hmset(namespace+key, counterDict)
  return counterDict


@app.route("/")
def hello():
  return render_template('hello.html',
    user_agent = request.user_agent.string,
    platforms = increment_user_agent_details('platform', request.user_agent),
    browsers = increment_user_agent_details('browser', request.user_agent)
  )

app.run(host='0.0.0.0')
