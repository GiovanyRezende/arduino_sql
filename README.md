# Projeto Arduino-MySQL
*Este projeto cadastra dados eletrônicos oriundos do Arduino em um banco de dados MySQL.* O tema do trabalho é sobre dados climáticos e do ambiente, sendo que o projeto foca, precisamente, nos três seguintes atributos: *temperatura, umidade e luminosidade.* Para ter a conexão do Arduino com o MySQL, foi utilizado o Python como conector. Diferente do [projeto de BD SQL anterior](https://github.com/GiovanyRezende/sql_db_com_python), foi utilizada uma biblioteca diferente, uma vez que anteriormente foi utilizado o SQLite3.

# O circuito no Arduino
Para fazer o circuito, é necessário ter:

|Item|Quantidade|
|-|-|
|Arduino Uno|1|
|Sensor DHT11|1|
|Fotorresistor|1|
|Resistor 10kΩ|1|
|Jumpers|±8|

A montagem é a seguinte (assim como no [projeto da Lógica Fuzzy](https://github.com/GiovanyRezende/fuzzy_arduino/), o sensor DHT11 está sendo representado pelo LM35):

![image](https://github.com/GiovanyRezende/arduino_sql/assets/111097597/ebb5dcde-0a5a-42a0-9ceb-244ac50da558)

# Modelo Conceitual e Lógico do Banco
![image](https://github.com/GiovanyRezende/arduino_sql/assets/111097597/bb1d6049-6bd7-4ec0-9367-1ab0d5f4d765)

![image](https://github.com/GiovanyRezende/arduino_sql/assets/111097597/8a816166-b544-45d0-be48-8d5456cd5a59)

# Modelo Físico do Banco
Há duas tabelas, uma associativa e uma visualização no banco, sendo elas:
|Tabela|
|-|
|tb_clima|
|tb_temp|
|tb_clima_temp|
|vw_dados|

O código do banco pode ser tanto feito no Python quanto no SQL. Eis aqui um exemplo de criação do banco no Python:

```
import mysql.connector as bd

mydb = bd.connect(
user="root",
password=""
)

cursor = mydb.cursor()

cursor.execute("USE db_clima")

cursor.execute('''CREATE TABLE IF NOT EXISTS tb_clima(
    id INT PRIMARY KEY AUTO_INCREMENT,
    temp_celsius FLOAT NOT NULL,
    humid FLOAT NOT NULL,
    taxa_luz FLOAT NOT NULL,
    horario TIME NOT NULL,
    data DATE NOT NULL
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS tb_temp(
    id INT PRIMARY KEY AUTO_INCREMENT,
    classificacao VARCHAR(15) NOT NULL
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS tb_clima_temp(
    id_clima INT,
    id_temp INT,
    valor_fuzzy FLOAT NOT NULL,
    PRIMARY KEY (id_temp, id_clima),
    CONSTRAINT fk_id_clima_clima_temp
    FOREIGN KEY (id_clima) REFERENCES tb_clima (id),
    CONSTRAINT fk_id_temp_clima_temp
    FOREIGN KEY (id_temp) REFERENCES tb_temp (id)
)''')

cursor.execute('''CREATE VIEW vw_dados AS SELECT
                        c.data as data,
                        c.horario as horario,
                        c.temp_celsius as temperatura,
                        c.humid as umidade,
                        c.taxa_luz as luminosidade,
                        t.classificacao as classificacao,
                        ct.valor_fuzzy as fuzzy_temp
                        FROM tb_clima as c
                        INNER JOIN tb_clima_temp as ct
                        ON c.id = ct.id_clima
                        INNER JOIN tb_temp as t
                        ON t.id = ct.id_temp
                        ORDER BY c.data ASC, c.horario ASC''')

mydb.commit()
cursor.close()
mydb.close()
```

# O código do Arduino
O Arduino envia uma linha CSV para a porta serial contendo as informações de temperatura, umidade e luminosidade, como descrito à seguir:
```
#include "dht.h"

const int sensor = A0;
dht DHT;
const int foto = A1;
float temp;
float umid;
int lum;

void setup() {
  Serial.begin(9600);
}

void loop() {
  DHT.read11(sensor);
  temp = DHT.temperature;
  umid = DHT.humidity;
  lum = analogRead(foto);

  Serial.print(temp);
  Serial.print(",");
  Serial.print(umid);
  Serial.print(",");
  Serial.println(lum);
  
  delay(1000);
}
```
Essa linha CSV será processada no Python.

# O código do Python
## Bibliotecas utilizadas e conexão com o banco
```
import mysql.connector as bd
import time
import serial

mydb = bd.connect(
user="",
password="",
)
```
As informações de conexão variam de acordo com o usuário. Por exemplo, o usuário ```root``` não precisa inserir uma senha. Pode ser necessário utilizar o [XAMPP](https://www.apachefriends.org/pt_br/index.html) para criar o servidor.

## Funções de inclusão para Lógica Fuzzy
As funções de inclusão utilizadas no [projeto de Lógica Fuzzy](https://github.com/GiovanyRezende/fuzzy_arduino/) foram utilizadas para cadastrar a classificação de uma temperatura no banco.
```
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
```
A tabela tb_temp foi previamente cadastrada e já foram inseridos as classificações 1 - Frio, 2 - Confortável e 3 - Quente

## Criação do cursor e conexão com a porta USB
```
cursor = mydb.cursor()
cursor.execute("USE db_clima")

ser = serial.Serial("COMx", 9600, timeout=1)
```
O x de "COMx" é o número da porta, por exemplo, a porta utilizada para o projeto foi a COM5. Isso pode ser descoberto de diversas formas, como na própria IDE do Arduino que diz a porta conectada.

## Programação de um horário de termino do cadastro
O Arduino manda dados até ele ser desligado ou desconectado fisicamente, ou seja, funciona como um ```while True```. Por isso, é interessante programar um horário de término da receção de dados de acordo com a preferência e/ou necessidade. Como exemplo, as informações temporais utilizadas foram a hora e o minuto, mas pode ter mais informações como segundo ou dia.
```
hora = int(input("Programe uma hora para terminar o cadastro de dados: "))
minuto = int(input("Programe um minuto para terminar o cadastro de dados: "))

try:
    while (time.localtime().tm_hour <= hora) and (time.localtime().tm_min != minuto):
```
O horário programado é utilizado no ```while``` para definir até quando os dados serão cadastrados.

## A recepção de dados do USB e o cadastro no MySQL
```
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
```
A interessante notar quatro fatos:
- A temperatura é em Celsius;
- O dado de umidade é convertido para porcentagem, ou seja, fica um valor entre 0 e 1;
- O dado de luminosidade também é convertido para porcentagem. No Arduino, esse valor fica entre 0 e 1023, então esse dado é tratado o dividindo por 1023;
- Como pela lógica Fuzzy é possível ter mais de uma classificação (que só muda a intensidade), há condições if para ```Frio```, ```Confortável``` e ```Quente```, o que possibilita uma informação climática ter duas classificações, o que pode ser visto quando se visualiza vw_dados.

Para ver os dados já tratados, se realiza a consulta:
```SELECT * FROM vw_dados;```

<div align= center>

# Redes sociais e formas de contato



[![logo](https://cdn-icons-png.flaticon.com/256/174/174857.png)](https://br.linkedin.com/in/giovanyrezende)
[![logo](https://images.crunchbase.com/image/upload/c_lpad,f_auto,q_auto:eco,dpr_1/v1426048404/y4lxnqcngh5dvoaz06as.png)](https://github.com/GiovanyRezende)[
![logo](https://logospng.org/download/gmail/logo-gmail-256.png)](mailto:giovanyrmedeiros@gmail.com)

</div>
