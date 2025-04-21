from flask import Flask, request, jsonify, render_template, redirect, url_for, json

app = Flask(__name__)

chord_items = [
    {
        "id": 1,
        "name": "A",
        "image": "https://github.com/SarahNasser576/Sarah_Tesfalem_Samuel_UI-Design_Final-Project/blob/main/images/A_chord_image.jpg?raw=true",
        "audio": "https://github.com/SarahNasser576/Sarah_Tesfalem_Samuel_UI-Design_Final-Project/blob/main/chord_audios/A_chord_audio.mp3?raw=true",
        #"prev": "/",
        #"next": "/learn/2"
    },
    {
        "id": 2,
        "name": "D",
        "image": "https://github.com/SarahNasser576/Sarah_Tesfalem_Samuel_UI-Design_Final-Project/blob/main/images/D_chord_image.jpg?raw=true",
        "audio": "https://github.com/SarahNasser576/Sarah_Tesfalem_Samuel_UI-Design_Final-Project/blob/main/chord_audios/D_chord_audio.mp3?raw=true",
        #"prev": "/",
        #"next": "/learn/2"
    },
    {
        "id": 3,
        "name": "E",
        "image": "https://github.com/SarahNasser576/Sarah_Tesfalem_Samuel_UI-Design_Final-Project/blob/main/images/E_chord_image.jpg?raw=true",
        "audio": "https://github.com/SarahNasser576/Sarah_Tesfalem_Samuel_UI-Design_Final-Project/blob/main/chord_audios/E_chord_audio.mp3?raw=true",
        #"prev": "/",
        #"next": "/learn/2"
    },
    {
        "id": 4,
        "name": "Am",
        "image": "https://github.com/SarahNasser576/Sarah_Tesfalem_Samuel_UI-Design_Final-Project/blob/main/images/Am_chord_image.jpg?raw=true",
        "audio": "https://github.com/SarahNasser576/Sarah_Tesfalem_Samuel_UI-Design_Final-Project/blob/main/chord_audios/Am_chord_audio.mp3?raw=true",
        #"prev": "/",
        #"next": "/learn/2"
    },
    {
        "id": 5,
        "name": "Em",
        "image": "https://github.com/SarahNasser576/Sarah_Tesfalem_Samuel_UI-Design_Final-Project/blob/main/images/Em_chord_image.jpg?raw=true",
        "audio": "https://github.com/SarahNasser576/Sarah_Tesfalem_Samuel_UI-Design_Final-Project/blob/main/chord_audios/Em_chord_audio.mp3?raw=true",
        #"prev": "/",
        #"next": "/learn/2"
    },
    {
        "id": 6,
        "name": "Dm",
        "image": "https://github.com/SarahNasser576/Sarah_Tesfalem_Samuel_UI-Design_Final-Project/blob/main/images/Dm_chord_image.jpg?raw=true",
        "audio": "https://github.com/SarahNasser576/Sarah_Tesfalem_Samuel_UI-Design_Final-Project/blob/main/chord_audios/Dm_chord_audio.mp3?raw=true",
        #"prev": "/",
        #"next": "/learn/2"
    },
    {
        "id": 7,
        "name": "C",
        "image": "https://github.com/SarahNasser576/Sarah_Tesfalem_Samuel_UI-Design_Final-Project/blob/main/images/C_chord_image.jpg?raw=true",
        "audio": "https://github.com/SarahNasser576/Sarah_Tesfalem_Samuel_UI-Design_Final-Project/blob/main/chord_audios/C_chord_audio.mp3?raw=true",
        #"prev": "/",
        #"next": "/learn/2"
    },
    {
        "id": 8,
        "name": "G",
        "image": "https://github.com/SarahNasser576/Sarah_Tesfalem_Samuel_UI-Design_Final-Project/blob/main/images/G_chord_image.jpg?raw=true",
        "audio": "https://github.com/SarahNasser576/Sarah_Tesfalem_Samuel_UI-Design_Final-Project/blob/main/chord_audios/G_chord_audio.mp3?raw=true",
        #"prev": "/",
        #"next": "/learn/2"
    }
]

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/learn')
def learn():
    return render_template('learn.html', chord_items=chord_items)

@app.route('/quiz')
def quiz():
    return render_template('quiz.html')

@app.route('/learn/<int:chord_id>')
def chord_detail(chord_id):
    chord_item = next((chord_item for chord_item in chord_items if chord_item["id"] == chord_id), None)
    return render_template('chord_detail.html', requested_chord=chord_item)

if __name__ == '__main__':
    app.run(debug=True, port=5001)