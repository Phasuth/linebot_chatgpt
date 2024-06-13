from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import (MessageEvent,
                            TextMessage,
                            TextSendMessage)

import openai
openai.api_key = "sk-proj-3kj2xfb8pzOi6W9JTKTTT3BlbkFJ8CM6S4I8g9skAmn2PutM"
model_use = "text-davinci-003"

channel_secret = "28fa8d53a5d322a1fc34e31204e3fdb5"
channel_access_token = "grDe5Mq86by+YIyfH19DyeWNglgEGK8hqCYTXT/7zQqe/XHNgNA0NKDXZrgssinUfCYdXxFX2wMiItzhIlO7eQPN72y3awANItmNCA2TDDbGt9zS59TcTOapui427Y4oyhaoXRKNVScw0C3AdccWRAdB04t89/1O/w1cDnyilFU="

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def home():
    try:
        signature = request.headers["X-Line-Signature"]
        body = request.get_data(as_text=True)
        handler.handle(body, signature)
    except:
        pass
    
    return "Hello Line Chatbot"

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    text = event.message.text
    print(text)

    prompt_text = text

    response = openai.Completion.create(
        model=model_use,
        prompt=prompt_text,  
        max_tokens=1024) # max 4096

    text_out = response.choices[0].text 
    line_bot_api.reply_message(event.reply_token,
                               TextSendMessage(text=text_out))

if __name__ == "__main__":          
    app.run()

