import os
import requests
import asyncio
from telegram import Bot

# Все источники тестов, сгруппированные по кластерам
TEST_CLUSTERS = [
    {
        "cluster_name": "🔬 Кластери 1 - Табиӣ ва техникӣ",
        "subjects": [
            {
                "subject": "Забони тоҷикӣ",
                "url": "https://raw.githubusercontent.com/meetmeonlinefree/dovtalab2026/refs/heads/main/normal_test_cluster_1_subject_1.json"
            },
            {
                "subject": "Математика",
                "url": "https://raw.githubusercontent.com/meetmeonlinefree/dovtalab2026/refs/heads/main/normal_test_cluster_1_subject_2.json"
            },
            {
                "subject": "Химия",
                "url": "https://raw.githubusercontent.com/meetmeonlinefree/dovtalab2026/refs/heads/main/normal_test_cluster_1_subject_3.json"
            },
            {
                "subject": "Физика",
                "url": "https://raw.githubusercontent.com/meetmeonlinefree/dovtalab2026/refs/heads/main/normal_test_cluster_1_subject_4.json"
            }
        ]
    },
    {
        "cluster_name": "🗺️ Кластери 2 - Иқтисод ва география",
        "subjects": [
            {
                "subject": "Забони тоҷикӣ",
                "url": "https://raw.githubusercontent.com/meetmeonlinefree/dovtalab2026/refs/heads/main/normal_test_cluster_2_subject_5.json"
            },
            {
                "subject": "Математика",
                "url": "https://raw.githubusercontent.com/meetmeonlinefree/dovtalab2026/refs/heads/main/normal_test_cluster_2_subject_6.json"
            },
            {
                "subject": "География",
                "url": "https://raw.githubusercontent.com/meetmeonlinefree/dovtalab2026/refs/heads/main/normal_test_cluster_2_subject_7.json"
            }
            # Если появятся другие предметы для Кластера 2, просто добавьте их сюда по аналогии
        ]
    },
    {
        "cluster_name": "📚 Кластери 3 - Филология, педагогика ва санъат",
        "subjects": [
            {
                "subject": "Забони тоҷикӣ",
                "url": "https://raw.githubusercontent.com/meetmeonlinefree/dovtalab2026/refs/heads/main/normal_test_cluster_3_subject_9.json"
            },
            {
                "subject": "Таърих",
                "url": "https://raw.githubusercontent.com/meetmeonlinefree/dovtalab2026/refs/heads/main/normal_test_cluster_3_subject_10.json"
            },
            {
                "subject": "География",
                "url": "https://raw.githubusercontent.com/meetmeonlinefree/dovtalab2026/refs/heads/main/normal_test_cluster_2_subject_7.json"
            }
            # Если появятся другие предметы для Кластера 2, просто добавьте их сюда по аналогии
        ]
    },
    {
        "cluster_name": "⚖️ Кластери 4 - Ҷомеашиносӣ ва ҳуқуқ",
        "subjects": [
            {
                "subject": "Забони тоҷикӣ",
                "url": "https://raw.githubusercontent.com/meetmeonlinefree/dovtalab2026/refs/heads/main/normal_test_cluster_4_subject_13.json"
            },
            {
                "subject": "Таърих",
                "url": "https://raw.githubusercontent.com/meetmeonlinefree/dovtalab2026/refs/heads/main/normal_test_cluster_4_subject_14.json"
            },
            {
                "subject": "Ҳуқуқ",
                "url": "https://raw.githubusercontent.com/meetmeonlinefree/dovtalab2026/refs/heads/main/normal_test_cluster_4_subject_15.json"
            }
            # Если появятся другие предметы для Кластера 2, просто добавьте их сюда по аналогии
        ]
    },
    {
        "cluster_name": "🧬 Кластери 5 - Тиб, биология ва варзиш",
        "subjects": [
            {
                "subject": "Забони тоҷикӣ",
                "url": "https://raw.githubusercontent.com/meetmeonlinefree/dovtalab2026/refs/heads/main/normal_test_cluster_5_subject_17.json"
            },
            {
                "subject": "Биология",
                "url": "https://raw.githubusercontent.com/meetmeonlinefree/dovtalab2026/refs/heads/main/normal_test_cluster_5_subject_18.json"
            },
            {
                "subject": "Химия",
                "url": "https://raw.githubusercontent.com/meetmeonlinefree/dovtalab2026/refs/heads/main/normal_test_cluster_5_subject_18.json"
            },
            {
                "subject": "Физика",
                "url": "https://raw.githubusercontent.com/meetmeonlinefree/dovtalab2026/refs/heads/main/normal_test_cluster_5_subject_20.json"
            }
        ]
    }
]

CHANNEL_USERNAME = "@dovtalabonline"

async def main():
    # Токен берем из секретов GitHub (чтобы никто не украл ваш токен в открытом репозитории)
    TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not TOKEN:
        print("Ошибка: Токен бота не найден!")
        return

    bot = Bot(token=TOKEN)

    # Простейшая логика для автоматики: отправляем тесты первого попавшегося кластера
    # (Для продвинутого сохранения прогресса по часам лучше сохранять индекс в файл на GitHub, 
    # но для старта можно отправлять случайный или первый кластер каждый час)
    cluster = TEST_CLUSTERS[0] 
    cluster_name = cluster["cluster_name"]

    for sub in cluster["subjects"]:
        subject_name = sub["subject"]
        url = sub["url"]
        
        response = requests.get(url)
        if response.status_code != 200:
            continue
            
        tests = response.json()
        if not tests:
            continue
        
        # Берем первый вопрос (или можете усложнить логику со временем)
        item = tests[0] 
        
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
            print(f"Отправлен: {cluster_name} — {subject_name}")
        except Exception as e:
            print(f"Ошибка: {e}")

if __name__ == "__main__":
    asyncio.run(main())
