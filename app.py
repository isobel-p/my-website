from flask import Flask, render_template, abort, send_from_directory

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

@app.route('/tea')
def tea():
    abort(418)

if __name__ == '__main__':
    app.run(debug=True)