def validar_resultado(resultado):
    requerido = ["parametro", "valor"]
    for campo in requerido:
        if campo not in resultado or resultado[campo] is None:
            return False
    return True
