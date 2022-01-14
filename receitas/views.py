from django.shortcuts import render, get_list_or_404, get_object_or_404
from .models import Receita

def index(request):

    receitas = Receita.objects.all()

    dados = {
        'receitas' : receitas
    }

    return render(request,'index.html', dados) 

def receita(request, receita_id):
    receita = get_object_or_404(Receita, pk=receita_id) # vai verifica se possui a receita que vai exibir pelo id se não vai ter erro 404

    receita_a_exibir = {
        'receita' : receita
    }

    return render(request, 'receita.html', receita_a_exibir)