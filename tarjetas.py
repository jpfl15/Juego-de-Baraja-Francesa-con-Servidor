import random
import copy

'''
    Programa del juego de la baraja francesa
'''


class Jugador:
    nombre = None
    mano = None
    puntuacion = None

    def __init__(self, nombre, baraja):
        self.nombre = nombre
        self.mano = []
        self.puntuacion = 0
        baraja.guarda_jugador(self)

    def despliega_mano(self, baraja):
        '''
            imprime la mano de un jugador
            recibe: un objeto baraja
        '''
        cartas_mano = []
        #print("\nJugador: " + self.nombre)
        # print("--------------------\n")
        for carta in self.mano:
            cartas = f"{carta.display(baraja.diccionario_cartas)}"
            # print(cartas)
            cartas_mano.append(cartas)
            # Aquí había una línea de puntuación

        return cartas_mano


class Carta:
    valor = None
    figura = None

    def __init__(self, valor, figura):
        self.valor = valor
        self.figura = figura

    def __str__(self):
        return f"{self.valor}-{self.figura}"

    def display(self, dict_cartas):
        '''
            POSIBLEMENTE QUEDE EN DESHUSO
        '''
        carta_cara = dict_cartas[self.valor]
        return f"{carta_cara}-{self.figura}"


class Baraja:
    diccionario_cartas = None
    figuras = None
    lista_cartas = None
    lista_jugadores = None

    def __init__(self):
        # El método Genera_lista_cartas() debe de hacer la lista de 52 cartas
        self.diccionario_cartas = {
            2: "2",
            3: "3",
            4: "4",
            5: "5",
            6: "6",
            7: "7",
            8: "8",
            9: "9",
            10: "10",
            11: "J",
            12: "Q",
            13: "K",
            20: "A",
        }
        # Corazones, Picas, Trébol, Diamante
        self.figuras = ["C", "P", "T", "D"]
        self.lista_cartas = genera_lista_cartas()
        self.lista_jugadores = []

    def genera_mano(self, num_cartas, nombre_jugador):
        '''
            Se genera una nueva lista de cartas revueltas con la cantidad de la mano
            recibe: numero de cartas en mano (int)
            recibe: nombre de jugador (str), uso: "Emilio"
            regresa: una lista de cartas del jugador (list<str>)
        '''
        # debe asignar una mano aleatoriamente a cada uno de los jugadores de la lista

        # busca en la lista el jugador
        for j in self.lista_jugadores:
            if j.nombre == nombre_jugador:
                jugador = j

                jugador.mano = random.sample(self.lista_cartas, num_cartas)

        # Se eliminan las cartas del jugador en la lista de cartas disponibles
                for carta in jugador.mano:
                    self.lista_cartas.remove(carta)

        # ACÁ DEBE HABER UNA FORMA DE REGRESAR LAS CARTAS QUE YA USASTE

                return jugador.mano

    def cambia_mano(self, num_cartas, nombre_jugador):
        '''
            Regresa una mano nueva
            recibe: numero de cartas en mano (int), uso: 5
            recibe: nombre de jugador (str), uso: "Emilio"
            regresa: una lista de cartas del jugador (list<str>)
        '''
        for jugador in self.lista_jugadores:
            if jugador.nombre == nombre_jugador:
                for carta in jugador.mano:
                    # se regresan las cartas a la baraja
                    self.lista_cartas.append(carta)

                jugador.mano = random.sample(
                    self.lista_cartas, num_cartas)  # revolvemos baraja

                for carta in jugador.mano:
                    self.lista_cartas.remove(carta)  # se las damos al jugador

                return jugador.despliega_mano(self)

    def regresa_mano(self, num_cartas, nombre_jugador):
        '''
            Elimina al jugador y regresa su mano
            recibe: numero de cartas en mano (int), uso: 5
            recibe: nombre de jugador (str), uso: "Emilio"
            Regresa un boolean si el jugador ya tenía cartas
        '''
        for jugador in self.lista_jugadores:
            if jugador.nombre == nombre_jugador:
                for carta in jugador.mano:
                    # se regresan las cartas a la baraja
                    self.lista_cartas.append(carta)

                self.lista_jugadores.remove(jugador)

    def guarda_jugador(self, jugador):
        self.lista_jugadores.append(jugador)

    def calcula_puntaje(self):
        '''
            Calcula el puntaje de todos los jugadores
            regresa: diccionario de jugadores con lista de pares y tercias
            dicc["Emilio"] = pares:2, tercias:1
            key = "Emilio", value = [2, 1]
        '''
        # ESTO ES SUPONIENDO QUE LA MANO ESTA ORDENDA
        for jugador in self.lista_jugadores:  # recorremos los jugadores
            dicc_jugadores = dict()
            pares = 0
            tercias = 0
            cartas_repetidas = list()
            valor_temp = int()
            i = 0
            for carta in jugador.mano:  # obtendremos cada carta de cada jugador
                valor = carta.valor
                if i == 0:  # es la primera carta
                    # importante el copiar objeto y no referenciar
                    valor_temp = copy.copy(valor)
                    cartas_repetidas.append(carta)
                    i = 1

                elif valor_temp == valor:  # si la carta anterior es igual a la siguiente
                    cartas_repetidas.append(carta)
                else:
                    if len(cartas_repetidas) > 1:  # no puede ser par o tercia
                        if len(cartas_repetidas) % 2 == 0:  # son pares
                            # la verdad no se si el referenciar sea problema
                            pares += len(copy.copy(cartas_repetidas))/2
                        elif len(cartas_repetidas) % 3 == 0:  # son tercias
                            # la verdad no se si el referenciar sea problema
                            tercias += len(copy.copy(cartas_repetidas))/3

                            cartas_repetidas = list()
                            valor_temp = int()

            dicc_jugadores[jugador.nombre] = [pares, tercias]

        return dicc_jugadores


def genera_lista_cartas():
    ''' 
        genera una lista de todas las cartas de la baraja (52 cartas)
        y regresa una lista de estas
    '''
    lista_cartas = list()
    for i in range(0, 4):
        if i == 0:
            figura = "♥"  # Corazones
        elif i == 1:
            figura = "♠"  # Picas
        elif i == 2:
            figura = "♣"  # Trébol
        elif i == 3:
            figura = "♦"  # Diamante
        for valor in range(2, 15):  # los valores de las cartas empiezan en 2
            if valor == 14:
                valor = 20  # As vale 20
            carta_nueva = Carta(valor, figura)
            lista_cartas.append(carta_nueva)

    return lista_cartas


def genera_jugador(jugador, baraja):
    '''
        genera los jugadores dentro del objeto baraja
        recibe: un nombre de jugador (string)
        recibe: un objeto baraja
    '''
    nombre = Jugador(jugador, baraja)
