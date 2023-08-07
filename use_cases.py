from sqlalchemy import select, text
from random import randint
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

from database import db

from model import Cartao, Compra, Fatura

class EntidadeNaoEncontradaException(Exception):
    pass


def lista_cartoes():
    comando = select(Cartao).order_by(Cartao.cliente, Cartao.numero)
    resultado = db.session.scalars(comando)

    return list(resultado)


def cria_numero_do_cartao():
    grupos_de_numeros = [f'{randint(1, 9999):04}' for i in range(4)]
    return ' '.join(grupos_de_numeros)


def cadastra_cartao(cliente, limite):
    numero = cria_numero_do_cartao()
    cvv = f'{randint(1, 999):03}'

    validade = date.today() + relativedelta(years=4, months=6, day=31)
    cartao = Cartao(numero=numero, validade=validade, cvv=cvv, limite=limite, cliente=cliente)

    db.session.add(cartao)
    db.session.commit()


def pesquisa_cartao_por_id(id):
    return db.session.get(Cartao, id)


def altera_status_cartao(id, operacao):
    cartao = pesquisa_cartao_por_id(id)
    operacao(cartao)

    db.session.commit()


def ativa_cartao(id):
    altera_status_cartao(id, lambda c: c.ativa())


def cancela_cartao(id):
    altera_status_cartao(id, lambda c: c.cancela())


def define_limite(id, limite):
    cartao = pesquisa_cartao_por_id(id)
    cartao.limite = limite

    db.session.commit()


def cadastra_compra(cartao_id, valor, categoria, estabelecimento):
    cartao = pesquisa_cartao_por_id(cartao_id)
    if not cartao:
        raise EntidadeNaoEncontradaException
    
    
    agora = datetime.now()
    compra = Compra(valor=valor, categoria=categoria, estabelecimento=estabelecimento, cartao=cartao, data=agora)
    
    db.session.add(compra)
    db.session.commit()


def consulta_fatura(cartao, data):
    inicio_mes = data + relativedelta(day=1)
    fim_mes = data + relativedelta(day=31)

    
    consulta = select(Compra)                   \
        .filter(Compra.cartao_id == cartao.id)  \
        .filter(Compra.data >= str(inicio_mes)) \
        .filter(Compra.data <= str(fim_mes))    \
        .order_by(Compra.data)
    
    resultado = db.session.scalars(consulta)
    return Fatura(compras=list(resultado), data=data)


def monta_relatorio_gastos_por_categoria(data, cartao):
    consulta = ("select categoria, sum(valor) valor "
                   "from compra "
                  "where cartao_id = :cartao_id "
                    "and year(data) = :ano "
                    "and month(data) = :mes "
                  "group by categoria "
                  "order by categoria")
    
    resultado = db.session.execute(text(consulta), {'cartao_id': cartao, 'ano': data.year, 'mes': data.month})
    
    registros = resultado.mappings().all()
    
    total = 0
    for registro in registros:
        total += registro['valor']

    return {
        'gastos': registros,
        'total_gasto': total
    }