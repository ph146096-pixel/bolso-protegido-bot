import os
import requests
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Novo Token do Bot Recém-Criado
TOKEN = "8995166674:AAExzB04Z5oL_RdvDpF-qwT4roz4VpE1yXg"
CHAT_ID = "8911306648"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

print("A gerar dica financeira com a OpenAI...")
client = OpenAI(api_key=OPENAI_API_KEY)

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "És um assistente especializado em finanças pessoais para o canal Bolso Protegido."},
        {"role": "user", "content": "Dá-me uma dica curta, prática e impactante de poupança para o próximo vídeo."}
    ]
)

dica = response.choices[0].message.content
print("Dica gerada com sucesso!\n")

print("A enviar mensagem para o teu Telegram...")
url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
payload = {
    "chat_id": CHAT_ID,
    "text": f"🤖 **Nova Dica do Bolso Protegido:**\n\n{dica}"
}

res = requests.post(url, json=payload)

if res.status_code == 200:
    print("✅ SUCESSO! Verifica o teu telemóvel, a mensagem já lá deve estar!")
else:
    print(f"❌ Erro ao enviar: {res.text}")