import json
import re
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Exists, OuterRef
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings

from .models import Text, BuzzWord, Bookmarks, MediaFile, Favorites


def greeting(request):
    user = request.user
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('greeting')
        else:
            messages.error(request, 'Error')
    return render(request, 'greetings.html')


def logout_view(request):
    logout(request)
    return redirect('greeting')

@login_required
def heads(request):
    has_bookmark = Exists(Bookmarks.objects.filter(bookmark=OuterRef('pk'), user=request.user))
    query = request.GET.get('q', '').strip().lower()
    texts = Text.objects.annotate(first_page=has_bookmark).order_by('-first_page', 'pk')

    if query:
        texts = [
            text for text in texts
            if query in text.title_current_city.lower()
            or query in str(text.chapter_number)
            or query in text.get_title_home_city_display().lower()
        ]

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'texts': [
                {
                    'title': text.title_current_city,
                    'chapter_number': text.chapter_number,
                    'home_city': text.get_title_home_city_display(),
                    'cover': str(text.chapter_cover) if text.chapter_cover else None
                }
                for text in texts
            ]
        })

    return render(request, 'chapters.html', {'texts': texts})


@login_required
def chapter(request, pk):
    chapter_text = get_object_or_404(Text, pk=pk)
    chapter_buzzwords = BuzzWord.objects.filter(text=chapter_text)
    bookmark = Bookmarks.objects.filter(user=request.user, bookmark=chapter_text).first()
    if request.method == 'POST':
        if bookmark:
            bookmark.delete()
        else:
            Bookmarks.objects.filter(user=request.user).delete()
            Bookmarks.objects.create(user=request.user, bookmark=chapter_text)
        return redirect('chapter', pk=pk)

    try:
        next_chapter=Text.objects.get(pk=(pk+1)).pk
    except Text.DoesNotExist:
        next_chapter = None
    try:
        prev_chapter=Text.objects.get(pk=(pk-1)).pk
    except Text.DoesNotExist:
        prev_chapter = None
    return render(request, 'single_chapter.html', {'text': chapter_text,
                                                   'chapter_buzzwords': chapter_buzzwords,
                                                   'next_chapter': next_chapter,
                                                   'prev_chapter': prev_chapter,
                                                   'bookmark': bookmark,
    })

@login_required
def postcards(request):
    postcards = BuzzWord.objects.all()
    favorites = Favorites.objects.filter(user=request.user).values_list('favorites_id', flat=True)

    return render(request, 'postcards.html', {
        'postcards': postcards,
        'favorites': favorites
    })

@login_required
def single_postcard(request, target_buzzword):
    postcard = BuzzWord.objects.get(id=target_buzzword)
    file_id = str(postcard.linked_file.file)
    match = re.search(r"id=([\w-]+)", file_id)
    if match:
        file_id_tr = match.group(1)
        file_id=f"https://drive.google.com/file/d/{file_id_tr}/preview"
    
    return render(request, 'single_postcard.html', {'postcard':postcard,
                                                    'file_id':file_id})

@login_required
def add_to_favorite(request, pic_id):
    fav_picture = get_object_or_404(MediaFile, id=pic_id)
    add_to_fav, if_exist = Favorites.objects.get_or_create(user=request.user, favorites=fav_picture)
    if not if_exist:
        add_to_fav.delete()
        if request.GET.get('from') == 'favorites':
            return redirect('favorites')
        return redirect('postcards')
    return redirect('postcards')

@login_required
def favorites(request):
    favorites = Favorites.objects.select_related('favorites').prefetch_related('favorites__buzzword_set__text').all()
    return render(request, 'favorites.html', {'favorites': favorites})

def map(request):
    locations = Text.objects.all().values(
        'pk',
        'title_current_city',
        'title_current_city_coord'
    )
    for location in locations:
        location['url'] = f"/chapters/{location['pk']}/"

    return render(request, 'map.html', {
        'locations_json': json.dumps(list(locations)),
        'key': settings.GOOGLE_API_KEY
    })
