from modelo.acceso_analisis import (
    crear_analisis as crear_analisis_bd,
    actualizar_datos_analisis,
    eliminar_resultados_analisis,
    insertar_resultado_analisis,
    eliminar_analisis as eliminar_analisis_bd
)

def crear_analisis_con_resultados(tipo_id, fecha, descripcion, resultados, id_parcela=None, id_arbol=None):
    """
    Crea un análisis vinculado a una parcela o árbol e inserta sus resultados.

    Parámetros:
        tipo_id (int): ID del tipo de análisis.
        fecha (str): Fecha en formato YYYY-MM-DD.
        descripcion (str): Descripción libre del análisis.
        resultados (list): Lista de diccionarios con los campos:
            - parametro
            - metodo
            - unidad
            - valor
            - incertidumbre (opcional)
            - limite_cuantificacion (opcional)
        id_parcela (int): ID de la parcela (si aplica).
        id_arbol (int): ID del árbol (si aplica).

    Levanta:
        ValueError: Si faltan datos obligatorios.
    """
    if not resultados or not isinstance(resultados, list):
        raise ValueError("Debe proporcionar al menos un resultado válido.")

    if id_parcela is None and id_arbol is None:
        raise ValueError("El análisis debe vincularse a una parcela o un árbol.")

    return crear_analisis_bd(
        idTipoAnalisis=tipo_id,
        fecha=fecha,
        descripcion=descripcion,
        resultados=resultados,
        id_parcela=id_parcela,
        id_arbol=id_arbol
    )



def actualizar_analisis(id_analisis, tipo_id, fecha, descripcion, resultados):
    actualizar_datos_analisis(id_analisis, tipo_id, fecha, descripcion)
    eliminar_resultados_analisis(id_analisis)
    for r in resultados:
        insertar_resultado_analisis(
            id_analisis,
            r['parametro'],
            r.get('metodo'),
            r.get('unidad'),
            r.get('valor'),
            r.get('incertidumbre'),
            r.get('limite_cuantificacion')
        )


def eliminar_analisis(id_analisis):
    return eliminar_analisis_bd(id_analisis)