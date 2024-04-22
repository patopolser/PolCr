# PolCr

PolCr es un lenguaje de programación interpretado desarrollado en Python. Este documento proporciona una breve guía sobre la sintaxis y las características principales de PolCr.

## Condicionales

Los condicionales en PolCr se definen de la siguiente manera:

```polser
si expresion entonces
    expresion

sino_si expresion entonces
    expresion

sino
    expresion

fin
```

## Bucles
Los bucles en PolCr tienen dos formas principales:

### Bucle "Desde"
```
desde variable = numero hasta numero paso numero entonces
    expresion
fin
```

* **variable**: Inicialización de la variable que determinará al bucle.

* **hasta numero**: Número al que tendrá que llegar la variable para dar por finalizado el bucle.

* **paso numero**: Cantidad que se le sumará a la variable en cada iteración (por defecto es 0).

### Bucle "Mientras"
```
mientras condicion entonces
    expresion
fin
```
* **condicion**: Condición a cumplir para seguir ejecutando el bucle.


## Variables
En PolCr, se pueden declarar variables de la siguiente manera:

```
polser nombre = 0         # Int
polser nombre = 0.1       # Float
polser nombre = "asd"     # String
polser nombre = [1, 2, 3] # Lista
polser nombre = fun()     # Función
```
* **nombre**: Nombre de la variable.
* **dato**: Dato de cualquier tipo que se asigna a la variable.

## Operadores Aritméticos (Números)
En PolCr, se pueden utilizar los siguientes operadores aritméticos con números:

```
1 + 1 = 2 # Suma
1 - 1 = 0 # Resta
1 * 1 = 1 # Multiplicación
1 / 1 = 1 # División
1 % 1 = 0 # Resto de la división
1 ^ 1 = 1 # Potenciación
```

## Operadores Aritméticos (Strings)
También se pueden realizar operaciones con strings:
```
"asd" + "asd" = "asdasd" # Concatenación
"asd" * 3 = "asdasdasd"  # Repetición
```

## Operadores Aritméticos (Listas)
Los operadores para listas son los siguientes:

```
[1, 2, 3] - 1 = [1, 3]                     # Borra el elemento en el índice indicado
[1, 2, 3] + 4 = [1, 2, 3, 4]               # Agrega un elemento al final de la lista
[1, 2, 3] * [4, 5, 6] = [1, 2, 3, 4, 5, 6] # Concatena dos listas
[1, 2, 3] / 0 = 1                          # Accede al índice de la lista indicado
```

## Funciones Precompiladas
PolCr incluye varias funciones precompiladas:

* **pout(texto)**: Output
* **pin(texto)**: Input
* **pin_int(texto)**: Int input
* **limpiar()**: Limpia la consola
* **es_numero(objeto)**: Devuelve true o false dependiendo de si el objeto es un número o no
* **es_string(objeto)**: Devuelve true o false dependiendo de si el objeto es una string o no
* **es_lista(objeto)**: Devuelve true o false dependiendo de si el objeto es una lista o no
* **es_funcion(objeto)**: Devuelve true o false dependiendo de si el objeto es una función o no
* **redondear(numero)**: Elimina la parte decimal de un número
* **entero(numero)**: Convierte un número flotante a un número entero

## Funciones
En PolCr, se pueden definir funciones de la siguiente manera:

```
funcion nombre()
    expresion
fin

funcion nombre(a, b) 
    expresion
fin
```

* **nombre**: Nombre de la función.
* **(a, b)**: Parámetros de la función.

# Creditos:

[Let’s Build A Simple Interpreter](https://ruslanspivak.com/lsbasi-part1/)

[CodePulse Tutorial](https://www.youtube.com/playlist?list=PLZQftyCk7_SdoVexSmwy_tBgs7P0b97yD)
