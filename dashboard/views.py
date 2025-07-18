from django.shortcuts import render

# Create your views here.

def mian_dashboard(request):

    return render(request, 'dashboard.html')