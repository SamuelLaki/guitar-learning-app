from flask import Flask, request, jsonify, render_template, redirect, url_for, json

app = Flask(__name__)

chord_items = [
    {"id": 1,
     "chord": "A",
     "image": "https://www.til.co/_next/image?url=%2Fguitar%2Fchords%2FAmajor.png&w=640&q=75"}
]


@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/learn')
def learn():
    return render_template('learn.html')

@app.route('/quiz')
def quiz():
    return render_template('quiz.html')

@app.route('/learn/<chord_name>')
def chord_detail(chord_name):
    return render_template('chord_detail.html', chord=chord_name)

if __name__ == '__main__':
    app.run(debug=True, port=5001)