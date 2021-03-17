from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/about')
def about():
    return render_template('about.html') #render_template() expects html files to be in 'templates' directory


@app.route('/ema') #this adds a route
def ema():
    return render_template('ema.html')

# an url like http://127.0.0.1:5000/brudi uses the variable 'name' in the associated html file
@app.route('/<username>')
def hello_user(username=None):
    return render_template('about.html', name=username)


if __name__ == "__main__":
    app.run(debug=True, host='192.168.0.29')