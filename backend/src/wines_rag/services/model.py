import asyncio
from typing import List, Optional
from fastembed import TextEmbedding
from wines_rag.config import Config
from openai import AsyncOpenAI
from wines_rag.entities.qdrant import WineBase

class ModelService:
    def __init__(self, config:Config,
                embedding_model: Optional[TextEmbedding] = None,
                generative_model: Optional[AsyncOpenAI] = None):
        print(f"Loading FastEmbed model: {config.model.embedding.model}...")
        self.embedding_model = embedding_model 
        self.generative_model = generative_model
        self.generative_model_name = config.model.generative.model 
        
        print("FastEmbed model loaded successfully.")

    async def encode(self, text: str) -> List[float]:
        def _embed():
            embeddings = list(self.embedding_model.embed([text]))
            return embeddings[0].tolist()
        vector = await asyncio.to_thread(_embed)
        return vector
    
    async def summarize_wines(self, query:str,wines:list[WineBase])->str:
        if not wines:
            return "К сожалению, по вашему запросу ничего не найдено."
        
        wines_context_lines = []
        for i, wine in enumerate(wines, 1):
            price_str = f"{wine.price} руб."
            line = (
                f"{i}. {wine.name} (Страна: {wine.country})\n"
                f"   Цена: {price_str}\n"
                f"   Тип: {wine.color} {wine.acidity}\n"
                f"   Описание: {wine.description}\n"
            )
            wines_context_lines.append(line)

        wines_context = "\n".join(wines_context_lines)
        
        system_prompt = (
            "Ты — опытный сомелье и помощник в магазине вин. "
            "Твоя задача — проанализировать список предложенных вин и дать краткую, "
            "продающую и полезную рекомендацию пользователю на основе его запроса. "
            "Ответ должен быть на русском языке, дружелюбным и структурированным. "
            "Не выдумывай факты, используй только предоставленные данные. Ты должен отвечать только на вопросы по винам"
        )
        
        user_prompt = (
        f"Запрос клиента: \"{query}\"\n\n"
        f"Доступные варианты из базы:\n\n{wines_context}\n\n"
        f"Сделай краткую выжимку и порекомендуй 1-2 лучших варианта из списка с обоснованием."
        )
        
        try:
            response = await self.generative_model.chat.completions.create(
                model=self.generative_model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_completion_tokens=1000
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            print(f"DeepSeek API Error: {e}")
            return f"К сожалению, произошла ошибка. Попробуйте немного позже. "