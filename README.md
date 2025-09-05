# Quiz Website

A simple quiz website built with Django, featuring multiple categories and difficulty levels.

## Features

- Multiple quiz categories: IT, Computer Fundamentals, Maths, Computer Networking, OS
- Three difficulty levels per category: Easy, Medium, Hard
- Timed quizzes with automatic submission
- Detailed assessment with strengths and areas for improvement
- Responsive design with clean UI

## Setup Instructions

1. Create a virtual environment and activate it:
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
source venv/bin/activate  # On Unix/macOS
```

2. Install dependencies:
```bash
pip install django
```

3. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

4. Create quiz categories:
```bash
python manage.py shell
```
Then in the Python shell:
```python
from core.models import Category
categories = [
    {'name': 'IT', 'slug': 'it'},
    {'name': 'Computer Fundamentals', 'slug': 'computer-fundamentals'},
    {'name': 'Maths', 'slug': 'maths'},
    {'name': 'Computer Networking', 'slug': 'computer-networking'},
    {'name': 'Operating Systems', 'slug': 'operating-systems'},
]
for cat in categories:
    Category.objects.create(**cat)
exit()
```

5. Start the development server:
```bash
python manage.py runserver
```

Visit http://localhost:8000 to access the quiz website.

## Project Structure

```
quizsite/
├── core/
│   ├── static/
│   │   ├── css/
│   │   │   └── styles.css
│   │   └── js/
│   │       └── quiz.js
│   ├── templates/
│   │   ├── landing.html
│   │   ├── quiz.html
│   │   └── assessment.html
│   ├── questions/
│   │   └── computer-fundamentals_easy.json
│   ├── models.py
│   ├── views.py
│   └── urls.py
└── quizsite/
    ├── settings.py
    └── urls.py
```

## Adding Questions

Questions are stored in JSON files in the `core/questions/` directory. Each file should follow the naming pattern: `{category-slug}_{difficulty}.json`.

Example question format:
```json
[
    {
        "id": 1,
        "question": "Question text here?",
        "options": {
            "A": "Option A",
            "B": "Option B",
            "C": "Option C",
            "D": "Option D"
        },
        "answer": "A",
        "topic": "Topic Name",
        "difficulty": "easy"
    }
]
```
