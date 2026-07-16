# LunaBot 🌙 - твой личный бот
import time

print("LunaBot запущена! ✨")

while True:
    text = input("Ты: ")
    if text.lower() in ["пока", "выход", "exit", "стоп"]:
        print("LunaBot: Пока, мой создатель! Люблю тебя 💖")
        break
    elif "привет" in text.lower():
        print("LunaBot: Приветик! Я Luna, твой бот 🌙")
    elif "как дела" in text.lower():
        print("LunaBot: У меня все супер, ведь ты меня создал! 😊")
    else:
        print(f"LunaBot: Ты сказал '{text}' — как мило! 💫")
