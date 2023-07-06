from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Conta, Categoria
from django.contrib import messages
from django.contrib.messages import constants
from .utils import *

def home(request):
    contas = Conta.objects.all()
    total_contas = calculaTotal(contas, 'valor')

    return render(request, 'home.html', {'contas' : contas, 'total_contas' : total_contas})

def update_categoria(request, id):
    categoria = Categoria.objects.get(id = id)
    categoria.essencial = not(categoria.essencial)
    categoria.save()
    return redirect('/perfil/gerenciar')

def gerenciar(request):
    contas = Conta.objects.all()
    total_conta = calculaTotal(contas, 'valor')

    categorias = Categoria.objects.all()

    return render(request, 'gerenciar.html', {'contas' : contas, 'total_conta' : total_conta, 'categorias' : categorias})

def cadastrar_banco(request):
    apelido = request.POST.get('apelido')
    banco = request.POST.get('banco')
    tipo = request.POST.get('tipo')
    valor = request.POST.get('valor')
    icone = request.FILES.get('icone')

    if len(apelido.strip()) == 0 or len(valor.strip()) == 0 or len(icone) == 0:
        messages.add_message(request, constants.WARNING, 'Preencha todos os campos')
        return redirect('/perfil/gerenciar')

    conta = Conta(
        apelido = apelido,
        banco = banco,
        tipo = tipo,
        valor = valor,
        icone = icone
    ).save()

    messages.add_message(request, constants.SUCCESS, 'Conta cadastrada com sucesso')

    return redirect('/perfil/gerenciar')

def deletar_banco(request, id):
    conta = Conta.objects.get(id = id)
    conta.delete()
    # messages.success(request, constants.SUCCESS, 'Conta deletada com sucesso!')
    return redirect('/perfil/gerenciar')

def cadastrar_categoria(request):
    nome = request.POST.get('categoria')
    essencial = bool(request.POST.get('essencial'))

    categoria = Categoria(
        categoria = nome,
        essencial = essencial
    ).save()

    messages.add_message(request, constants.SUCCESS, 'Categoria cadastrada com sucesso!')
    return redirect('/perfil/gerenciar')
