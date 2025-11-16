from os import getenv
from dotenv import load_dotenv, dotenv_values
import site
from pathlib import Path

load_dotenv()

from langchain_openai import ChatOpenAI
# from fastapi.security import APIKeyHeader
from supabase import create_client, Client # type: ignore
import requests


site_packages = site.getsitepackages()[0]
site_packages_path = Path(site_packages) / "site-packages"
if not site_packages_path.exists():
    site_packages_path = Path(site_packages)

sizes = []
for pkg in site_packages_path.iterdir():
    if pkg.is_dir() and not pkg.name.startswith("_") and pkg.name != "__pycache__":
        size = sum(f.stat().st_size for f in pkg.rglob('*') if f.is_file()) / (1024**2)
        sizes.append((size, pkg.name))

for size, name in sorted(sizes, reverse=True)[:20]:
    print(f"{size:8.2f} MB  {name}")


# Check if the key exists
api_key = getenv("OPENROUTER_API_KEY")

SUPABASE_URL = getenv("SUPABASE_URL")
SUPABASE_KEY = getenv("SUPABASE_API_KEY") #SUPABASE_KEY
SUPABASE: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

api_key=getenv("OPENROUTER_API_KEY")
base_url=getenv("OPENROUTER_BASE_URL_DEEPSEEK")

if not api_key:
    raise ValueError("OPENROUTER_API_KEY environment variable not set")





SUMMARIZATION_LLM = ChatOpenAI(
    api_key=api_key,
    base_url=getenv("OPENROUTER_BASE_URL_DEEPSEEK"),
    # model="deepseek/deepseek-chat-v3.1:free",
    # model="qwen/qwen3-235b-a22b:free"
    # model = "arliai/qwq-32b-arliai-rpr-v1:free"
    model = "z-ai/glm-4.5-air:free"
    # model="google/gemma-3n-e2b-it:free",
    # model="openai/gpt-oss-120b:free"
)

# Initialize Primary LLM
PRIMARY_LLM  = ChatOpenAI(
    api_key=api_key,
    base_url=getenv("OPENROUTER_BASE_URL_DEEPSEEK"),
    model = "qwen/qwen3-30b-a3b:free"
)

# Initialize Fallback LLM
FALLBACK_LLM_1= ChatOpenAI(
  api_key=api_key,
  base_url=getenv("OPENROUTER_BASE_URL_DEEPSEEK"),
  model="z-ai/glm-4.5-air:free",
)

FALLBACK_LLM_2= ChatOpenAI(
  api_key=api_key,
  base_url=getenv("OPENROUTER_BASE_URL_DEEPSEEK"),
  model="minimax/minimax-m2:free",
)


FALLBACK_LLM_3= ChatOpenAI(
  api_key=api_key,
  base_url=getenv("OPENROUTER_BASE_URL_DEEPSEEK"),
  model="tngtech/deepseek-r1t2-chimera:free",
)


FALLBACK_LLM_4= ChatOpenAI(
  api_key=api_key,
  base_url=getenv("OPENROUTER_BASE_URL_DEEPSEEK"),
  model="deepseek/deepseek-r1-0528-qwen3-8b:free",
)


# Obtain CTRL API key from .env
CTRL_API_KEY = getenv("CTRL_API_KEY")

# Create API key header dependency
# API_KEY_HEADER = APIKeyHeader(name="CTRL_API_KEY", description="API Key needed to access the protected endpoint")
            