import os
import re

# Diretório base do projeto (src/)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Pasta de dados (dentro de src/)
DATA_DIR = os.path.join(BASE_DIR, "data")

# Caminho base para arquivos PDF
PDF_BASE_PATH = DATA_DIR

# Caminho para o dataset.json
DATASET_JSON_PATH = os.path.join(DATA_DIR, "dataset.json")

# Padrões robustos para carteira da OAB
OAB_SCHEMA_ADVANCED = {
    "nome": [        r"(?:Nome|Nome Completo)[:\s]*([^\n]+)",
        r"^([A-ZÀ-Ú\s']+)\n",  # Nome no início da linha, tudo maiúsculo
    ],
    "inscricao": [        r"Inscrição[:\s]*([0-9A-Z\s\-]+)",
        r"([0-9]{6})\s",  # Número de 6 dígitos
    ],
    "seccional": [        r"Seccional[:\s]*([A-Z]{2})",
        r"([A-Z]{2})\s*Conselho",
    ],
    "subsecao": [        r"Subseção[:\s]*([^\n]+)",
    ],
    "categoria": [        r"Categoria[:\s]*([^\n]+)",
    ],
    "endereco_profissional": [        r"Endereço Profissional[:\s]*([^\n]+(?:\n[^\n]+)*)",  # Pode ser multilinha
    ],
    "telefone_profissional": [        r"Telefone Profissional[:\s]*([0-9\-\s\(\)]+)",
    ],
    "situacao": [        r"Situação[:\s]*([^\n]+)",
    ],
}

# Validações simples
OAB_VALIDATORS = {
    "inscricao": lambda x: re.match(r"^[0-9]{6}$", x),
    "seccional": lambda x: re.match(r"^[A-Z]{2}$", x),
    "telefone_profissional": lambda x: re.match(r"^[0-9\-\s\(\)]{8,}$", x),
}

# Padrões robustos para tela de sistema
TELA_SISTEMA_SCHEMA_ADVANCED = {
    "data_base": [        r"Data Base[:\s]*([0-9]{2}/[0-9]{2}/[0-9]{4})",
        r"Data Referência[:\s]*([0-9]{2}/[0-9]{2}/[0-9]{4})",
    ],
    "data_vencimento": [        r"Data Vencimento[:\s]*([0-9]{2}/[0-9]{2}/[0-9]{4})",
        r"Vcto mais antigo[:\s]*([0-9]{2}/[0-9]{2}/[0-9]{4})",
    ],
    "quantidade_parcelas": [        r"Qtd\. Parcelas[:\s]*([0-9]+)",
        r"Intervalo de parcelas?\s*:\s*([0-9]+)",
    ],
    "produto": [        r"Produto[:\s]*([^\n]+)",
    ],
    "sistema": [        r"Sistema[:\s]*([^\n]+)",
    ],
    "tipo_de_operacao": [        r"Tipo Operação[:\s]*([^\n]+)",
        r"Tipo de Operação[:\s]*([^\n]+)",
    ],
    "tipo_de_sistema": [        r"Tipo Sistema[:\s]*([^\n]+)",
        r"Tipo de Sistema[:\s]*([^\n]+)",
    ],
}

# Validações simples
TELA_SISTEMA_VALIDATORS = {
    "data_base": lambda x: re.match(r"^[0-9]{2}/[0-9]{2}/[0-9]{4}$", x),
    "data_vencimento": lambda x: re.match(r"^[0-9]{2}/[0-9]{2}/[0-9]{4}$", x),
    "quantidade_parcelas": lambda x: re.match(r"^[0-9]+$", x),
}