#Tipos de peticiones HTTP más usados#

HTTP define un grupo de métodos de petición con los que se especifica la __acción__ correspondiente a un recurso determinado. Aunque pueden ser sustantivos, también son conocidos como __HTTP verbs__.

##GET##
Solicitud de lectura que recupera datos de un recurso específico, en forma de identidad.

##HEAD##
Funciona como la solicitud __GET__, pero sin el cuerpo de la respuesta.

##POST##
Envía una entidad a un recurso especifico.

##PUT##
Envía una entidad para que sea guardada, de manera que si esta se refiere a un recurso existente será guardada como la actualización del recurso.

##DELETE##
Elimina el recurso especifico señalado.

##CONNECT##
Proporciona un tunel hacia el servidor determinado por el recurso.

##OPTIONS##
Describe las opciones de comunicación al servidor, seleccionadas por el recurso.

##TRACE##
Usado para obtener información de flujo de mensajes con el servidor.

#Codigos de respuesta HTTP#

Los códigos de estado de respuesta HTTP indican si se ha completado satisfactoriamente una solicitud HTTP específica. Estos codigos se agrupan en 5 clases: respuestas informativas, respuestas satisfactorias, redirecciones, errores de cliente y errores de servidor.

##Respuestas informativas##

__100 Continue__: Indican normalidad.
__101 Switching Protocols__: Informa que se acepta el cambio de protocolo propuesto.
__102 Processing__: Se refiere que el servidor se encuentra procesando la solicitud enviada.
__103 Early Hints__: Permite pre cargar recursos usando el encabezado Link.

##Respuestas Satisfactorias##

