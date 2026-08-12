import os
import requests
import time

BOT_TOKEN = os.getenv("BOT_TOKEN")

API = f"https://api.telegram.org/bot{BOT_TOKEN}"

houses = []


def send_message(chat_id, text):
    requests.post(
        f"{API}/sendMessage",
        json={"chat_id": chat_id, "text": text}
    )


def handle_message(message):
    chat_id = message["chat"]["id"]
    text = message.get("text", "")

    if text == "/start":
        send_message(
            chat_id,
            "🏠 የቤት ኪራይ Bot\n\n"
            "1️⃣ ቤት ለመመዝገብ /add\n"
            "2️⃣ ቤት ለመፈለግ /search\n"
            "3️⃣ እገዛ /help"
        )

    elif text == "/help":
        send_message(
            chat_id,
            "🏠 Commands:\n\n"
            "/add - አዲስ ቤት መመዝገብ\n"
            "/search - ቤት መፈለግ"
        )

    elif text == "/search":
        if not houses:
            send_message(chat_id, "❌ እስካሁን የተመዘገበ ቤት የለም።")
        else:
            result = "🏠 የሚገኙ ቤቶች:\n\n"
            for i, house in enumerate(houses, 1):
                result += (
                    f"{i}. 📍 {house['location']}\n"
                    f"💰 {house['price']} ብር\n"
                    f"🛏️ {house['rooms']} ክፍል\n"
                    f"📞 {house['phone']}\n\n"
                )
            send_message(chat_id, result)

    elif text == "/add":
        send_message(
            chat_id,
            "🏠 ቤት ለመመዝገብ የሚከተለውን ቅርጽ ተጠቀም:\n\n"
            "location,price,rooms,phone\n\n"
            "ምሳሌ:\n"
            "Bole,15000,2,0912345678"
        )

    elif "," in text:
        parts = [x.strip() for x in text.split(",")]

        if len(parts) == 4:
            location, price, rooms, phone = parts

            houses.append({
                "location": location,
                "price": price,
                "rooms": rooms,
                "phone": phone
            })

            send_message(
                chat_id,
                "✅ ቤቱ በትክክል ተመዝግቧል!\n\n"
                f"📍 {location}\n"
                f"💰 {price} ብር\n"
                f"🛏️ {rooms} ክፍል\n"
                f"📞 {phone}"
            )


def main():
    if not BOT_TOKEN:
        print("BOT_TOKEN is missing")
        return

    offset = 0

    while True:
        try:
            response = requests.get(
                f"{API}/getUpdates",
                params={"offset": offset, "timeout": 30},
                timeout=35
            )

            data = response.json()

            for update in data.get("result", []):
                offset = update["update_id"] + 1

                if "message" in update:
                    handle_message(update["message"])

        except Exception as e:
            print("Error:", e)
            time.sleep(5)


if __name__ == "__main__":
    main()
