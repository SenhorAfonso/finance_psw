
def calculaTotal(obj, campo):
    total = 0
    for elemento in obj:
        total +=  getattr(elemento, campo)
    
    return total
