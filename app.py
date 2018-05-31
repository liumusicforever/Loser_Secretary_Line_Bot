# -*- coding: utf-8 -*-

import csv
import random


from flask import Flask, request, abort



from linebot import (

    LineBotApi, WebhookHandler

)

from linebot.exceptions import (

    InvalidSignatureError

)

from linebot.models import *

token = '7mBi3Z0k7gsS+p4zXNzSmQKNWli4KoKDVPYfvfwjNhAacjeAI9PgCUe5aVRNXV+c93c1NLtVr1BrrdMGFikE5B8zpkY3T0FTIo0O01TDIUAK4yA4JtBCIsfTZG4P4QY/Z8J4HOw5Tvat9gMp8a/fWwdB04t89/1O/w1cDnyilFU='

screte = '952a4f95456a8034857dec111b51836d'


app = Flask(__name__)



line_bot_api = LineBotApi(token)

handler = WebhookHandler(screte)





@app.route("/callback", methods=['POST'])

def callback():

    # get X-Line-Signature header value

    signature = request.headers['X-Line-Signature']



    # get request body as text

    body = request.get_data(as_text=True)
    print ('*****'+body)
    app.logger.info("Request body: " + body)



    # handle webhook body

    try:

        handler.handle(body, signature)

    except InvalidSignatureError:

        abort(400)



    return 'OK'





@handler.add(MessageEvent, message=TextMessage)

def handle_message(event):


    print ('~~~~',event.message.text)

    if event.message.text == '未婚妻':
        with open('data/sex girl.txt', 'r') as f: 
            data = list(csv.reader(f))
            url = random.choice(data)[1]
        image_message = ImageSendMessage(
            original_content_url=url,

            preview_image_url=url
        )
        context = '老闆，這是為您所挑選的未婚妻，請問您滿意嗎?'
        # line_bot_api.reply_message(event.reply_token,TextSendMessage(text=context))

        line_bot_api.reply_message(
            event.reply_token,
            image_message)
    elif event.message.text == '未婚夫':
        with open('data/sex man.txt', 'r') as f: 
            data = list(csv.reader(f))
            url = random.choice(data)[1]
        image_message = ImageSendMessage(
            original_content_url=url,

            preview_image_url=url
        )
        context = '老闆，這是為您所挑選的未婚夫，請問您滿意嗎?'
        
        line_bot_api.reply_message(
            event.reply_token,
            image_message)
    elif '我愛' in event.message.text:
        
        av_nets = [
            'https://www.pornhub.com/video/search?search=',
            'https://www.xvideos.com/?k=',
            'http://www.whichav.com/node/keywords?q=',
            'https://xo104.com/?s=',

        ]
        keyword = event.message.text.split('我愛')[-1]
        url = random.choice(av_nets)+keyword        
        
        context = '老闆，這是為您個人喜好所準備的網站:{} , 請您過目，希望您您精神滿滿。'.format(url)

        line_bot_api.reply_message(

            event.reply_token,

            TextSendMessage(text=context))
    elif event.message.text == "有錢是老大":
        import json
        with open('data/sex_girl_line_ids.json') as json_data:
            girls = json.load(json_data)
        
        selected_g = random.sample(girls,3)

        print (selected_g)

        Carousel_template = TemplateSendMessage(

        alt_text='老闆，以下是精心為您挑選的極品',

        template=CarouselTemplate(

        columns=[

            CarouselColumn(

                thumbnail_image_url=g["show_image"],

                title=g["title"],

                text=g["description"],

                actions=[

                    URITemplateAction(

                        label=g["action"][0],

                        uri=g["action"][1]

                    )

                ]

            ) for g in selected_g

        ]))
        line_bot_api.reply_message(event.reply_token, Carousel_template)
    else:
        line_bot_api.reply_message(

            event.reply_token,

            TextSendMessage(text=event.message.text))





if __name__ == "__main__":

    app.run(host = 'localhost' , port = 7777)









