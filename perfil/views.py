from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Conta, Categoria
from extrato.models import Valores
from django.contrib import messages
from django.contrib.messages import constants
from .utils import *
from datetime import datetime
from contas.views import ver_contas

def home(request):
    valores = Valores.objects.filter(data__month = datetime.now().month)

    total_entradas = calculaTotal(valores.filter(tipo = 'E'), 'valor')
    total_saidas = calculaTotal(valores.filter(tipo = 'S'), 'valor')

    saldo_mensal = calculaTotal(valores.filter(tipo = 'E').filter(data__month = datetime.now().month), 'valor')
    despesa_mensal = calculaTotal(valores.filter(tipo = 'S').filter(data__month = datetime.now().month), 'valor')
    livre = saldo_mensal - despesa_mensal

    contas = Conta.objects.all()
    total_contas = calculaTotal(contas, 'valor')

    gastos_essenciais, gastos_nao_essenciais = calcula_equilibrio_financeiro()

    contas_vencidas, contas_proximas_vencimento, _ = calcula_contas()

    return render(request, 'home.html', {'contas' : contas, 
                                         'total_contas' : total_contas, 
                                         'total_entradas' : total_entradas, 
                                         'total_saidas' : total_saidas,
                                         'gastos_essenciais' : int(gastos_essenciais),
                                         'gastos_nao_essenciais' : int(gastos_nao_essenciais),
                                         'saldo_mensal' : saldo_mensal,
                                         'despesa_mensal' : despesa_mensal,
                                         'livre' : livre,
                                         'contas_vencidas' : contas_vencidas,
                                         'contas_proximas_vencimento' : contas_proximas_vencimento})


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

def dashboard(request):
    categorias = Categoria.objects.all()
    dados = {}
    for categoria in categorias:
        total = 0
        valores = Valores.objects.filter(categoria = categoria)
        for item in valores:
            total += item.valor
        
        dados[categoria.categoria] = total

    return render(request, 'dashboard.html', {'labels' : list(dados.keys()), 'values' : list(dados.values())})