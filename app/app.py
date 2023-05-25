import time
import redis
from flask import Flask, render_template
import os
from dotenv import load_dotenv
import pandas
import matplotlib.pyplot as plt

load_dotenv() 
cache = redis.Redis(host=os.getenv('REDIS_HOST'), port=6379,  password=os.getenv('REDIS_PASSWORD'))
app = Flask(__name__)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def hello():
    count = get_hit_count()
    return render_template('hello.html', name= "BIPM", count = count)

@app.route('/titanic')
def titanic():
    
    file_path = 'static/titanicData/TitanicTrain.csv'
    df = pandas.read_csv(file_path)
    df_preview = df.head(5)

    return render_template('titanic.html', table=df_preview.to_html(classes='data', index=False))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)

