"""
Utilidades matemáticas de conversión para Ingeniería y Producción.
"""
from decimal import Decimal

def calcular_peso_teorico(metros: Decimal, altura_mm: Decimal, gramaje: Decimal) -> Decimal:
    """
    Calcula el peso en Kg basado en área y gramaje.
    Peso_Kg = (Metros * Ancho_Mts * Gramaje_g_m2) / 1000
    """
    if metros <= 0 or altura_mm <= 0 or gramaje <= 0:
        return Decimal("0.0000")
    
    ancho_m = altura_mm / Decimal("1000")
    peso_gr = metros * ancho_m * gramaje
    return (peso_gr / Decimal("1000")).quantize(Decimal("0.0001"))

def calcular_longitud_lineal(piezas: int, pistas: int, avance_mm: Decimal) -> Decimal:
    """
    Determina los metros necesarios para una cantidad de piezas.
    Metros = (Piezas / Pistas) * (Avance_mm / 1000)
    """
    if pistas <= 0 or avance_mm <= 0:
        return Decimal("0.0")
    return (Decimal(piezas) / Decimal(pistas)) * (avance_mm / Decimal("1000"))