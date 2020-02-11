import RPi.GPIO as G
G.setmode(G.BOARD)
G.setup(32,G.OUT)
G.setup(31,G.OUT)
G.setup(40,G.OUT)
from flask import Flask
from flask import render_template
app = Flask(__name__)

@app.route('/')
def hello_world():
    #return 'hi'
    return render_template('index.html')

@app.route('/alarmon')
def on_buzzer():
    G.output(31,G.HIGH)
    return 'Intruder alarm is turned on'

@app.route('/alarmoff')
def off_buzzer():
    G.output(31,G.LOW)
    return 'Intruder alarm is turned off'

@app.route('/houselighton')
def on_light():
    G.output(32,G.HIGH)
    return 'Light inside the house is on'

@app.route('/houselightoff')
def off_light():
    G.output(32,G.LOW)
    return 'Light inside the house is off'

@app.route('/cmpdlightoff')
def off_cmpd():
    G.output(40,G.LOW)
    return 'Light on the compound is off'

@app.route('/cmpdlighton')
def on_cmpd():
    G.output(40,G.HIGH)
    return 'Light on the compound is on'

if __name__ == "__main__":
    app.run()
