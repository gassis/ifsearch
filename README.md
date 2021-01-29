

# IFSearch

O IFSearch é uma ferramenta que propicia a busca em documentos oficiais do IFG que são publicados oficialmente no Boletim de Notícias. Em virtude da dificuldade na busca por palavras em cada um dos documentos disponíveis, este sistema oferece uma interface a partir da qual os usuários poderão simplesmente digitar um termo de interesse como nomes próprios (pessoas, empresas,...), datas e quaisquer outras palavras.

Para instruções de como baixar os arquivos necessários à instalação do sistema a partir do Git, siga os passos descritos no link abaixo:

https://docs.github.com/pt/github/creating-cloning-and-archiving-repositories/cloning-a-repository

## Uso:

Instale o docker-compose. As instruções podem ser obtidas em:

   https://docs.docker.com/compose/install/


### Docker Compose

Realize o clone do repositório:

   `$git clone https://github.com/gassis/ifsearch.git`
   `$cd ifsearch`


A partir da pasta criada acima, execute:


   `$docker-compose up`
   
   
Após a instalação, acesse a ferramenta por meio da seguinte URL:


   http://localhost:5000


