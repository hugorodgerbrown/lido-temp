"""
stats.py web app used to generate data for geckoboard.
"""
from flask import Flask, render_template, request

app = Flask(__name__)
app.debug = True


@app.route('/')
def temp():
    return render_template('chart.html', browser=request.user_agent.browser)


if __name__ == '__main__':
    app.run()
