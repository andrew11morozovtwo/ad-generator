#Я остановился на таком коде, как работающем наиболее стабильно:
from flask import Flask, render_template, request, redirect, url_for
from openai_module import (
    generate_future_prompts_from_url,
    query_with_custom_system_prompt,
    generate_final_ad_post
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
            prompts_data = generate_future_prompts_from_url(url)
            prompts = prompts_data['prompts']
            results = []
            # tasks = [
            #     ("Анализ ЦА", "Определи целевую аудиторию сайта в 1-2 предложениях."),
            #     ("Ключевые темы", "Выдели 3-5 ключевых тем контента."),
            #     ("Стиль подачи", "Опиши стиль подачи информации на сайте."),
            #     ("Уникальные особенности", "Выдели 2-3 уникальные особенности сайта."),
            #     ("Тональность", "Определи тональность контента (формальная/дружелюбная)."),
            #     ("Рекомендации", "Дай 1-2 рекомендации по улучшению контента.")
            # ]
            
            tasks = [
                   ("1."),
                   ("2."),
                   ("3."),
                   ("4."),
                   ("5."),
                   ("6.")
             ]
            for prompt, task in zip(prompts, tasks):
                result = query_with_custom_system_prompt(task[1], f"Сайт: {url}\nКонтент: {prompt}")
                results.append(f"{task[0]}: {result}")
            
            analysis_results['data'] = {
                'url': url,
                'prompts': prompts,
                'results': results,
                'final_post': generate_final_ad_post(results)
            }
            return redirect(url_for('results'))
        except Exception as e:
            return render_template('error.html', error=str(e))
    return render_template('index.html')

@app.route('/processing')
def processing():
    url = analysis_results.get('processing_url')
    if not url:
        return redirect(url_for('index'))
    
    # Передаем URL в шаблон
    return render_template('processing.html', url=url)


@app.route('/results')
def results():
    data = analysis_results.get('data')
    return render_template('results.html', **data) if data else redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

