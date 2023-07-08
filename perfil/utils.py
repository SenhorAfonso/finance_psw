
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


def calcula_contas():
    from contas.models import ContaPaga, ContaPagar

    MES_ATUAL = datetime.now().month
    DIA_ATUAL = datetime.now().day

    contas = ContaPagar.objects.all()
    contasPagas = ContaPaga.objects.filter(data_pagamento__month = MES_ATUAL).values('conta')
    contas_vencidas = contas.filter(dia_pagamento__lt = DIA_ATUAL).exclude(id__in = contasPagas)
    contas_proximas_vencimento = contas.filter(dia_pagamento__lte = DIA_ATUAL + 5).filter(dia_pagamento__gt = DIA_ATUAL).exclude(id__in = contasPagas)
    contas_restantes = contas.exclude(id__in = contas_vencidas).exclude(id__in = contasPagas).exclude(id__in = contas_proximas_vencimento)

    return contas_vencidas, contas_proximas_vencimento, contas_restantes