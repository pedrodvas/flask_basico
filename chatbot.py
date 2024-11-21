from pinecone.grpc import PineconeGRPC as Pinecone
import time
from groq import Groq


def process_input(request):
    '''
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
    '''
    return("retornado!")