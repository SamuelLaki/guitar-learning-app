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

# Quiz data configuration
quiz_data = [
    {
        "page": 1,
        "chords": [
            {
                "id": "chord1",
                "chord_id": 4,  # Reference to Am chord
                "correctAnswer": "Am"
            },
            {
                "id": "chord2",
                "chord_id": 7,  # Reference to C chord
                "correctAnswer": "C" 
            }
        ],
        "options": ["Am", "E", "C", "D"]
    },
    {
        "page": 2,
        "chords": [
            {
                "id": "chord1",
                "chord_id": 1,  # Reference to A chord
                "correctAnswer": "A"
            },
            {
                "id": "chord2",
                "chord_id": 8,  # Reference to G chord
                "correctAnswer": "G"
            }
        ],
        "options": ["G", "A", "C", "Am"]
    }
]

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/learn')
def learn():
    return render_template('learn.html', chord_items=chord_items)

@app.route('/quiz/<int:page_num>')
def quiz_page(page_num):
    # Find the quiz data for the requested page
    page_data = next((data for data in quiz_data if data["page"] == page_num), None)
    
    # If page doesn't exist, redirect to page 1
    if not page_data:
        if page_num > len(quiz_data):
            return redirect(url_for('quiz_page', page_num=1))
        else:
            # Create a default page if somehow we have a gap
            page_data = {
                "page": page_num,
                "chords": [
                    {"id": "chord1", "chord_id": 4, "correctAnswer": "Am"},
                    {"id": "chord2", "chord_id": 7, "correctAnswer": "C"}
                ],
                "options": ["Am", "E", "C", "D"]
            }
    
    # Enrich the chord data with the actual chord details from chord_items
    for chord in page_data["chords"]:
        chord_item = next((item for item in chord_items if item["id"] == chord["chord_id"]), None)
        if chord_item:
            chord["image"] = chord_item["image"]
    
    return render_template('quiz.html', page_num=page_num, quiz_data=page_data, chord_items=chord_items)

@app.route('/learn/<int:chord_id>')
def chord_detail(chord_id):
    chord_item = next((chord_item for chord_item in chord_items if chord_item["id"] == chord_id), None)
    return render_template('chord_detail.html', requested_chord=chord_item)

@app.route('/chord-reading-basics')
def chord_reading_basics():
    return render_template('chord_reading_basics.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)