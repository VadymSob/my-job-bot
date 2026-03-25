import requests
from bs4 import BeautifulSoup

# 1. Налаштовуємо Telegram (куди писати)
TOKEN = "ТВІЙ_ТОКЕН_БОТА"
CHAT_ID = "ТВІЙ_ID_ЧАТУ"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_id}&text={message}"
    requests.get(url)

# 2. Йдемо на сайт (приклад для демонстрації)
def check_jobs():
    url = "ПОСИЛАННЯ_НА_РЕЗУЛЬТАТИ_ПОШУКУ" # Встав посилання з фільтрами
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Шукаємо заголовки вакансій (це залежить від сайту)
    jobs = soup.find_all('h2')[:5] # Беремо перші 5
    
    report = "Доброго ранку! Ось нові кандидати:\n"
    for job in jobs:
        report += f"- {job.text.strip()}\n"
    
    send_telegram(report)

if __name__ == "__main__":
    check_jobs()
