from flask import Flask, render_template, request
from pinecone.grpc import PineconeGRPC as Pinecone
import time
from groq import Groq


def chatbot(input):
    pc = Pinecone(api_key="pcsk_4qyxrD_42QS74uKmJSp9uUBk1iPk7Gb3AsU4eoG3yRqFuZPUbSGFvgUdySAyQXJDKpM3xB")

    index_name = "index-unicamp"
        
    while not pc.describe_index(index_name).status['ready']:
        time.sleep(1)

    #guardando as vector embeddings no índice especificado
    index = pc.Index(index_name)

    query = input   #processa a entrada do usuário
    query_embedding = pc.inference.embed(
        model="multilingual-e5-large",
        inputs=[query],
        parameters={
            "input_type": "query"
        }
    )

    #busca os 7 resultados mais relevantes para a resposta
    result = index.query(
        namespace="example-namespace",
        vector=query_embedding[0].values,
        top_k=7,
        include_values=False,
        include_metadata=True
    )

    #usa os resultados para dar contexto
    matched_info = ' '.join(item['metadata']['text'] for item in result['matches'])
    context = f"Information: {matched_info}"
    sys_prompt = f"""
    Instruções:
    - Responda as questões sobre o vestibular da unicamp consultando ao documento sempre que necessário
    - Seja prestativo e responda as questões com cautela, caso não saiba de algo diga "não sei"
    - Utilize o contexto fornecido para aumentar a precisão dos dados
    - Utilize seu conhecimento anterior para melhorar as respostas
    - sempre cite o artigo e em qual página a informação está
    - para as vagas de cada curso a tabela tem formato: curso, soma total de vagas, tota de vagas VU, ampla concorrência mínimo, ampla concorrência máximo, reserva de vagas para PP 15%, reserva de vagas para PP 27,2%
    Contexto: {context}
    """


    #dá o contexto e a entrada do usuário para o Groq
    client = Groq(
        api_key=("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"),  # This is the default and can be omitted
    )
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": sys_prompt
            },
            {
                "role": "user",
                "content": query,
            }
        ],
        model="llama3-8b-8192",
    )

    #retorna a resposta fornecida para a interface Flask
    return(chat_completion.choices[0].message.content)

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    output = None
    if request.method == 'POST':
        user_input = request.form['user_input']
        output = chatbot(user_input)  # Chama a função de processamento em main.py
    return render_template('index.html', output=output)

if __name__ == "__main__":
    app.run(debug=True)
