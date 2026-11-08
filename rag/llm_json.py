import json
import re
from typing import TypeVar
 
from pydantic import BaseModel
 
from rag.llm import generate  # <-- ADAPTAR se necessário
 
T = TypeVar("T", bound=BaseModel)
 
SYSTEM_JSON = "Responda SOMENTE com um objeto JSON válido, sem markdown e sem texto extra."
 
 
def gerar_json(prompt: str, modelo: type[T], system: str = "") -> T:
    bruto = generate(prompt, system=f"{system}\n{SYSTEM_JSON}".strip())
    bruto = re.sub(r"^```(?:json)?|```$", "", bruto.strip(), flags=re.MULTILINE).strip()
    return modelo.model_validate(json.loads(bruto))