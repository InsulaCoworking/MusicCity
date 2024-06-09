from django.shortcuts import render


def bot_info(request):
    return render(request, 'bot_info.html', {})