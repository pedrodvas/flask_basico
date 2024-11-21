# Copyright 2015 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_flex_quickstart]
from flask import Flask, render_template, request
from pinecone.grpc import PineconeGRPC as Pinecone
import time
from groq import Groq


def chatbot(input):
    pc = Pinecone(api_key="pcsk_4qyxrD_42QS74uKmJSp9uUBk1iPk7Gb3AsU4eoG3yRqFuZPUbSGFvgUdySAyQXJDKpM3xB")

    index_name = "index-unicamp"
        
    while not pc.describe_index(index_name).status['ready']:
        time.sleep(1)

    # Target the index where you'll store the vector embeddings
    index = pc.Index("index-unicamp")

    query = request
    query_embedding = pc.inference.embed(
        model="multilingual-e5-large",
        inputs=[query],
        parameters={
            "input_type": "query"
        }
    )

    result = index.query(
        namespace="example-namespace",
        vector=query_embedding[0].values,
        top_k=7,
        include_values=False,
        include_metadata=True
    )

    matched_info = ' '.join(item['metadata']['text'] for item in result['matches'])
    #sources = [item['metadata']['source'] for item in result['matches']]
    #context = f"Information: {matched_info} and the sources: {sources}"
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


'''
@app.route("/")
def hello() -> str:
    """Return a friendly HTTP greeting.

    Returns:
        A string with the words 'Hello World!'.
    """
    return "Hello World!"


if __name__ == "__main__":
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app.
    app.run(host="127.0.0.1", port=8080, debug=True)
# [END gae_flex_quickstart]'''