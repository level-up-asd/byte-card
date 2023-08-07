from flask import (
    Flask, 
    redirect, 
    render_template, 
    request, 
    flash
)

from database import db
import use_cases
import forms

app = Flask(__name__)
app.secret_key = b'uma-chave-muito-secreta-mesmo-carai'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3307/bytecard'
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)


@app.route('/')
def index():
    return redirect('/cartoes/lista')


@app.route('/cartoes/lista')
def lista_cartoes():
    return render_template('cartao/lista.html', cartoes = use_cases.lista_cartoes())


@app.route('/cartoes/formulario')
def formulario_cartao(form = None):
    return render_template('cartao/formulario.html', form=form)


@app.route('/cartoes/cadastrar', methods=['POST'])
def cadastra_cartao():
    form = forms.CadastraCartaoForm(request.form)
    if form.validate():
        use_cases.cadastra_cartao(form.cliente.data, form.limite.data)
        flash('Cartão cadastrado com sucesso.', 'info')

        return redirect('/cartoes/lista')
    
    return formulario_cartao(form)


@app.route('/cartoes/<id>/cancelar')
def cancela_cartao(id):
    use_cases.cancela_cartao(id)
    return redirect('/cartoes/lista')


@app.route('/cartoes/<id>/ativar')
def ativa_cartao(id):
    use_cases.ativa_cartao(id)
    return redirect('/cartoes/lista')


@app.route('/cartoes/<id>/limite')
def formulario_limite(id, form = None):
    cartao = use_cases.pesquisa_cartao_por_id(id)
    return render_template('cartao/limite.html', cartao=cartao, form=form)


@app.route('/cartoes/alterar-limite', methods=['POST'])
def altera_limite():
    form = forms.AlteraLimiteForm(request.form)
    if form.validate():
        use_cases.define_limite(form.id.data, form.limite.data)
        flash('Limite alterado com sucesso.', 'info')
    
        return redirect('/cartoes/lista')
    
    return formulario_limite(form.id.data, form=form)


@app.route('/compras/formulario')
def formulario_compra(form= None):
    cartoes = use_cases.lista_cartoes()

    return render_template('compra/formulario.html', cartoes=cartoes, form=form)


@app.route('/compras/cadastrar', methods=['POST'])
def cadastra_compra():
    form = forms.CadastraCompraForm(request.form)
    if form.validate():
        use_cases.cadastra_compra(
            form.cartao.data, 
            form.valor.data, 
            form.categoria.data, 
            form.estabelecimento.data
        )

        flash('Compra cadastrada com sucesso.', 'info')
        return redirect('/compras/cadastrar')
    
    return formulario_compra(form)


@app.route('/cartoes/<cartao_id>/fatura')
def formulario_fatura(cartao_id):
    cartao = use_cases.pesquisa_cartao_por_id(cartao_id)
    
    form = forms.VisualizaFaturaForm(request.args)
    dados = {'cartao': cartao}
    
    if form.mes_ano.data and form.validate():
        dados['fatura'] = use_cases.consulta_fatura(cartao, form.mes_ano.data)


    return render_template('cartao/fatura.html', **dados)


@app.route('/relatorios/gastos-por-categoria')
def relatorio_gastos():
    dados = {
        'cartoes': use_cases.lista_cartoes()
    }
    
    form = forms.RelatorioGastosPorCategoriaForm(request.args)
    if form.is_valido:
        relatorio = use_cases.monta_relatorio_gastos_por_categoria(form.mes_ano.data, form.cartao.data)
        dados['relatorio'] = relatorio

    return render_template('relatorio/gastos-por-categoria.html', **dados)



if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)