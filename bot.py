import json
import os
import asyncio
import requests
from telegram import Bot

# Все источники тестов, сгруппированные по кластерам
TEST_CLUSTERS = [
    {
        "cluster_name": "🔬 Кластери 1 - Табиӣ ва техникӣ",
        "subjects": [
            {"subject": "Забони тоҷикӣ", "url": "https://raw.githubusercontent.com/meetmeonlinefree/dovtalab2026/refs/heads/main/normal_test_cluster_1_subject_1.json"},
            {"subject": "Математика", "url": "https://raw.githubusercontent.com/meetmeonlinefree/dovtalab2026/refs/heads/main/normal_test_cluster_1_subject_2.json"},
            {"subject": "Химия", "url": "https://raw.githubusercontent.com/meetmeonlinefree/dovtalab2026/refs/heads/main/normal_test_cluster_1_subject_3.json"},
            {"subject": "Физика", "url": "https://raw.githubusercontent.com/meetmeonlinefree/dovtalab2026/refs/heads/main/normal_test_cluster_1_subject_4.json"}
        ]
    },
    {
        "cluster_name": "🗺️ Кластери 2 - Иқтисод ва география",
        "subjects": [
            {"subject": "Забони тоҷикӣ", "url": "https://raw.githubusercontent.com/meetmeonlinefree/dovtalab2026/refs/heads/main/normal_test_cluster_2_subject_5.json"},
            {"subject": "Математика", "url": "https://raw.githubusercontent.com/meetmeonlinefree/dovtalab2026/refs/heads/main/normal_test_cluster_2_subject_6.json"},
            {"subject": "География", "url": "https://raw.githubusercontent.com/meetmeonlinefree/dovtalab2026/refs/heads/main/normal_test_cluster_2_subject_7.json"}
        ]
    },
    {
        "cluster_name": "📚 Кластери 3 - Филология, педагогика ва санъат",
        "subjects": [
            {"subject": "Забони тоҷикӣ", "url": "https://raw.githubusercontent.com/meetmeonlinefree/dovtalab2026/refs/heads/main/normal_test_cluster_3_subject_9.json"},
            {"subject": "Таърих", "url": "https://raw.githubusercontent.com/meetmeonlinefree/dovtalab2026/refs/heads/main/normal_test_cluster_3_subject_10.json"},
            {"subject": "География", "url": "https://raw.githubusercontent.com/meetmeonlinefree/dovtalab2026/refs/heads/main/normal_test_cluster_2_subject_7.json"}
        ]
    },
    {
        "cluster_name": "⚖️ Кластери 4 - Ҷомеашиносӣ ва ҳуқуқ",
        "subjects": [
            {"subject": "Забони тоҷикӣ", "url": "https://raw.githubusercontent.com/meetmeonlinefree/dovtalab2026/refs/heads/main/normal_test_cluster_4_subject_13.json"},
            {"subject": "Таърих", "url": "https://raw.githubusercontent.com/meetmeonlinefree/dovtalab2026/refs/heads/main/normal_test_cluster_4_subject_14.json"},
            {"subject": "Ҳуқуқ", "url": "https://raw.githubusercontent.com/meetmeonlinefree/dovtalab2026/refs/heads/main/normal_test_cluster_4_subject_15.json"}
        ]
    },
    {
        "cluster_name": "🧬 Кластери 5 - Тиб, биология ва варзиш",
        "subjects": [
            {"subject": "Забони тоҷикӣ", "url": "https://raw.githubusercontent.com/meetmeonlinefree/dovtalab2026/refs/heads/main/normal_test_cluster_5_subject_17.json"},
            {"subject": "Биология", "url": "https://raw.githubusercontent.com/meetmeonlinefree/dovtalab2026/refs/heads/main/normal_test_cluster_5_subject_18.json"},
            {"subject": "Химия", "url": "https://raw.githubusercontent.com/meetmeonlinefree/dovtalab2026/refs/heads/main/normal_test_cluster_5_subject_18.json"},
            {"subject": "Физика", "url": "https://raw.githubusercontent.com/meetmeonlinefree/dovtalab2026/refs/heads/main/normal_test_cluster_5_subject_20.json"}
        ]
    }
]

CHANNEL_USERNAME = "@dovtalabonline"
PROGRESS_FILE = "progress.json"

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            pass
    return {"subject_progress": {}, "current_cluster_index": 0}

def save_progress(data):
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

async def main():
    TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not TOKEN:
        print("❌ Ошибка: Не найдена переменная окружения TELEGRAM_BOT_TOKEN!")
        return

    bot = Bot(token=TOKEN)
    data = load_progress()
    subject_progress = data["subject_progress"]
    current_cluster_index = data["current_cluster_index"]
    
    cluster = TEST_CLUSTERS[current_cluster_index]
    cluster_name = cluster["cluster_name"]
    
    print(f"🕒 Отправка тестов для: {cluster_name}")
    
    for sub in cluster["subjects"]:
        subject_name = sub["subject"]
        url = sub["url"]
        
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Ошибка загрузки JSON для {cluster_name} - {subject_name}")
            continue
            
        tests = response.json()
        
        if url not in subject_progress:
            subject_progress[url] = 0
            
        q_index = subject_progress[url]
        
        if q_index >= len(tests):
            q_index = 0
            subject_progress[url] = 0
            
        item = tests[q_index]
        
        question_text = f"🎯 {cluster_name} | {subject_name}\nСаволи №{item['id']}:\n{item['question']}"
        options = item['options']
        correct_index = item['correctIndex']
        image_url = item.get("image")
        
        try:
            if image_url:
                await bot.send_photo(chat_id=CHANNEL_USERNAME, photo=image_url, caption=question_text)
                await bot.send_poll(
                    chat_id=CHANNEL_USERNAME,
                    question=f"🎯 {cluster_name} | {subject_name} (Савол №{item['id']}):",
                    options=options,
                    type='quiz',                  
                    correct_option_id=correct_index, 
                    is_anonymous=True            
                )
            else:
                await bot.send_poll(
                    chat_id=CHANNEL_USERNAME,
                    question=question_text,
                    options=options,
                    type='quiz',                  
                    correct_option_id=correct_index, 
                    is_anonymous=True            
                )
                
            print(f"  ✅ Отправлен тест: {subject_name} (ID: {item['id']})")
            subject_progress[url] += 1
            
        except Exception as e:
            print(f"  ❌ Ошибка отправки теста {subject_name}: {e}")
            
    # Переходим к следующему кластеру на следующий час
    data["current_cluster_index"] = (current_cluster_index + 1) % len(TEST_CLUSTERS)
    data["subject_progress"] = subject_progress
    save_progress(data)
    print("✅ Рассылка пачки завершена, прогресс сохранен.")

if __name__ == '__main__':
    asyncio.run(main())
