import requests
from bs4 import BeautifulSoup
import os

def get_candidates():
    # Ваше посилання з фільтрами
    url = "https://www.work.ua/resumes-vinnytsya-комерційний+директор/"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
        "Cookie": os.getenv("WORK_UA_COOKIE")
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return f"Помилка: сайт повернув код {response.status_code}"

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Шукаємо картки кандидатів
    # На Work.ua це зазвичай блоки div з класом card-resumes
    cards = soup.find_all('div', class_='card-resumes')[:5] 
    
    if not cards:
        return "Сьогодні нових кандидатів не знайдено або доступ обмежено."

    report = "💼 Нові кандидати (Вінниця | Комерційний директор):\n\n"
    for card in cards:
        title_tag = card.find('h2')
        if title_tag:
            name = title_tag.text.strip()
            link = "https://www.work.ua" + title_tag.find('a')['href']
            # Можна додати короткий опис, якщо він є в карті
            info = card.find('p', class_='text-muted')
            info_text = info.text.strip() if info else ""
            
            report += f"👤 {name}\nℹ️ {info_text}\n🔗 {link}\n\n"
    
    return report

def send_telegram(message):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("CHAT_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url, data={"chat_id": chat_id, "text": message})

if __name__ == "__main__":
    content = get_candidates()
    send_telegram(content)
