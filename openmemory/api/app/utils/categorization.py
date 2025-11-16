import logging
import os
import json
from typing import List

from app.utils.prompts import MEMORY_CATEGORIZATION_PROMPT
from pydantic import BaseModel
from tenacity import retry, stop_after_attempt, wait_exponential
from openai import OpenAI


class MemoryCategories(BaseModel):
    categories: List[str]


def _load_llm_config():
    """Load LLM configuration from config.json"""
    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'config.json')
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        # Extract LLM configuration
        llm_config = config.get('mem0', {}).get('llm', {})
        model_name = llm_config.get('config', {}).get('model', 'gpt-4o-mini')
        api_key = llm_config.get('config', {}).get('api_key', '')
        base_url = llm_config.get('config', {}).get('base_url', '')
        
        # Handle environment variable references
        if api_key.startswith('env:'):
            env_var = api_key.split(':', 1)[1]
            api_key = os.getenv(env_var, '')
            
        return {
            'model': model_name,
            'api_key': api_key,
            'base_url': base_url
        }
    except Exception as e:
        logging.warning(f"Failed to load config.json, using defaults: {e}")
        return {
            'model': 'gpt-4o-mini',
            'api_key': os.getenv('OPENAI_API_KEY', ''),
            'base_url': ''
        }


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=15))
def get_categories_for_memory(memory: str) -> List[str]:
    try:
        # 从config.json加载LLM配置
        llm_config = _load_llm_config()
        model_name = llm_config['model']
        api_key = llm_config['api_key']
        base_url = llm_config['base_url']
        
        # 初始化OpenAI客户端
        if base_url:
            client = OpenAI(api_key=api_key, base_url=base_url)
        else:
            client = OpenAI(api_key=api_key)
        
        messages = [
            {"role": "system", "content": MEMORY_CATEGORIZATION_PROMPT},
            {"role": "user", "content": memory}
        ]

        # 使用配置的LLM而不是硬编码的模型
        completion = client.chat.completions.create(
            model=model_name,
            messages=messages,
            response_format={"type": "json_object"},
            temperature=0
        )

        # 解析响应
        response_data = json.loads(completion.choices[0].message.content)
        categories = response_data.get("categories", [])
        
        return [cat.strip().lower() for cat in categories]

    except Exception as e:
        logging.error(f"[ERROR] Failed to get categories: {e}")
        try:
            logging.debug(f"[DEBUG] Raw response: {completion.choices[0].message.content}")
        except Exception as debug_e:
            logging.debug(f"[DEBUG] Could not extract raw response: {debug_e}")
        raise