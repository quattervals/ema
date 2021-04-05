import ematool
from flask import Flask, render_template, request


app = Flask(__name__)

@app.route('/', methods = ['POST', 'GET'])
def home():
    #run ema on reload button click
    if request.method == "POST":
        ematool.ema()

    return render_template('home.html')

@app.route('/cgrad')
def cgrad():
    return render_template('cgrad.html')

@app.route('/rgrad')
def rgrad():
    return render_template('rgrad.html')



if __name__ == "__main__":

    # app.run(debug=True, host='192.168.0.29')
    app.run(debug=True)