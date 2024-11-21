from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
import time
from PyPDF2 import PdfReader
from groq import Groq
import pandas as pd

pc = Pinecone(api_key="pcsk_4qyxrD_42QS74uKmJSp9uUBk1iPk7Gb3AsU4eoG3yRqFuZPUbSGFvgUdySAyQXJDKpM3xB")


reader = PdfReader("regras.pdf")
data = []

for i, page in enumerate(reader.pages):
    content = page.extract_text().strip()  # Extrair texto da página e remover espaços extras
    if content:  # Apenas adicionar se o conteúdo não estiver vazio
        data.append({"id": f"page_{i}", "text": content})


vagas_df = pd.read_csv("vagas.csv")  # Ler o CSV
csv_text = vagas_df.to_string(index=False)
data.append({"id": f"page_15", "text": csv_text})
#caso results aponte para a tabela, o llm vai saber que
#a página 15 é das tabelas de vagas

embeddings = pc.inference.embed(
    model="multilingual-e5-large",
    inputs=[d['text'] for d in data],
    parameters={"input_type": "passage", "truncate": "END"}
)

index_name = "index-unicamp"


if not pc.has_index(index_name):
    pc.create_index(
        name=index_name,
        dimension=1024,
        metric="cosine",
        spec=ServerlessSpec(
            cloud='aws', 
            region='us-east-1'
        ) 
    )

while not pc.describe_index(index_name).status['ready']:
    time.sleep(1)

index = pc.Index("index-unicamp")

records = []
for d, e in zip(data, embeddings):
    records.append({
        "id": d['id'],
        "values": e['values'],
        "metadata": {'text': d['text']}
    })


index.upsert(
    vectors=records,
    namespace="example-namespace"
)

time.sleep(10)

query = "quantas vagas há para engenharia de computação ampla concorrência?"
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


print(result)

matched_info = ' '.join(item['metadata']['text'] for item in result['matches'])
context = f"Information: {matched_info}"
sys_prompt = f"""
Instruções:
- Responda as questões sobre o vestibular da unicamp consultando ao documento sempre que necessário
- Seja prestativo e responda as questões com cautela, caso não saiba de algo diga "não sei"
- Utilize o contexto fornecido para aumentar a precisão dos dados
- Utilize seu conhecimento anterior para melhorar as respostas
- sempre cite o artigo e em qual página a informação está
- para as vagas de cada curso a tabela tem formato: curso, total de vagas regulares, tota de vagas VU, ampla concorrência mínimo, ampla concorrência máximo, reserva de vagas para PP 15%, reserva de vagas para PP 27,2%
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

print(chat_completion.choices[0].message.content)