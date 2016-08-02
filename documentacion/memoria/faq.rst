F.A.Q
=====

Qué significa ZOE ?
-------------------

Zoe es el nombre de mi hija de tres años.

Por qué python ?
----------------

Es cierto que python no es un lenguaje extendido en ambientes empresariales, pero cada
vez son más los desarrolladores que apuestan por él debido a sus virtudes, como 

- OpenSource:

  Python es un lenguaje OpenSource.

- Productividad:

  El tamaño del código en python para realizar la misma tarea es varias veces menor que en otros
  lenguajes.

  Al no ser compilado, se evita el ciclo típico de edición/compilación/prueba, pasando directamente
  de edición a prueba.

- Legibilidad:

  El código de python es muy legible, gracias a su organización tabulada y a la aplicación de PEP8

- Sencillez:

  Python es un lenguaje muy fácil de aprender. El famoso programa "hello world":

  En python:

  .. code-block:: python

     print "hello world"

  En C++:

  .. code-block:: python

     #include <iostream>
     using namespace std;

     int main() {
        cout << "Hola Mundo" << endl;
     return 0;
     }

  En java:

  .. code-block:: python

    public class HelloWorld {

    public static void main(String[] args) {
        System.out.println("Hello, World");
    }
    }

- Multiplataforma:

  Al ser un lenguaje interpretado, las aplicaciones python pueden correr en cualquier plataforma
  que tenga python instalado.

- Modo consola:

  Python proporciona una consola sobre la que se pueden probar rápidamente sus funcionalidades.

  Adicionalmente, mediante una librería, se puede acceder "en caliente" a las entrañas de una
  aplicación python ejecutándose.

- Librerías:

  Existen cientos si no miles de librerías para python.

- El Zen de python [#zen]_:

 .. class:: table-cita:

  - Bello es mejor que feo.
  - Explícito es mejor que implícito.
  - Simple es mejor que complejo.
  - Complejo es mejor que complicado.
  - Plano es mejor que anidado.
  - Disperso es mejor que denso.
  - La legibilidad cuenta.
  - Los casos especiales no son tan especiales como para quebrantar las reglas.
  - Aunque lo práctico gana a la pureza.
  - Los errores nunca deberían dejarse pasar silenciosamente.
  - A menos que hayan sido silenciados explícitamente.
  - Frente a la ambigüedad, rechaza la tentación de adivinar.
  - Debería haber una -y preferiblemente sólo una- manera obvia de hacerlo.
  - Aunque esa manera puede no ser obvia al principio a menos que usted sea holandés.15
  - Ahora es mejor que nunca.
  - Aunque nunca es a menudo mejor que ya mismo.
  - Si la implementación es difícil de explicar, es una mala idea.
  - Si la implementación es fácil de explicar, puede que sea una buena idea.
  - Los espacios de nombres (namespaces) son una gran idea ¡Hagamos más de esas cosas!

Por qué no se ha incluido un GUI ?
----------------------------------

El objetivo de este trabajo es diseñar y desarrollar un "core" completamente operativo que sea
capaz de intercambiar mensajes entre peers de forma directa ( sin que la información pase por servidores )
y encriptada.

Como criterio de diseño, el core dispone, a la manera de mldonlkey,  una consola telnet y un 
sistema de plugins que permite
que el GUI esté completamente desacoplado del mismo y que pueda ser desarrollado por terceros
de la forma que más convenga. De hecho, se pueden desarrollar múltiples GUIs con diferentes 
tecnologías.

Por qué no se ha implementado para dispositivos móviles como Android o iPhone ?
-------------------------------------------------------------------------------

No es objetivo de este trabajo realizar una aplicación para android o iPhone, sino diseñar,
desarrollar y validar una tecnología de comunicaciones.

En este sentido, linux es, a juicio del autor, el mejor "ambiente" para ello.

No obstante, se ha evitado utilizar funcionalidades específicas de linux y en el código
escrito no se han utilizado facilidades propias de python como funciones lambda [#lambda]_ o generadores
yield [#yield]_, de manera que el código sea fácilmente portable a cualquier plataforma.

.. [#lambda] `lambda en python <http://www.secnetix.de/olli/Python/lambda_functions.hawk>`_
.. [#yield] `yield en python <http://www.linuxtopia.org/online_books/programming_books/python_programming/python_ch18.html>`_

Cómo se puede evitar la sobrecarga en las comunicaciones ?
----------------------------------------------------------

Existen dos motivos fundamentales para que ZOE añada una gran sobrecarga a las comunicaciones:

- Por una parte, el protocolo de prueba suministrado -Zoe- se limita a hacer una serialización
  del mensaje enviado y los datos necesarios para la cabecera del protocolo.

  Es muy sencillo derivar otro protocolo más eficiente que sea binario.

- Por otra parte, la encriptación fuerte RSA de 512 bits y la firma de los mensajes hace que
  los datagramas enviados sean mucho mayores que el payload.

  Posibles soluciones pasan por, o bien no encriptar si no es necesario o bien negociar una
  clave AES, encriptada con RSA y, a partir de ahí, utilizar esa clave AES.

Es necesario que exista un Presentador ?
-----------------------------------------  

El presentador es necesario siempre que se necesiten traspasar NATs.  Independientemente
de que un nodo especifique cual ha de ser su puerto UDP, ese puerto será distinto una vez
que sus mensajes salgan a internet.

La IP pública se podría conocer de otras formas, pero la única forma de conocer el puerto
UDP por el que se sale es que exista un nodo -el presentador- que tenga un puerto UDP 
accesible y así obtenga la dirección física.

Además, el presentador es el que pone en conocimiento a dos nodos que se quieren conectar,
enviándoles un pequeño datagrama a ambos con información de contacto del otro extremo.

En cualquier caso, todos los nodos de ZOE son presentadores en potencia. Sólo es necesario
que utilicen un puerto UDP conocido y accesoble.

Y no es, entonces, un SPOF el Presentador?
------------------------------------------

En la implementación actual es imprescindible un presentador para que los nodos puedan
localizarse. Pero si se tiene en cuenta que todos los nodos son presentadores si sus puertos
udp fueran accesibles, resulta fácil poder desplegar una red de confianza donde siempre
existan presentadores "vivos".

En ambiente LAN se podría utilizar una técnica de broadcast para localizar otros nodos de ZOE
en la red local, sin dependencia de presentador, pero no es del alcance de este trabajo.

En ambiente internet, los presentadores se podrían publicar, por ejemplo, en una red DHT o
en un cluster de "servidores de presentadores" de forma que se garantizara la localización
de ellos.

Si existiera un sólo presentador conocido, ciertamente sería un SPOF.

Cual es el modelo de negocio de ZOE?
------------------------------------

Pese a que este trabajo comenzaba hablando sobre la batalla entre las empresas por dominar
el mercado de los mensajes OTT, la vocación de Zoe no es ser una solución empresarial. 
Está concebido para que la gente pueda comunicarse de forma privada entre ellos, sin que 
sus mensajes y contenidos pasen por ningún servidor susceptible de ser espiado o comprometido.

Pero se puede hacer: si se quisiera establecer algún modelo de negocio sobre ZOE, podría pasar
por desplegar Presentadores que ofrecieran funcionalidades atractivas a los usuarios. En
este contexto, el modelo de negocio podría consistir en cobrar cuotas por servicios o
tener ingresos por publicidad.


ZOE sirve para localizar contenidos otros nodos unidos a la red ?
------------------------------------------------------------------ 

No por defecto. Zoe proporciona un core que es capaz de enviar y recibir mensajes a contactos
de confianza, sin necesidad de conocer a priori sus direcciones, traspasando NATs y cortafuegos y 
de forma encriptada. 

Pero puede ser extendido fácilmente para localizar y compartir contenido expuesto por los contactos.


Si la comunicación es P2P, qué pasa si dos nodos no coinciden conectados en la misma ventana de tiempo ?
--------------------------------------------------------------------------------------------------------

Los mensajes no llegarán jamás. 

Esto puede resolverse fácilmente en futuras ampliaciones de este trabajo, de manera que los contactos
elegidos puedan ser "rely" de mensajes que no son para ellos. De esta forma se incrementa la 
posibilidad de que los mensajes prosperen.

Por qué no se intercambian las claves públicas en la invitación/aceptación ?
----------------------------------------------------------------------------

Un ataque "Man in the middle" [#man_middle] podría interceptar las comunicaciones y proporcionar
su propia clave pública. Ese atacante podría interceptar las comunicaciones posteriormente
encriptadas y pasarlas de un extremo a otro sin que ninguno se percatara de ello.

Por eso, las claves públicas se deben intercambiar por algún método seguro garantizado.
 

Qué hace falta para empezar a usar ZOE ?
----------------------------------------

- Deben existir, al menos, dos nodos y

- Tener python instalado.
- Copiar los ficheros de ZOE en el equipo a utilizar.
- Editar el fichero config.cfg e indicar:

  - id ( normalmente una dirección de correo propio )
  - Puerto UDP si es que está accesible -bien directamente o porque se ha podido hacer un NAT en el router)
  - IP:puerto del presentador ( al menos uno de los dos nodos debe hacer de presentador )

- Arrancar zoe: ./zoe.py
- En tanto existan GUIs, utilizar la consola telnet para operar.

.. note::

  Puesto que, en principio, no existen Autoridades Presentadoras, la única forma de garantizar 
  la privacidad en las comunicaciones es enviando por un canal seguro ( en mano, email, otros ...)
  nuestra clave publica <email>.pub a los contactos que vayamos invitar o por los que seamos invitados.

.. note::

  Como futuras ampliaciones de este trabajo, se podría implementar un instalador que minimice
  las tareas de configuración
















































  




