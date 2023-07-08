
from datetime import datetime

def calculaTotal(obj, campo):
    total = 0
    for elemento in obj:
        total +=  getattr(elemento, campo)
    
    return total

def calcula_equilibrio_financeiro():
    from extrato.models import Valores
    gastos_essenciais = calculaTotal(Valores.objects.filter(data__month = datetime.now().month).filter(tipo = 'S').filter(categoria__essencial = True), 'valor')
    gastos_nao_essenciais = calculaTotal(Valores.objects.filter(data__month = datetime.now().month).filter(tipo = 'S').filter(categoria__essencial = False), 'valor')
    total = gastos_essenciais + gastos_nao_essenciais

    try:
        per_gastos_essenciais = (gastos_essenciais * 100) / total
        per_gastos_nao_essenciais = (gastos_nao_essenciais * 100) / total
    except:
        return 0, 0
    return per_gastos_essenciais, per_gastos_nao_essenciais
