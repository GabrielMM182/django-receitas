from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from .models import Receita
from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def index(request):

    # receitas = Receita.objects.all() mostra todos sem filtro
    receitas = Receita.objects.order_by('-date_receita').filter(publicada=True)
    paginator = Paginator(receitas, 3)
    page = request.GET.get('page')
    receitas_por_pagina = paginator.get_page(page) # identificar a pagina

    dados = { # vai trazer a receita
        'receitas' : receitas_por_pagina
    }

    return render(request,'receitas/index.html', dados) 

def receita(request, receita_id):
    receita = get_object_or_404(Receita, pk=receita_id) # vai verifica se possui a receita que vai exibir pelo id se não vai ter erro 404

    receita_a_exibir = {
        'receita' : receita
    }

    return render(request, 'receitas/receita.html', receita_a_exibir)

def buscar(request):
    lista_receitas = Receita.objects.order_by('-date_receita').filter(publicada=True)

    if 'buscar' in request.GET:
        nome_a_buscar = request.GET['buscar']
        if buscar:
            lista_receitas = lista_receitas.filter(nome_receita__icontains = nome_a_buscar) # __icontains  se existe
    
    dados = {
        'receitas': lista_receitas    
    }

    return render(request, 'receitas/buscar.html', dados)

def cria_receita(request):
    if request.method == 'POST':
        nome_receita = request.POST['nome_receita']
        ingredientes = request.POST['ingredientes']
        modo_preparo = request.POST['modo_preparo']
        tempo_preparo = request.POST['tempo_preparo']
        rendimento = request.POST['rendimento']
        categoria = request.POST['categoria']
        foto_receita = request.FILES['foto_receita']
        print(nome_receita, ingredientes, modo_preparo, tempo_preparo, rendimento, categoria, foto_receita)
        user = get_object_or_404(User, pk=request.user.id)
        receita = Receita.objects.create(pessoa = user, # vai pegar pessoa de Receita que e uma foreignkey
        nome_receita = nome_receita, ingredientes=ingredientes, modo_preparo=modo_preparo,
        tempo_preparo=tempo_preparo, rendimento=rendimento,
        categoria=categoria, foto_receita=foto_receita) # vai salvar a receita dentro do db
        receita.save()
        return redirect('dashboard')
    else:
        return render(request, 'receitas/cria_receita.html')

def deleta_receita(request, receita_id):
    receita = get_object_or_404(Receita, pk=receita_id)
    receita.delete()
    return redirect('dashboard')

def edita_receita(request, receita_id):
    receita = get_object_or_404(Receita, pk=receita_id)
    receita_a_editar = { 'receita':receita }
    return render(request, 'receitas/edita_receita.html', receita_a_editar)   

def atualiza_receita(request):
    if request.method == 'POST':
        receita_id = request.POST['receita_id']
        r = Receita.objects.get(pk=receita_id)
        r.nome_receita = request.POST['nome_receita']
        r.ingredientes = request.POST['ingredientes']
        r.modo_preparo = request.POST['modo_preparo']
        r.tempo_preparo = request.POST['tempo_preparo']
        r.rendimento = request.POST['rendimento']
        r.categoria = request.POST['categoria']
        if 'foto_receita' in request.FILES: # vai verificar se possui uma foto, se possuir e não mudar vai manter a mesma
            r.foto_receita = request.FILES['foto_receita']
        r.save()
        return redirect('dashboard')