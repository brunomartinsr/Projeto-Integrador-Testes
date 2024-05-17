import mysql.connector
from mysql.connector import Error
from mysql.connector import ProgrammingError
from tabulate import tabulate

#Configuração do banco de dados
try:
    conexao_bd = mysql.connector.connect(
        host="172.16.12.14", # IP do servidor da PUC
        user="BD080324137",
        password="Orinf7",
        database="BD080324137"
    )
    if conexao_bd.is_connected():
        executor_sql = conexao_bd.cursor() #executor de comandos SQL
        print("SUCESSO AO CONECTAR AO BANCO DE DADOS")
except Error as e:
    print(f'\nERRO AO CONECTAR AO BANCO DE DADOS: {e}\n')

#Função para obter o valor de um input
def obter_input(texto):
    valor = input(texto)
    while not valor.strip():
        print('\nINSIRA UM VALOR VÁLIDO!')
        valor = input(texto)
    return valor

#Função para obter um valor do tipo float em um input  
def obter_num_float(numero):
    while True:
        try:
            valor = round(float(input(numero)), 2)
            while valor <= 0:
                print('\nINSIRA UM VALOR NUMÉRICO POSITIVO E ACIMA DE 0!')
                valor = round(float(input(numero)), 2)
            return valor
        except ValueError:
            print('\nINSIRA UM VALOR NUMÉRICO!')

#Função para criar menu de opções
def opcaoEscolhida(mnu):
    print ()

    opcoesValidas=[]
    posicao=0
    while posicao<len(mnu):
        print (posicao+1,') ',mnu[posicao],sep='')
        opcoesValidas.append(str(posicao+1))
        posicao+=1

    print()
    opcao = obter_input('Qual é a sua opção? ')
    while opcao not in opcoesValidas:
        print('\nOPÇÃO INVÁLIDA!')
        opcao = obter_input('Qual é a sua opção? ')
    return opcao

#Função decorativa que exibe a quantidade de '-' (traços) igual o tamanho do texto recebido
def fazer_linhas(string):
    linhas = ''
    for caracter in string:
        linhas += '-'
    print(linhas)

#Função para inserir um produto
def inserir_produto(produto):
    try:
        executor_sql.execute(f'insert into PRODUTOS (Cod_produto, Nome_produto, Descricao_produto, CP, CF, CV, IV, ML) values ({produto[0]}, "{produto[1]}", "{produto[2]}", {produto[3]}, {produto[4]}, {produto[5]}, {produto[6]}, {produto[7]})')
        conexao_bd.commit()
        print()
        print("PRODUTO CADASTRADO COM SUCESSO!")
    except Error as e:
        print(f'\nERRO AO INSERIR PRODUTO: {e}\n')
        
#Função para consultar um dado especifico de um certo produto
def consultar_dado(dado, cod_produto):
    try:
        executor_sql.execute('SELECT column_name FROM information_schema.columns WHERE table_name = "PRODUTOS"')
        colunas_tabela = [item[0] for item in executor_sql.fetchall()]
        
        if dado in colunas_tabela:
            executor_sql.execute(f'SELECT {dado} FROM PRODUTOS WHERE Cod_produto = {cod_produto}')
            resultado = executor_sql.fetchone()
            return resultado[0] #pega o primeiro item dos dados que no caso será o dado solicitado
        else: print(f'\n"{dado}" NÃO EXISTE NA TABELA!')
    except Error as e:
        print(f'\nERRO AO CONSULTAR DADO: {e}\n')

#Função para exibir os cálculos de um produto
def calcular(cod_produto):
    CP = consultar_dado('CP', cod_produto)
    CF = consultar_dado('CF', cod_produto)
    CV = consultar_dado('CV', cod_produto)
    IV = consultar_dado('IV', cod_produto)
    ML = consultar_dado('ML', cod_produto)
        
    PV = round((CP / (1 - ((CF + CV + IV + ML) / 100))), 2) #preço de venda
    RB = PV - CP  #receita bruta
    OC = CF + CV + IV #outros custos
        
    calculo_custo_aquisicao = round((CP / PV) * 100, 2) 
    calculo_receita_bruta = round(((PV - CP) / PV) * 100, 2)
    calculo_custo_fixo = round((PV * CF) / 100, 2)
    calculo_comissao_vendas = round((CV * PV) / 100, 2)
    calculo_impostos = round((IV * PV) / 100, 2)       
    calculo_outros_custos = calculo_custo_fixo + calculo_comissao_vendas + calculo_impostos
    calculo_rentabilidade = calculo_receita_bruta - calculo_outros_custos
        
    #Aqui a gente checa tbm quais dados foram alterados e tal mas acredito que todos os dados seriam, uma opção seria a gente sempre zerar os calculos do produto e re-inserir
    # calculos = [cod_produto, PV, RB, OC, calculo_custo_aquisicao, calculo_receita_bruta, calculo_custo_fixo, calculo_comissao_vendas, calculo_impostos, calculo_outros_custos, calculo_rentabilidade]
    # inserir_calculos(calculos)
        
    print()
    print(f'PRODUTO: {consultar_dado('Nome_produto', cod_produto)}')
    tabela_cabecalho = ["DESCRIÇÃO", "VALOR", "%"]
    tabela_resultados = [
        ["A. Preço de Venda", PV, "100"],
        ["B. Custo de Aquisição (Fornecedor)", CP, calculo_custo_aquisicao],
        ["C. Receita Bruta (A-B)", RB, calculo_receita_bruta],
        ["D. Custo Fixo/Administrativo", calculo_custo_fixo, CF],
        ["E. Comissão de Vendas", calculo_comissao_vendas, CV],
        ["F. Impostos", calculo_impostos, IV],
        ["G. Outros custos (D+E+F)", calculo_outros_custos, OC],
        ["H. Rentabilidade (C-G)", calculo_rentabilidade, ML]
    ]  
    print(tabulate(tabela_resultados, headers = tabela_cabecalho))
                                            
    #Faixa de lucro do produto
    if ML >= 20:
        print('\nSua classificação de rentabilidade é de nivel ALTO')
    elif ML >= 10 and ML < 20:
        print('\nSua classificação de rentabilidade é de nivel MÉDIO')
    elif ML > 0 and ML < 10:
        print('\nSua classificação de rentabilidade é de nivel BAIXO')
    elif ML == 0:
        print('\nSua classificação de rentabilidade é de nivel EQUILIBRADO')
    else:
        print('\nSua classificação de rentabilidade é de PREJUIZO')
    
#Função que pega dados do produto caso o usuário escolha cadastrar um produto
def cadastrar():
    dados_inseridos = False
    while not dados_inseridos:
        try:
            cod_produto = obter_input("\nDigite o código do produto: ") #chave primária
                
            #Verificando se o produto já existe logo no input do código
            executor_sql.execute(f'SELECT * FROM PRODUTOS WHERE Cod_produto = {cod_produto}')
            resultado = executor_sql.fetchone()
            if resultado:
                print("ESSE CÓDIGO JÁ FOI REGISTRADO!")
                continue

            nome_produto = obter_input("Digite o nome do produto: ")
            descricao_produto = obter_input("Digite a descrição do produto: ")

            #custo do produto
            CP = obter_num_float("Digite o custo do produto (R$): ")
                    
            #custo fixo/administrativo
            CF = obter_num_float("Digite o custo do fixo (%): ")
                        
            #comissão de vendas
            CV = obter_num_float("Digite a comissão sobre a venda (%): ")
                        
            #impostos 
            IV = obter_num_float("Digite o valor dos impostos (%): ")
                        
            #rentabilidade
            ML = obter_num_float("Digite a rentabilidade desejada (%): ")

            #Pegando dados para inserir na tabela PRODUTOS
            produto = [cod_produto, nome_produto, descricao_produto, CP, CF, CV, IV, ML]
            inserir_produto(produto)

            calcular(cod_produto)

            dados_inseridos = True

        except ProgrammingError:
            print("DIGITE UM CÓDIGO VÁLIDO!")
            continue

#Função para consultar todas as informações de um certo produto
def consultar():
    try:
        cod_produto = obter_input("\nDigite o código do produto que deseja consultar: ")

        executor_sql.execute(f'SELECT * FROM PRODUTOS WHERE Cod_produto = "{cod_produto}"')
        produto = executor_sql.fetchone()

        if produto:
            print(f'\nCÓDIGO DO PRODUTO: {consultar_dado('Cod_produto', cod_produto)}')
            print(f'NOME DO PRODUTO: {consultar_dado('Nome_produto', cod_produto)}')
            print(f'DESCRIÇÃO DO PRODUTO: {consultar_dado('Descricao_produto', cod_produto)}')
            print(f'CUSTO DO PRODUTO: R$ {consultar_dado('CP', cod_produto)}')
            print(f'CUSTO FIXO DO PRODUTO: {consultar_dado('CF', cod_produto)}%')
            print(f'COMISSÃO DE VENDAS: {consultar_dado('CV', cod_produto)}%')
            print(f'IMPOSTOS DO PRODUTO: {consultar_dado('IV', cod_produto)}%')
            print(f'RENTABILIDADE DO PRODUTO: {consultar_dado('ML', cod_produto)}%')

            calcular(cod_produto)
        else: print('\nPRODUTO NÃO CADASTRADO')

    except Error as e:
        print(f'ERRO AO CONSULTAR PRODUTO: {e}')

#Função para atualizar um produto especifico
def atualizar():
    try:
        cod_produto = obter_input("\nDigite o código do produto que deseja atualizar: ")      
        
        executor_sql.execute(f'SELECT * FROM PRODUTOS WHERE Cod_produto = "{cod_produto}"')
        resultado = executor_sql.fetchone()

        if resultado:
            dado = None
            novo_valor = None

            print('Qual dado você gostaria de atualizar?')
            menu=['Nome do produto',\
                'Descrição do produto',\
                'Custo de produto',\
                'Custo fixo',\
                'Comissão de vendas',\
                'Impostos',\
                'Rentabilidade',\
                'Sair']
            
            while dado == None:
                opcao = int(opcaoEscolhida(menu))

                if opcao == 1:
                    dado = 'Nome_produto'
                elif opcao == 2:
                    dado = 'Descricao_produto'
                elif opcao == 3:
                    dado = 'CP'
                elif opcao == 4:
                    dado = 'CF'
                elif opcao == 5:
                    dado = 'CV'
                elif opcao == 6:
                    dado = 'IV'
                elif opcao == 7:
                    dado = 'ML'
                else: break

            if dado != None:
                antigo_valor = consultar_dado(dado, cod_produto)
                if dado in ['CP', 'CF', 'CV', 'IV', 'ML']:
                    novo_valor = obter_num_float("Digite o novo valor para esse dado: ")
                else: novo_valor = obter_input("Digite o novo valor para esse dado: ")
                
                if antigo_valor == novo_valor:
                    print('\nESSA INFORMAÇÃO JÁ ESTÁ ARMAZENADA!')
                else:
                    if isinstance(novo_valor, str): #verifica se o valor é uma string
                        novo_valor = f'"{novo_valor}"'
                    executor_sql.execute(f'UPDATE PRODUTOS SET {dado} = {novo_valor} WHERE Cod_produto = {cod_produto}')
                    conexao_bd.commit()
                    print(f'\nPRODUTO ATUALIZADO!')
                    print(f'{dado} = {antigo_valor} -> {dado} = {novo_valor}')
                    
                    if dado in ['CP', 'CF', 'CV', 'IV', 'ML']:
                        calcular(cod_produto)
                    
        else: print('\nPRODUTO NÃO EXISTENTE!') 
    except Error as e:
        print(f'\nERRO AO ATUALIZAR PRODUTO: {e}')

#Função para listar todos os produtos do banco de dados
def listar():
    try:
        executor_sql.execute('SELECT * FROM PRODUTOS')
        produtos = [produto for produto in executor_sql.fetchall()]
        
        if len(produtos) > 0:
            for dados_produto in produtos:
                cod_produto = dados_produto[0]
                print(f'\nCÓDIGO DO PRODUTO: {consultar_dado('Cod_produto', cod_produto)}')
                print(f'NOME DO PRODUTO: {consultar_dado('Nome_produto', cod_produto)}')
                print(f'DESCRIÇÃO DO PRODUTO: {consultar_dado('Descricao_produto', cod_produto)}')
                print(f'CUSTO DO PRODUTO: R$ {consultar_dado('CP', cod_produto)}')
                print(f'CUSTO FIXO DO PRODUTO: {consultar_dado('CF', cod_produto)}%')
                print(f'COMISSÃO DE VENDAS: {consultar_dado('CV', cod_produto)}%')
                print(f'IMPOSTOS DO PRODUTO: {consultar_dado('IV', cod_produto)}%')
                print(f'RENTABILIDADE DO PRODUTO: {consultar_dado('ML', cod_produto)}%')
        else: print('\nVOCÊ NÃO POSSUE PRODUTOS!')
    except Error as e:
        print(f'\nERRO AO LISTAR PRODUTOS: {e}\n')

#Função para excluir um produto especifico
def excluir():
    try:
        cod_produto = obter_input("\nDigite o código do produto que deseja excluir: ")
        executor_sql.execute(f'SELECT * FROM PRODUTOS WHERE Cod_produto = {cod_produto}')
        resultado = executor_sql.fetchone()

        if resultado:
            print(f'\nCÓDIGO DO PRODUTO: {consultar_dado('Cod_produto', cod_produto)}')
            print(f'NOME DO PRODUTO: {consultar_dado('Nome_produto', cod_produto)}')

            resposta = obter_input('\nGOSTARIA DE EXCLUIR O PRODUTO ACIMA? [S/N]: ').upper()
            while resposta not in ['S', 'N']:
                print('\nDIGITE SOMENTE OPÇÕES ENTRE "S" e "N"!')
                resposta = obter_input('\nGOSTARIA DE EXCLUIR O PRODUTO ACIMA? [S/N]:').upper()
            if resposta == 'S':
                executor_sql.execute(f'DELETE FROM PRODUTOS WHERE Cod_produto = {cod_produto}')
                conexao_bd.commit()
                print('\nPRODUTO EXCLUÍDO COM SUCESSO!')
        else: print('\nPRODUTO NÃO EXISTENTE!')
    except Error as e:
        print(f'\nERRO AO EXCLUIR PRODUTO: {e}\n')

def acessar():
    acesso_liberado = False
    while not acesso_liberado:
        try:
            nome_digitado = obter_input('Nome de usuário: ').lower()
            senha_digitada = obter_input('Senha: ').lower()

            executor_sql.execute(f'SELECT * FROM USUARIOS WHERE nome_usuario = "{nome_digitado}"')
            usuario = executor_sql.fetchone()

            if usuario:
                nome_usuario = usuario[0]
                senha_usuario = usuario[1]

                while senha_usuario != senha_digitada:
                    print('\nSENHA INCORRETADA\n')
                    senha_digitada = obter_input('Senha: ').lower()

                print(f'\nSEJA BEM-VINDO AO INSTOCK {nome_usuario}')
                acesso_liberado = True
            else: 
                print('\nUSUÁRIO NÃO CADASTRADO!\n')

                resposta = obter_input('GOSTARIA DE REALIZAR O CADASTRO? [S/N]: ').upper()
                while resposta not in ['S', 'N']:
                    print('\nDIGITE SOMENTE OPÇÕES ENTRE "S" e "N"!')
                    resposta = obter_input('\nGOSTARIA DE REALIZAR O CADASTRO? [S/N]: ').upper()

                if resposta == 'S':
                    executor_sql.execute(f'insert into USUARIOS (nome_usuario, senha_usuario) values ("{nome_digitado}", "{senha_digitada}")')
                    conexao_bd.commit()
                    print('\nUSUÁRIO CADASTRADO!\n')
                    print(f'SEJA BEM-VINDO AO INSTOCK {nome_digitado}')
                    acesso_liberado = True
        except Error as e:
            print(f'\nERRO AO REALIZAR LOGIN: {e}\n') 
        except KeyboardInterrupt:
            print("\nPROGRAMA INTERROMPIDO!\n")



#Inicio do programa
acessar()
print('PARA INICIARMOS ESCOLHA UMA DAS OPÇÕES ABAIXO:')

menu=['CADASTRAR PRODUTO',\
      'CONSULTAR PRODUTO',\
      'ATUALIZAR PRODUTO',\
      'LISTAR PRODUTOS',\
      'EXCLUIR PRODUTO',\
      'SAIR']

opcao=666
while opcao!=6:
    try: 
        opcao = int(opcaoEscolhida(menu))
    
        if opcao==1:
            cadastrar()
    
        elif opcao==2:
            consultar()
    
        elif opcao==3:
            atualizar()
    
        elif opcao==4:
            listar()
    
        elif opcao==5:
            excluir()
    except KeyboardInterrupt:
        print("\nPROGRAMA INTERROMPIDO!\n")

print('\nOBRIGADO POR UTILIZAR O PROGRAMA!\n')