from django.shortcuts import render
from perfil.models import Conta, Categoria

def novo_valor(request):
    # sempre que a requisição for via url
    if request.method == 'GET':

        conta = Conta.objects.all()
        categorias = Categoria.objects.all()        

        return render(request, 'novo_valor.html', {'contas' : conta, 'categorias' : categorias})
