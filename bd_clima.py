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
