from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.conf import settings

def index(request):
    return render(request, 'main/index.html')

def about(request):
    return render(request, 'main/about.html')

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        subject = f"Yeni Mesaj: {name}"
        message_body = f"Mesaj: {message}\nGönderen: {email}"
        send_mail(subject, message_body, settings.EMAIL_HOST_USER, ['4mizacinfo@gmail.com'])
        context = {'success_message': 'Mesajınız başarıyla gönderilmiştir.'}
        return render(request, 'main/about.html', context)
    return redirect('about')
