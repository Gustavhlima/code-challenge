# Indicium Tech Code Challenge

## Introdução

Este repositório contém a solução para o desafio de código da Indicium Tech, focado em projetos de dados. O objetivo final é demonstrar o conhecimento técnico do candidato em construir uma pipeline dentro das especificações do desafio, incluindo a capacidade de executar uma consulta que mostra os pedidos e seus detalhes. 

## Índice

- Ferramentas Utilizadas
- Etapas do Projeto
- Execução do Projeto

## Ferramentas Utilizadas

As seguintes ferramentas foram usadas para resolver este desafio:

- Scheduler: Airflow
- Data Loader: Embulk (Java-based)
- Database: PostgreSQL
- JDK 8 (instalado via gerenciador de pacotes de aplicativos usando um JDK open source)
- Docker
- WSL emulando Ubuntu no VSCode

## Etapas do Projeto

Antes de iniciar o projeto, foi necessário organizar o ambiente de trabalho para o desafio:

1. Baixar as ferramentas necessárias: Embulk, Airflow, PostgreSQL, JDK 8, Docker.
2. Para melhor utilização do Embulk, foi necessária a instalação do JDK 8.
3. A ferramenta Airflow necessitou da utilização do ambiente Linux para operar. Dessa forma, o projeto foi todo desenvolvido utilizando WSL emulando Ubuntu no VSCode.
4. Utilização do Docker para criação e gerenciamento de containers, possibilitando a realização das tarefas.
5. A versão do Embulk utilizada foi a 0.9.25. Além disso, foram instaladas duas gems necessárias para os plugins do PostgreSQL:
   - embulk-input-postgresql (0.13.2 java)
   - embulk-output-postgresql (0.10.6 java)
6. Com todas as ferramentas instaladas e o ambiente de trabalho organizado e operando, iniciou-se a realização das tarefas exigidas no desafio.
7. Clone deste repositório no VSCode, importando todos os arquivos necessários do projeto.
8. Inicialização dos containers do Docker, criando os parâmetros necessários no docker-compose.yml.
9. Instalação e inicialização do Airflow, usando o ambiente virtual do Python venv.
10. Criação dos códigos usados nas duas DAGs criadas:
   - Um código criando funções necessárias para a DAG principal.
   - A DAG principal que realiza todas as atribuições de ELT requeridas no desafio.
   - Uma DAG para rodar uma query após o fim do processo.
11. Para a implementação de composição de endereços e data dinâmicos, foi utilizado o framework Liquid no Embulk.

## Execução do Projeto

Os passos a seguir seguem exigências de garantias: o passo seguinte deve ser realizado somente se o anterior for bem-sucedido.

Para executar o projeto, siga as etapas abaixo:

1. Certifique-se de que seu ambiente de trabalho está apto para realizar as tarefas do projeto de acordo com as ferramentas utilizadas descritas acima.
2. Clone este repositório na sua máquina local.
3. Instale as ferramentas necessárias (Embulk, Airflow, PostgreSQL, JDK 8) conforme mencionado na seção de Etapas do Projeto. Utilize os links fornecidos para cada ferramenta.
4. Abra os arquivos no VSCode.
5. Implementando os containers no Docker:
   - Verifique se dentro dos arquivos baixados encontra-se o docker-compose.yml, que contém as definições necessárias para implementação.
   - Importante: O projeto roda utilizando as portas padrão do PostgreSQL. Neste caso, as portas 5432 e 5433 são necessárias para que o projeto seja executado fielmente. Verifique se sua máquina não está utilizando essas portas em outra implementação.
   - Tendo garantido a liberação das portas, abra o terminal e execute o comando: `docker-compose up -d`
6. Com o Docker funcionando, passe para a implementação do Airflow. No terminal, digite a seguinte sequência de comandos:
   - Crie um ambiente virtual Python: `python3 -m venv venv`
   - Agora ative o ambiente virtual: `source venv/bin/activate`
   - Agora, você pode notar que o terminal está rodando no ambiente virtual (venv), indicado antes da linha de endereço.
   - Instale o Airflow no ambiente virtual executando o arquivo de instalação install_airflow.sh: `bash install_airflow.sh`
   - Carregue o arquivo setup.sh no ambiente: `source setup.sh`
   - Inicialize o Airflow: `airflow standalone`
   - Nota: Neste momento, este terminal ficará disponível apenas para o Airflow. Ao inicializar o Airflow, ele disponibilizará login e senha para acessar o Airflow no seu navegador.
7. Acesse o Airflow no navegador:
   - Digite o seguinte endereço: localhost:8080
   - O Airflow irá pedir o login e senha que foram disponibilizados no terminal.
8. Uma vez acessado o Airflow, a interface deve mostrar as seguintes DAGs.    
   - ![dags](docs/dags.jpg)
8. A DAG `northwind_elt_dag` que realiza todas as atribuições de ELT deve executar automaticamente.
   - ![dags_exec](docs/dag_executada.jpg)
9. A DAG `final_query_results_dag` que roda a query após o fim do processo precisa ser executada manualmente.
   - ![dags_query](docs/dag_query_exec.jpg)
10. Verifique o resultado no arquivo CSV gerado ao final da task na pasta data/results.


# Indicium Tech Code Challenge

Code challenge for Software Developer with focus in data projects.


## Context

At Indicium we have many projects where we develop the whole data pipeline for our client, from extracting data from many data sources to loading this data at its final destination, with this final destination varying from a data warehouse for a Business Intelligency tool to an api for integrating with third party systems.

As a software developer with focus in data projects your mission is to plan, develop, deploy, and maintain a data pipeline.


## The Challenge

We are going to provide 2 data sources, a PostgreSQL database and a CSV file.

The CSV file represents details of orders from an ecommerce system.

The database provided is a sample database provided by microsoft for education purposes called northwind, the only difference is that the **order_detail** table does not exists in this database you are beeing provided with. This order_details table is represented by the CSV file we provide.

Schema of the original Northwind Database: 

![image](https://user-images.githubusercontent.com/49417424/105997621-9666b980-608a-11eb-86fd-db6b44ece02a.png)

Your challenge is to build a pipeline that extracts the data everyday from both sources and write the data first to local disk, and second to a PostgreSQL database. For this challenge, the CSV file and the database will be static, but in any real world project, both data sources would be changing constantly.

Its important that all writing steps (writing data from inputs to local filesystem and writing data from local filesystem to PostgreSQL database) are isolated from each other, you shoud be able to run any step without executing the others.

For the first step, where you write data to local disk, you should write one file for each table. This pipeline will run everyday, so there should be a separation in the file paths you will create for each source(CSV or Postgres), table and execution day combination, e.g.:

```
/data/postgres/{table}/2024-01-01/file.format
/data/postgres/{table}/2024-01-02/file.format
/data/csv/2024-01-02/file.format
```

You are free to chose the naming and the format of the file you are going to save.

At step 2, you should load the data from the local filesystem, which you have created, to the final database.

The final goal is to be able to run a query that shows the orders and its details. The Orders are placed in a table called **orders** at the postgres Northwind database. The details are placed at the csv file provided, and each line has an **order_id** field pointing the **orders** table.

## Solution Diagram

As Indicium uses some standard tools, the challenge was designed to be done using some of these tools.

The following tools should be used to solve this challenge.

Scheduler:
- [Airflow](https://airflow.apache.org/docs/apache-airflow/stable/installation/index.html)

Data Loader:
- [Embulk](https://www.embulk.org) (Java Based)
**OR**
- [Meltano](https://docs.meltano.com/?_gl=1*1nu14zf*_gcl_au*MTg2OTE2NDQ4Mi4xNzA2MDM5OTAz) (Python Based)

Database:
- [PostgreSQL](https://www.postgresql.org/docs/15/index.html)

The solution should be based on the diagrams below:
![image](docs/diagrama_embulk_meltano.jpg)


### Requirements

- You **must** use the tools described above to complete the challenge.
- All tasks should be idempotent, you should be able to run the pipeline everyday and, in this case where the data is static, the output shold be the same.
- Step 2 depends on both tasks of step 1, so you should not be able to run step 2 for a day if the tasks from step 1 did not succeed.
- You should extract all the tables from the source database, it does not matter that you will not use most of them for the final step.
- You should be able to tell where the pipeline failed clearly, so you know from which step you should rerun the pipeline.
- You have to provide clear instructions on how to run the whole pipeline. The easier the better.
- You must provide evidence that the process has been completed successfully, i.e. you must provide a csv or json with the result of the query described above.
- You should assume that it will run for different days, everyday.
- Your pipeline should be prepared to run for past days, meaning you should be able to pass an argument to the pipeline with a day from the past, and it should reprocess the data for that day. Since the data for this challenge is static, the only difference for each day of execution will be the output paths.

### Things that Matters

- Clean and organized code.
- Good decisions at which step (which database, which file format..) and good arguments to back those decisions up.
- The aim of the challenge is not only to assess technical knowledge in the area, but also the ability to search for information and use it to solve problems with tools that are not necessarily known to the candidate.
- Point and click tools are not allowed.


Thank you for participating!