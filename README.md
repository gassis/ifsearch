# IFSearch

<p align="center">
  <img width="210" height="180" src="/ifsearch.png">
</p>

O IFSearch é uma ferramenta de busca em documentos do IFG que são publicados oficialmente no [**Boletim de Serviços**](https://www.ifg.edu.br/boletim-de-servico).  Em virtude da dificuldade na busca por palavras em cada um dos documentos disponíveis, este sistema oferece uma interface a partir da qual os usuários poderão simplesmente digitar um termo de interesse como nomes próprios (pessoas, empresas,...), datas e quaisquer outras palavras.


Para instruções de como baixar os arquivos necessários à instalação do sistema a partir do Git, siga os passos descritos no link abaixo:

https://docs.github.com/pt/github/creating-cloning-and-archiving-repositories/cloning-a-repository


## Windows

Faça o download e instalação do Docker Compose seguindo as instruções abaixo:

   https://docs.docker.com/compose/install/
   
   
   
## Linux

### Usando o APT


Faça o download e instalação do Docker Compose usando o gerenciador de instalação de pacotes, como o apt:


`$ sudo apt install docker-compose`

> Obs.: O Docker Compose exige que a versão do Python seja a 3.6 or superior.


Para verificar se a instalação foi bem-sucedida, execute:


`$ docker-compose --version`


Você deverá visualizar um resultado parecido com este:


Saída:
> docker-compose version 1.26.0, build 8a1c60f6



### Docker Compose


Realize o clone do repositório:


   `$ git clone https://github.com/gassis/ifsearch.git`
   
   `$ cd ifsearch`


A partir da pasta criada acima, execute:

   `$ cd crawler`
   `~/ifsearch/crawler$ docker-compose up`
   
   > Obs.: Como o índice de busca é construído na **primeira execução do aplicativo**, é necessário que a aplicação fique em **execução ininterrupta por um prazo de aproximadamente 24 horas, dependendo do equipamento.**

   
Após a instalação, acesse a ferramenta por meio da seguinte URL, em seu próprio browser:

   http://localhost:5000
   
   > Obs.: Além da porta **5000**, o sistema também irá demandar o uso das portas **9200** e **9300 (Elasticsearch)**.


### Observações importantes


- Para realizar o agendamento de execução do processo de indexação, recomendamos a utilização do utilitário **CRON**. Exemplo de entrada no **crontab**:

  `#* * * * * docker exec -it crawler_monitor python crawler/monitor.py`

- É possível também a execução do script de indexação de forma direta, caso seja necessário a reindexação de algum período do ano. Exemplo de comando para execução da (re)indexação do ano de *2015*:

  `~/ifsearch/crawler$ docker exec -it crawler_monitor python monitor.py -y 2015`
  
- Caso o usuário deseje especificar um ou mais meses específicos de um certo ano, como por exemplo, os meses de *março e abril de 2020*:
    
  `~/ifsearch/crawler$ docker exec -it crawler_monitor python monitor.py -y 2020 -m março,abril`

- Segue abaixo a sintaxe para o comando monitor.py. É importante ressaltar que para se definir mais de um ano ou mês, basta inserir listas com os itens separados por vírgula (sem espaços):
  
  ` monitor.py -y <year> -m <month>`
  
  - Exemplo de uso do comando monitor.py para (re)indexação dos anos de 2014, 2015 e 2016. Neste caso, quando se define mais de um ano, serão processados todos os meses.
  - 
    `monitor.py -y 2014,2015,2016`




Para fins de referência, ressaltamos que para este projeto foram utilizadas as seguintes tecnologias e ferramentas:

- Python
  - Flask (Web framework)
  - Jinja (Template Language)
- Javascript
- Elasticsearch
- Shellscript
- Docker
