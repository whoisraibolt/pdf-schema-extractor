from langchain_community.document_loaders import PDFPlumberLoader
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.prompts import PromptTemplate
import json
import os

os.environ["OPENAI_API_KEY"] = "CHAVE_API"

class PDFExtractorRAG:
    def __init__(self, model_name="gpt-5-mini", embedding_model="text-embedding-ada-002"):
        self.embeddings = OpenAIEmbeddings(model=embedding_model)
        self.llm = ChatOpenAI(model=model_name, temperature=0)
        self.vectorstores = {}
        self.schema_cache = {}

    def load_and_index_pdf(self, pdf_path):
        pdf_path = os.path.abspath(pdf_path)
        if pdf_path in self.vectorstores:
            return self.vectorstores[pdf_path]
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF não encontrado: {pdf_path}")
        try:
            loader = PDFPlumberLoader(pdf_path)
            docs = loader.load()
        except Exception as e:
            raise RuntimeError(f"Erro ao carregar PDF: {e}")
        chunker = SemanticChunker(self.embeddings)
        chunks = chunker.split_documents(docs)
        vectorstore = FAISS.from_documents(chunks, self.embeddings)
        self.vectorstores[pdf_path] = vectorstore
        return vectorstore

    def extract(self, label, campos_faltantes, pdf_path):
        if label not in self.schema_cache:
            self.schema_cache[label] = {}
        self.schema_cache[label].update(campos_faltantes)
        pdf_path = os.path.abspath(pdf_path)
        try:
            vectorstore = self.load_and_index_pdf(pdf_path)
        except Exception as e:
            print(f"Erro ao indexar PDF: {e}")
            return {}
        campos_json = json.dumps(campos_faltantes, ensure_ascii=False, indent=2)
        prompt_template = """
Você é um assistente que extrai informações estruturadas de documentos PDF.

Extraia os seguintes campos do documento conforme o schema abaixo, mas apenas para os campos que estão faltando (valores null):

{campos_faltantes}

Retorne apenas um JSON com os campos faltantes e seus valores extraídos. Se não encontrar algum campo, retorne null.

Documento:
{context}

Resposta (apenas JSON):
"""
        prompt = PromptTemplate(
            input_variables=["context", "campos_faltantes"],
            template=prompt_template
        )
        combine_docs_chain = create_stuff_documents_chain(llm=self.llm, prompt=prompt)
        retrieval_chain = create_retrieval_chain(
            retriever=vectorstore.as_retriever(),
            combine_docs_chain=combine_docs_chain
        )
        try:
            result = retrieval_chain.invoke({
                "input": "",
                "campos_faltantes": campos_json
            })
            output = result.get("output", result)
        except Exception as e:
            print(f"Erro ao invocar chain: {e}")
            return {}
        try:
            output_dict = json.loads(output)
        except Exception as e:
            print(f"Erro ao converter saída para JSON: {e}")
            output_dict = {}
        return output_dict