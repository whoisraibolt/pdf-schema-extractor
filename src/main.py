from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Union
import uvicorn
import os
import json
import time

from src.utilities.RAG import PDFExtractorRAG
from src.utilities.regex import extract_fields_advanced
from src.config import (
    OAB_SCHEMA_ADVANCED,
    OAB_VALIDATORS,
    TELA_SISTEMA_SCHEMA_ADVANCED,
    TELA_SISTEMA_VALIDATORS,
)

from datetime import timedelta

app = FastAPI(title="PDF Extraction API")

extractor_rag = PDFExtractorRAG()

# Mapeamento de schemas e validadores por label
REGEX_SCHEMA = {
    "carteira_oab": OAB_SCHEMA_ADVANCED,
    "tela_sistema": TELA_SISTEMA_SCHEMA_ADVANCED,
}

REGEX_VALIDATORS = {
    "carteira_oab": OAB_VALIDATORS,
    "tela_sistema": TELA_SISTEMA_VALIDATORS,
}

def converter_para_serializavel(obj):
    if isinstance(obj, dict):
        return {key: converter_para_serializavel(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [converter_para_serializavel(item) for item in obj]
    elif hasattr(obj, "__dict__"):
        return converter_para_serializavel(obj.__dict__)
    elif isinstance(obj, (str, int, float, bool, type(None))):
        return obj
    else:
        return str(obj)

def formatar_tempo(segundos):
    td = timedelta(seconds=int(segundos))
    total_seconds = int(td.total_seconds())
    horas = total_seconds // 3600
    minutos = (total_seconds % 3600) // 60
    segundos = total_seconds % 60
    return f"{horas:02d}:{minutos:02d}:{segundos:02d}"

def ler_texto_pdf(pdf_path):
    import fitz  # PyMuPDF
    doc = fitz.open(pdf_path)
    texto = ""
    for page in doc:
        texto += page.get_text()
    doc.close()
    return texto

def extrair_com_regex(label, extraction_schema, pdf_path):
    texto = ler_texto_pdf(pdf_path)
    schema_completo = REGEX_SCHEMA.get(label, {})
    validators = REGEX_VALIDATORS.get(label, {})

    resultado = extract_fields_advanced(texto, schema_completo, validators)

    faltando = any(
        resultado.get(campo) is None or resultado.get(campo) == "NULL"
        for campo in extraction_schema.keys()
    )

    resultado_filtrado = {k: resultado.get(k) for k in extraction_schema.keys()}

    return resultado_filtrado, faltando

class ExtractionRequest(BaseModel):
    label: str = Field(..., example="carteira_oab")
    extraction_schema: Dict[str, str]
    pdf_path: str

class ExtractionResponse(BaseModel):
    label: str
    extraction_schema: Dict[str, Optional[str]]
    pdf_path: str
    extracao_com: str
    tempo_de_extracao: str

@app.post("/extract", response_model=List[ExtractionResponse])
async def extract(data: Union[List[ExtractionRequest], ExtractionRequest]):
    if isinstance(data, ExtractionRequest):
        requests = [data]
    else:
        requests = data

    resultados = []

    for req in requests:
        start_time = time.time()

        pdf_full_path = os.path.join("src", "data", req.pdf_path)
        print("Caminho completo:", pdf_full_path)
        if not os.path.isfile(pdf_full_path):
            raise HTTPException(status_code=400, detail=f"Arquivo PDF não encontrado: {pdf_full_path}")

        resultado_regex, faltando = extrair_com_regex(req.label, req.extraction_schema, pdf_full_path)

        if not faltando:
            metodo_extracao = "REGEX"
            resultado_final = resultado_regex
        else:
            campos_faltantes = {
                k: req.extraction_schema[k]
                for k, v in resultado_regex.items()
                if v is None or v == "NULL"
            }

            resultado_rag = extractor_rag.extract(req.label, campos_faltantes, req.pdf_path)

            if isinstance(resultado_rag, str):
                try:
                    resultado_rag = json.loads(resultado_rag)
                except Exception:
                    resultado_rag = {}

            resultado_final = resultado_regex.copy()
            for campo, valor in resultado_rag.items():
                if valor is not None and valor != "NULL":
                    resultado_final[campo] = valor

            metodo_extracao = "MISTO"

        end_time = time.time()
        tempo_de_extracao = formatar_tempo(end_time - start_time)

        resultado_final_limpo = converter_para_serializavel(resultado_final)

        resultados.append(
            ExtractionResponse(
                label=req.label,
                extraction_schema=resultado_final_limpo,
                pdf_path=os.path.basename(req.pdf_path),
                extracao_com=metodo_extracao,
                tempo_de_extracao=tempo_de_extracao,
            )
        )

    return resultados

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)