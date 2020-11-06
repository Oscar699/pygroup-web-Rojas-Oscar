from flask import Blueprint, Response


products = Blueprint('products', __name__, url_prefix='/products')
test = Blueprint('test', __name__, url_prefix='/Tareaflask')

@products.route('/')
def index():
    """Description"""
    return "<b><h1>Testeando funcionamiento</h1>"
@test.route('/<string:name>', methods=['GET'])
def resp(name):
    """Description
    Muestra un mensaje en la pagina segun el nombre que se indique
    en la Url.

    params: name - El sting nombre en la url.
    return: Response 200 El nombre es diferente de "pygroup"
                     400 El nombre es "pygroup"
    """
    if name != 'pygroup':
        return Response('Felicitaciones! Trabajo exitoso {}'.format(name), status=200)
    elif name == 'pygroup':
        return  Response('ERROR! No se puede usar el nombre pygroup', status=400)

    """ 
    método render_template: La operación que convierte una plantilla en una página HTML completa se llama renderizado. 
    Para renderizar la plantilla se debe de importar una función que viene con el marco de Flask llamada 
    render_template (). Esta función toma un nombre de archivo de plantilla y una lista variable de argumentos de 
    plantilla y devuelve la misma plantilla, pero con todos los marcadores de posición en ella
    reemplazados por valores reales.
    Fuente: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-ii-templates
    """





