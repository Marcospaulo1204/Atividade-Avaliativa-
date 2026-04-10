import mysql.connector
from mysql.connector import Error

# Configuração do Banco de Dados
configuracao = {
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "", # Corrigido: password
    "database": "sistema_clientes"
}

def conectar():
    try:
        conexao = mysql.connector.connect(**configuracao)
        return conexao
    except Error as e:
        print(f'ERRO ao conectar: {e}')
        return None

def cadastrar_cliente(nome, cpf, email, telefone, cidade):
    conexao = conectar()
    if not conexao:
        return
    
    cursor = conexao.cursor()
    try:  
        sql = ''' 
            INSERT INTO cliente (nome, cpf, email, telefone, cidade)
            VALUES (%s, %s, %s, %s, %s)
            '''
        valores = (nome, cpf, email, telefone, cidade)
        cursor.execute(sql, valores)
        conexao.commit()
        print(f'Cliente Cadastrado! ID: {cursor.lastrowid}')
    except Error as e:
        if e.errno == 1062: # CPF duplicado
            print('ERRO: CPF já cadastrado.')
        else:
            print(f'ERRO: {e}')
    finally:
        cursor.close()
        conexao.close()

def listar_cliente():
    conexao = conectar()
    if not conexao: 
        return
        
    cursor = conexao.cursor()
    try:
        cursor.execute('''
            SELECT id, nome, cpf, email, telefone, cidade, data_cadastro
            FROM cliente
            ORDER BY nome ASC
        ''')
        
        cliente = cursor.fetchall() 
        print('=' * 70)
        for c in cliente:
            id_val, nome, cpf, email, telefone, cidade, data = c
            print(f'{id_val:<4} {nome:<25} {cidade:<15}')
    except Exception as e:
        print(f"Erro ao listar cliente: {e}")
    finally:
        cursor.close()
        conexao.close()

def buscar_por_nome(nome_busca):
    conexao = conectar()
    if not conexao:
        return
        
    cursor = conexao.cursor()
    try:
        cursor.execute('''
            SELECT id, nome, cpf, cidade
            FROM cliente
            WHERE nome LIKE %s
            ''', (f'%{nome_busca}%',))
        
        resultados = cursor.fetchall()
        for c in resultados:
            print(f'ID {c[0]} | {c[1]} | {c[3]}')
    finally:
        cursor.close()
        conexao.close()

# Função auxiliar para capturar dados da tela
def tela_cadastro():
    nome = input("Nome: ")
    cpf = input("CPF: ")
    email = input("Email: ")
    telefone = input("Telefone: ")
    cidade = input("Cidade: ")
    cadastrar_cliente(nome, cpf, email, telefone, cidade)

def menu():
    while True:
        print('\n' + '=' * 40)
        print('SISTEMA DE CLIENTES')
        print('1. Cadastrar Novo Cliente')
        print('2. Listar Todos Clientes')
        print('3. Buscar por Nome')
        print('0. Sair')
        opcao = input('Escolha: ').strip() # Corrigido: strip() com parênteses

        if opcao == "1":
            tela_cadastro()
        elif opcao == "2":
            listar_clientes()
        elif opcao == "3":
            nome = input('Nome para buscar: ')
            buscar_por_nome(nome)
        elif opcao == '0':
            print("Saindo...")
            break
        else:
            print("Opção inválida!")

if __name__ == '__main__':
    menu()

#funcao buscar_por_cpf()

def buscar_por_cpf(cpf):
    conexao = conectar()
    if not conexao: return None
    cursor = conexao.cursor()
    try:
        cursor.execute ('''
            SELECT id, nome, cpf, email, telefone, cidade
                FROM clientes WHERE cpf = %s
                ''', (cpf,))
        return cursor.fetchone()
    finally:
        cursor.close()
        conexao.close()

