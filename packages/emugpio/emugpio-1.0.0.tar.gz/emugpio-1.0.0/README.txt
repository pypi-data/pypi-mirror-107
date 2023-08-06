Libreria EmuGpio Version 1.0 Final 

*****************************************************************
Autor: Claudio Ravagnan - Escuela Tecnica Rojas(Buenos Aires)
Licencia: GNU GPL v3+
*****************************************************************

===================
CARACTERISTICAS
===================

EmuGpio(Emulador Gpio de 8 puertos digitales) es una libreria en python que permite emular el funcionamiento de una gpio 8 puertos digitales
(por ahora solo salidas) programables desde paython. Es un proyecto educativo que permite con instrucciones simples ver el funcionamiento de una gpio
y ejercitar diferentes situaciones como puede ser el encendido de una serie de leds.

EmuGpio es el paso previo para después utilizar PHI2, el modulo en python que permite controlar un arduino nano desde python, dando el paso
de una emulador gpio a la utilización de la gpio de arduino, todo controilado y sincronizado desde la pc con Python

==================
INSTALACION:
=================

Localmente(sin Internet):    pip install emugpio-3.1.5.tar.gz     --> La version puede variar

	*********************************************************
	Para desisntalar pip uninstall pemugpio-3.1.5.tar.gz
	*********************************************************

Internet: pip install emugpio


*************************************
Esquema de Entradas y Salidas
*************************************

init("Nombre de Proyecto") 
Permite habilitar 8 puertos numerados del 8 al 1  cuyo estado inician en Cerrado (C) y su valor digital sin definir (X)

openOutputPort(D) --> Abre los puertos indicados como de Salida e inicializa su valor digital a 0. D debe ser un numero decimal
                      entre 0 t 255 que convertido a binario servirá para definir que puerto abrir como de salida. Aquella
                      posición que tenga un 1 abrirá el puerto correspondinte. Por ejemplo: OpenOutputPort(36) 36= 00100100
                                                                                                        Puerto --> 87654321
                                                                                                      Abiertos -->   6  3


writePort(D) --> Escribe en forma paralela sobre los puertos. D es un numero decimal que convertido a binario establece
                 según la posición de cada digito el valor de cada puerto. Por ejemplo writePort(6) 6=00000110 
											   Puerto --> 87654321
											   Salida --> XX0XX1XX
	         Observar que solo se escribe en los puertos definidos como salida.


