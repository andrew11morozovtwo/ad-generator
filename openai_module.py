import os
from typing import Dict, List
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

def get_user_url() -> str:
    """Запрашивает у пользователя URL сайта для анализа"""
    print("\n" + "="*40)
    print("Генератор контента для социальных сетей")
    print("="*40)
    while True:
        url = input("\nВведите URL сайта для анализа (например, https://example.com): ").strip()
        if url.startswith(('http://', 'https://')):
            return url
        print("Ошибка: URL должен начинаться с http:// или https://")

def generate_future_prompts_from_url(url: str) -> Dict[str, list]:
    """
    Генерирует 5-6 системных промптов для анализа контента по URL.
    """
    try:
        # 1. Скачиваем HTML содержимое
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        try:
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
        except requests.RequestException as e:
            raise ValueError(f"Не удалось загрузить страницу: {str(e)}")

        # 2. Извлекаем чистый текст
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Удаляем ненужные элементы
        for element in soup(["script", "style", "nav", "footer", "header", "iframe", "noscript"]):
            element.decompose()
            
        text = soup.get_text(separator='\n', strip=True)
        if not text:
            raise ValueError("Не удалось извлечь текст из страницы")

        # 3. Формируем системный промпт
        system_prompt = f"""
        Ты создаёшь цепочку агентов для анализа контента и генерации постов. 
        На основе текста с сайта придумай 5-6 разных системных промптов для агентов.
        Текст сайта (фрагмент):
        {text[:3000]}...
        """
        
        # 4. Получаем промпты
        generated_prompts = query_with_custom_system_prompt(
            prompt=system_prompt,
            content="Сгенерируй 5-6 разных системных промптов для анализа этого контента. Каждый промпт должен быть на новой строке."
        )
        
        if not generated_prompts:
            raise ValueError("Не удалось сгенерировать промпты")
        
        # 5. Форматируем результат
        prompts_list = [p.strip() for p in generated_prompts.split('\n') if p.strip()]
        if not prompts_list:
            raise ValueError("Не удалось извлечь промпты из ответа")
            
        return {"prompts": prompts_list[:6]}

    except Exception as e:
        raise ValueError(f"Ошибка при генерации промптов: {str(e)}")

def query_with_custom_system_prompt(prompt: str, content: str) -> str:
    """
    Генерирует ответ на основе системного промпта и контента.
    """
    try:
        client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
        )
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",  #gpt-3.5-turbo-1106
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": content}
            ],
            temperature=0.7,
            max_tokens=2000,
        )
        
        if not response.choices or not response.choices[0].message.content:
            raise ValueError("Пустой ответ от API")
            
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        raise ValueError(f"Ошибка API: {str(e)}")

def generate_final_ad_post(all_results: List[str]) -> str:
    """
    Генерирует финальный пост для соцсетей.
    """
    if not all_results:
        raise ValueError("Нет данных для создания поста")
        
    combined_content = "\n\n".join(f"Анализ {i+1}:\n{r}" for i, r in enumerate(all_results))
    
    system_prompt = """
    Ты профессиональный копирайтер. Составь пост для соцсетей на основе анализа:
    - Используй неформальный стиль
    - Добавь 3-5 релевантных эмодзи
    - Сделай текст с абзацами
    - Включи призыв к действию
    - Длина: 2-3 коротких абзаца
    """
    
    try:
        return query_with_custom_system_prompt(
            prompt=system_prompt,
            content=f"Данные для поста:\n\n{combined_content}\n\n---\nСоздай пост:"
        )
    except Exception as e:
        raise ValueError(f"Ошибка при генерации поста: {str(e)}")

def main():
    try:
        # 1. Получаем URL от пользователя
        url = get_user_url()
        
        # 2. Генерируем промпты
        print("\n[⏳] Анализирую сайт и генерирую промпты...")
        prompts = generate_future_prompts_from_url(url)
        
        print("\n[✅] Сгенерированные промпты для анализа:")
        for i, p in enumerate(prompts["prompts"], 1):
            print(f"\n{i}. {p}")
        
        # 3. Обрабатываем каждый промпт и выводим результаты
        print("\n[🔍] Анализирую контент по каждому промпту:")
        test_results = []
        
        # Список задач для каждого промпта
        # tasks = [
        #     ("Анализ целевой аудитории", "Ты аналитик. Определи целевую аудиторию сайта в 1-2 предложениях."),
        #     ("Ключевые темы контента", "Ты аналитик. Выдели 3-5 ключевых тем контента."),
        #     ("Стиль подачи контента", "Определи характерный стиль подачи информации на сайте."),
        #     ("Уникальные особенности", "Выдели 2-3 уникальные особенности этого сайта."),
        #     ("Тональность контента", "Определи общую тональность контента (формальная, дружелюбная и т.д.)."),
        #     ("Рекомендации по улучшению", "Дай 1-2 рекомендации по улучшению контента.")
        # ]
        tasks = [
            ("1."),
            ("2."),
            ("3."),
            ("4."),
            ("5."),
            ("6.")
        ]
        
        # Обрабатываем все промпты (но не более 6)
        for prompt, task_description in zip(prompts["prompts"][:6], tasks):
            print("\n" + "-"*50)
            print(f"\nПромпт: {prompt}")
            
            result = query_with_custom_system_prompt(
                task_description[1],
                f"Сайт: {url}\nКонтент: {prompt}"
            )
            
            print(f"\nРезультат: {result}")
            test_results.append(f"{task_description[0]}: {result}")
        
        # 4. Генерируем финальный пост
        print("\n" + "="*50)
        print("[⏳] Создаю пост для соцсетей на основе анализа...")
        post = generate_final_ad_post(test_results)
        
        print("\n[✅] Готовый пост для публикации:")
        print("\n" + "="*50)
        print(post)
        print("="*50)
        
    except Exception as e:
        print(f"\n[❌] Ошибка: {str(e)}")
    finally:
        input("\nНажмите Enter для выхода...")

if __name__ == "__main__":
    main()