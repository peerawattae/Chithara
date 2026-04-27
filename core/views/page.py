from django.shortcuts import render


def library_page(request):
    return render(request, "core/library.html")
