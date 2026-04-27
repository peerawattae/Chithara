from django.shortcuts import render


def library_page(request):
    return render(request, "core/library.html")

def create_page(request):
    return render(request, "core/create.html")

def song_page(request, pk):
    return render(request, "core/song.html", {"song_id": pk})

def description_page(request, pk):
    return render(request, "core/description.html", {"song_id": pk})