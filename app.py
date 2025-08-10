#Я остановился на таком коде, как работающем наиболее стабильно:
from flask import Flask, render_template, request, redirect, url_for
from openai_module import (
    generate_future_prompts_from_url,
    query_with_custom_system_prompt,
    generate_final_ad_post,
    get_clean_text  # Добавляем новый импорт
)
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
analysis_results = {}

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        try:
            # Получаем чистый текст с сайта
            website_text = get_clean_text(url)
            if not website_text:
                raise ValueError("Не удалось получить текст с указанного сайта")
            
            # Сохраняем текст для использования в обработке
            analysis_results['website_text'] = website_text
            analysis_results['processing_url'] = url
            
            return redirect(url_for('processing'))
            
        except Exception as e:
            return render_template('error.html', error=str(e))
    return render_template('index.html')

@app.route('/processing')
def processing():
    url = analysis_results.get('processing_url')
    website_text = analysis_results.get('website_text')
    
    if not url or not website_text:
        return redirect(url_for('index'))
    
    try:
        # Генерация промптов на основе текста сайта
        prompts_data = generate_future_prompts_from_url(url)
        prompts = prompts_data['prompts']
        results = []
        
        tasks = ["1.", "2.", "3.", "4.", "5.", "6."]
        
        # Обработка каждого промпта с передачей текста сайта
        for prompt, task in zip(prompts, tasks):
            result = query_with_custom_system_prompt(
                f"{task} {prompt}",  # Объединяем номер задачи и промпт
                f"Текст с сайта:\n{website_text}\n\nЗадание:"
            )
            results.append(f"{task}: {result}")
        
        # Сохранение результатов
        analysis_results['data'] = {
            'url': url,
            'prompts': prompts,
            'results': results,
            'final_post': generate_final_ad_post(results)
        }
        
        return redirect(url_for('results'))
    
    except Exception as e:
        return render_template('error.html', error=str(e))

@app.route('/results')
def results():
    data = analysis_results.get('data')
    return render_template('results.html', **data) if data else redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

