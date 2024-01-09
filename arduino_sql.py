import mysql.connector as bd
import time
import serial

mydb = bd.connect(
user="root",
password=""
)

def frio(x):
    if x <= 12:
        return 1
    elif x > 12 and x < 21:
        return round((21-x)/(21-12),2)
    else:
        return 0

def confortavel(x):
    if x > 12 and x < 21:
        return round((x-12)/(21-12),2)
    elif x >= 21 and x <= 24:
        return 1
    elif x > 24 and x < 33:
        return round((33-x)/(33-24),2)
    else:
        return 0

def quente(x):
    if x > 24 and x < 33:
        return round((x-24)/(33-22),2)
    elif x >= 33:
        return 1
    else:
        return 0

cursor = mydb.cursor()
cursor.execute("USE db_clima")

ser = serial.Serial("COM5", 9600, timeout=1)

#tb_temp já foi previamente cadastrada com as classificações 1 - Frio, 2 - Confortável e 3 - Quente

hora = int(input("Programe uma hora para terminar o cadastro de dados: "))
minuto = int(input("Programe um minuto para terminar o cadastro de dados: "))

try:
    while (time.localtime().tm_hour <= hora) and (time.localtime().tm_min != minuto):
        line = ser.readline().decode('utf-8').strip()
        dados = line.split(',')
        if dados != ['']:
            try:
                cadastro_clima = '''INSERT INTO tb_clima (
                    temp_celsius,
                    humid,
                    taxa_luz,
                    horario,
                    data
                ) VALUES (%s,%s,%s,CURTIME(),CURDATE())'''
                valores_clima = (float(dados[0]), float(dados[1]) / 100, round(int(dados[2]) / 1023, 2))
                cursor.execute(cadastro_clima, valores_clima)

                try:
                    cursor.execute('''SELECT MAX(id) FROM tb_clima''')
                    id_clima = cursor.fetchone()[0]
                    cursor.execute('''SELECT temp_celsius FROM tb_clima WHERE id = %s''', (id_clima,))
                    temperatura = cursor.fetchone()[0]

                    cadastro_temp = '''INSERT INTO tb_clima_temp VALUES (%s,%s,%s)'''
                    if frio(temperatura) > 0:
                        cursor.execute(cadastro_temp, (id_clima, 1, frio(temperatura)))
                    if confortavel(temperatura) > 0:
                        cursor.execute(cadastro_temp, (id_clima, 2, confortavel(temperatura)))
                    if quente(temperatura) > 0:
                        cursor.execute(cadastro_temp, (id_clima, 3, quente(temperatura)))
                except Exception as e:
                    print(f"Deu erro na tentativa de cadastrar a associativa: {e}")
                    ser.close()
                else:
                    mydb.commit()
            except Exception as e:
                print(f"Deu erro no cadastro de dados climáticos: {e}")
                ser.close()
            else:
                mydb.commit()
except Exception as e:
    print(f"Deu erro na recepção de dados: {e}")
    ser.close()
else:
    cursor.close()
    mydb.close()
    ser.close()
    print("Procedimento concluído!")
