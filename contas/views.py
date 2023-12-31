from django.shortcuts import render, redirect
from perfil.models import Categoria
from .models import ContaPagar, ContaPaga
from django.contrib.messages import constants
from django.contrib import messages
from datetime import datetime

def definir_contas(request):
    if request.method == 'GET':
        categorias = Categoria.objects.all()
        return render(request, 'definir_contas.html', {'categorias' : categorias})
    elif request.method == 'POST':
        titulo = request.POST.get('titulo')
        categoria = request.POST.get('categoria')
        descricao = request.POST.get('descricao')
        valor = request.POST.get('valor')
        dia_pagamento = request.POST.get('dia_pagamento')
        
        conta = ContaPagar(
            titulo = titulo,
            categoria_id = categoria,
            descricao = descricao,
            valor = valor,
            dia_pagamento = dia_pagamento
        ).save()

        messages.add_message(request, constants.SUCCESS, 'Conta cadastrada com sucesso!')

        print(titulo)
        return redirect('/contas/definir_contas/')

def ver_contas(request):
    from perfil.utils import calcula_contas

    MES_ATUAL = datetime.now().month
    DIA_ATUAL = datetime.now().day

    contas_vencidas, contas_proximas_vencimento, contas_restantes = calcula_contas()
    return render(request, 'ver_contas.html', {'contas_vencidas' : contas_vencidas,
                                               'contas_proximas_vencimento' : contas_proximas_vencimento,
                                               'contas_restantes' : contas_restantes})