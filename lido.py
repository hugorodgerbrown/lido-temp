"""
stats.py web app used to generate data for geckoboard.
"""
from flask import Flask, render_template

app = Flask(__name__)
app.debug = True


@app.route('/')
def temp():
    return render_template('chart.html')


if __name__ == '__main__':
    app.run()
