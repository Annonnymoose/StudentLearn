import json
import random
import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Category

def landing_view(request):
    categories = Category.objects.all()
    return render(request, 'landing.html', {'categories': categories})

def load_questions(category):
    # Load questions from all difficulty levels
    difficulties = ['easy', 'medium', 'hard']
    all_questions = []
    
    for difficulty in difficulties:
        try:
            file_path = f'core/questions/{category.slug}_{difficulty}.json'
            with open(file_path, 'r') as f:
                questions = json.load(f)
                all_questions.extend(questions)
        except FileNotFoundError:
            continue
    
    # Return 20 random questions from all difficulties
    return random.sample(all_questions, min(len(all_questions), 20))

def quiz_view(request, slug):
    category = get_object_or_404(Category, slug=slug)

    if request.method == 'POST':
        attempt_id = request.POST.get('attempt_id')
        answers = {k[2:]: v for k, v in request.POST.items() 
                  if k.startswith('q_') and v}
        
        stored_questions = request.session.get(f'quiz_{attempt_id}', {})
        if not stored_questions:
            return redirect('landing')

        correct_count = 0
        topic_stats = {}

        for q_id, answer in answers.items():
            question = stored_questions.get(q_id)
            if question and answer == question['answer']:
                correct_count += 1
                topic = question['topic']
                topic_stats[topic] = topic_stats.get(topic, {'correct': 0, 'total': 0})
                topic_stats[topic]['correct'] += 1
                topic_stats[topic]['total'] += 1
            elif question:
                topic = question['topic']
                topic_stats[topic] = topic_stats.get(topic, {'correct': 0, 'total': 0})
                topic_stats[topic]['total'] += 1

        result = {
            'total': len(answers),
            'correct': correct_count,
            'percentage': (correct_count / len(answers)) * 100 if answers else 0,
            'topic_stats': topic_stats
        }

        request.session[f'result_{attempt_id}'] = result
        return redirect('assessment', slug=slug)

    questions = load_questions(category)
    attempt_id = str(uuid.uuid4())
    
    # Store answers in session
    question_store = {str(q['id']): q for q in questions}
    request.session[f'quiz_{attempt_id}'] = question_store

    # Remove answers before sending to template
    for q in questions:
        q['original_id'] = q['id']
        q.pop('answer', None)
        # Randomize options order
        options = list(q['options'].items())
        random.shuffle(options)
        q['options'] = dict(options)

    random.shuffle(questions)
    
    return render(request, 'quiz.html', {
        'category': category,
        'questions': questions,
        'attempt_id': attempt_id,
    })

def assessment_view(request, slug):
    category = get_object_or_404(Category, slug=slug)
    attempt_id = request.GET.get('attempt_id')
    
    if not attempt_id:
        return redirect('landing')
    
    result = request.session.get(f'result_{attempt_id}')
    if not result:
        return redirect('landing')

    topic_stats = result['topic_stats']
    strengths = []
    needs_improvement = []

    for topic, stats in topic_stats.items():
        percentage = (stats['correct'] / stats['total']) * 100
        if percentage >= 70:
            strengths.append(topic)
        else:
            needs_improvement.append(topic)

    context = {
        'category': category,
        'result': result,
        'strengths': strengths,
        'needs_improvement': needs_improvement,
    }
    
    return render(request, 'assessment.html', context)
