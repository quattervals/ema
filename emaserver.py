import ematool
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/cema')
def cema():
    return render_template('cema.html')

@app.route('/rema')
def rema():
    return render_template('rema.html')



if __name__ == "__main__":

    #ematool.ema()
    app.run(debug=True, host='192.168.0.29')
    # app.run(debug=True)