# django imports
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from brain import Scripts
from .models import *

# user imports
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import *



def home(request):
    urlEnc = ""    
    usuario = False if request.user.username=="" else True

    if request.method == 'POST':
        urlOrig = request.POST.get('urlOriginal')

        # adicionar o protocolo na url original, se não possuir
        if "http" not in urlOrig:
            urlOrig = "http://" + urlOrig

        # verificar se já possui algum dado com o usuario e a url original
        if len(Url.objects.all().filter(usuario = request.user.username, urlOriginal = urlOrig)) == 0:
            
            # gerar url encurtada / não permitir dados repetidos
            while True:
                urlEnc = Scripts.generateUrl()
                urlQuerry = Url.objects.all().filter(urlEncurtada = urlEnc)
                if(len(urlQuerry) == 0):
                    break
            
            # salvar o registro
            Url.objects.create(
                urlOriginal = urlOrig,
                urlEncurtada = urlEnc,
                usuario = request.user.username if request.user.username != "" else ""
            )
        
        # caso ja possua url encurtada com esse usuario, retornar a url encurtada
        else:
            urlEnc = Url.objects.get(urlOriginal = urlOrig, usuario = request.user.username)
            
        urlEnc = "enclink.herokuapp.com/r/" + str(urlEnc)
        
    context = {'urlenc': urlEnc, 'user': usuario}
    return render(request, 'index.html', context)


def redirecionar(request, link):
    caminho = Url.objects.get(urlEncurtada=link)    
    return redirect(caminho.urlOriginal)


def encLinkUser(request):

    messageLogin = ""
    messageSignUp = ""

    if request.method == "POST":

        #login
        if request.POST.get('type') == 'login':
            username = request.POST.get('user')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request,'Identificação não encontrada')
                return redirect('login')

        #signup
        elif request.POST.get('type') == 'sign':
            username = request.POST.get('user-sign')
            password1 = request.POST.get('password1-sign')
            password2 = request.POST.get('password2-sign')
            
            if password1 == password2:               
                try:
                    user = User.objects.create_user(username, '', password1)
                    user.save()
                    messageSignUp = "Usuario cadastrado, entre no sistema"
                except:
                    messageSignUp = "Ja existe um usuário com este nome"
            else:
                messageSignUp = "Senhas não correspondem"

    context = {'messageLogin' : messageLogin, 'messageSignUp': messageSignUp}
    return render(request, 'user.html', context)


@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('home')


@login_required(login_url='login')
def logs(request):
    urls = Url.objects.all().filter(usuario = request.user.username)
    return render(request, 'logs.html', {'logs': urls})

@login_required(login_url='login')
def deletar(request, id):
    link = Url.objects.all().filter(urlEncurtada = id)
    link.delete()
    return redirect('logs')


def handlerErrorPage(request, exception):
    return render(request, '404.html')