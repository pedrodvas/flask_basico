from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

# Inicializando o modelo de embeddings de frases
model = SentenceTransformer('all-MiniLM-L6-v2')

# Respostas esperadas do dataset (lista com as respostas esperadas)
respostas_esperadas = [
    "O prazo de inscrição para o vestibular da Unicamp 2024 é de 1º a 31 de agosto.",
    "Existem 120 vagas para Engenharia Civil, sendo 40 para cotas e 80 de ampla concorrência.",
    "O PAAIS é o Programa de Ação Afirmativa e Inclusão Social da Unicamp, que concede bônus a alunos de escolas públicas.",
    "As provas específicas para Medicina incluem Química e Biologia, além da prova geral.",
    "O Vestibular Unicamp 2025 oferece um total de 3.340 vagas regulares para os cursos de graduação.",
    "Os sistemas de ingresso além do Vestibular Unicamp são: Edital ENEM-Unicamp 2025 (314 vagas), Provão Paulista 2025 (325 vagas), Vestibular Indígena 2025 (49 vagas regulares e 81 adicionais), Olimpíadas Científicas e Competições de Conhecimento (115 vagas regulares e 16 adicionais).",
    "A 1ª fase do VU 2025 será composta por uma prova de Conhecimentos Gerais, com 72 questões objetivas que avaliam as áreas de conhecimento desenvolvidas no Ensino Médio, incluindo questões interdisciplinares. A nota da 1ª fase será padronizada e calculada com base na fórmula especificada no Art. 19, § 4º."
]

# Respostas geradas pelo chatbot
respostas_geradas = [
    "De acordo com o documento, o prazo de inscrição para o Vestibular Unicamp 2025 é de 01 a 30 de agosto de 2024.",
    "De acordo com o documento, existem 90 vagas para o curso Engenharia de Computação, todas elas integrais.",
    "Não encontrei informações sobre o PAAIS no documento fornecido. Por favor, forneça mais contexto ou informações sobre o PAAIS para que eu possa ajudar melhor.",
    "De acordo com o documento, as provas específicas para Medicina são: Prova de História da Medicina, Prova de Biologia, Prova de Física, Prova de Matemática, Prova de Sociologia, Prova de Habilidades Específicas para a área de Medicina.",
    "De acordo com a Resolução GR-029/2024, o número total de vagas disponíveis no Vestibular Unicamp 2025 é de 3340 vagas regulares.",
    "Segundo a Resolução GR-029/2024 da Reitoria da Universidade Estadual de Campinas (Unicamp), os sistemas de ingresso da Unicamp, além do Vestibular Unicamp (VU), são:\n\n1. Edital ENEM-Unicamp: É um sistema de ingresso que aproveita as notas obtidas no Exame Nacional do Ensino Médio (ENEM) para admitir estudantes em cursos específicos da Unicamp.\n2. Provão Paulista: É um sistema de ingresso que avalia a capacidade dos candidatos em atividades específicas, como provas práticas, teóricas ou estudos de caso, para ingressar em cursos da Unicamp.\n3. Vestibular Indígena (VI): É um sistema de ingresso específico para candidatos indígenas, que avalia sua capacidade em diferentes áreas, como línguas, matemática e história.\n4. Reserva de Vagas (cotas) para autodeclarados pretos, pardos e indígenas: A Unicamp reserva vagas para estes grupos, que podem ser ingressados em diferentes sistemas de ingresso.\n5. Inscrição automática para estudantes do curso de Medicina: É um sistema de ingresso que admite estudantes que já cursam o curso de Medicina da Unicamp a ingressar em cursos diferentes da instituição.\n\nEsses sistemas buscam ampliar as oportunidades de ingresso para uma variedade de estudantes e promover a diversidade e a igualdade de oportunidades na universidade.",
    "De acordo com o documento, nos Anexos I e IV, os critérios de avaliação para a 1ª fase do VU 2025 são:\n\n* para candidatos regulares:\n    + Conhecimento geral (conhecimento das áreas do conhecimento desenvolvidas no ensino médio)\n    + Organização de sua ideia (capacidade de organizar sua ideia e argumentos de forma coerente)\n    + Estabelecimento de relações (capacidade de estabelecer relações entre conceitos e ideias)\n    + Interpretação de dados (capacidade de interpretar dados e informações)\n    + Elaboração de hipóteses (capacidade de elaborar hipóteses e argumentos)\n    + Domínio dos conteúdos das áreas de conhecimento desenvolvidas no ensino médio\n\n* para candidatos às vagas de amplo concurso:\n    + Realização de provas escritas, que avaliam as habilidades de resolução de problemas, capacidade de análise e síntese, e conhecimento das áreas de conhecimento desenvolvidas no ensino médio.\n\nEsses critérios são aplicados para todos os cursos, exceto para o Curso de Música, que tem um padrão de avaliação específico descrito no Anexo VI."
]

# Gerando embeddings das respostas (usando o modelo)
embeddings_esperadas = model.encode(respostas_esperadas)
embeddings_geradas = model.encode(respostas_geradas)

# Calculando a similaridade de cosseno entre as respostas esperadas e as geradas
similarities = cosine_similarity(embeddings_esperadas, embeddings_geradas)

# Definindo um limiar de similaridade para considerar as respostas como corretas
threshold = 0.7  # Por exemplo, consideramos que a similaridade acima de 0.7 é uma resposta aceitável
corretas = sum(sim >= threshold for sim in similarities.diagonal())  # Apenas valores na diagonal (respostas comparadas)

# Acurácia baseada na similaridade
accuracy = corretas / len(respostas_esperadas)
print(f"Precisão do Chatbot (usando similaridade de cosseno): {accuracy * 100:.2f}%")
