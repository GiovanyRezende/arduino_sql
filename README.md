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

```


<div align= center>

# Redes sociais e formas de contato



[![logo](https://cdn-icons-png.flaticon.com/256/174/174857.png)](https://br.linkedin.com/in/giovanyrezende)
[![logo](https://images.crunchbase.com/image/upload/c_lpad,f_auto,q_auto:eco,dpr_1/v1426048404/y4lxnqcngh5dvoaz06as.png)](https://github.com/GiovanyRezende)[
![logo](https://logospng.org/download/gmail/logo-gmail-256.png)](mailto:giovanyrmedeiros@gmail.com)

</div>
