import pytest
from personajes import Personaje, Guerrero, Mago, Arquero, Combate


# ==========================================
# Pruebas automatizadas para Pytest
# ==========================================

def test_creacion_personajes():
    guerrero = Guerrero("Arthas", 100, 30, 20)
    mago = Mago("Gandalf", 80, 40, 10)
    arquero = Arquero("Legolas", 90, 35, 15)

    assert guerrero.nombre == "Arthas" and guerrero.vida == 100
    assert mago.nombre == "Gandalf" and mago.ataque == 40
    assert arquero.nombre == "Legolas" and arquero.defensa == 15


def test_clase_abstracta():
    with pytest.raises(TypeError):
        Personaje("Base", 100, 20, 10)


def test_rechazo_vida_invalida():
    with pytest.raises(ValueError):
        Guerrero("Arthas", 120, 30, 20)
    with pytest.raises(ValueError):
        Guerrero("Arthas", -10, 30, 20)


def test_rechazo_nombre_vacio():
    with pytest.raises(ValueError):
        Mago("", 80, 40, 10)
    with pytest.raises(ValueError):
        Mago("   ", 80, 40, 10)


def test_rechazo_ataque_y_defensa_invalidos():
    with pytest.raises(ValueError):
        Arquero("Legolas", 90, 0, 15)
    with pytest.raises(ValueError):
        Arquero("Legolas", 90, -5, 15)
    with pytest.raises(ValueError):
        Arquero("Legolas", 90, 35, -1)


def test_habilidad_guerrero():
    guerrero = Guerrero("Arthas", 100, 30, 20)
    objetivo = Guerrero("Orco", 100, 20, 10)
    # 30 * 1.20 = 36 -> 36 - 10 = 26
    danio = guerrero.atacar(objetivo)
    assert danio == 26
    assert objetivo.vida == 74


def test_habilidad_mago():
    mago = Mago("Gandalf", 80, 40, 10)
    objetivo = Guerrero("Golem", 100, 20, 20)
    # Ignora defensa: daño = 40
    danio = mago.atacar(objetivo)
    assert danio == 40
    assert objetivo.vida == 60


def test_habilidad_arquero():
    arquero = Arquero("Legolas", 90, 35, 15)
    objetivo_debil = Guerrero("Bandido", 100, 20, 15)
    objetivo_tanque = Guerrero("Muralla", 100, 20, 40)

    # Ataque (35) > Defensa (15) -> (35 - 15) * 2 = 40
    danio_critico = arquero.atacar(objetivo_debil)
    assert danio_critico == 40
    assert objetivo_debil.vida == 60

    # Ataque (35) <= Defensa (40) -> daño 0
    danio_nulo = arquero.atacar(objetivo_tanque)
    assert danio_nulo == 0
    assert objetivo_tanque.vida == 100


def test_vida_nunca_negativa():
    mago = Mago("Gandalf", 80, 50, 10)
    objetivo = Guerrero("Soldado", 20, 15, 10)
    danio_efectivo = mago.atacar(objetivo)
    assert danio_efectivo == 20
    assert objetivo.vida == 0
    assert not objetivo.esta_vivo()


def test_derrotado_no_puede_atacar():
    caido = Guerrero("Caido", 0, 30, 10)
    objetivo = Mago("Gandalf", 80, 40, 10)
    with pytest.raises(ValueError):
        caido.atacar(objetivo)


def test_combate_completo_y_ganador():
    arthas = Guerrero("Arthas", 100, 30, 20)
    gandalf = Mago("Gandalf", 80, 40, 10)
    combate = Combate(arthas, gandalf)
    ganador = combate.iniciar()

    assert ganador is gandalf
    assert gandalf.vida == 2
    assert arthas.vida == 0
    assert combate.turno == 6


def test_combate_empate_tecnico():
    tanque1 = Guerrero("Tanque 1", 100, 10, 30)
    tanque2 = Guerrero("Tanque 2", 100, 10, 30)
    combate = Combate(tanque1, tanque2)
    ganador = combate.iniciar()

    assert ganador is None
    assert combate.empate_tecnico is True
    assert combate.ronda == 1


# ==========================================
# Ejecución principal de casos de prueba
# ==========================================

def ejecutar_pruebas():
    print("PRUEBAS DEL SISTEMA - GUARDIANS OF THE ANCIENT KINGDOM\n")

    # 1. Creación correcta de los tres tipos de personajes
    print("1. Creación de los tres tipos de personajes:")
    g = Guerrero("Arthas", 100, 30, 20)
    m = Mago("Gandalf", 80, 40, 10)
    a = Arquero("Legolas", 90, 35, 15)
    g.mostrar_estado()
    m.mostrar_estado()
    a.mostrar_estado()

    # 2. Rechazo de personajes con vida superior a 100 o negativa
    print("\n2. Validación de vida fuera de rango:")
    for vida_invalida in (150, -5):
        try:
            Guerrero("Prueba", vida_invalida, 20, 10)
        except ValueError as e:
            print(f"Rechazado (vida={vida_invalida}): {e}")

    # 3. Rechazo de nombres vacíos
    print("\n3. Validación de nombre vacío:")
    try:
        Mago("   ", 80, 30, 10)
    except ValueError as e:
        print(f"Rechazado (nombre vacío): {e}")

    # 4. Rechazo de ataques y defensas inválidos
    print("\n4. Validación de ataque y defensa inválidos:")
    try:
        Arquero("Legolas", 80, 0, 10)
    except ValueError as e:
        print(f"Rechazado (ataque=0): {e}")

    try:
        Arquero("Legolas", 80, 25, -10)
    except ValueError as e:
        print(f"Rechazado (defensa=-10): {e}")

    # 5. Aplicación correcta de la habilidad del Guerrero
    print("\n5. Habilidad del Guerrero (Golpe poderoso):")
    guerrero_prueba = Guerrero("Arthas", 100, 30, 20)
    objetivo_g = Guerrero("Enemigo", 100, 20, 10)
    danio_g = guerrero_prueba.atacar(objetivo_g)
    print(f"Ataque: 30, Defensa rival: 10 -> Daño causado: {danio_g} | Vida restante rival: {objetivo_g.vida}")

    # 6. Aplicación correcta del ataque del Mago ignorando defensa
    print("\n6. Habilidad del Mago (Hechizo penetrante):")
    mago_prueba = Mago("Gandalf", 80, 40, 10)
    objetivo_m = Guerrero("Enemigo", 100, 20, 20)
    danio_m = mago_prueba.atacar(objetivo_m)
    print(f"Ataque: 40, Defensa rival: 20 -> Daño causado: {danio_m} | Vida restante rival: {objetivo_m.vida}")

    # 7. Aplicación correcta del disparo crítico del Arquero
    print("\n7. Habilidad del Arquero (Disparo crítico):")
    arquero_prueba = Arquero("Legolas", 90, 35, 15)
    objetivo_a = Guerrero("Enemigo", 100, 20, 15)
    danio_a = arquero_prueba.atacar(objetivo_a)
    print(f"Ataque: 35, Defensa rival: 15 -> Daño causado: {danio_a} | Vida restante rival: {objetivo_a.vida}")

    # 8. Imposibilidad de tener vida negativa
    print("\n8. Control de vida mínima (no negativa):")
    objetivo_poca_vida = Guerrero("Guardia", 20, 15, 5)
    danio_real = mago_prueba.atacar(objetivo_poca_vida)
    print(f"Vida previa: 20, Ataque recibido: 40 -> Daño efectivo: {danio_real} | Vida actual: {objetivo_poca_vida.vida}")

    # 9. Imposibilidad de atacar estando derrotado
    print("\n9. Imposibilidad de atacar estando derrotado:")
    try:
        objetivo_poca_vida.atacar(mago_prueba)
    except ValueError as e:
        print(f"Ataque bloqueado: {e}")

    # 10 y 11. Ejecución de combate completo e identificación del ganador (Ejemplo del documento)
    print("\n10 y 11. Combate completo (Arthas vs Gandalf):")
    arthas = Guerrero("Arthas", 100, 30, 20)
    gandalf = Mago("Gandalf", 80, 40, 10)
    combate_principal = Combate(arthas, gandalf)
    combate_principal.iniciar()

    # 12. Finalización de un combate sin daño mediante empate técnico
    print("\n12. Combate sin daño (Empate técnico):")
    guardian1 = Guerrero("Guardián Norte", 100, 10, 25)
    guardian2 = Arquero("Guardián Sur", 100, 15, 25)
    combate_empate = Combate(guardian1, guardian2)
    combate_empate.iniciar()


if __name__ == "__main__":
    ejecutar_pruebas()

