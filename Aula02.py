import psutil as ps
import time
from tabulate import tabulate
import csv

#Percentual de uso da CPU
def cpu_p():
    return ps.cpu_percent(interval=5)

#Percentual de uso da Memória RAM
def mem_p():
    return ps.virtual_memory().percent

#Percentual de espaço usado no Disco
def disk_p():
    return ps.disk_usage('/').percent

#Quantidade de dados enviados
def data_sent():
    return ps.net_io_counters().bytes_sent/(1024*1024)

#Quantidade de dados recebidos pela Rede
def data_recv():
    return ps.net_io_counters().bytes_recv/(1024*1024)

def period(funcao):
    a = funcao()
    d1 = time.strftime("%Y-%m-%d %H:%M:%S")
    time.sleep(5)
    d2 = time.strftime("%Y-%m-%d %H:%M:%S")
    b = funcao()
    
    return a,b,d1,d2

#CPU
cpu_1, cpu_2, cpu_d1, cpu_d2 = period(cpu_p)

#MEM
mem_1, mem_2, mem_d1, mem_d2 = period(mem_p)

#DISK
disk_1, disk_2, disk_d1, disk_d2 = period(disk_p)

#RECEBIMENTO DE DADOS
recv_1, recv_2, recv_d1, recv_d2 = period(data_recv)

#ENVIO DE DADOS
sent_1, sent_2, sent_d1, sent_d2 = period(data_sent)

data = [
    ('', 'Pre 5 segundos', 'Po"s 5 segundos', 'Data pre 5 segundos', 'Data pos 5 segundos'),
    ('CPU', cpu_1, cpu_2, cpu_d1, cpu_d2),
    ('Memoria', mem_1, mem_2, mem_d1, mem_d2),
    ('Disco', disk_1, disk_2 , disk_d1, disk_d2),
    ('Recebimento de dados', recv_1, recv_2 , recv_d1, recv_d2),
    ('Envio de dados', sent_1, sent_2 , sent_d1, sent_d2)
]

print('--------------------------------------------------------------------------------------------------------------------------------')
print('Uso da CPU: ',cpu_1, '% | Uso da CPU apos 5 segundos: ',cpu_2, '%')
print('Uso da MEM: ',mem_1, '% | Uso da MEM apos 5 segundos: ',mem_2,'%')
print('Uso do DISK: ',disk_1, '% | Uso do DISK apos 5 segundos: ',disk_2, '%')
print('Recebimento de dados: ',recv_1, 'MB | Recebimento de dados apos 5 segundos: ',recv_1, 'MB')
print('Envio de dados: ',sent_1, 'MB | Envio de dados apos 5 segundos: ',sent_1, 'MB \n')

if (cpu_1 or cpu_2)> 70:
    print('ALERTA [MEDIO] - CPU está com uso alto')

if (mem_1 or mem_2)> 85:
    print('ALERTA [CRITICO] - Memoria proxima do limite de uso!')

print(tabulate(data, headers="firstrow", tablefmt="grid"))

with open('CSV/Desafio.csv', mode = 'w', newline= '') as arquivo_csv:
    escritor = csv.writer(arquivo_csv)
    escritor.writerows(data)

print("Dados gravados com sucesso")
