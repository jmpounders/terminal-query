from typing import Callable
import os

from terminal_query.llm import openaiapi as openai
from terminal_query.llm import anthropicapi as anthropic

def get_llm_client(
        llm_api_key: str,
    ) -> Callable:
    """Get an LLM client."""

    if 'OPENAI' in llm_api_key:
        api_client = openai.get_openaiai_client(
            os.environ[llm_api_key],
        )
    elif 'PERPLEXITY' in llm_api_key:
        api_client = openai.get_openaiai_client(
            os.environ[llm_api_key],
            base_url='https://api.perplexity.ai'
        )
    elif 'ANTHROPIC' in llm_api_key:
        api_client = anthropic.get_anthropic_client(
            os.environ[llm_api_key]
        )
    else:
        print('Unrecognized API')
        exit()

    return api_client
