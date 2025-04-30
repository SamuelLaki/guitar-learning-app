from flask import Flask, request, jsonify, render_template, redirect, url_for, session, abort, json
import random  # Import the random module
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'guitar_chord_quiz_key'  # Secret key for session management

chord_items = [
    {
        "id": 1,
        "name": "A",
        "image": "https://github.com/SarahNasser576/Sarah_Tesfalem_Samuel_UI-Design_Final-Project/blob/main/images/A_chord_image.jpg?raw=true",
        "audio": "https://github.com/SarahNasser576/Sarah_Tesfalem_Samuel_UI-Design_Final-Project/blob/main/chord_audios/A_chord_audio.mp3?raw=true"
    },
    {
        "id": 2,
        "name": "D",
        "image": "https://github.com/SarahNasser576/Sarah_Tesfalem_Samuel_UI-Design_Final-Project/blob/main/images/D_chord_image.jpg?raw=true",
        "audio": "https://github.com/SarahNasser576/Sarah_Tesfalem_Samuel_UI-Design_Final-Project/blob/main/chord_audios/D_chord_audio.mp3?raw=true"
    },
    {
        "id": 3,
        "name": "E",
        "image": "https://github.com/SarahNasser576/Sarah_Tesfalem_Samuel_UI-Design_Final-Project/blob/main/images/E_chord_image.jpg?raw=true",
        "audio": "https://github.com/SarahNasser576/Sarah_Tesfalem_Samuel_UI-Design_Final-Project/blob/main/chord_audios/E_chord_audio.mp3?raw=true"
    },
    {
        "id": 4,
        "name": "Am",
        "image": "https://github.com/SarahNasser576/Sarah_Tesfalem_Samuel_UI-Design_Final-Project/blob/main/images/Am_chord_image.jpg?raw=true",
        "audio": "https://github.com/SarahNasser576/Sarah_Tesfalem_Samuel_UI-Design_Final-Project/blob/main/chord_audios/Am_chord_audio.mp3?raw=true"
    },
    {
        "id": 5,
        "name": "Em",
        "image": "https://github.com/SarahNasser576/Sarah_Tesfalem_Samuel_UI-Design_Final-Project/blob/main/images/Em_chord_image.jpg?raw=true",
        "audio": "https://github.com/SarahNasser576/Sarah_Tesfalem_Samuel_UI-Design_Final-Project/blob/main/chord_audios/Em_chord_audio.mp3?raw=true"
    },
    {
        "id": 6,
        "name": "Dm",
        "image": "https://github.com/SarahNasser576/Sarah_Tesfalem_Samuel_UI-Design_Final-Project/blob/main/images/Dm_chord_image.jpg?raw=true",
        "audio": "https://github.com/SarahNasser576/Sarah_Tesfalem_Samuel_UI-Design_Final-Project/blob/main/chord_audios/Dm_chord_audio.mp3?raw=true"
    },
    {
        "id": 7,
        "name": "C",
        "image": "https://github.com/SarahNasser576/Sarah_Tesfalem_Samuel_UI-Design_Final-Project/blob/main/images/C_chord_image.jpg?raw=true",
        "audio": "https://github.com/SarahNasser576/Sarah_Tesfalem_Samuel_UI-Design_Final-Project/blob/main/chord_audios/C_chord_audio.mp3?raw=true"
    },
    {
        "id": 8,
        "name": "G",
        "image": "https://github.com/SarahNasser576/Sarah_Tesfalem_Samuel_UI-Design_Final-Project/blob/main/images/G_chord_image.jpg?raw=true",
        "audio": "https://github.com/SarahNasser576/Sarah_Tesfalem_Samuel_UI-Design_Final-Project/blob/main/chord_audios/G_chord_audio.mp3?raw=true"
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

# Make chord_items available in all templates
@app.context_processor
def inject_chords():
    return dict(chord_items=chord_items)

@app.route('/')
def homepage():
    # Initialize completed_chords in session if not already there
    if 'completed_chords' not in session:
        session['completed_chords'] = []
    return render_template('homepage.html')

@app.route('/learn')
def learn():
    # Initialize completed_chords in session if not already there
    if 'completed_chords' not in session:
        session['completed_chords'] = []
    return render_template('learn.html', chord_items=chord_items)

@app.route('/quiz/start')
def start_quiz():
    last_page = session.get('last_quiz_page')
    total_pages = len(quiz_data)

    # Check if there's a valid last page stored and it's not beyond the last question
    if last_page and 0 < last_page <= total_pages:
        # Resume from the last page, score is already maintained
        # max_quiz_page_reached should already be in session from previous attempt
        return redirect(url_for('quiz_page', page_num=last_page))
    else:
        # Start fresh: Reset score, last page, and max page reached
        session['quiz_score'] = 0
        session['last_quiz_page'] = 1 # Start at page 1
        session['current_page'] = 1 # Ensure current_page is also reset
        session['max_quiz_page_reached'] = 1 # Initialize max page reached
        return redirect(url_for('quiz_page', page_num=1))

@app.route('/quiz/<int:page_num>')
def quiz_page(page_num):
    page_data_original = next((data for data in quiz_data if data["page"] == page_num), None)
    if not page_data_original:
        session.pop('last_quiz_page', None)
        session.pop('max_quiz_page_reached', None) # Clear max page on invalid access
        if page_num > len(quiz_data):
             return redirect(url_for('quiz_results'))
        else:
             return redirect(url_for('start_quiz'))

    page_data = page_data_original.copy()
    page_data['options'] = page_data['options'][:]
    random.shuffle(page_data['options'])

    # Store the current page number for potential resume
    session['last_quiz_page'] = page_num
    session['current_page'] = page_num

    # Update max page reached if current page is higher
    max_reached = session.get('max_quiz_page_reached', 1)
    if page_num > max_reached:
        session['max_quiz_page_reached'] = page_num
        max_reached = page_num # Update local variable for percentage calculation

    # ... existing chord image logic ...
    chord_item = next((item for item in chord_items if item["id"] == page_data["chord"]["chord_id"]), None)
    if chord_item:
        page_data["chord"]["image"] = chord_item["image"]

    total_pages = len(quiz_data)
    # Calculate percentage based on pages *before* the current one for initial display
    # (Progress reflects completed questions)
    quiz_percent_complete = round(((page_num - 1) / total_pages) * 100) if total_pages > 0 and page_num > 1 else 0

    return render_template('quiz.html',
                           page_num=page_num,
                           quiz_data=page_data,
                           chord_items=chord_items,
                           total_pages=total_pages,
                           quiz_percent_complete=quiz_percent_complete,
                           max_quiz_page_reached=max_reached) # Pass max_reached to template

@app.route('/quiz/submit_answer', methods=['POST'])
def submit_answer():
    data = request.get_json()
    user_answer = data.get('answer')
    correct_answer = data.get('correct_answer')
    current_page = session.get('current_page', 1)
    is_correct = (user_answer == correct_answer)
    correct_chord_id = None
    if is_correct:
        session['quiz_score'] = session.get('quiz_score', 0) + 1
    else:
        correct_chord_item = next((item for item in chord_items if item["name"] == correct_answer), None)
        if correct_chord_item:
            correct_chord_id = correct_chord_item["id"]
    result = {
        'correct': is_correct,
        'next_page': current_page + 1 if current_page < len(quiz_data) else 'results',
        'correct_chord_id': correct_chord_id
    }
    return jsonify(result)

@app.route('/quiz/results')
def quiz_results():
    score = session.get('quiz_score', 0)
    total = len(quiz_data)
    # Clear all quiz-related session data
    session.pop('last_quiz_page', None)
    session.pop('quiz_score', None)
    session.pop('current_page', None)
    session.pop('max_quiz_page_reached', None) # Clear max page reached
    return render_template('quiz_results.html', score=score, total=total)

@app.route('/learn/<int:chord_id>')
def chord_detail(chord_id):
    chord_item = next((item for item in chord_items if item["id"] == chord_id), None)
    if not chord_item:
        abort(404)
    
    # Initialize completed_chords in session if not already there
    if 'completed_chords' not in session:
        session['completed_chords'] = []
    
    # Mark this chord as completed/viewed
    if chord_id not in session['completed_chords']:
        session['completed_chords'].append(chord_id)
        # Convert to list for modifiability then back to ensure session updates properly
        completed_chords = list(session['completed_chords'])
        session['completed_chords'] = completed_chords
    
    # Calculate progress based on completed chords
    total_chords = len(chord_items)
    completed_count = len(session['completed_chords'])
    percent_complete = round((completed_count / total_chords) * 100)
    
    # Get the current chord's position for navigation
    current_chord = next((i + 1 for i, c in enumerate(chord_items) if c["id"] == chord_id), 1)
    
    return render_template('chord_detail.html',
                           requested_chord=chord_item,
                           current_chord=current_chord,
                           total_chords=total_chords,
                           percent_complete=percent_complete,
                           completed_chords=session['completed_chords'])

@app.route('/chord-reading-basics')
def chord_reading_basics():
    return render_template('chord_reading_basics.html')

@app.route('/log-chord-access', methods=['POST'])
def log_chord_access():
    data = request.get_json() or json.loads(request.data.decode('utf-8'))
    
    # Only print log message if it's NOT a 'viewed' or 'completed' event
    if data['event'] not in ['viewed', 'completed']:
        log_msg = f"User {data['event']} {data['chord_name']} chord at {data['timestamp']}"
        if 'duration' in data:
            log_msg += f" (Time spent: {data['duration']})"
        print(log_msg)
    
    # If this is a view or completion event, add the chord to completed chords
    if data['event'] in ['viewed', 'completed']:
        chord_id = next((c['id'] for c in chord_items if c['name'] == data['chord_name']), None)
        if chord_id and 'completed_chords' in session and chord_id not in session['completed_chords']:
            completed_chords = list(session['completed_chords'])
            completed_chords.append(chord_id)
            session['completed_chords'] = completed_chords
    
    return jsonify({"status": "logged"}), 200

@app.route('/reset-progress', methods=['POST'])
def reset_progress():
    """Reset user's completed chords progress"""
    session['completed_chords'] = []
    return jsonify({"status": "reset successful"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5001)