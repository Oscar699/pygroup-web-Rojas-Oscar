# Tipos de peticiones HTTP más usados

HTTP define un grupo de métodos de petición con los que se especifica la __acción__ correspondiente a un recurso determinado. Aunque pueden ser sustantivos, también son conocidos como __HTTP verbs__.

## GET
Solicitud de lectura que recupera datos de un recurso específico, en forma de identidad.

## HEAD
Funciona como la solicitud __GET__, pero sin el cuerpo de la respuesta.

## POST
Envía una entidad a un recurso especifico.

## PUT
Envía una entidad para que sea guardada, de manera que si esta se refiere a un recurso existente será guardada como la actualización del recurso.

## DELETE
Elimina el recurso especifico señalado.

## CONNECT
Proporciona un tunel hacia el servidor determinado por el recurso.

## OPTIONS
Describe las opciones de comunicación al servidor, seleccionadas por el recurso.

## TRACE
Usado para obtener información de flujo de mensajes con el servidor.

# Codigos de respuesta HTTP

Los códigos de estado de respuesta HTTP indican si se ha completado satisfactoriamente una solicitud HTTP específica. Estos códigos se agrupan en 5 clases: respuestas informativas, respuestas satisfactorias, redirecciones, errores de cliente y errores de servidor.

## Respuestas informativas

- __100 Continue__: Indica normalidad.
- __101 Switching Protocols__: Informa que se acepta el cambio de protocolo propuesto.
- __102 Processing__: Se refiere que el servidor se encuentra procesando la solicitud enviada.
- __103 Early Hints__: Permite precargar recursos usando el encabezado Link.

## Respuestas Satisfactorias

- __200 Ok__: Señala que la solicitud ha tenido éxito, este éxito depende del método HTTP usado.
- __201 Created__: Respuesta típica a un PUT que indica que se ha creado un recurso gracias a que la solicitud ha tenido éxito.
- __2002 Accepted__: Indica que la solicitud se ha aceptado, sin embargo no se tiene una respuesta a la misma.
- __203 Non-Authoritave Information__: Informa que la petición se completó exitosamente, pero que el contenido no se adquirió de la fuente indicada, si no que fue obtenida de una copia o de un recurso externo.
- __206 Partial Content__: Significa que la petición entregará el contenido solicitado de manera parcial, comúnmente utilizado para descargas interrumpidas o dividirlas y procesarlas simultáneamente.

## Redirecciones

- __300 Multiple Choice__: Indica que el usuario tiene múltiples opciones para acceder al recurso solicitado.
- __301 Moved Permanentrly__: Este código señala que la URI del recurso ha sido cambiada.
- __302 Found__: Nos informa que la URI ha sido cambiada temporalmente.
- __304 Not Modified__: Señala al cliente que la respuesta no tiene modificaciones, por lo que podrá seguir utilizando la que tiene almacenada en su caché.
- __307 Temporary Redirect__: Esta respuesta se da para dirigir al cliente a otra URI en busca del recurso solicitado, usando el mismo método que se usó en la petición anterior.

## Errores del cliente

- __400 Bad Request__: Significa Sintaxis de peticion invalida.
- __401 Unauthorized__: Señala que el cliente no está autorizado para obtener la respuesta solicitada. Sin embargo, la autenticación es posible.
- __403 Forbidden__: Indica que el cliente no cuenta con los permisos necesarios para acceder al contenido solicitado.
- __404 Not Found__: Respuesta del servidor cuando no fue posible encontrar el contenido solicitado.
- __408 Request Timeot__: El servidor devuelve esta respuesta cuando se tiene la intención de desconectar una conexión inactiva.
- __409 Conflict__: Se refiere a que el estado del servidor tiene un conflicto con una petición.
- __429 Too Many Requests__: Se da cuando el cliente a hecho demasiadas peticiones en un intervalo de tiempo dado.

## Errores del servidor

- __500 Internal Server Error__: El servidor no sabe cómo proceder ante una situación.
- __501 Not Implemented__: El método requerido no está soportado, no se admite o no está implementado en el servidor.
- __502 Bad Gateway__: Significa que el servidor obtuvo una respuesta inválida durante el manejo de la petición.
- __503 Servide Unavailable__: Indica que el servidor no está disponible, comúnmente causado porque está en mantenimiento o porque hay sobrecarga de peticiones.
- __504 Gateway Timeot__: Respuesta obtenida cuando el servidor está siendo usado como puerta de enlace y no obtiene una respuesta a tiempo.

# Referencias

- [1]"Métodos de petición HTTP", Documentación web de MDN, 2020. [Online]. Disponible en: https://developer.mozilla.org/es/docs/Web/HTTP/Methods. [Accessed: 29- Oct- 2020].
- [2]"Códigos de estado de respuesta HTTP", Documentación web de MDN, 2020. [Online]. Disponible en: https://developer.mozilla.org/es/docs/Web/HTTP/Status. [Accessed: 29- Oct- 2020].
- [3]M. Vásquez, "Protocolo HTTP". Disponible en: https://profesores.virtual.uniandes.edu.co/~isis3710/dokuwiki/doku.php.




