no link a seguir segue o relatório da implementação do chatbot: https://docs.google.com/document/d/18Md9l57gMHjx74CO5zMkrx7Lm0NUo_nX0iQtcuTHTj4/edit?usp=sharing
Arquivos que não forem mencionados no documento acima ou neste README são necessários para a execução do Google Cloud. Ou seja, podem ser ignorados para testes.

Uso (web): A aplicação pode ser testada remotamente a partir do link: https://chatbot-vestibular.rj.r.appspot.com/
Pelo plano grátis, não há boa estabilidade. No caso de erro 500, tente trocar de navegador ou me contatar em pedro.d.vas@gmail.com

acurácia do LLM analisada no relatório.

Instalação e uso(local): Para usar a aplicação localmente, é necessário ter python instalado, de preferência as versões 3.11 ou 3.12. A versão 3.11.8 tem um instalador pronto no site oficial do Python

Com python instalado, é necessário instalar bibliotecas presentes apenas em requirements.txt caso queira apenas enviar prompts.
Caso também queira mudar o contexto disponível no banco de dados também são necessárias as bibliotecas PyPDF2 e Pandas.

Para o caso de uso de apenas entradas para o LLM, basta rodar o main.py locamente, onde um link será gerado e o teste pode ser feito.

Para o caso com alteração do Banco de Dados e uma entrada do LLM, basta rodar o programa groq_1.py, alterando a variável query conforme necessário. Entretando este programa NÃO foi feito para o usuário final, e sim apenas para desenvolvimento e criação do banco de dados no Pinecone. Além disso este programa contém apenas a lógica, então as saídas são dadas no terminal (uma saída sobre contextos e outra sobre a resposta final)
