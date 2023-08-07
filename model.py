from __future__ import annotations
from typing import List

from sqlalchemy import create_engine
from sqlalchemy import ForeignKey
from sqlalchemy import String, Date, Numeric, DateTime

from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.orm import Mapped

from datetime import date, datetime
from decimal import Decimal

from database import db

class Cartao(db.Model):
    __tablename__ = "cartao"

    id: Mapped[int] = mapped_column(primary_key=True)
    numero: Mapped[str] = mapped_column(String(30))
    cvv: Mapped[str] = mapped_column(String(3))
    
    limite: Mapped[float] = mapped_column(Numeric(precision=15, scale=2))
    validade: Mapped[date] = mapped_column(Date())

    cliente: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(100))

    def __init__(self, **kwargs):
        super().__init__(status='ATIVO', **kwargs)
    
    def cancela(self):
        self.status = 'CANCELADO'

    def ativa(self):
        self.status = 'ATIVO'
    
    @property
    def is_ativo(self):
        return self.status == 'ATIVO'
    
    @property
    def is_cancelado(self):
        return self.status == 'CANCELADO'
    
    def __repr__(self) -> str:
        return f'Cartao(id={self.id!r}, numero={self.numero!r}, cvv={self.cvv!r}, validade={self.validade!r}, limite={self.limite!r}, cliente={self.cliente!r}, status={self.status!r})'



class Compra(db.Model):
    __tablename__ = "compra"

    id: Mapped[int] = mapped_column(primary_key=True)

    valor: Mapped[float] = mapped_column(Numeric(precision=15, scale=2))
    data: Mapped[datetime] = mapped_column(DateTime())
    estabelecimento: Mapped[str] = mapped_column(String(1000))
    categoria: Mapped[str] = mapped_column(String(255))

    cartao_id: Mapped[int] = mapped_column(ForeignKey("cartao.id"))
    cartao: Mapped['Cartao'] = relationship()

    
    def __repr__(self) -> str:
        return f'Compra(id={self.id!r}, valor={self.valor!r}, data={self.data!r}, estabelecimento={self.estabelecimento!r}, categoria={self.categoria!r}, cartao={self.cartao!r})'
    

class Fatura():

    def __init__(self, data, compras):
        self.__mes = data.strftime('%B/%Y')
        self.__compras = compras

        self.__total = None

    
    @property
    def compras(self):
        return self.__compras
    

    @property
    def mes(self):
        return self.__mes
    

    @property
    def total(self):
        if self.__total:
            return self.__total
        
        soma = Decimal(0)
        for c in self.compras:
            soma += c.valor

        self.__total = soma
        return self.__total

    
