# from django.shortcuts import render
# from .mood_data import mood_recommendations
# from .api_utils import get_movies_by_mood

# def home(request):
#     mood = request.GET.get('mood')
#     recommendations = {}

#     if mood:
#         music_list = mood_recommendations.get(mood, {}).get("music", [])
#         movie_list = get_movies_by_mood(mood)

#         recommendations = {
#             "movies": movie_list,
#             "music": music_list
#         }

#     context = {
#         'selected_mood': mood,
#         'recommendations': recommendations
#     }

#     return render(request, 'home.html', context)




from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from textblob import TextBlob

from .tmdb_client import get_movies_by_mood
from .youtube_client import get_music_by_mood  # YouTube from RapidAPI
from textblob import TextBlob  # 📦 NLP package for mood detection

@login_required(login_url='login')
def home(request):
    mood = request.GET.get('mood')
    feeling_text = request.GET.get('feeling_text')
    recommendations = {}

    # Step 1: Detect mood from free text if provided
    if feeling_text:
        analysis = TextBlob(feeling_text)
        polarity = analysis.sentiment.polarity

        if polarity > 0.3:
            mood = 'happy'
        elif polarity < -0.3:
            mood = 'sad'
        else:
            mood = 'chill'

        messages.info(request, f"Detected mood: {mood.title()} 🎯")

    # Step 2: Fetch recommendations if mood is known
    if mood:
        movie_list = get_movies_by_mood(mood)
        music_list = get_music_by_mood(mood)

        print("DEBUG MOVIES:", movie_list)
        print("DEBUG MUSIC:", music_list)

        # Movie fallback if API fails
        if not movie_list:
            movie_list = [{
                "title": "Example Movie",
                "url": "https://www.imdb.com/title/tt0111161/",
                "poster": "https://via.placeholder.com/300x450?text=No+Image",
                "rating": "9.3",
                "release_year": "1994"
            }]

        # Music fallback if API fails or less than 3
        if not music_list or len(music_list) < 3:
            music_list = [
                {"title": "Fallback Song 1", "youtube": "https://www.youtube.com/embed/dQw4w9WgXcQ"},
                {"title": "Fallback Song 2", "youtube": "https://www.youtube.com/embed/oHg5SJYRHA0"},
                {"title": "Fallback Song 3", "youtube": "https://www.youtube.com/embed/3GwjfUFyY6M"}
            ]

        recommendations = {
            "movies": movie_list,
            "music": music_list
        }

    return render(request, 'home.html', {
        'selected_mood': mood,
        'recommendations': recommendations
    })


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, '⚠️ Username already exists. Please choose another one.')
        else:
            User.objects.create_user(username=username, password=password)
            messages.success(request, '✅ Registered successfully! Please log in.')
            return redirect('login')

    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, '❌ Invalid username or password.')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    messages.info(request, "🔓 You have been logged out.")
    return redirect('login')
