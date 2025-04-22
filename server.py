from flask import Flask, request, jsonify, render_template, redirect, url_for, json, session
import random # Import the random module
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'guitar_chord_quiz_key'  # Secret key for session management

chord_items = [
    {
        "id": 1,
        "name": "A",
        "image": "https://github.com/SarahNasser576/Sarah_Tesfalem_Samuel_UI-Design_Final-Project/blob/main/images/A_chord_image.jpg?raw=true",
        "audio": "https://github.com/SarahNasser576/Sarah_Tesfalem_Samuel_UI-Design_Final-Project/blob/main/chord_audios/A_chord_audio.mp3?raw=true",
        "audio": "https://github.com/SarahNasser576/Sarah_Tesfalem_Samuel_UI-Design_Final-Project/blob/main/chord_audios/A_chord_audio.mp3?raw=true"
    },
    {
        "id": 2,
        "name": "D",
        "image": "https://github.com/SarahNasser576/Sarah_Tesfalem_Samuel_UI-Design_Final-Project/blob/main/images/D_chord_image.jpg?raw=true",
        "audio": "https://github.com/SarahNasser576/Sarah_Tesfalem_Samuel_UI-Design_Final-Project/blob/main/chord_audios/D_chord_audio.mp3?raw=true",
        "audio": "https://github.com/SarahNasser576/Sarah_Tesfalem_Samuel_UI-Design_Final-Project/blob/main/chord_audios/D_chord_audio.mp3?raw=true"
    },
    {
        "id": 3,
        "name": "E",
        "image": "https://github.com/SarahNasser576/Sarah_Tesfalem_Samuel_UI-Design_Final-Project/blob/main/images/E_chord_image.jpg?raw=true",
        "audio": "https://github.com/SarahNasser576/Sarah_Tesfalem_Samuel_UI-Design_Final-Project/blob/main/chord_audios/E_chord_audio.mp3?raw=true",
        "audio": "https://github.com/SarahNasser576/Sarah_Tesfalem_Samuel_UI-Design_Final-Project/blob/main/chord_audios/E_chord_audio.mp3?raw=true"
    },
    {
        "id": 4,
        "name": "Am",
        "image": "https://github.com/SarahNasser576/Sarah_Tesfalem_Samuel_UI-Design_Final-Project/blob/main/images/Am_chord_image.jpg?raw=true",
        "audio": "https://github.com/SarahNasser576/Sarah_Tesfalem_Samuel_UI-Design_Final-Project/blob/main/chord_audios/Am_chord_audio.mp3?raw=true",
        "audio": "https://github.com/SarahNasser576/Sarah_Tesfalem_Samuel_UI-Design_Final-Project/blob/main/chord_audios/Am_chord_audio.mp3?raw=true"
    },
    {
        "id": 5,
        "name": "Em",
        "image": "https://github.com/SarahNasser576/Sarah_Tesfalem_Samuel_UI-Design_Final-Project/blob/main/images/Em_chord_image.jpg?raw=true",
        "audio": "https://github.com/SarahNasser576/Sarah_Tesfalem_Samuel_UI-Design_Final-Project/blob/main/chord_audios/Em_chord_audio.mp3?raw=true",
        "audio": "https://github.com/SarahNasser576/Sarah_Tesfalem_Samuel_UI-Design_Final-Project/blob/main/chord_audios/Em_chord_audio.mp3?raw=true"
    },
    {
        "id": 6,
        "name": "Dm",
        "image": "https://github.com/SarahNasser576/Sarah_Tesfalem_Samuel_UI-Design_Final-Project/blob/main/images/Dm_chord_image.jpg?raw=true",
        "audio": "https://github.com/SarahNasser576/Sarah_Tesfalem_Samuel_UI-Design_Final-Project/blob/main/chord_audios/Dm_chord_audio.mp3?raw=true",
        "audio": "https://github.com/SarahNasser576/Sarah_Tesfalem_Samuel_UI-Design_Final-Project/blob/main/chord_audios/Dm_chord_audio.mp3?raw=true"
    },
    {
        "id": 7,
        "name": "C",
        "image": "https://github.com/SarahNasser576/Sarah_Tesfalem_Samuel_UI-Design_Final-Project/blob/main/images/C_chord_image.jpg?raw=true",
        "audio": "https://github.com/SarahNasser576/Sarah_Tesfalem_Samuel_UI-Design_Final-Project/blob/main/chord_audios/C_chord_audio.mp3?raw=true",
        "audio": "https://github.com/SarahNasser576/Sarah_Tesfalem_Samuel_UI-Design_Final-Project/blob/main/chord_audios/C_chord_audio.mp3?raw=true"
    },
    {
        "id": 8,
        "name": "G",
        "image": "https://github.com/SarahNasser576/Sarah_Tesfalem_Samuel_UI-Design_Final-Project/blob/main/images/G_chord_image.jpg?raw=true",
        "audio": "https://github.com/SarahNasser576/Sarah_Tesfalem_Samuel_UI-Design_Final-Project/blob/main/chord_audios/G_chord_audio.mp3?raw=true",
    }
]

# Quiz data with one chord per page and three options each
quiz_data = [
    {
        "page": 1,
        "chord": {
            "id": "chord1",
            "chord_id": 1,  # Reference to A chord
            "correctAnswer": "A"
        },
        "options": ["A", "C", "D"]
    },
    {
        "page": 2,
        "chord": {
            "id": "chord1",
            "chord_id": 2,  # Reference to D chord
            "correctAnswer": "D"
        },
        "options": ["D", "G", "E"]
    },
    {
        "page": 3,
        "chord": {
            "id": "chord1",
            "chord_id": 3,  # Reference to E chord
            "correctAnswer": "E"
        },
        "options": ["E", "Am", "D"]
    },
    {
        "page": 4,
        "chord": {
            "id": "chord1",
            "chord_id": 4,  # Reference to Am chord
            "correctAnswer": "Am"
        },
        "options": ["Am", "Em", "A"]
    },
    {
        "page": 5,
        "chord": {
            "id": "chord1",
            "chord_id": 5,  # Reference to Em chord
            "correctAnswer": "Em"
        },
        "options": ["Em", "E", "Dm"]
    },
    {
        "page": 6,
        "chord": {
            "id": "chord1",
            "chord_id": 6,  # Reference to Dm chord
            "correctAnswer": "Dm"
        },
        "options": ["Dm", "D", "Am"]
    },
    {
        "page": 7,
        "chord": {
            "id": "chord1",
            "chord_id": 7,  # Reference to C chord
            "correctAnswer": "C"
        },
        "options": ["C", "G", "A"]
    },
    {
        "page": 8,
        "chord": {
            "id": "chord1",
            "chord_id": 8,  # Reference to G chord
            "correctAnswer": "G"
        },
        "options": ["G", "C", "D"]
    }
]

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/learn')
def learn():
    return render_template('learn.html', chord_items=chord_items)

@app.route('/quiz/start')
def start_quiz():
    # Reset the quiz score
    session['quiz_score'] = 0
    session['current_page'] = 1
    return redirect(url_for('quiz_page', page_num=1))

@app.route('/quiz/<int:page_num>')
def quiz_page(page_num):
    # Find the quiz data for the requested page
    # IMPORTANT: Make a copy to avoid modifying the original quiz_data
    page_data_original = next((data for data in quiz_data if data["page"] == page_num), None)
    
    # If page doesn't exist and we've gone through all pages, show results
    if not page_data_original:
        if page_num > len(quiz_data):
            return redirect(url_for('quiz_results'))
        else:
            # Use the first question as a default fallback
            page_data_original = quiz_data[0]
    
    # Make a deep copy to shuffle options without affecting the original list
    page_data = page_data_original.copy()
    page_data['options'] = page_data['options'][:] # Shallow copy of options list is sufficient
    
    # Shuffle the options for this specific request
    if 'options' in page_data:
        random.shuffle(page_data['options'])
    
    # Update current page in session
    session['current_page'] = page_num
    
    # Enrich the chord data with the actual chord details
    chord_item = next((item for item in chord_items if item["id"] == page_data["chord"]["chord_id"]), None)
    if chord_item:
        page_data["chord"]["image"] = chord_item["image"]
    
    total_pages = len(quiz_data)
    return render_template('quiz.html', page_num=page_num, quiz_data=page_data, chord_items=chord_items, total_pages=total_pages)

@app.route('/quiz/submit_answer', methods=['POST'])
def submit_answer():
    data = request.get_json()
    
    user_answer = data.get('answer')
    correct_answer = data.get('correct_answer')
    current_page = session.get('current_page', 1)
    
    is_correct = (user_answer == correct_answer)
    correct_chord_id = None

    # Update the score if answer is correct
    if is_correct:
        session['quiz_score'] = session.get('quiz_score', 0) + 1
    else:
        # Find the ID of the correct chord to allow linking back
        correct_chord_item = next((item for item in chord_items if item["name"] == correct_answer), None)
        if correct_chord_item:
            correct_chord_id = correct_chord_item["id"]
    
    # Return the result including the correct chord ID if wrong
    result = {
        'correct': is_correct,
        'next_page': current_page + 1 if current_page < len(quiz_data) else 'results',
        'correct_chord_id': correct_chord_id # Will be None if correct
    }
    
    return jsonify(result)

@app.route('/quiz/results')
def quiz_results():
    score = session.get('quiz_score', 0)
    total = len(quiz_data)
    return render_template('quiz_results.html', score=score, total=total)

@app.route('/learn/<int:chord_id>')
def chord_detail(chord_id):
    chord_item = next((chord_item for chord_item in chord_items if chord_item["id"] == chord_id), None)
    return render_template('chord_detail.html', requested_chord=chord_item)

@app.route('/chord-reading-basics')
def chord_reading_basics():
    return render_template('chord_reading_basics.html')

@app.route('/log-chord-access', methods=['POST'])
def log_chord_access():
    data = request.get_json()  # Works for jQuery AJAX

    # Fallback if request.json is None (common with sendBeacon)
    if data is None:
        data = json.loads(request.data.decode('utf-8'))

    log_msg = f"User {data['event']} chord ID {data['chord_id']} at {data['timestamp']}"
    if 'duration' in data:
        log_msg += f" (Time spent: {data['duration']})"

    print(log_msg)

    return jsonify({"status": "logged"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5001)