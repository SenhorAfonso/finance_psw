from django.shortcuts import render, redirect
from perfil.models import Conta, Categoria
from .models import Valores 
from django.http import FileResponse
from django.contrib import messages
from django.contrib.messages import constants
from datetime import datetime
from django.template.loader import render_to_string
import os
from django.conf import settings
from weasyprint import HTML
from io import BytesIO

def novo_valor(request):
    # sempre que a requisição for via url
    if request.method == 'GET':

        conta = Conta.objects.all()
        categorias = Categoria.objects.all()        

        return render(request, 'novo_valor.html', {'contas' : conta, 'categorias' : categorias})

    # quando a requisição for um post para a URL (o envio de um formulário)
    elif request.method == 'POST':
        valor = request.POST.get('valor')
        categoria_id = request.POST.get('categoria')
        descricao = request.POST.get('descricao')
        data = request.POST.get('data')
        conta_id = request.POST.get('conta')
        tipo = request.POST.get('tipo')

        try:
            valores = Valores(
                valor = valor,
                categoria_id = categoria_id,
                descricao = descricao,
                data = data,
                conta_id = conta_id,
                tipo = tipo
            ).save()
        except ValueError:
            messages.add_message(request, constants.ERROR, 'O campo "Valor" aceita apenas valores numéricos!')
            return redirect('/extrato/novo_valor')

        conta = Conta.objects.get(id = conta_id)

        if tipo == 'S':
            messages.add_message(request, constants.SUCCESS, 'Saída cadastrada com sucesso!')
            conta.valor -= float(valor)
        else:
            messages.add_message(request, constants.SUCCESS, 'Entrada cadastrada com sucesso!')
            conta.valor += float(valor)

        conta.save()

        return redirect('/extrato/novo_valor')

def view_extrato(request):

    conta = Conta.objects.all()
    categorias = Categoria.objects.all()
    conta_get = request.GET.get('conta')
    categoria_get = request.GET.get('categoria')
    periodo_get = request.GET.get('periodo')
    valores = Valores.objects.filter(data__month = datetime.now().month)

    print(periodo_get)

    if conta_get:
        valores = valores.filter(conta__id = conta_get)
    
    if categoria_get:
        valores = valores.filter(categoria__id = categoria_get)

    return render(request, 'view_extrato.html', {'valores' : valores, 'contas' : conta, 'categorias' : categorias})
    
def exportar_pdf(request):
    valores = Valores.objects.filter(data__month = datetime.now().month)
    path_template = os.path.join(settings.BASE_DIR, 'templates/partials/extrato.html')
    template_render = render_to_string(path_template, {'valores' : valores})

    # salvar o pdf em memória ao invés de no disco
    path_output = BytesIO()
    HTML(string = template_render).write_pdf(path_output)
    path_output.seek(0)

    return FileResponse(path_output, filename='extrato.pdf')