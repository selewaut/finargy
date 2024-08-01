from pydantic import BaseModel
from typing import List, Dict
import datetime


class Puntas(BaseModel):
    cantidad_compra: int
    precio_compra: float
    precio_venta: int
    cantidad_venta: float

class Simbolo(BaseModel):
    simbolo : str
    puntas = Puntas
    ultimo_precio: float
    variacion_porcentual: float
    apertura: float
    cierre: float
    maximo: float
    minimo: float
    ultimo_cierre: float
    volumen: int
    fecha: datetime.datetime
    tipo_opcion: str
    mercad: str
    moneda: str
    descripcion: str
    plazo: str
    lamina_minima: str
    lote : int






