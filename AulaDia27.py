import sqlite3
import random
import time

conn = sqlite3.connect("banco_carga_trabalho.db") # Conecta-se ao banco
cursor = conn.cursor()

# Criação de tabelas
cursor.executescript("""
    CREATE TABLE IF NOT EXISTS contas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        saldo REAL NOT NULL CHECK (saldo >= 0)
    );

    CREATE TABLE IF NOT EXISTS transacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        conta_id INTEGER,
        tipo TEXT CHECK (tipo IN ('deposito', 'saque', 'transferencia')),
        valor REAL NOT NULL,
        destino_id INTEGER NULL,
        data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (conta_id) REFERENCES contas(id),
        FOREIGN KEY (destino_id) REFERENCES contas(id)
    );
""")
conn.commit()

# Cria 100 contas bancárias na tabela contas
cursor.executemany("INSERT INTO contas (nome, saldo) VALUES (?, ?)", [
    (f"Cliente {i}", random.uniform(1000, 10000)) for i in range(1, 101)
])
conn.commit()

print("Banco de dados e contas criados com sucesso!")


# --------------------- FUNÇÃO DE TRANSAÇÃO - INÍCIO DA IMPLEMENTAÇÃO ----------------------------

def processar_transacoes(quantidade=100000, usar_transacao=True):

    # Início do tempo de processamento
    t_inicial = time.time()

    try:
        # Se usar_transacao for verdadeiro, então executar: conn.execute("BEGIN TRANSACTION;")

        if usar_transacao:
            conn.execute("BEGIN TRANSACTION;")

        for _ in range(quantidade):

            # Escolha aleatória da conta origem
            conta_origem = random.randint(1,100)

            # Escolha aleatória da conta destino
            conta_destino = random.randint(1,100)
            
            while conta_destino == conta_origem:
                # Escolha aleatória da conta destino
                conta_destino = random.randint(1,100)
                



            tipo = random.choice(["deposito", "saque", "transferencia"]) # Escolha aleatória do tipo (deposito, saque ou transferencia)
            
            # Escolha aleatória do valor (Ex.: valor entre 10 e 500)
            valor = random.randint(10,500)


            if tipo == "deposito": # Caso tipo == "deposito":
                cursor.execute("UPDATE contas SET saldo = saldo + ? WHERE id = ?", (valor, conta_origem))
                cursor.execute("INSERT INTO transacoes (conta_id, tipo, valor) VALUES (?, ?, ?)",
                               (conta_origem, "deposito", valor))
                if usar_transacao:
                    print("deposito")
                        
                

            # Caso tipo === "saque":
            
            
            if tipo == "saque": # Caso tipo == "deposito":
                cursor.execute("UPDATE contas SET saldo = saldo - ? WHERE id = ? AND ? < saldo", (valor, conta_origem,valor))
                cursor.execute("INSERT INTO transacoes (conta_id, tipo, valor) VALUES (?, ?, ?)",
                               (conta_origem, "saque", valor))
                if usar_transacao:
                    print("saque")



            # Caso tipo === "transferencia":
            if tipo == "transferencia": # Caso tipo == "deposito":
                cursor.execute("UPDATE contas SET saldo = saldo - ? WHERE id = ? AND ? < saldo", (valor, conta_origem, valor))
                cursor.execute("UPDATE contas SET saldo = saldo + ? WHERE id = ?", (valor, conta_destino))
                cursor.execute("INSERT INTO transacoes (conta_id, destino_id, tipo, valor) VALUES (?, ?, ?, ?)",
                               (conta_origem, conta_destino, "transferencia", valor))
                if usar_transacao:
                    print("transf")




        if usar_transacao:
            conn.commit()  # Confirma a transação
    except Exception as e:
        conn.rollback()  # Reverte em caso de erro
        print("Erro:", e)

    # Print do tempo de resposta total em segundos

    print(f"Tempo de resposta: {time.time() - t_inicial} segundos")


# ------------------------ TESTES ------------------------

# Teste sem transações (processar_transacoes)

processar_transacoes(usar_transacao=False)


# Teste com transações (processar_transacoes)

processar_transacoes(usar_transacao=True)



cursor.close()
conn.close()