from modelo.acceso_analisis import obtener_analisis_por_parcela, obtener_analisis_por_arbol

def consultar_analisis_por_objetivo(id_parcela=None, id_arbol=None):
    """
    Devuelve los análisis asociados a una parcela o a un árbol específico.

    Parámetros:
        id_parcela (int): ID de la parcela (opcional).
        id_arbol (int): ID del árbol (opcional).

    Retorna:
        list: Lista de análisis [(id, fecha, descripcion, tipo, ...)]

    Nota:
        Si se proporciona id_arbol, tiene prioridad sobre id_parcela.
    """
    if id_arbol:
        return obtener_analisis_por_arbol(id_arbol)
    elif id_parcela:
        return obtener_analisis_por_parcela(id_parcela)
    else:
        return []
