# ChordTutor


ChordTutor is a Guitar Chord Learning web application designed to help users learn and practice guitar chords through interactive lessons and quizzes.

Made with Tesfalem Eshetu and Sarah Nasser

## Features

- Interactive chord learning interface
- Chord visualization with images
- Audio playback for each chord
- Drag and Drop quiz mode to test your knowledge
- Progress tracking

<img width="1439" height="693" alt="Screenshot 2025-07-18 at 8 45 44 PM" src="https://github.com/user-attachments/assets/9e347c02-b24e-49ad-b86e-c4ada838b1bc" />

<img width="1435" height="689" alt="Screenshot 2025-07-18 at 8 47 15 PM" src="https://github.com/user-attachments/assets/fb036d6b-fc99-464e-a62a-2253eaf5e227" />

<img width="1432" height="694" alt="Screenshot 2025-07-18 at 8 46 32 PM" src="https://github.com/user-attachments/assets/68d41a2f-d5c6-4fff-840b-fa748344ddca" />


## Requirements

- Python 3.6 or higher
- Flask

## Installation

1. Clone the repository:
```bash
git clone https://github.com/SamuelLaki/guitar-learning-app.git
cd guitar-learning-app
```

2. Create a virtual environment (optional but recommended):
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install flask
```

## Running the Application Locally

1. Start the Flask development server:
```bash
python server.py
```

2. Open your web browser and navigate to:
```
http://127.0.0.1:5000/
```

## Project Structure

- `server.py` - Main Flask application file
- `templates/` - HTML templates
- `static/` - Static files (CSS, JavaScript, images, audio)

## How to Use

1. Visit the homepage to get started
2. Navigate to the "Learn" section to explore different chords
3. Use the Quiz feature to test your knowledge
4. Track your progress as you learn
