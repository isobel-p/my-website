from flask import Flask, render_template, abort, send_from_directory, redirect
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from dotenv import load_dotenv
import os

class Contact(FlaskForm):
    name = StringField('name', validators=[DataRequired()])

app = Flask(__name__)
load_dotenv()
app.config['SECRET_KEY'] = "Hello123"

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = Contact()
    if form.validate_on_submit():
        name = form.name.data
        with open("test", "a") as file:
            file.write(name + "\n")
        return redirect('/success')
    return render_template("contact.html", form=form)

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

@app.route('/418')
def tea():
    abort(418)

if __name__ == '__main__':
    app.run(debug=True)