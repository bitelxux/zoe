|
|

.. class:: title150
   
   |

   ZOE: UN SISTEMA DE MENSAJERÍA F2F

   |

   Carlos Enrique Novo Negrillo

   Sevilla, Septiembre 2013 

.. raw:: pdf

   PageBreak cutePage

.. header:: ZOE. Un sistema de mensajería F2F. Carlos Novo 2013.
.. footer:: ###Page###

.. |si| image:: ./images/verde.on.gif 
.. |no| image:: ./images/rojo.on.gif 
.. |rojo| image:: ./images/rojo.on.gif 
.. |verde| image:: ./images/verde.on.gif 
.. |amarillo| image:: ./images/amarillo.on.gif 


.. Contents::

Introducción
============

.. page::

Objetivos
---------

Objetivos Generales
*******************

Se pretende desarrollar el software para un nodo que sea capaz de comunicarse
punto a punto con otros nodos de confianza.

Si bien el presente trabajo puede servir como base para desarrollar una red anónima y descentralizada tipo Freenet o Turtle, queda fuera 
del alcance del mismo. Queda a disposición de futuros trabajos el extender el mismo para dotarle de mayores funcionalidades.

El que, como se mostrará posteriormente, existan múltiples desarrollos que contemplan muchas de las características de nuestra propuesta, 
esto no descalifica el presente trabajo por considerarse que se trata de un campo en continuo desarrollo cuya aplicación será habitual
en las comunicaciones de los próximos años.

Incluso Retroshare, que incluye dos de las principales características deseadas: F2F a través de NATs y descentralización, convierte una de
sus características: ausencia total de servidores, en una desventaja, ya que al depender de redes DHT la localización de los nodos tarda mucho
tiempo o llega incluso a no tener éxito.

En este sentido, las características deseables de dicho nodo son:

- Debe ser *GUI independent*
- No debe requerir que el usuario final configure ningún tipo de firewall o redireccionamiento.
- Debe tener canales de actuación, al menos una consola telnet y un canal TCP para manejarlo. 
- Debe ser multiplataforma
- En este trabajo, el alcance será *Poder enviar un mensaje encriptado a un contacto sin que pase por ningún tercero*. 
- Esta funcionalidad básica deberá ser fácilmente extensible para poder transmitir cualquier tipo de contenido.
- Si bien, otros desarrolladores podrán tener acceso a los fuentes y extenderlos directamente, lo expuesto en
  el canal TCP deberá ser suficiente para poder extender la funcionalidad aunque no se tuviera acceso a fuentes ni API.

.. page::

Objetivos Específicos
*********************

- En cuanto al software:

  Se debe diseñar y construir un software que implemente un nodo que:

  - Una vez instalado, el nodo debe ser capaz de arrancar y funcionar tan sólo definiendo en la
    configuración un id único de usuario (ej. email) y la dirección de, al menos,  un presentador.
  - Debe ser capaz de localizar otros nodos en internet o en LAN
  - Debe ser capaz de enviar mensajes a otros nodos, sin importar dónde están, qué IP tienen o en qué puerto están accesibles.
  - Debe ser capaz de recibir mensajes de otros nodos sin que estos sepan dónde están ni tras qué topología de red.
  - Toda la información que necesita un nodo para comunicarse con otro será un UUID del otro nodo, por ejemplo, una dirección
    de correo electrónico.
  - Todas las actividades que ejecute el nodo deberán ser, siempre que sea posible, asíncronas.
  - Debe tener una consola de debug por telnet, que dé acceso al código ejecutándose, con objeto  de debug. 
  - Debe tener un canal TCP para que aplicaciones de terceros se conecten a él y lo manejen a modo de *core*
  - Debe ser *plugeable*. Se podrán añadir fácilmente plugins escritos por terceros.
  - Debe soportar encriptación fuerte por defecto.
  - Debe poder manejarse desde una consola telnet, con un repertorio suficiente de comandos con los que:

      - Invitar a contacto
      - Aceptar invitación
      - Eliminar contacto
      - Enviar un mensaje, plano o encriptado,  a contacto
      - Acceder a los mensajes recibidos
      - Acceder al historial y estado de mensajes enviados

|

- En cuanto a metodología:

  - Profundizar en la planificación de proyectos de software.
  - Utilizar GIT como control de versiones
  - Utilizar Trac como gestor de tickets
  - Hacer uso de algún sistema de Integración Contínua.
  - Generar toda la documentación utlizando RestructuredText para perfecta integración con control de versiones.
 

Motivaciones personales
-----------------------

Si bien, existe un buen número de soluciones de mensajería instantánea y algunas de ellas soportan casi todas las
características deseadas en el presente trabajo, las redes descentralizadas es un tema que me atrae profundamente, 
por lo que desarrollar un trabajo en este contexto, me parece una forma inmejorable de profundizar en el conocimiento  
de las mismas y me ofrece la oportunidad de aportar una pieza de sowftare operativa, basada en mis propios criterios y decisiones.

En concreto, la lectura de un artículo sobre la técnica "UDP Hole Punching" que permite comunicaciones directas entre
equipos que, en principio, no son accesibles, me hizo intesarme en estas cuestiones y tras
realizar algunos experimentos, me asaltó la inquietud de construir algo que "sirviera para algo" alrededor de dicha técnica.

Por otra parte, a lo largo de casi 20  años de experiencia profesional, la experiencia me dice que gran número de las empresas
que se dedican al desarrollo de software están, aún lejos, de aplicar metodologías de ingeniería informática en
sus proyectos.

Incluso empresas de renombre, empujadas casi siempre por los hitos y los *dead lines*, generan una enorme *deuda tecnológica* 
y el trabajo que realizan tiene, en demasiadas ocasiones, una carencia muy grande de calidad, 
tanto en diseño como en implementación.

Esto me motiva a realizar este trabajo en la forma en que me gustaría que mis proveedores lo realizaran.

Personalmente, también me apasiona aprender nuevas técnicas, herramientas y profundizar en cuestiones que tan sólo
he podido rozar en mi experiencia profesional.

.. page:: 

.. include:: requisitos.rst

.. page::

.. include:: implementacion.rst

.. page::

.. include:: punch.rst

.. include:: despues.rst

.. page::

.. include:: faq.rst

