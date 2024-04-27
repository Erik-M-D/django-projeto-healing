from django.shortcuts import render, redirect
from django.http import HttpResponse
# User é uma tabela do banco de dados
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages
# autenticando
from django.contrib import auth


def cadastro(request):
    if request.method == 'GET':
        return render(request, 'cadastro.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        if not senha == confirmar_senha:
            messages.add_message(request, constants.ERROR, "As senhas precisam ser iguais")
            return redirect('/usuarios/cadastro/')
            # 
        if len(senha) < 6:
            messages.add_message(request, constants.ERROR, "A senha tem que ter mais de 6 digitos")
            return redirect('/usuarios/cadastro/')
        # try:
        
        # verificando se o usuario já existe
        users = User.objects.filter(username=username)
        if users.exists():
            messages.add_message(request, constants.ERROR, "Já existe um usuário com esse username")
            return redirect('/usuarios/cadastro/')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=senha
        )

        return redirect('/usuarios/login/')
        # except:
        #     return redirect('/usuarios/cadastro/')

def login_view(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        user = auth.authenticate(request, username=username, password=senha)

        if user:
            # vai ligar o usuario com o ip
            auth.login(request, user)
            return redirect('/pacientes/home')
        
        messages.add_message(request, constants.ERROR, 'Usuário ou senha inválidos')
        return redirect('/usuarios/login')
    

def sair(request):
    auth.logout(request)

    return redirect("/usuarios/login")