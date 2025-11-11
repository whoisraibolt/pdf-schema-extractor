# 📄 pdf-schema-extractor

Ferramenta para extração automática de dados estruturados de PDFs, transformando documentos não organizados em formatos como JSON, de acordo com um esquema definido pelo usuário. 🚀

### 🔍 Visão Geral

O `pdf-schema-extractor` utiliza uma abordagem em camadas para extrair dados de PDFs com alta precisão e baixo custo computacional:

- **Regex simples:** Extração rápida de campos com formatos previsíveis. ⚡
- **Regex avançado:** Tratamento de variações e padrões complexos. 🧩
- **RAG (Retrieval-Augmented Generation):** Extração inteligente com LLMs para casos onde regex não é suficiente. ✅

A solução garante extração em menos de 10 segundos por documento, com acurácia acima de 80%.

## 🔤 Regex

Expressões regulares (regex) são padrões usados para localizar e extrair sequências específicas de texto. São ideais para campos com formatos fixos, como números, datas e nomes. 📏

## 🤖 RAG

Retrieval-Augmented Generation (RAG) combina recuperação de informações com geração de texto por modelos de linguagem (LLMs), permitindo extrair dados mesmo em documentos mal formatados ou com variações. 🧠

## 🔄 Fluxo de Extração

![Fluxograma da Lógica de Extração](https://github.com/whoisraibolt/pdf-schema-extractor/blob/main/fluxograma.png "Fluxograma da Lógica de Extração")

O processo segue três etapas: regex simples → regex avançado → RAG, garantindo extração completa mesmo em casos complexos. 🔄

## 💪 Pontos Fortes

- **Abordagem em camadas:** Otimiza desempenho e custo, usando métodos rápidos primeiro e avançando para técnicas mais complexas apenas quando necessário. ⚙️
- **Fallback automático:** Transição entre regex e RAG garante maior completude dos dados. 🔄
- **Adaptabilidade:** Funciona com diferentes layouts e tipos de PDFs. 📐
- **Validação implícita:** O uso de `NULL` como gatilho assegura que todos os campos sejam extraídos. ✅

## 🚀 Como Usar

### 💡 Recomendação: use um ambiente virtual

Para isolar as dependências da aplicação e evitar conflitos, recomenda-se criar um ambiente virtual antes de instalar os pacotes. Você pode usar:

###### venv (embutido no Python):

```bash
python -m venv env
source env/bin/activate   # Linux/macOS
.\env\Scripts\activate    # Windows
```

###### conda (se usar Anaconda/Miniconda):

```bash
conda create --name myenv python=3.x
conda activate myenv
```

###### 1. Clone o repositório: 📥

`git clone https://github.com/whoisraibolt/pdf-schema-extractor.git`

###### 2. Instale as dependências: 🔧

`pip install -r requirements.txt`

###### 3. Inicie o servidor: 🌐

`uvicorn src.main:app --reload`

4. Envie uma requisição para o endpoint /extract com o seguinte payload: 📤

```json
{
  "label": "carteira_oab",
  "extraction_schema": {
    "nome": "Nome do profissional",
    "inscricao": "Número de inscrição",
    "seccional": "Seccional do profissional"
  },
  "pdf_path": "oab_1.pdf"
}
```
Ou:

```json
[
    {
      "label": "carteira_oab",
      "extraction_schema": {
        "nome": "Nome do profissional, normalmente no canto superior esquerdo da imagem",
        "inscricao": "Número de inscrição do profissional",
        "seccional": "Seccional do profissional",
        "subsecao": "Subseção à qual o profissional faz parte",
        "categoria": "Categoria, pode ser ADVOGADO, ADVOGADA, SUPLEMENTAR, ESTAGIARIO, ESTAGIARIA",
        "endereco_profissional": "Endereço do profissional",
        "telefone_profissional": "Telefone do profissional",
        "situacao": "Situação do profissional, normalmente no canto inferior direito."
      },
      "pdf_path": "oab_1.pdf"
    },
    {
      "label": "carteira_oab",
      "extraction_schema": {
        "nome": "Nome do profissional, normalmente no canto superior esquerdo da imagem",
        "inscricao": "Número de inscrição do profissional",
        "seccional": "Seccional do profissional",
        "subsecao": "Subseção à qual o profissional faz parte",
        "categoria": "Categoria, pode ser ADVOGADO, ADVOGADA, SUPLEMENTAR, ESTAGIARIO, ESTAGIARIA",
        "endereco_profissional": "Endereço do profissional",
        "situacao": "Situação do profissional, normalmente no canto inferior direito."
      },
      "pdf_path": "oab_2.pdf"
    },
    {
      "label": "carteira_oab",
      "extraction_schema": {
        "nome": "Nome do profissional, normalmente no canto superior esquerdo da imagem",
        "inscricao": "Número de inscrição do profissional",
        "seccional": "Seccional do profissional",
        "subsecao": "Subseção à qual o profissional faz parte",
        "categoria": "Categoria, pode ser ADVOGADO, ADVOGADA, SUPLEMENTAR, ESTAGIARIO, ESTAGIARIA",
        "telefone_profissional": "Telefone do profissional",
        "situacao": "Situação do profissional, normalmente no canto inferior direito."
      },
      "pdf_path": "oab_3.pdf"
    },
    {
      "label": "tela_sistema",
      "extraction_schema": {
        "data_base": "Data base da operação selectionada",
        "data_verncimento": "Data de vencimento da operação selectionada",
        "quantidade_parcelas": "Quantidade de parcelas da operação selectionada",
        "produto": "Produto da operação selectionada",
        "sistema": "Sistema da operação selectionada",
        "tipo_de_operacao": "Tipo de operação",
        "tipo_de_sistema": "Tipo de sistema"
      },
      "pdf_path": "tela_sistema_1.pdf"
    },
    {
      "label": "tela_sistema",
      "extraction_schema": {
        "pesquisa_por": "Na consulta de cobrança, a pesquisa é efetuado por? Ela pode ser feita por cliente, parente, prestador ou outro",
        "pesquisa_tipo": "Tipo de pesquisa, pode ser por cpf, cnpj, Nome ou email",
        "sistema": "Sistema da operação selectionada",
        "valor_parcela": "Valor da parcela da operação selectionada",
        "cidade": "Cidade da operação selectionada"
      },
      "pdf_path": "tela_sistema_2.pdf"
    },
    {
      "label": "tela_sistema",
      "extraction_schema": {
        "data_referencia": "Data de referencia da operação selectionada do detalhamento de saldos por parcelas",
        "selecao_de_parcelas": "Seleção de parcelas da operação selectionada do detalhamento de saldos por parcelas, pode ser vencido, pago ou pendente",
        "total_de_parcelas": "Valor total, normalmente no canto inferior esquerdo da imagem"
      },
      "pdf_path": "tela_sistema_3.pdf"
    }
  ]
```

### 🧪 Testes da API

Para testar a API, foi utilizado o Postman, mas qualquer cliente HTTP (como cURL, Insomnia ou scripts personalizados) pode ser utilizado para enviar requisições ao endpoint de extração. 💻

### 🚧 Trabalhos Futuros

- **Extração zonal antes do regex:** Implementar uma etapa de pré-processamento para extrair texto apenas de regiões específicas do PDF (zonas delimitadas), reduzindo ruído e aumentando a eficácia do regex. 📊
- **Cache inteligente:** Armazenar resultados parciais para acelerar extrações repetidas em documentos semelhantes. 🗃️
- **Melhoria contínua do modelo RAG:** Ajustar o contexto e otimizar prompts para reduzir chamadas ao LLM e acelerar respostas. 🔄

### 📬 Contato

Para dúvidas ou sugestões, entre em contato. 🤝

### 📜 Licença

Código lançado sob a licença [MIT](https://github.com/whoisraibolt/pdf-schema-extractor/blob/main/LICENSE "MIT"). 🛡️
