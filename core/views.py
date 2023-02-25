from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from agenda.forms import CreateUserForm
from core.models import Evento
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from datetime import datetime, timedelta, date
from django.http.response import Http404, JsonResponse



# def index(request):
#     return redirect('/agenda/')

def login_user(request):
    if request.user.is_authenticated:
        return redirect('/agenda') #se estiver autenticado ele vai pra página principal
    return render(request, 'pages/login.html') #se não estiver autenticado ele renderiza a tela de login


def register_user(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login')

    context = {'form': form}
    return render(request, 'pages/cadastro.html', context)

def logout_user(request):
    logout(request)
    return redirect('/')


def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(username=username, password=password)

        if usuario is not None:
            login(request, usuario)
            return redirect('/')
        else:
            messages.error(request, "Usuario ou senha inválido")
    return redirect('/')


@login_required(login_url='/login/')  # se não estiver autenticado não irá abrir a página da agenda e s erá levado até a página de autenticar.
def lista_eventos(request):

    usuario = request.user
    data_atual = datetime.now() - timedelta(hours=1)
    evento = Evento.objects.filter(usuario=usuario,
                                   data_evento__gt=data_atual)

    dados = {'eventos': evento}
    return render(request, 'pages/agenda.html', dados)


@login_required(login_url='/login/')
def evento(request):
    id_evento = request.GET.get('id')
    dados = {}
    if id_evento:
        dados['evento'] = Evento.objects.get(id=id_evento)
    return render(request, 'pages/evento.html', dados)


@login_required(login_url='/login/')
def submit_evento(request):
    if request.POST:
        titulo = request.POST.get('titulo')
        data_evento = request.POST.get('data_evento')
        descricao = request.POST.get('descricao')
        usuario = request.user
        id_evento = request.POST.get('id_evento')
        if id_evento:
            evento = Evento.objects.get(id=id_evento)
            if evento.usuario == usuario:
                evento.titulo = titulo
                evento.descricao = descricao
                evento.data_evento = data_evento
                evento.save()

            # Evento.objects.filter(id=id_evento).update(titulo=titulo,
            #                                            data_evento=data_evento,
            #                                            descricao=descricao)
        else:
            Evento.objects.create(titulo=titulo,
                                  data_evento=data_evento,
                                  descricao=descricao,
                                  usuario=usuario)
    return redirect('/')


@login_required(login_url='/login/')
def delete_evento(request, id_evento):
    usuario = request.user
    try:
        evento = Evento.objects.get(id=id_evento)
    # essa validação serve para que cada usuario exclua apenas o evento próprio. Se por acaso tentarem exluir o evento pela url, será feito:
    # O ID do evento perteece ao usuario logado? se não pertence, não consegue excluir
    except Exception:
        raise Http404()
    if usuario == evento.usuario:
        evento.delete()
    else:
        raise Http404()
    return redirect('/')


# @login_required(login_url='/login/')
def json_lista_evento(request, id_usuario):
    usuario = User.objects.get(id=id_usuario)
    evento = Evento.objects.filter(usuario=usuario).values('id', 'titulo')
    return JsonResponse(list(evento), safe=False)

