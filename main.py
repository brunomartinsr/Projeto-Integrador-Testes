from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
from mysql.connector import ProgrammingError
from tabulate import tabulate

root = Tk()


class Funcoes():
    
    #função que conecta ao bd    
    def dados_bd(self):
        self.host = "172.16.12.14"
        self.user = "BD080324137"
        self.password = "Orinf7"
        self.database = "BD080324137"
        self.conectar()

    def conectar(self):
        try:
            self.conexao_bd = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.conexao_bd.is_connected():
                self.executor_sql = self.conexao_bd.cursor()  # Executor de comandos SQL
                messagebox.showinfo("Sucesso", "Conexão ao banco de dados realizada com sucesso!")
        except Error as e:
            messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {e}")
            root.destroy() 
    
    #Função para obter o valor de um input
    def obter_input(self, valor):
        while True:           
            if valor.strip():
                return valor
            else:
                resposta = messagebox.showerror("Erro", 'INSIRA UM VALOR VÁLIDO!') 
                if resposta == 'ok':
                    self.erro_window.destroy()
                    return None
                    
    #Função para cadastrar o usuário ou verificar se o mesmo já está cadastrado
    def acessar(self):
        acesso_liberado = False
        while not acesso_liberado:
            try:
                nome_digitado = self.obter_input(self.nome_entry.get())
                senha_digitada = self.obter_input(self.senha_entry.get())

                if nome_digitado is None or senha_digitada is None:
                    continue

                self.executor_sql.execute(f'SELECT * FROM USUARIOS WHERE nome_usuario = "{nome_digitado}"')
                usuario = self.executor_sql.fetchone()

                if usuario:
                    nome_usuario = usuario[0]
                    senha_usuario = usuario[1]

                    while senha_usuario != senha_digitada:
                        resposta = messagebox.showwarning("Senha Incorreta", "Senha incorreta, por favor, tente novamente.")
                        if resposta == 'ok':
                            self.erro_window.destroy()
                            return None
                        senha_digitada = self.obter_input(self.senha_entry.get())

                    messagebox.showinfo("Login", f'Seja bem-vindo ao Instock, {nome_usuario}!')
                    acesso_liberado = True
                    
                    self.frame_menu()                     

                else:
                    resposta = messagebox.askquestion("Usuário não cadastrado", "Usuário não cadastrado, gostaria de realizar o cadastro?")
                    if resposta == 'yes':
                        self.executor_sql.execute(f'insert into USUARIOS (nome_usuario, senha_usuario) values ("{nome_digitado}", "{senha_digitada}")')
                        self.conexao_bd.commit()
                        messagebox.showinfo("Cadastro", "Usuário cadastrado com sucesso!")
                        acesso_liberado = True
                    else: 
                        resposta.destroy()

            except Error as e:
                messagebox.showerror("Erro", f'Erro ao realizar login: {e}')
               
    #Função para verificar se o produto existe no banco de dados
    def retorna_produto(self, cod_produto):
        try:
            cod_produto = int(cod_produto)
            self.executor_sql.execute(f'SELECT * FROM PRODUTOS WHERE Cod_produto = {cod_produto}')
            resultado = self.executor_sql.fetchone()
            if resultado: 
                return resultado
            else: 
                return False
        except Error as e:
            messagebox.showerror('Erro',f'\nERRO AO VERIFICAR PRODUTO, VERIFIQUE SE O CAMPO DO CÓDIGO DO PRODUTO ESTEJA PREENCHIDO E SOMENTE COM VALORES NUMÉRICOS: {e}\n')
            
    #Função que retorna os cálculos de um certo produto
    def retorna_calculos(self, cod_produto):
        try:
            self.executor_sql.execute(f'SELECT * FROM CALCULOS JOIN PRODUTOS ON CALCULOS.cod = PRODUTOS.Cod_produto WHERE PRODUTOS.Cod_produto = {cod_produto}')
            resultado = self.executor_sql.fetchone()
            if resultado: 
                return resultado
            else: 
                return False
        except Error as e:
            print(f'ERRO AO CONSULTAR CÁLCULOS: {e}\n')
                 
    #Função para inserir um produto
    def inserir_produto(self, produto):
        try:
            self.executor_sql.execute(f'insert into PRODUTOS (Cod_produto, Nome_produto, Descricao_produto, CP, CF, CV, IV, ML) values ({produto[0]}, "{produto[1]}", "{produto[2]}", {produto[3]}, {produto[4]}, {produto[5]}, {produto[6]}, {produto[7]})')
            self.conexao_bd.commit()
            messagebox.showinfo('Sucesso', "PRODUTO CADASTRADO COM SUCESSO!")
            resultado = self.calcular(produto)
            return resultado
            
        except Error as e:
            messagebox.showerror('Erro',f'ERRO AO INSERIR PRODUTO: {e}')
                        
    #Função para obter um valor do tipo float em um input  
    def obter_num_float(self, numero):
        while True:
            try:
                valor = float(numero)
                valor = round(valor, 2)
                while valor <= 0:
                    resposta = messagebox.showerror('Erro', 'INSIRA UM VALOR NUMÉRICO POSITIVO E ACIMA DE 0!')
                    if resposta == 'ok':
                        self.erro_window.destroy()
                        return None
                return valor
            except ValueError:
                messagebox.showerror('Erro', 'PREENCHA TODOS OS CAMPOS DE CUSTOS E COM VALORES NUMÉRICO!') 
                if resposta == 'ok':
                    self.erro_window.destroy()
                    return None
            
    def inserir_calculos(self, calculos):
        try:
            self.executor_sql.execute(f'insert into CALCULOS (cod, PV, RB, OC, calculo_custo_aquisicao, calculo_receita_bruta, calculo_custo_fixo, calculo_comissao_vendas, calculo_impostos, calculo_outros_custos, calculo_rentabilidade) values ({calculos[0]}, {calculos[1]}, {calculos[2]}, {calculos[3]}, {calculos[4]}, {calculos[5]}, {calculos[6]}, {calculos[7]}, {calculos[8]}, {calculos[9]}, {calculos[10]})')
            self.conexao_bd.commit()
        except Error as e:
            print(f'\nERRO AO INSERIR CÁLCULOS: {e}\n')
                   
    #Função para atualizar os cálculos de um produto
    def atualizar_calculo(self, cod_calculo, calculo, novo_valor):
        try:
            self.executor_sql.execute(f'UPDATE CALCULOS SET {calculo} = {novo_valor} WHERE cod = {cod_calculo}')
            self.conexao_bd.commit()
        except Error as e:
            print(f'\nERRO AO ATUALIZAR CÁLCULO {calculo}: {e}\n')   
            
    def faixa_lucro(self):         
        #Faixa de lucro do produto
            if self.ML >= 20:
                messagebox.showinfo('Status de rentabilidade', 'Sua classificação de rentabilidade é de nivel ALTO')
            elif self.ML >= 10 and self.ML < 20:
                messagebox.showinfo('Status de rentabilidade', 'Sua classificação de rentabilidade é de nivel MÉDIO')
            elif self.ML > 0 and self.ML < 10:
                messagebox.showinfo('Status de rentabilidade', 'Sua classificação de rentabilidade é de nivel BAIXO')
            elif self.ML == 0:
                messagebox.showinfo('Status de rentabilidade', 'Sua classificação de rentabilidade é de nivel EQUILIBRADO')
            else:
                messagebox.showinfo('Status de rentabilidade', 'Sua classificação de rentabilidade é de PREJUIZO')
    
    #Função para exibir os cálculos de um produto
    def calcular(self, produto):
            cod_produto = produto[0]
            self.CP = produto[3]
            self.CF = produto[4]
            self.CV = produto[5]
            self.IV = produto[6]
            self.ML = produto[7]
            
            self.PV = round((self.CP / (1 - ((self.CF + self.CV + self.IV + self.ML) / 100))), 2) #preço de venda
            self.RB =  self.PV - self.CP #receita bruta
            self.OC = self.CF + self.CV + self.IV #outros custos
            
            self.calculo_custo_aquisicao = round((self.CP / self.PV) * 100, 2) 
            self.calculo_receita_bruta = round((self.RB / self.PV) * 100, 2)
            self.calculo_custo_fixo = round((self.PV * self.CF) / 100, 2)
            self.calculo_comissao_vendas = round((self.CV * self.PV) / 100, 2)
            self.calculo_impostos = round((self.IV * self.PV) / 100, 2)       
            self.calculo_outros_custos = self.calculo_custo_fixo + self.calculo_comissao_vendas + self.calculo_impostos
            self.calculo_rentabilidade = self.RB - self.calculo_outros_custos
            
            calculos = self.retorna_calculos(produto[0])
            
            if calculos:
                self.cod_calculo = calculos[0]
                self.PV_bd = calculos[1]
                self.RB_bd = calculos[2]
                self.OC_bd = calculos[3]
                self.calculo_custo_aquisicao_bd = calculos[4]
                self.calculo_receita_bruta_bd = calculos[5]
                self.calculo_custo_fixo_bd = calculos[6]
                self.calculo_comissao_vendas_bd = calculos[7]
                self.calculo_impostos_bd = calculos[8]
                self.calculo_outros_custos_bd = calculos[9]
                self.calculo_rentabilidade_bd = calculos[10]
                
                if self.PV_bd != self.PV: self.atualizar_calculo(self.cod_calculo, 'PV', self.PV)
                elif self.RB_bd != self.RB: self.atualizar_calculo(self.cod_calculo, 'RB', self.RB)
                elif self.OC_bd != self.OC: self.atualizar_calculo(self.cod_calculo, 'OC', self.OC)
                elif self.calculo_custo_aquisicao_bd != self.calculo_custo_aquisicao: 
                    self.atualizar_calculo(self.cod_calculo, 'calculo_custo_aquisicao', self.calculo_custo_aquisicao)
                elif self.calculo_receita_bruta_bd != self.calculo_receita_bruta: 
                    self.atualizar_calculo(self.cod_calculo, 'calculo_receita_bruta', self.calculo_receita_bruta)
                elif self.calculo_custo_fixo_bd != self.calculo_custo_fixo: 
                    self.atualizar_calculo(self.cod_calculo, 'calculo_custo_fixo', self.calculo_custo_fixo)
                elif self.calculo_comissao_vendas_bd != self.calculo_comissao_vendas: 
                    self.atualizar_calculo(self.cod_calculo, 'calculo_comissao_vendas', self.calculo_comissao_vendas)
                elif self.calculo_impostos_bd != self.calculo_impostos: 
                    self.atualizar_calculo(self.cod_calculo, 'calculo_impostos', self.calculo_impostos)
                elif self.calculo_outros_custos_bd != self.calculo_outros_custos: 
                    self.atualizar_calculo(self.cod_calculo, 'calculo_outros_custos', self.calculo_outros_custos)
                elif self.calculo_rentabilidade_bd != self.calculo_rentabilidade: 
                    self.atualizar_calculo(self.cod_calculo, 'calculo_rentabilidade', self.calculo_rentabilidade)
            else:    
                calculos = [cod_produto, self.PV, self.RB, self.OC, self.calculo_custo_aquisicao, self.calculo_receita_bruta, self.calculo_custo_fixo, self.calculo_comissao_vendas, self.calculo_impostos, self.calculo_outros_custos, self.calculo_rentabilidade]
                self.inserir_calculos(calculos)
                
            tabela_cabecalho = ["DESCRIÇÃO", "VALOR", "%"]
            tabela_resultados = [
                ["A. Preço de Venda", self.PV, "100"],
                ["B. Custo de Aquisição (Fornecedor)", self.CP, self.calculo_custo_aquisicao],
                ["C. Receita Bruta (A-B)", self.RB, self.calculo_receita_bruta],
                ["D. Custo Fixo/Administrativo", self.calculo_custo_fixo, self.CF],
                ["E. Comissão de Vendas", self.calculo_comissao_vendas, self.CV],
                ["F. Impostos", self.calculo_impostos, self.IV],
                ["G. Outros custos (D+E+F)", self.calculo_outros_custos, self.OC],
                ["H. Rentabilidade (C-G)", self.calculo_rentabilidade, self.ML]
            ]  
            # Criar a nova janela (Toplevel)
            nova_janela = Toplevel()
            nova_janela.title('Tabela do produto pesquisado')

            # Criar um widget Text para exibir a tabela
            texto_tabela = Text(nova_janela, height=10, width=50)
            texto_tabela.pack()

            # Inserir os dados na widget Text
            texto_tabela.insert(END, tabulate(tabela_resultados, headers=tabela_cabecalho))

            # Botão para fechar a nova janela
            botao_fechar = Button(nova_janela, text='Fechar', command=lambda: [nova_janela.destroy(), self.faixa_lucro()])
            botao_fechar.pack()

            # Exibir a nova janela
            nova_janela.mainloop()
                                                    
    
    #Função que pega dados do produto caso o usuário escolha cadastrar um produto
    def cadastrar(self, cod_produto):
        dados_inseridos = False
        while not dados_inseridos:
            try:
                produto = self.retorna_produto(cod_produto)
                
                if produto:
                    messagebox.showerror('Erro', 'ESSE CÓDIGO JÁ FOI REGISTRADO!')
        
                nome_produto = self.obter_input(self.nome_produto_entry.get())
                descricao_produto = self.obter_input(self.descricao_produto_entry.get())
        
                #custo do produto
                CP = self.obter_num_float(self.CP_entry.get())
                            
                #custo fixo/administrativo
                CF = self.obter_num_float(self.CF_entry.get())
                                
                #comissão de vendas
                CV = self.obter_num_float(self.CV_entry.get())
                                
                #impostos 
                IV = self.obter_num_float(self.IV_entry.get())
                                
                #rentabilidade
                ML = self.obter_num_float(self.ML_entry.get())
        
                #Pegando dados para inserir na tabela PRODUTOS
                produto = [cod_produto, nome_produto, descricao_produto, CP, CF, CV, IV, ML]
                self.inserir_produto(produto)
                
                dados_inseridos = True
            except ProgrammingError:
                print()             
                
    #Função para consultar todas as informações de um certo produto
    def consultar(self, cod_produto):
            produto = self.retorna_produto(cod_produto)

            if produto:
                nome_produto = produto[1]
                descricao_produto = produto[2]
                CP = produto[3]
                CF = produto[4]
                CV = produto[5]
                IV = produto[6]
                ML = produto[7]
                
                calculos = self.retorna_calculos(cod_produto)
                PV = calculos[1]
                RB = calculos[2]
                OC = calculos[3]
                calculo_custo_aquisicao = calculos[4]
                calculo_receita_bruta = calculos[5]
                calculo_custo_fixo = calculos[6]
                calculo_comissao_vendas = calculos[7]
                calculo_impostos = calculos[8]
                calculo_outros_custos = calculos[9]
                calculo_rentabilidade = calculos[10]

                messagebox.showinfo('Resultado da pesquisa', f'CÓDIGO DO PRODUTO: {cod_produto}\n'
                                    f'NOME DO PRODUTO: {nome_produto}\n'
                                    f'DESCRIÇÃO DO PRODUTO: {descricao_produto}')
                
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
                # Criar a nova janela (Toplevel)
                nova_janela = Toplevel()
                nova_janela.title('Tabela do produto pesquisado')

                # Criar um widget Text para exibir a tabela
                texto_tabela = Text(nova_janela, height=10, width=50)
                texto_tabela.pack()

                # Inserir os dados na widget Text
                texto_tabela.insert(END, tabulate(tabela_resultados, headers=tabela_cabecalho))

                # Botão para fechar a nova janela
                botao_fechar = Button(nova_janela, text='Fechar', command=lambda: [nova_janela.destroy(), self.faixa_lucro()])
                botao_fechar.pack()

                # Exibir a nova janela
                nova_janela.mainloop()
            
            else:
                messagebox.showerror('Erro','ERRO AO CONSULTAR PRODUTO')
            
    #Função para atualizar um produto especifico
    def atualizar(self, cod_produto):
        try:
            self.novo_nome = self.nome_entry.get()
            self.novo_CP = float(self.CP_entry.get())
            self.novo_CF = float(self.CF_entry.get())
            self.novo_CV = float(self.CV_entry.get())
            self.novo_IV = float(self.IV_entry.get())
            self.novo_ML = float(self.ML_entry.get())
            
            print(f"Novos valores: Nome_produto={self.novo_nome} CP={self.novo_CP}, CF={self.novo_CF}, CV={self.novo_CV}, IV={self.novo_IV}, ML={self.novo_ML}")
        
            self.executor_sql.execute('UPDATE PRODUTOS SET Nome_produto=%s, CP = %s, CF = %s, CV = %s, IV = %s, ML = %s WHERE Cod_produto = %s', (self.novo_nome, self.novo_CP, self.novo_CF, self.novo_CV, self.novo_IV, self.novo_ML, cod_produto))
            self.conexao_bd.commit()
            
            produto = self.retorna_produto(cod_produto)
            self.calcular(produto)
            
            messagebox.showinfo('Sucesso', 'Produto atualizado')
        except Error as e:
            print(f'\nERRO AO ATUALIZAR PRODUTO: {e}')
            
    def listar(self):
        self.lista_produtos.delete(*self.lista_produtos.get_children())
        self.executor_sql.execute('SELECT * FROM PRODUTOS ORDER BY cod_produto ASC')
        resultado = self.executor_sql.fetchall()
        
        for i in resultado:
            self.lista_produtos.insert("", END, values=i)
            
    def excluir(self, cod_produto):
        produto = self.retorna_produto(cod_produto)
        if produto:
            resposta = messagebox.askyesno('Atenção', f'Deseja realmente excluir o produto {produto[1]} do estoque?')
            
            if resposta:
                self.executor_sql.execute(f'DELETE FROM PRODUTOS WHERE Cod_produto = {cod_produto}')
                self.conexao_bd.commit()
                messagebox.showinfo('Sucesso', f'O produto {produto[1]} foi excluido com sucesso!')
            else:
                messagebox.showwarning('Cancelando...', 'Operação cancelada! O produto não foi excluído')
        else:
            messagebox.showerror('Erro', 'Produto não encontrado.')
        
    def finalizar(self):
        messagebox.showinfo('Saindo...', 'Obrigado por utilizar o Instock!')
        root.destroy()
    
class Application(Funcoes):
    def __init__(self):
        self.root = root
        self.dados_bd()
        self.tela()
        self.frame_login()
        self.atributos()
        
        root.mainloop()
    
    def tela(self):
        self.root.title("Instock")
        self.root.geometry("700x500")
        self.root.resizable(True, True)
        self.root.maxsize(width = 900, height = 700)
        self.root.minsize(width = 500, height= 400)
        
    def frame_login(self):
        #Frame do login
        self.frame_login = Frame(self.root, bd = 4, bg = '#dfe3ee', highlightbackground= '#759fe6', highlightthickness=3)
        self.frame_login.place(relx= 0.02, rely= 0.02, relwidth= 0.96, relheight= 0.96)
        
        titulo_label = Label(self.frame_login, text="Login", font=("Arial", 16, "bold"), bg='#dfe3ee', fg='#107db2')
        titulo_label.pack(pady=90)
        
        #Nome do usuário
        self.lb_nome = Label(self.frame_login, text= 'Nome', font=("Arial", 10, "bold"),bg='#dfe3ee', fg='#107db2')
        self.lb_nome.place(relx= 0.25, rely= 0.30)
        self.nome_entry = Entry(self.frame_login)
        self.nome_entry.place(relx= 0.25, rely= 0.35, relwidth= 0.5)
        
        #Senha do usuário
        self.lb_senha = Label(self.frame_login, text= 'Senha', font=("Arial", 10, "bold"),bg='#dfe3ee', fg='#107db2')
        self.lb_senha.place(relx= 0.25, rely= 0.45)
        self.senha_entry = Entry(self.frame_login)
        self.senha_entry.place(relx= 0.25, rely= 0.50, relwidth= 0.5)
        
        #Botão entrar
        self.btn_login = Button(self.frame_login, text='Entrar',bd=2, bg='#107db2', fg='white', font= ('verdana', 10, 'bold'), command= self.acessar)
        self.btn_login.place(relx= 0.25, rely= 0.65, relwidth= 0.5, height=30)
    
        
    def frame_menu(self):
        #Frame do menu, aparece logo após o usuário ser liberado
        self.frame_menu = Frame(self.root, bd = 4, bg = '#dfe3ee', highlightbackground= '#759fe6', highlightthickness=3)
        self.frame_menu.place(relx= 0.02, rely= 0.02, relwidth= 0.96, relheight= 0.96)
        
        #Título
        titulo_menu = Label(self.frame_menu, text="Menu", font=("Arial", 18, "bold"), bg='#dfe3ee', fg='#107db2')
        titulo_menu.pack(pady=90)
        
        #Opção de cadastrar
        self.btn_inserir = Button(self.frame_menu, text='Inserir', bd=2, bg='#107db2', fg='white', font= ('verdana', 10, 'bold'), command= self.frame_inserir)
        self.btn_inserir.place(relx= 0.35, rely= 0.35, relwidth= 0.3)
        
        self.btn_consultar = Button(self.frame_menu, text='Consultar', bd=2, bg='#107db2', fg='white', font= ('verdana', 10, 'bold'), command= self.frame_consultar)
        self.btn_consultar.place(relx= 0.35, rely= 0.45, relwidth= 0.3)
        
        self.btn_atualizar = Button(self.frame_menu, text='Atualizar', bd=2, bg='#107db2', fg='white', font= ('verdana', 10, 'bold'), command= self.frame_atualizar)
        self.btn_atualizar.place(relx= 0.35, rely= 0.55, relwidth= 0.3)
        
        self.btn_listar = Button(self.frame_menu, text='Listar', bd=2, bg='#107db2', fg='white', font= ('verdana', 10, 'bold'), command=self.frame_listar)
        self.btn_listar.place(relx= 0.35, rely= 0.65, relwidth= 0.3)
        
        self.btn_excluir = Button(self.frame_menu, text='Excluir', bd=2, bg='#107db2', fg='white', font= ('verdana', 10, 'bold'), command=self.frame_excluir)
        self.btn_excluir.place(relx= 0.35, rely= 0.75, relwidth= 0.3)
        
        self.btn_sair = Button(self.frame_menu, text='Sair', bd=2, bg='#107db2', fg='white', font= ('verdana', 10, 'bold'), command= self.finalizar)
        self.btn_sair.place(relx= 0.35, rely= 0.85, relwidth= 0.3)
        
    def frame_inserir(self):
        # Adicionar um espaçamento
        espacamento = 0.06 
        
        #Frame da função de inserir
        self.frame_inserir = Frame(self.root, bd = 4, bg = '#dfe3ee', highlightbackground= '#759fe6', highlightthickness=3)
        self.frame_inserir.place(relx= 0.02, rely= 0.02, relwidth= 0.96, relheight= 0.96)
        
        #Título
        titulo_inserir = Label(self.frame_inserir, text="Inserir produto",font=("Arial", 18, "bold"), bg='#dfe3ee', fg='#107db2')
        titulo_inserir.place(relx= 0.40, rely= 0.05)
        
        #codigo do produto
        self.lb_codigo_produto = Label(self.frame_inserir, text="Código:", font=("Arial", 10, "bold"),bg='#dfe3ee', fg='#107db2')
        self.lb_codigo_produto.place(relx=0.25, rely=0.15)
        self.codigo_produto_entry = Entry(self.frame_inserir)
        self.codigo_produto_entry.place(relx=0.40, rely=0.15, relwidth=0.3)

        # Nome do produto
        self.lb_nome_produto = Label(self.frame_inserir, text="Nome:", font=("Arial", 10, "bold"),bg='#dfe3ee', fg='#107db2')
        self.lb_nome_produto.place(relx=0.25, rely=0.15 + espacamento)
        self.nome_produto_entry = Entry(self.frame_inserir)
        self.nome_produto_entry.place(relx=0.40, rely=0.15 + espacamento, relwidth=0.3)
        
        #Descrição do produto
        self.lb_descricao_produto = Label(self.frame_inserir, text="Descrição:", font=("Arial", 10, "bold"),bg='#dfe3ee', fg='#107db2')
        self.lb_descricao_produto.place(relx=0.25, rely=0.15 + (2 * espacamento))
        self.descricao_produto_entry = Entry(self.frame_inserir)
        self.descricao_produto_entry.place(relx=0.40, rely=0.15 + (2 * espacamento), relwidth=0.5)
        
        #Custo do produto(CP)
        self.lb_CP = Label(self.frame_inserir, text="Custo do produto (R$):", font=("Arial", 10, "bold"),bg='#dfe3ee', fg='#107db2')
        self.lb_CP.place(relx=0.10, rely=0.15 + (4 * espacamento))
        self.CP_entry = Entry(self.frame_inserir)
        self.CP_entry.place(relx=0.40, rely=0.15 + (4 * espacamento), relwidth=0.2)

        # Custo fixo (CF)
        self.lb_CF = Label(self.frame_inserir, text="Custo fixo (%):", font=("Arial", 10, "bold"),bg='#dfe3ee', fg='#107db2')
        self.lb_CF.place(relx=0.10, rely=0.15 + (5 * espacamento))
        self.CF_entry = Entry(self.frame_inserir)
        self.CF_entry.place(relx=0.40, rely=0.15 + (5 * espacamento), relwidth=0.2)

        # Custo de comissão de vendas (CV)
        self.lb_CV = Label(self.frame_inserir, text="Comissão sobre a venda (%):", font=("Arial", 10, "bold"),bg='#dfe3ee', fg='#107db2')
        self.lb_CV.place(relx=0.10, rely=0.15 + (6 * espacamento))
        self.CV_entry = Entry(self.frame_inserir)
        self.CV_entry.place(relx=0.40, rely=0.15 + (6 * espacamento), relwidth=0.2)

        # Impostos (IV)
        self.lb_IV = Label(self.frame_inserir, text="Valor dos impostos (%):", font=("Arial", 10, "bold"),bg='#dfe3ee', fg='#107db2')
        self.lb_IV.place(relx=0.10, rely=0.15 + (7 * espacamento))
        self.IV_entry = Entry(self.frame_inserir)
        self.IV_entry.place(relx=0.40, rely=0.15 + (7 * espacamento), relwidth=0.2)

        # Rentabilidade (ML)
        self.lb_ML = Label(self.frame_inserir, text="Rentabilidade desejada (%):", font=("Arial", 10, "bold"),bg='#dfe3ee', fg='#107db2')
        self.lb_ML.place(relx=0.10, rely=0.15 + (8 * espacamento))
        self.ML_entry = Entry(self.frame_inserir)
        self.ML_entry.place(relx=0.40, rely=0.15 + (8 * espacamento), relwidth=0.2)

        # Botão calcular
        self.btn_calcular = Button(self.frame_inserir, text='Calcular', bd=2, bg='#107db2', fg='white', font= ('verdana', 10, 'bold'), command=lambda: self.cadastrar(self.codigo_produto_entry.get()))
        self.btn_calcular.place(relx=0.35, rely=0.15 + (10 * espacamento), relwidth=0.3)
        #Botão voltar
        self.btn_voltar = Button(self.frame_inserir, text='Voltar', bd=2, bg='#107db2', fg='white', font= ('verdana', 10, 'bold'), command=lambda: self.voltar(self.frame_inserir, self.frame_menu))
        self.btn_voltar.place(relx=0.05, rely=0.20 + (11.5 * espacamento), relwidth=0.1)
        
    def frame_consultar(self):
        # Adicionar um espaçamento
        espacamento = 0.06 
        
        #Frame da função de inserir
        self.frame_consultar = Frame(self.root, bd = 4, bg = '#dfe3ee', highlightbackground= '#759fe6', highlightthickness=3)
        self.frame_consultar.place(relx= 0.02, rely= 0.02, relwidth= 0.96, relheight= 0.96)
        
        #Título
        titulo_consultar = Label(self.frame_consultar, text="Consultar produto", font=("Arial", 18, "bold"), bg='#dfe3ee', fg='#107db2')
        titulo_consultar.place(relx=0.5, rely=0.15, anchor='center')
        
        #codigo do produto
        self.lb_codigo_produto = Label(self.frame_consultar, text="Digite o código do produto que deseja consultar:", font=("Arial", 10, "bold"),bg='#dfe3ee', fg='#107db2')
        self.lb_codigo_produto.place(relx=0.5, rely=0.40, anchor='center')
        self.codigo_produto_entry = Entry(self.frame_consultar)
        self.codigo_produto_entry.place(relx=0.5, rely=0.50, anchor='center')
        
        self.btn_pesquisar = Button(self.frame_consultar, text='Pesquisar', bd=2, bg='#107db2', fg='white', font= ('verdana', 10, 'bold'), command=lambda: self.consultar(self.codigo_produto_entry.get()))
        self.btn_pesquisar.place(relx=0.5, rely=0.05 + (10 * espacamento), relwidth=0.3, anchor='center')
        
        #Botão voltar
        self.btn_voltar = Button(self.frame_consultar, text='Voltar', bd=2, bg='#107db2', fg='white', font= ('verdana', 10, 'bold'), command=lambda: self.voltar(self.frame_consultar, self.frame_menu))
        self.btn_voltar.place(relx=0.05, rely=0.20 + (11.5 * espacamento), relwidth=0.1)
        
    def pesquisar_dados(self):
        cod_produto = self.codigo_produto_entry.get()
        self.mostrar_dados(cod_produto)
        
    def mostrar_dados(self, cod_produto):
        
        produto = self.retorna_produto(cod_produto)

        if produto:
            Nome_pesquisado = produto[1]
            
            CP_pesquisado = produto[3]
            self.CP_entry.delete(0, END)
            self.CP_entry.insert(END, CP_pesquisado)
            
            CF_pesquisado = produto[4]
            self.CF_entry.delete(0, END)
            self.CF_entry.insert(END, CF_pesquisado)
            
            CV_pesquisado = produto[5]
            self.CV_entry.delete(0, END)
            self.CV_entry.insert(END, CV_pesquisado)
            
            IV_pesquisado = produto[6]
            self.IV_entry.delete(0, END)
            self.IV_entry.insert(END, IV_pesquisado)
            
            ML_pesquisado = produto[7]
            self.ML_entry.delete(0, END)
            self.ML_entry.insert(END, ML_pesquisado)
            
            # Botão Alterar
            self.btn_alterar = Button(self.frame_atualizar, text='Alterar', command=lambda: self.atualizar(cod_produto))
            self.btn_alterar.place(relx=0.35, rely=0.80, relwidth=0.3)
            
        else:
            messagebox.showinfo("Produto não encontrado", "O código do produto não foi encontrado na base de dados.")
                    
    def frame_atualizar(self): 
        espacamento = 0.06
        
        #Frame da função de atualizar
        self.frame_atualizar = Frame(self.root, bd = 4, bg = '#dfe3ee', highlightbackground= '#759fe6', highlightthickness=3)
        self.frame_atualizar.place(relx= 0.02, rely= 0.02, relwidth= 0.96, relheight= 0.96)
        
        #Título
        titulo_atualizar = Label(self.frame_atualizar, text="Atualizar produto", font=("Arial", 18, "bold"), bg='#dfe3ee', fg='#107db2')
        titulo_atualizar.place(relx=0.5, rely=0.05, anchor='center')
        
        #codigo do produto
        self.lb_codigo_produto = Label(self.frame_atualizar, text="Digite o código do produto que deseja atualizar:", font=("Arial", 10, "bold"),bg='#dfe3ee', fg='#107db2')
        self.lb_codigo_produto.place(relx=0.5, rely=0.18, anchor='center')
        self.codigo_produto_entry = Entry(self.frame_atualizar)   
        self.codigo_produto_entry.place(relx=0.5, rely=0.25, relwidth=0.3, anchor='center')
        
        self.lb_editar = Label(self.frame_atualizar, text="Editar valores:", font=("Arial", 10, "bold"),bg='#dfe3ee', fg='#107db2')
        self.lb_editar.place(relx=0.5, rely=0.45, anchor='center')
        
        #Nome do produto
        self.lb_nome = Label(self.frame_atualizar, text="Nome do produto:", font=("Arial", 10, "bold"),bg='#dfe3ee', fg='#107db2')
        self.lb_nome.place(relx=0.10, rely=0.25 + (4 * espacamento))
        self.nome_entry = Entry(self.frame_atualizar)
        self.nome_entry.place(relx=0.40, rely=0.25 + (4 * espacamento), relwidth=0.2)
        
        #Custo do produto(CP)
        self.lb_CP = Label(self.frame_atualizar, text="Custo do produto (R$):", font=("Arial", 10, "bold"),bg='#dfe3ee', fg='#107db2')
        self.lb_CP.place(relx=0.10, rely=0.25 + (5 * espacamento))
        self.CP_entry = Entry(self.frame_atualizar)
        self.CP_entry.place(relx=0.40, rely=0.25 + (5 * espacamento), relwidth=0.2)

        # Custo fixo (CF)
        self.lb_CF = Label(self.frame_atualizar, text="Custo fixo (%):", font=("Arial", 10, "bold"),bg='#dfe3ee', fg='#107db2')
        self.lb_CF.place(relx=0.10, rely=0.25 + (6 * espacamento))
        self.CF_entry = Entry(self.frame_atualizar)
        self.CF_entry.place(relx=0.40, rely=0.25 + (6 * espacamento), relwidth=0.2)

        # Custo de comissão de vendas (CV)
        self.lb_CV = Label(self.frame_atualizar, text="Comissão sobre a venda (%):", font=("Arial", 10, "bold"),bg='#dfe3ee', fg='#107db2')
        self.lb_CV.place(relx=0.10, rely=0.25 + (7 * espacamento))            
        self.CV_entry = Entry(self.frame_atualizar)
        self.CV_entry.place(relx=0.40, rely=0.25 + (7 * espacamento), relwidth=0.2)

        # Impostos (IV)
        self.lb_IV = Label(self.frame_atualizar, text="Valor dos impostos (%):", font=("Arial", 10, "bold"),bg='#dfe3ee', fg='#107db2')
        self.lb_IV.place(relx=0.10, rely=0.25 + (8 * espacamento))
        self.IV_entry = Entry(self.frame_atualizar)
        self.IV_entry.place(relx=0.40, rely=0.25 + (8 * espacamento), relwidth=0.2)

        # Rentabilidade (ML)
        self.lb_ML = Label(self.frame_atualizar, text="Rentabilidade desejada (%):", font=("Arial", 10, "bold"),bg='#dfe3ee', fg='#107db2')
        self.lb_ML.place(relx=0.10, rely=0.25 + (9 * espacamento))
        self.ML_entry = Entry(self.frame_atualizar)
        self.ML_entry.place(relx=0.40, rely=0.25 + (9 * espacamento), relwidth=0.2)    
        
        #Pesquisar
        self.btn_pesquisar = Button(self.frame_atualizar, text='Pesquisar', bd=2, bg='#107db2', fg='white', font= ('verdana', 10, 'bold'), command=lambda: self.mostrar_dados(self.codigo_produto_entry.get()))
        self.btn_pesquisar.place(relx=0.5, rely=0.33, relwidth=0.3, anchor='center')
        
        #Botão voltar
        self.btn_voltar = Button(self.frame_atualizar, text='Voltar', bd=2, bg='#107db2', fg='white', font= ('verdana', 10, 'bold'), command=lambda: self.voltar(self.frame_atualizar, self.frame_menu))
        self.btn_voltar.place(relx=0.05, rely=0.20 + (11.5 * espacamento), relwidth=0.1)
        
    def frame_listar(self):
        espacamento = 0.06
        
        #Frame da função de listar
        self.frame_listar = Frame(self.root, bd = 4, bg = '#dfe3ee', highlightbackground= '#759fe6', highlightthickness=3)
        self.frame_listar.place(relx= 0.02, rely= 0.02, relwidth= 0.96, relheight= 0.96)
        
        #Título
        titulo_listar = Label(self.frame_listar, text="Listar produtos", font=("Arial", 18, "bold"), bg='#dfe3ee', fg='#107db2')
        titulo_listar.place(relx= 0.40, rely= 0.05)
        
        self.lista_produtos = ttk.Treeview(self.frame_listar, height=3, columns=("col1", 'col2', 'col3', 'col4', 'col5', 'col6', 'col7', 'col8'))
        self.lista_produtos.place(relx=0.01, rely=0.15, relwidth=0.95, relheight=0.70)
        self.lista_produtos.heading('#0', text='')
        self.lista_produtos.heading('#1', text='Código')
        self.lista_produtos.heading('#2', text='Nome')        
        self.lista_produtos.heading('#3', text='Descrição')
        self.lista_produtos.heading('#4', text='CP')
        self.lista_produtos.heading('#5', text='CF')
        self.lista_produtos.heading('#6', text='CV')
        self.lista_produtos.heading('#7', text='IV')
        self.lista_produtos.heading('#8', text='ML')
        
        
        self.lista_produtos.column('#0', width=1)
        self.lista_produtos.column('#1', width=50)
        self.lista_produtos.column('#2', width=100)
        self.lista_produtos.column('#3', width=200)
        self.lista_produtos.column('#4', width=50)
        self.lista_produtos.column('#5', width=50)
        self.lista_produtos.column('#6', width=50)
        self.lista_produtos.column('#7', width=50)
        self.lista_produtos.column('#8', width=50)
        
        
        self.scroolLista = Scrollbar(self.frame_listar, orient='vertical')
        self.lista_produtos.configure(yscroll=self.scroolLista.set)
        self.scroolLista.place(relx= 0.96, rely= 0.15, relwidth= 0.04, relheight= 0.70)
        
        #Botão voltar
        self.btn_voltar = Button(self.frame_listar, text='Voltar', bd=2, bg='#107db2', fg='white', font= ('verdana', 10, 'bold'), command=lambda: self.voltar(self.frame_listar, self.frame_menu))
        self.btn_voltar.place(relx=0.05, rely=0.20 + (11.5 * espacamento), relwidth=0.1)
        
        self.listar()
        
    def frame_excluir(self):
        espacamento = 0.06
        
        #Frame da função de listar
        self.frame_excluir = Frame(self.root, bd = 4, bg = '#dfe3ee', highlightbackground= '#759fe6', highlightthickness=3)
        self.frame_excluir.place(relx= 0.02, rely= 0.02, relwidth= 0.96, relheight= 0.96)
        
        #Título
        titulo_excluir = Label(self.frame_excluir, text="Excluir produto", font=("Arial", 18, "bold"), bg='#dfe3ee', fg='#107db2')
        titulo_excluir.place(relx=0.5, rely=0.05, anchor='center')
        
        #codigo do produto
        self.lb_codigo_produto = Label(self.frame_excluir, text="Digite o código do produto que deseja excluir:", font=("Arial", 10, "bold"),bg='#dfe3ee', fg='#107db2')
        self.lb_codigo_produto.place(relx=0.5, rely=0.20, anchor='center')
        self.codigo_produto_entry = Entry(self.frame_excluir)
        self.codigo_produto_entry.place(relx=0.5, rely=0.26, relwidth=0.3, anchor='center')
        
        #Botão excluir
        self.btn_excluir = Button(self.frame_excluir, text='Excluir', bd=2, bg='#107db2', fg='white', font= ('verdana', 10, 'bold'), command=lambda: self.excluir(self.codigo_produto_entry.get()))
        self.btn_excluir.place(relx=0.34, rely=0.32, relwidth=0.3)
        
        #Botão voltar
        self.btn_voltar = Button(self.frame_excluir, text='Voltar', bd=2, bg='#107db2', fg='white', font= ('verdana', 10, 'bold'), command=lambda: self.voltar(self.frame_excluir, self.frame_menu))
        self.btn_voltar.place(relx=0.05, rely=0.20 + (11.5 * espacamento), relwidth=0.1)
        
    def voltar(self, frame, frame_voltar):
        self.frame_atual = frame 
        self.frame_anterior = frame_voltar
        self.frame_atual.destroy()
        self.frame_anterior.lift()
        
    def atributos(self):
        self.CP = 0
        self.CF = 0
        self.CV = 0
        self.IV = 0
        self.ML = 0
        self.PV = 0
        self.RB = 0
        self.OC = 0
        self.calculo_custo_aquisicao = 0
        self.calculo_receita_bruta = 0
        self.calculo_custo_fixo = 0
        self.calculo_comissao_vendas = 0
        self.calculo_impostos = 0
        self.calculo_outros_custos = 0
        self.calculo_rentabilidade = 0
        self.cod_calculo = 0
        self.PV_bd = 0
        self.RB_bd = 0
        self.OC_bd = 0
        self.calculo_custo_aquisicao_bd = 0
        self.calculo_receita_bruta_bd = 0
        self.calculo_custo_fixo_bd = 0
        self.calculo_comissao_vendas_bd = 0
        self.calculo_impostos_bd = 0
        self.calculo_outros_custos_bd = 0
        self.calculo_rentabilidade_bd = 0
        
Application()