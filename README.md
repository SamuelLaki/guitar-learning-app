# Guitar Chord Learning Application

This is a web application designed to help users learn and practice guitar chords through interactive lessons and quizzes.

Made with Tesfalem Eshetu and Sarah Nasser

## Features

- Interactive chord learning interface
- Chord visualization with images
- Audio playback for each chord
- Quiz mode to test your knowledge
- Progress tracking

## Requirements

- Python 3.6 or higher
- Flask

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-directory>
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
