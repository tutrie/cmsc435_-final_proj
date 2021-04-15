from django.shortcuts import render


def home_view(request):
    print(request.GET)
    return render(request, 'login.html')
