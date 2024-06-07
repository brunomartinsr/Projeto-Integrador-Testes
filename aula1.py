from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
import mysql.connector
from mysql.connector import Error
from mysql.connector import ProgrammingError
from tabulate import tabulate


    
root = Tk()

class Funcs():
    def conecta_bd(self):
        #Configuração do banco de dados
        try:
            self.conexao_bd = mysql.connector.connect(
                host="172.16.12.14", # IP do servidor da PUC
                user="BD080324137",
                password="Orinf7",
                database="BD080324137"
            )
            if self.conexao_bd.is_connected():
                self.executor_sql = self.conexao_bd.cursor() #executor de comandos SQL
                print("SUCESSO AO CONECTAR AO BANCO DE DADOS")
        except Error as e:
            print(f'\nERRO AO CONECTAR AO BANCO DE DADOS: {e}\n')
    
    def limpa_tela(self):
        self.codigo_entry.delete(0,END)
        self.nome_entry.delete(0,END)
        self.cidade_entry.delete(0,END)
        self.telefone_entry.delete(0,END)
        
    def variaveis(self):
        self.codigo = self.codigo_entry.get()
        self.nome = self.nome_entry.get()
        self.cidade = self.cidade_entry.get()
        self.telefone = self.telefone_entry.get()    
    
    def inserir(self):
        self.variaveis()
        
        self.executor_sql.execute('INSERT INTO clientes2 (codigo, nome, telefone, cidade) VALUES (%s, %s, %s, %s)', (self.codigo, self.nome, self.cidade, self.telefone))
        
        self.conexao_bd.commit()
        self.selecionar()
        self.limpa_tela()
        
    def selecionar(self):
        self.listaCli.delete(*self.listaCli.get_children())
        self.executor_sql.execute('SELECT codigo, nome, telefone, cidade FROM clientes2 ORDER BY nome ASC')
        resultado = self.executor_sql.fetchall()
        
        for i in resultado:
            self.listaCli.insert("", END, values=i)
            
    def doubleClick(self, event):
        self.limpa_tela()
        self.listaCli.selection()
        
        for n in self.listaCli.selection():
            col1, col2, col3, col4 = self.listaCli.item(n, 'values')
            self.codigo_entry.insert(END, col1)
            self.nome_entry.insert(END, col2)
            self.telefone_entry.insert(END, col3)
            self.cidade_entry.insert(END, col4)
            
    def deleta(self):
        self.variaveis()
        self.executor_sql.execute('DELETE FROM clientes2 WHERE codigo = %s',(self.codigo,))
        self.conexao_bd.commit()
        self.limpa_tela()
        self.selecionar()
    
    def alterar(self):
        self.variaveis()
        self.executor_sql.execute('UPDATE clientes2 SET nome = %s, telefone = %s, cidade = %s WHERE codigo = %s', (self.nome, self.telefone, self.cidade, self.codigo))
        self.conexao_bd.commit()
        self.selecionar()
        self.limpa_tela()
    
class Application(Funcs):
    def __init__(self):
        self.root = root
        self.conecta_bd()
        self.tela()
        self.frames_da_tela()
        self.widgets_frame1()
        self.lista_frame2()
        self.selecionar()
        root.mainloop()
    
    def tela(self):
        self.root.title("Instock")
        self.root.configure(background='#1e3743')
        self.root.geometry("700x500")
        self.root.resizable(True, True)
        self.root.maxsize(width=900, height=700)
        self.root.minsize(width=500, height=400)

    def frames_da_tela(self):
        self.frame_1 = Frame(self.root, bd=4, bg='#dfe3ee', highlightbackground='#759fe6', highlightthickness=3)
        self.frame_1.place(relx= 0.02, rely= 0.02, relwidth= 0.96, relheight= 0.46)
        
        self.frame_2 = Frame(self.root, bd=4, bg='#dfe3ee', highlightbackground='#759fe6', highlightthickness=3)
        self.frame_2.place(relx= 0.02, rely= 0.5, relwidth= 0.96, relheight= 0.46)

    def widgets_frame1(self):
        #botao limpar
        self.bt_limpar = Button(self.frame_1, text='Limpar', bd=2, bg='#107db2', fg='white', font= ('verdana', 8, 'bold'), command=self.limpa_tela)
        self.bt_limpar.place(relx= 0.3, rely= 0.1, relwidth= 0.1, relheight= 0.15)
        
        #botao buscar
        self.bt_buscar = Button(self.frame_1, text='Buscar', bd=2, bg='#107db2', fg='white', font= ('verdana', 8, 'bold'))
        self.bt_buscar.place(relx= 0.4, rely= 0.1, relwidth= 0.1, relheight= 0.15)
        
        #botao novo
        self.bt_novo = Button(self.frame_1, text='Novo', bd=2, bg='#107db2', fg='white', font= ('verdana', 8, 'bold'), command=self.inserir)
        self.bt_novo.place(relx= 0.6,  rely= 0.1, relwidth= 0.1, relheight= 0.15)
        
        #botao alterar
        self.bt_alterar = Button(self.frame_1, text='Alterar', bd=2, bg='#107db2', fg='white', font= ('verdana', 8, 'bold'), command=self.alterar)
        self.bt_alterar.place(relx= 0.7, rely= 0.1, relwidth= 0.1, relheight= 0.15)
        
        #botao apagar
        self.bt_apagar = Button(self.frame_1, text='Apagar', bd=2, bg='#107db2', fg='white', font= ('verdana', 8, 'bold'), command=self.deleta)
        self.bt_apagar.place(relx= 0.8, rely= 0.1, relwidth= 0.1, relheight= 0.15)
        
        #código
        self.lb_codigo = Label(self.frame_1, text= 'Código do produto', bg='#dfe3ee', fg='#107db2')
        self.lb_codigo.place(relx=0.03, rely=0.05)
        
        self.codigo_entry = Entry(self.frame_1)
        self.codigo_entry.place(relx=0.03, rely= 0.15, relwidth= 0.2)  
        
        #nome
        self.lb_nome = Label(self.frame_1, text= 'Nome do produto', bg='#dfe3ee', fg='#107db2')
        self.lb_nome.place(relx=0.03, rely=0.35)
        
        self.nome_entry = Entry(self.frame_1)
        self.nome_entry.place(relx=0.03, rely= 0.45, relwidth= 0.3)
        
        #telefone
        self.lb_telefone = Label(self.frame_1, text= 'Telefone', bg='#dfe3ee', fg='#107db2')
        self.lb_telefone.place(relx=0.03, rely=0.65)
        
        self.telefone_entry = Entry(self.frame_1)
        self.telefone_entry.place(relx=0.03, rely= 0.75, relwidth= 0.4)  
        
        #cidade
        self.lb_cidade = Label(self.frame_1, text= 'Cidade', bg='#dfe3ee', fg='#107db2')
        self.lb_cidade.place(relx=0.5, rely=0.65)
        
        self.cidade_entry = Entry(self.frame_1)
        self.cidade_entry.place(relx=0.5, rely= 0.75, relwidth= 0.4)  
        
    def lista_frame2(self):
        self.listaCli = ttk.Treeview(self.frame_2, height=3, columns=("col1", 'col2', 'col3', 'col4'))
        self.listaCli.place(relx=0.01, rely=0.1, relwidth=0.95, relheight=0.85)
        self.listaCli.heading('#0', text='')
        self.listaCli.heading('#1', text='Código')
        self.listaCli.heading('#2', text='Nome')        
        self.listaCli.heading('#3', text='Telefone')
        self.listaCli.heading('#4', text='Cidade')
        
        self.listaCli.column('#0', width=1)
        self.listaCli.column('#1', width=50)
        self.listaCli.column('#2', width=200)
        self.listaCli.column('#3', width=125)
        self.listaCli.column('#4', width=125)
        
        self.scroolLista = Scrollbar(self.frame_2, orient='vertical')
        self.listaCli.configure(yscroll=self.scroolLista.set)
        self.scroolLista.place(relx= 0.96, rely= 0.1, relwidth= 0.04, relheight= 0.85)
        self.listaCli.bind("<Double-1>", self.doubleClick)
    
Application()



def atualizar(self, cod_produto):
        try:      
            produto = self.retorna_produto(self.codigo_produto_entry.get())

            if produto:
                dado = None
                dado_numerico = False

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
                    opcao = int(self.opcaoEscolhida(menu))

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
                    antigo_valor = produto[opcao]
                    if dado in ['CP', 'CF', 'CV', 'IV', 'ML']:
                        dado_numerico = True
                        novo_valor = self.obter_num_float("Digite o novo valor para esse dado: ")
                    else: novo_valor = self.obter_input("Digite o novo valor para esse dado: ")
                    
                    if antigo_valor == novo_valor:
                        print('\nESSA INFORMAÇÃO JÁ ESTÁ ARMAZENADA!')
                    else:
                        if isinstance(novo_valor, str): #verifica se o valor é uma string
                            novo_valor = f'"{novo_valor}"'
                        self.executor_sql.execute(f'UPDATE PRODUTOS SET {dado} = {novo_valor} WHERE Cod_produto = {cod_produto}')
                        self.conexao_bd.commit()
                        print(f'\nPRODUTO ATUALIZADO!')
                        print(f'{dado} = {antigo_valor} -> {dado} = {novo_valor}')
                        
                        if dado_numerico:
                            produto = self.retorna_produto(cod_produto)
                            self.calcular(produto)
            else: print('\nPRODUTO NÃO EXISTENTE!') 
        except Error as e:
            print(f'\nERRO AO ATUALIZAR PRODUTO: {e}')
            
            valores = [self.CP_entry.get(), self.CF_entry.get(), self.CV_entry.get(), self.IV_entry.get(), self.ML_entry.get()]
 