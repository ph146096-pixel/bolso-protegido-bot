import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is alive!")

def run_server():
    server = HTTPServer(('0.0.0.0', 10000), SimpleHandler)
    server.serve_forever()

threading.Thread(target=run_server, daemon=True).start()
import os
import time
import requests
from openai import OpenAI
from dotenv import load_dotenv
import schedule

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

def enviar_noticia_diaria():
    print("\n[Agendador] A gerar resumo de notícias financeiras diárias...")
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system", 
                    "content": "És o jornalista financeiro e analista do canal Bolso Protegido. O teu foco principal é informar sobre notícias do mercado financeiro, tendências económicas, inflação, taxas de juro e o impacto direto no bolso das pessoas."
                },
                {
                    "role": "user", 
                    "content": "Gera um boletim diário de notícias/atualidades financeiras num formato apelativo para o Telegram. Inclui: 1) Um título chamativo, 2) O resumo de 2 a 3 pontos/notícias marcantes do cenário atual ou tendências finanças, 3) Uma conclusão prática de como o leitor se pode proteger financeiramente."
                }
            ]
        )
        noticia = response.choices[0].message.content
        print("[Agendador] Notícia gerada com sucesso! A enviar para o Telegram...")
        
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_ID,
            "text": f"📰 **BOLSO PROTEGIDO - NOTÍCIAS & MERCADO**\n\n{noticia}"
        }

        res = requests.post(url, json=payload)
        if res.status_code == 200:
            print("✅ [Agendador] Boletim de notícias enviado com sucesso para o Telegram!")
        else:
            print(f"❌ Erro ao enviar: {res.text}")
            
    except Exception as e:
        print(f"❌ Ocorreu um erro: {e}")

# --- AGENDAMENTO DIÁRIO (09:00) ---
schedule.every().day.at("09:00").do(enviar_noticia_diaria)

print("📰 Bot de Notícias do Bolso Protegido iniciado!")
print("A aguardar pelo horário agendado (09:00 diárias)...")

while True:
    schedule.run_pending()
    time.sleep(1)
