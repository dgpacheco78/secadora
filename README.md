<h1>Secadora Industrial de Alimentos</h1>

<h2>Objetivo:</h2>
Diseñar e implementar la automatización del proceso del secado de alimentos, en la categoría de frutas y hortalizas.

<h2>Objetivos especificos:</h2>
<ul>
<li>Implementar un sistema converdidor de señales analógicas a digitales mediante Arduino</li>
<li>Desarrollar una aplicación en Python como sistema de control</li>
<li>Enviar los datos de los sensores mediante MQTT a Node-Red</li>
<li>Almacenar los datos de los sensores de una base de datos en MySQL</li>
</ul>

<h2>Introducción:</h2>
<p align = "justify">La deshidrataci  ́on es una operaci  ́on unitaria que tiene como finalidad la remoci  ́on de humedad de un alimento o material a trav  ́es de los principios de transferencia de materia y energ ́ıa. Uno de los principales m  ́etodos de deshidratación esel secado convectivo. El secado en general requiere de la transferencia de energ ́ıa, en cualquiera de sus formas conducci  ́on, convecci  ́on y radiaci  ́on. El secador de charolas tiene como principio el secado convectivo, el aire que ingresa a la c  ́amara de secado, por medio de un ventilador, es calentado por la acci  ́on de resistencias el  ́ectricas, principalmente. El secador de charolas, de la universidad, posee un sistema de control de temperatura y unas rejillas que permiten o bloquean el paso del aire. El secador de charolas se emplea para la remoci  ́on de humedad de productos s  ́olidos o semis  ́olidos, como frutas y hortalizas, productos c ́arnicos, pastas, pur ́es, pelets, etc.

<h2>Material necesario:</h2>
<h3>MAX6675</h3>
<p align = "justify">El MAX6675 es un convertidor Analógico a digital especializado para termopares tipo K. Con este módulo es posible conectar fácilmente un termopar a cualquier microcontrolador a través de una interfaz SPI unidireccional. Dentro de este pequeño circuito se encuentra la electrónica necesaria para amplificar, compensar y convertir a digital el voltaje generado por el termopar, lo que hace muy sencilla la tarea de conectar un termopar a un microcontrolador.

![Esta es una imagen](https://github.com/dgpacheco78/secadora/blob/main/secadora/imagenes/max6675.jpg)

<h3>Especificaciones tecnicas</h3>
<ul>
<li>GND: 0V, Tierra</li>
<li>VCC: +5V</li>
<li>SCK: SPI Clock</li>
<li>CS: SPI Chip Select</li>
<li>SO: SPI Data Output</li>
</ul>

<h2>HX711 Transmisor de celda de carga</h2>
<p align = "justify">El módulo HX711 es un transmisor entre las celdas de carga y un microcontrolador como Arduino/PIC/ESP, permitiendo leer el peso en la celda de manera sencilla. Es compatible con las celdas de carga de 1kg, 5kg, 20kg y 50kg. Utilizado en sistemas de medición automatizada, procesos industriales, industria médica.
  
![Esta es una imagen](https://github.com/dgpacheco78/secadora/blob/main/secadora/imagenes/hx711.jpg)
 
<h3>Especificaciones tecnicas</h3>
<ul>
<li>Rojo: Voltaje de excitación +, E+, VCC</li>
<li>Negro: Voltaje de excitación -, E-, GND</li>
<li>Verde: Amplificador -, Señal -, A-</li>
<li>Blanco: Amplificador +, Señal +, A+</li>
</ul>

<h2>Sensor de efecto Hall</h2>
<p align = "justify">El sensor Hall tiene una salida analógica y otra digital. La salida analógica devuelve una imagen de la medición y la salida digital devuelve un estado alto o bajo en función del umbral dado por el potenciómetro. Puede utilizar uno u otro dependiendo de su aplicación. El módulo puede ser alimentado por la salida de 5V del microcontrolador.
  
![Esta es una imagen](https://github.com/dgpacheco78/secadora/blob/main/secadora/imagenes/efectoHall.png)
 
<h3>Especificaciones tecnicas</h3>
<ul>
<li>S: entrada analogica</li>
<li>G: - GND</li>
<li>+: Vcc, 5V</li>
</ul>

<h2>Servomotor MG995</h2>
<p align = "justify">Es un pequeño actuador rotativo lineal que permite un control preciso de la posición, velocidad y aceleración angular. Este servomotor puede rotar de 0° hasta 180°, su voltaje de operación va desde los 4.8 a 7.2 VDC.
  
![Esta es una imagen](https://github.com/dgpacheco78/secadora/blob/main/secadora/imagenes/servo.jpg)
 
<h3>Especificaciones tecnicas</h3>
<ul>
<li>Cafe: GND</li>
<li>Naranja: Señal de entrada</li>
<li>Rojo: Vcc, 5V</li>
</ul>

<h2>Funcionamiento del sistema:</h2>
El sistema controla el funcionamiento de horno de secado de alimentos. El horno consta de un control manual obsoleto. La automatización es en la perilla que controla la temperatura. Se le instalo un servomotor, con el cual controlamos la posición. De acuerdo a la practica, colocamos el servomotor a 90 grados (la mitad de su movimiento) en la posición correspondiente a 70°C, la cual es la temperatura a la cual trabajan.

![Esta es una imagen](https://github.com/dgpacheco78/secadora/blob/main/secadora/imagenes/secadora.jpg)
![Esta es una imagen](https://github.com/dgpacheco78/secadora/blob/main/secadora/imagenes/secadoraControl.jpg)

Esto se efectua mendiante una interfaz grafica en Node-Red. Cuenta con las siguientes seccione:

<h3>Estado</h3>
En la sección estado se visualiza que esta haciendo el sistema:
<ol>
<li>Precalentando el horno</li>
<li>Recibiendo datos del horno</li>
<li>Paro de emergencia</li>
<li>Fin de ciclo</li>
</ol>

Sección donde se introducen los valores iniciales
<ul>
<li>Temperatura</li>
<li>Tiempo</li>
<li>Muestra</li>
<li>Peso inicial de la muestra</li>
<li>Tiempo transcurrido</li>
</ul>

Botones de acciones del sistema
<ul>
<li>Precalentado: Calienta el horno en la temperatura establecida, para poder iniciar el proceso</li>
<li>Iniciar proceso: Comienza el proceso de secado, durante el tiempo indicado</li>
<li>Paro de emergencia: detiene el proceso en caso de ser requerido</li>
</ul>


![Esta es una imagen](https://github.com/dgpacheco78/secadora/blob/main/secadora/imagenes/node-red1.png)

<h3>Gráficas</h3>

<ul>
<li>Peso: muestra la perdida del peso de la muestra en relación al tiempo, cada muestra se almacena en la base de datos</li>
<li>Temperatura: muestra la variación de la temperatura en el interior del horno, igual cada muestra se almacena en la base de datos</li>
</ul>

![Esta es una imagen](https://github.com/dgpacheco78/secadora/blob/main/secadora/imagenes/node-red2.png)

<h3>Variables</h3>

<ul>
<li>Temperatura actual: muestra la temperatura actual</li>
<li>Velocidad motor (rpm): muestra la variación de la velocidad del ventilador, cada muestra se almacena en la base de datos</li>
</ul>

![Esta es una imagen](https://github.com/dgpacheco78/secadora/blob/main/secadora/imagenes/node-red3.png)

<h2>Resultados</h2>

<h2>Concluciones</h2>
