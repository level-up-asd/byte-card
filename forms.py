from wtforms import Form, validators, StringField, DecimalField, IntegerField, DateField

class CadastraCartaoForm(Form):

    cliente = StringField('Cliente', [
        validators.DataRequired(message='Campo CLIENTE é obrigatório.')
    ])

    limite = DecimalField('Limite', [
        validators.DataRequired(message='Campo LIMITE é obrigatório.'),
        validators.NumberRange(min=0.01, message='Não é um limite válido.')
    ])


class AlteraLimiteForm(Form):

    id = IntegerField('ID', [
        validators.DataRequired(message='É preciso informar o identificador do cartão.'),
        validators.NumberRange(min=1, message='Não é um identificador válido.')
    ])

    limite = DecimalField('Limite', [
        validators.DataRequired(message='Campo LIMITE é obrigatório.'),
        validators.NumberRange(min=0.01, message='Não é um limite válido.')
    ])


class CadastraCompraForm(Form):

    cartao = IntegerField('Cartão', [
        validators.DataRequired(message='Campo CARTÃO é obrigatório.'),
        validators.NumberRange(min=1, message='Não é um cartão válido.')
    ])

    valor = DecimalField('Limite', [
        validators.DataRequired(message='Campo VALOR é obrigatório.'),
        validators.NumberRange(min=0.01, message='Não é um valor válido.')
    ])

    categoria = StringField('Categoria', [
        validators.DataRequired(message='Campo CATEGORIA é obrigatório.')
    ])

    estabelecimento = StringField('Estabelecimento', [
        validators.DataRequired(message='Campo ESTABELECIMENTO é obrigatório.'),
        validators.Length(min=5, message='Campo ESTABELECIMENTO deve ter, no mínimo, 5 caracteres.')
    ])


class VisualizaFaturaForm(Form):
    
    mes_ano = DateField('Selecione o mês', format= '%Y-%m')


class RelatorioGastosPorCategoriaForm(Form):
    
    mes_ano = DateField('Selecione o mês', format= '%Y-%m')

    cartao = IntegerField('Cartão', [
        validators.DataRequired(message='Campo CARTÃO é obrigatório.'),
        validators.NumberRange(min=1, message='Não é um cartão válido.')
    ])


    @property
    def is_valido(self):
        return self.mes_ano.data and self.cartao.data and self.validate()
