

# IFSearch

![alt text](https://www.ifg.edu.br/boletim-de-servico?showall=&limitstart=)

O IFSearch é uma ferramenta que propicia a busca em documentos oficiais do IFG que são publicados oficialmente no Boletim de Notícias. Em virtude da dificuldade na busca por palavras em cada um dos documentos disponíveis, este sistema oferece uma interface a partir da qual os usuários poderão simplesmente digitar um termo de interesse como nomes próprios (pessoas, empresas,...), datas e quaisquer outras palavras.


Para instruções de como baixar os arquivos necessários à instalação do sistema a partir do Git, siga os passos descritos no link abaixo:

https://docs.github.com/pt/github/creating-cloning-and-archiving-repositories/cloning-a-repository


## Windows

Faça o download e instalação do Docker Compose seguindo as instruções abaixo:

   https://docs.docker.com/compose/install/
   
   
   
## Linux

### Usando o pip


Faça o download e instalação do Docker Compose usando o pip3:


`$ pip3 install docker-compose`

Obs.: O Docker Compose exige que a versão do Python seja a 3.6 or superior.


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


   `$ ifsearch/docker-compose up`
   
   
Após a instalação, acesse a ferramenta por meio da seguinte URL:

   http://localhost:5000


