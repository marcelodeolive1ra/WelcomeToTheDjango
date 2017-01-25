from django.shortcuts import render, render_to_response, HttpResponseRedirect
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.shortcuts import HttpResponse

from django.contrib.auth.decorators import login_required

from .models import *


# Create your views here.
def index(request):
    materias = Materia.objects.all()

    return render_to_response('hello/index.html', {'materias': materias, 'pagina': 'Welcome to the Django'})


@login_required(login_url='/login/')
def supersecret(request):
    return render_to_response('hello/supersecret.html', {'pagina': 'Supersecret'})


def login(request):
    dict = {}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            usuario = User.objects.get(username=username)

            if usuario.is_active:
                usuario_autenticado = authenticate(username=username, password=password)

                if usuario_autenticado is not None:
                    django_login(request, usuario_autenticado)
                else:
                    dict['erro'] = 'Usuário ou senha inválidos'
            else:
                dict['erro'] = 'Usuário inativo.'


        except:
            dict['erro'] = 'Usuário ou senha inválidos.'

    dict['pagina'] = 'Login - Welcome to the Django'
    return render(request, 'hello/login.html', dict)


def logout(request):
    if request.user.is_authenticated:
        django_logout(request)

    return HttpResponseRedirect('/')


def cadastro(request):
    if request.method == 'POST':
        nome = request.POST['nome']
        sobrenome = request.POST['sobrenome']
        senha = request.POST['senha']
        email = request.POST['email']
        RA = request.POST['RA']
        curso = request.POST['curso']
        sexo = request.POST['sexo']

        user = User(username=email, email=email, first_name=nome, last_name=sobrenome, password=senha)
        user.save()

        curso = Curso.objects.get(id=curso)
        aluno = Aluno(user=user, RA=RA, curso=curso, sexo=sexo)
        aluno.save()

        # TODO Continuar na próxima aula

        return render(request, 'hello/cadastro.html', {})
    else:
        cursos = Curso.objects.all()
        return render(request, 'hello/cadastro.html', {'cursos': cursos})