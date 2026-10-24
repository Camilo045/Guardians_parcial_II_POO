from abc import ABC, abstractmethod


class Personaje(ABC):
    def __init__(self, nombre, vida, ataque, defensa):
        self.nombre = nombre
        self.vida = vida
        self.ataque = ataque
        self.defensa = defensa

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El nombre debe ser un texto no vacío.")
        self._nombre = valor.strip()

    @property
    def vida(self):
        return self._vida

    @vida.setter
    def vida(self, valor):
        if not isinstance(valor, int) or isinstance(valor, bool) or valor < 0 or valor > 100:
            raise ValueError("La vida debe ser un número entero entre 0 y 100.")
        self._vida = valor

    @property
    def ataque(self):
        return self._ataque

    @ataque.setter
    def ataque(self, valor):
        if not isinstance(valor, int) or isinstance(valor, bool) or valor <= 0:
            raise ValueError("El ataque debe ser un número entero positivo.")
        self._ataque = valor

    @property
    def defensa(self):
        return self._defensa

    @defensa.setter
    def defensa(self, valor):
        if not isinstance(valor, int) or isinstance(valor, bool) or valor < 0:
            raise ValueError("La defensa debe ser un número entero no negativo.")
        self._defensa = valor

    def recibir_danio(self, cantidad):
        if not isinstance(cantidad, int) or isinstance(cantidad, bool) or cantidad < 0:
            raise ValueError("La cantidad de daño no puede ser negativa.")
        vida_anterior = self._vida
        self._vida = max(0, self._vida - cantidad)
        return vida_anterior - self._vida

    def esta_vivo(self):
        return self._vida > 0

    def mostrar_estado(self):
        estado = (
            f"{self._nombre} ({self.__class__.__name__}) - "
            f"Vida: {self._vida} | Ataque: {self._ataque} | Defensa: {self._defensa}"
        )
        print(estado)
        return estado

    def _validar_ataque(self, objetivo):
        if not isinstance(objetivo, Personaje):
            raise ValueError("El objetivo no es un personaje válido.")
        if objetivo is self:
            raise ValueError("Un personaje no puede atacarse a sí mismo.")
        if not self.esta_vivo():
            raise ValueError(f"{self._nombre} está derrotado y no puede atacar.")
        if not objetivo.esta_vivo():
            raise ValueError(f"{objetivo.nombre} ya está derrotado.")

    @abstractmethod
    def atacar(self, objetivo):
        pass


class Guerrero(Personaje):
    def atacar(self, objetivo):
        self._validar_ataque(objetivo)
        ataque_potenciado = int(self.ataque * 1.20)
        danio = max(0, ataque_potenciado - objetivo.defensa)
        return objetivo.recibir_danio(danio)


class Mago(Personaje):
    def atacar(self, objetivo):
        self._validar_ataque(objetivo)
        danio = max(0, self.ataque)
        return objetivo.recibir_danio(danio)


class Arquero(Personaje):
    def atacar(self, objetivo):
        self._validar_ataque(objetivo)
        danio_base = max(0, self.ataque - objetivo.defensa)
        if self.ataque > objetivo.defensa:
            danio = danio_base * 2
        else:
            danio = 0
        return objetivo.recibir_danio(danio)


class Combate:
    def __init__(self, personaje1, personaje2):
        if not isinstance(personaje1, Personaje) or not isinstance(personaje2, Personaje):
            raise ValueError("Ambos participantes deben ser personajes válidos.")
        if personaje1 is personaje2:
            raise ValueError("Un personaje no puede combatir contra sí mismo.")
        if not personaje1.esta_vivo() or not personaje2.esta_vivo():
            raise ValueError("Ambos personajes deben estar vivos para iniciar el combate.")

        self.personaje1 = personaje1
        self.personaje2 = personaje2
        self.atacante = personaje1
        self.defensor = personaje2
        self.turno = 0
        self.ronda = 0
        self.ganador = None
        self.empate_tecnico = False
        self.empate_rondas = False

    def cambiar_turno(self):
        self.atacante, self.defensor = self.defensor, self.atacante

    def verificar_ganador(self):
        if self.personaje1.esta_vivo() and not self.personaje2.esta_vivo():
            self.ganador = self.personaje1
            return self.personaje1
        if self.personaje2.esta_vivo() and not self.personaje1.esta_vivo():
            self.ganador = self.personaje2
            return self.personaje2
        return None

    def mostrar_resultado(self):
        ganador = self.verificar_ganador()
        if ganador is not None:
            resultado = f"Ganador: {ganador.nombre}."
        elif self.empate_tecnico:
            resultado = "Resultado: Empate técnico."
        elif self.empate_rondas:
            resultado = "Resultado: Empate por límite de 50 rondas."
        else:
            resultado = "Resultado: Sin ganador."
        print(resultado)
        return resultado

    def iniciar(self):
        print(f"\nInicio del combate: {self.personaje1.nombre} vs {self.personaje2.nombre}")
        self.personaje1.mostrar_estado()
        self.personaje2.mostrar_estado()
        print("-" * 55)

        danio_ronda = 0
        ataques_en_ronda = 0

        while self.ronda < 50:
            self.turno += 1
            danio = self.atacante.atacar(self.defensor)
            danio_ronda += danio
            ataques_en_ronda += 1

            print(f"Turno {self.turno}: {self.atacante.nombre} ataca a {self.defensor.nombre} (Daño: {danio})")
            self.personaje1.mostrar_estado()
            self.personaje2.mostrar_estado()
            print("-" * 55)

            if self.verificar_ganador() is not None:
                break

            if ataques_en_ronda == 2:
                self.ronda += 1
                if danio_ronda == 0:
                    self.empate_tecnico = True
                    break
                if self.ronda >= 50:
                    self.empate_rondas = True
                    break
                danio_ronda = 0
                ataques_en_ronda = 0

            self.cambiar_turno()

        self.mostrar_resultado()
        return self.ganador

