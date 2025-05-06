# updated 9:35
from flask import Flask, request, jsonify, render_template, redirect, url_for, session, abort, json
import random  # Import the random module
from datetime import datetime
import os # Import os module

app = Flask(__name__)
# Load secret key from environment variable or use a default (change default for production!)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'default-dev-key-change-me')

chord_items = [
    {
        "id": 1,
        "name": "A",
        "image": "/static/images/A_chord_image.jpg",
        "audio": "/static/chord_audios/A_chord_audio.mp3"
    },
    {
        "id": 2,
        "name": "D",
        "image": "/static/images/D_chord_image.jpg",
        "audio": "/static/chord_audios/D_chord_audio.mp3"
    },
    {
        "id": 3,
        "name": "E",
        "image": "/static/images/E_chord_image.jpg",
        "audio": "/static/chord_audios/E_chord_audio.mp3"
    },
    {
        "id": 4,
        "name": "Am",
        "image": "/static/images/Am_chord_image.jpg",
        "audio": "/static/chord_audios/Am_chord_audio.mp3"
    },
    {
        "id": 5,
        "name": "Em",
        "image": "/static/images/Em_chord_image.jpg",
        "audio": "/static/chord_audios/Em_chord_audio.mp3"
    },
    {
        "id": 6,
        "name": "Dm",
        "image": "/static/images/Dm_chord_image.jpg",
        "audio": "/static/chord_audios/Dm_chord_audio.mp3"
    },
    {
        "id": 7,
        "name": "C",
        "image": "/static/images/C_chord_image.jpg",
        "audio": "/static/chord_audios/C_chord_audio.mp3"
    },
    {
        "id": 8,
        "name": "G",
        "image": "/static/images/G_chord_image.jpg",
        "audio": "/static/chord_audios/G_chord_audio.mp3"
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

@app.before_request
def initialize_session():
    # Initialize completed_chords in session if not already there before each request
    if 'completed_chords' not in session:
        session['completed_chords'] = []

@app.route('/')
def homepage():
    # 'completed_chords' is now initialized by before_request
    return render_template('homepage.html', active_page='home')

@app.route('/learn')
def learn():
    # 'completed_chords' is now initialized by before_request
    return render_template('learn.html', chord_items=chord_items, active_page='learn')

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
        session['quiz_score'] = 0 # Keep for now, calculate final from answers
        session['last_quiz_page'] = 1 # Start at page 1
        session['current_page'] = 1 # Ensure current_page is also reset
        session['max_quiz_page_reached'] = 1 # Initialize max page reached
        session['quiz_shuffled_options'] = {} # Initialize storage for shuffled options
        session['quiz_answers'] = {} # Initialize storage for user answers
        session.modified = True # Ensure the new dicts are saved
        return redirect(url_for('quiz_page', page_num=1))

@app.route('/quiz/<int:page_num>')
def quiz_page(page_num):
    page_data_original = next((data for data in quiz_data if data["page"] == page_num), None)
    if not page_data_original:
        session.pop('last_quiz_page', None)
        session.pop('max_quiz_page_reached', None) # Clear max page on invalid access
        session.pop('quiz_shuffled_options', None) # Clear shuffled options on invalid access
        if page_num > len(quiz_data):
             return redirect(url_for('quiz_results'))
        else:
             return redirect(url_for('start_quiz'))

    # Ensure quiz_shuffled_options exists in session
    if 'quiz_shuffled_options' not in session:
        session['quiz_shuffled_options'] = {}
        session.modified = True

    page_data = page_data_original.copy()

    # Check if options for this page were already shuffled and stored
    shuffled_options_map = session.get('quiz_shuffled_options', {})
    if str(page_num) in shuffled_options_map: # Use string key for JSON compatibility
        page_data['options'] = shuffled_options_map[str(page_num)]
    else:
        # Shuffle options only if not already done for this session/attempt
        current_options = page_data['options'][:] # Create a copy
        random.shuffle(current_options)
        page_data['options'] = current_options
        # Store the shuffled options
        session['quiz_shuffled_options'][str(page_num)] = current_options
        session.modified = True

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
    # Updated to use max_reached to prevent progress bar decrease on back navigation
    quiz_percent_complete = round(((max_reached - 1) / total_pages) * 100) if total_pages > 0 and max_reached > 1 else 0

    return render_template('quiz.html',
                           page_num=page_num,
                           quiz_data=page_data,
                           chord_items=chord_items,
                           total_pages=total_pages,
                           quiz_percent_complete=quiz_percent_complete,
                           max_quiz_page_reached=max_reached,
                           active_page='quiz') # Pass active page indicator

@app.route('/quiz/submit_answer', methods=['POST'])
def submit_answer():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid request"}), 400

    user_answer = data.get('answer')
    correct_answer = data.get('correct_answer')
    current_page = session.get('current_page')

    if user_answer is None or correct_answer is None or current_page is None:
        return jsonify({"error": "Missing data in request or session"}), 400

    is_correct = (user_answer == correct_answer)
    correct_chord_id = None

    # Store the answer details instead of just incrementing score
    if 'quiz_answers' not in session:
        session['quiz_answers'] = {}

    session['quiz_answers'][str(current_page)] = {
        'user_answer': user_answer,
        'correct_answer': correct_answer,
        'is_correct': is_correct
    }

    if not is_correct:
        # Find the ID of the correct chord if the answer was wrong
        correct_chord_item = next((item for item in chord_items if item["name"] == correct_answer), None)
        if correct_chord_item:
            correct_chord_id = correct_chord_item["id"]

    session.modified = True # Ensure answer is saved

    result = {
        'correct': is_correct,
        'next_page': current_page + 1 if current_page < len(quiz_data) else 'results',
        'correct_chord_id': correct_chord_id
    }
    return jsonify(result)

@app.route('/quiz/results')
def quiz_results():
    # Get the stored answers, default to empty dict if not found
    quiz_answers = session.get('quiz_answers', {})
    total_questions_in_quiz = len(quiz_data)

    # Calculate score from the stored answers
    score = sum(1 for answer in quiz_answers.values() if answer.get('is_correct'))

    # Prepare data for the template, including ALL quiz questions and their status
    quiz_review_data = []
    for question_data in quiz_data:
        page_num = question_data["page"]
        page_num_str = str(page_num)
        chord_id = question_data["chord"]["chord_id"]
        correct_answer_name = question_data["chord"]["correctAnswer"]
        
        # Find the corresponding chord details (name, image)
        chord_info = next((c for c in chord_items if c["id"] == chord_id), None)
        if not chord_info:
            # Handle case where chord_id might be invalid (though unlikely)
            continue 
            
        # Check if this question was answered
        answer_details = quiz_answers.get(page_num_str)
        
        status = 'unanswered' # Default status
        user_answer = None
        is_correct = None
        if answer_details:
            is_correct = answer_details.get('is_correct')
            user_answer = answer_details.get('user_answer')
            status = 'correct' if is_correct else 'incorrect'
            
        quiz_review_data.append({
            'page': page_num,
            'chord_id': chord_id,
            'chord_name': chord_info['name'],
            'chord_image': chord_info['image'],
            'status': status, # 'correct', 'incorrect', or 'unanswered'
            'user_answer': user_answer,
            'correct_answer': correct_answer_name, 
        })

    # Clear all quiz-related session data *after* retrieving needed info
    session.pop('last_quiz_page', None)
    session.pop('quiz_score', None) # Remove old score tracking
    session.pop('current_page', None)
    session.pop('max_quiz_page_reached', None)
    session.pop('quiz_shuffled_options', None)
    session.pop('quiz_answers', None) # Clear the stored answers

    return render_template('quiz_results.html', 
                           score=score, 
                           total=total_questions_in_quiz, 
                           quiz_review_data=quiz_review_data,
                           active_page='quiz') # Pass active page indicator

@app.route('/learn/<int:chord_id>')
def chord_detail(chord_id):
    chord_item = next((item for item in chord_items if item["id"] == chord_id), None)
    if not chord_item:
        abort(404)

    # 'completed_chords' is guaranteed to exist by before_request

    # Mark this chord as completed/viewed
    if chord_id not in session['completed_chords']:
        session['completed_chords'].append(chord_id)
        # Make sure Flask detects the change to the mutable list
        session.modified = True

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
                           completed_chords=session['completed_chords'],
                           active_page='learn') # Pass active page indicator

@app.route('/chord-reading-basics')
def chord_reading_basics():
    return render_template('chord_reading_basics.html', active_page='learn') # Consider this part of 'learn'

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
        # Check existence of 'completed_chords' (guaranteed by before_request)
        if chord_id and chord_id not in session['completed_chords']:
            session['completed_chords'].append(chord_id)
            # Make sure Flask detects the change to the mutable list
            session.modified = True
    
    return jsonify({"status": "logged"}), 200

@app.route('/reset-progress', methods=['POST'])
def reset_progress():
    """Reset user's progress by clearing the entire session."""
    session.clear()
    return jsonify({"status": "reset successful"}), 200

if __name__ == '__main__':
    # For production, set the FLASK_SECRET_KEY environment variable
    # and potentially turn off debug mode.
    app.run(debug=True, port=5001)