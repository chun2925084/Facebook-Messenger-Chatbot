#coding:utf-8
import urllib.request
from transitions.extensions import GraphMachine

from utils import send_text_message
from utils import send_button_message
from utils import send_image_url
from database_connect import insert_data
from database_connect import update_solution
from database_connect import update_finish
from useful_function import send_question
from useful_function import send_solution
from google_ocr import produce_word



name = ""
url = ""
temp = ""
ask_question = ""

class TocMachine(GraphMachine):
    def __init__(self, **machine_configs):
        self.machine = GraphMachine(
            model=self,
            **machine_configs
        )

    def is_going_to_user(self, event, count):
        if event.get("message"):
            print("WWWW")
            if event['message'].get('is_echo'):
                return False
            else:
                if event['message'].get('text'):
                    text = event['message']['text']
                    if text == '懂':
                        send_text_message(event['sender']['id'], "你怎麼這麼棒")
                        update_finish(str(count[0])+".jpg", '1')
                        return 1
                    elif text == '不懂':
                        send_text_message(event['sender']['id'], "那只好下次上課再幫你了!")
                        print(text)
                        return 1
                    elif text == 'Finish':
                        return 1
                # return text.lower() == 'finish'
        return False

    def is_going_to_asking(self, event, count):
        if event.get("message"):
            if event['message'].get('text'):
                text = event['message']['text']
                if text == '我想問問題':#:
                    return 1
        elif event.get("postback"):
            if event['postback'].get('title'):
                text = event['postback']['title']
                if text == '我想問問題':
                    print(text)
                    return 1

        return False

    def is_going_to_choose(self, event, count):

        if event.get("message"):
            if event['message'].get('text'):
                text = event['message']['text']
                if text == '我需要大量的題目':
                    return 1
        elif event.get("postback"):
            if event['postback'].get('title'):
                text = event['postback']['title']
                if text == '我需要大量的題目':
                    print(text)
                    return 1


        return False

    def is_going_to_label(self, event, count):
        global name
        global url
        if event.get("message"):
            if event['message'].get('text'):
                text = event['message']['text']
                return text.lower() == 'go to label'

            elif event['message'].get('attachments'):
                if event['message']['attachments'][0]['type'] == 'image':
                    print(event)
                    url = event['message']['attachments'][0]['payload']['url']
                    print(url)
                    # save_file = urllib.URLopener()
                    count[0] = count[0] + 1
                    name = "./upload/" + str(count[0]) + ".jpg"
                    # print(name)
                    # save_file.retrieve(url, name)
                    urllib.request.urlretrieve(url, name)
                    return 1
        return False

    def is_going_to_waiting(self, event, count):
        if event.get("postback"):
            if event['postback'].get('title'):
                text = event['postback']['title']
                insert_data('Physics', text, url, name, str(count[0])+".jpg", '0', '0')
                print(text)
                return 1
            
    def is_going_to_check(self, event, count):
        if event['message'].get('is_echo') and event['message'].get('attachments'):
            if event['message']['is_echo'] == True:
                url = event['message']['attachments'][0]['payload']['url']
                print(url)
                update_solution(str(count[0])+".jpg", url)
                print("good to get ")
                return 1


    def is_going_to_send_question(self, event, count):
        sender_id = event['sender']['id']
        global temp
        temp = sender_id
        global ask_question
        if event.get("postback"):
            if event['postback'].get('title'):
                text = event['postback']['title']
                if text == '運動學':
                    print(text)
                    ask_question = send_question(text)
                    send_image_url(sender_id, ask_question)
                elif text == '力學':
                    print(text)
                    ask_question = send_question(text)
                    send_image_url(sender_id, ask_question)
                button = [{
                    "type": "postback",
                    "title": "好!!!",
                    "payload":"DEVELOPER_DEFINED" 
                },
                {
                    "type": "postback",
                    "title": "不用, 我最厲害~",
                    "payload": "DEVELPER_DEFINED"
                }]
                send_button_message(temp, button, "需要答案嗎?")
                return 1
    
    def is_going_to_ans(self, event, count):
        sender_id = event['sender']['id']
        if event.get("postback"):
            if event['postback'].get('title'):
                text = event['postback']['title']
                if text == '好!!!':
                    print(text)
                    sol = send_solution(ask_question)
                    send_image_url(sender_id, sol)
                    return 1
                elif text == '不用, 我最厲害~':
                    print(text)
                    sol = send_solution(ask_question)
                    send_image_url(sender_id, sol)
                    return 1

    def is_going_to_convert(self, event, count):
        if event.get("message"):
            if event['message'].get('text'):
                text = event['message']['text']
                if text == '幫我把圖片轉成文字！！':
                    return 1
        elif event.get("postback"):
            if event['postback'].get('title'):
                text = event['postback']['title']
                if text == '幫我把圖片轉成文字！！':
                    print(text)
                    return 1

    def is_going_to_produces(self, event, count):
        global name
        global url
        if event.get("message"):
            if event['message'].get('text'):
                text = event['message']['text']
                return text.lower() == 'go to label'

            elif event['message'].get('attachments'):
                if event['message']['attachments'][0]['type'] == 'image':
                    print(event)
                    url = event['message']['attachments'][0]['payload']['url']
                    print(url)
                    #save_file = urllib.URLopener()
                    name = "./convert/sample.jpg"
                    #save_file.retrieve(url, name)
                    urllib.request.urlretrieve(url, name)
                    return 1
        return False

    def on_enter_user(self, event, count):

        print(self.state)
        sender_id = event['sender']['id']
        button = [{
                    "type": "postback",
                    "title": "我想問問題",
                    "payload":"DEVELOPER_DEFINED" 
                },
                {
                    "type": "postback",
                    "title": "我需要大量的題目",
                    "payload": "DEVELPER_DEFINED"
                },
                {
                    "type": "postback",
                    "title": "幫我把圖片轉成文字！！",
                    "payload":"DEVELOPER_DEFINED" 
                }]
                
        responese = send_button_message(sender_id, button, "要幹嘛拉~~~")
        return 1

    def on_enter_asking(self, event,count):
        print("I'm entering asking")
        global temp
        sender_id = event['sender']['id']
        temp = sender_id
        responese = send_text_message(sender_id, "ok, 把你的問題傳來吧!")
        print(self.state)
        return 1
        #self.go_back()
    def on_enter_choose(self, event, count):
        sender_id = event['sender']['id']
        button = [{
                    "type": "postback",
                    "title": "運動學",
                    "payload":"DEVELOPER_DEFINED" 
                },
                {
                    "type": "postback",
                    "title": "力學",
                    "payload": "DEVELPER_DEFINED"
                }]
        response = send_button_message(sender_id, button, "想要哪一種類型呢？")
        return 1

    def on_enter_convert(self, event, count):
        sender_id = event['sender']['id']
        send_text_message(sender_id, "ok! send it")


    def on_exit_asking(self, event, count):
        print('bye bye')

    def on_enter_label(self, event, count):
        print("I'm entering label")

        sender_id = event['sender']['id']
        button = [{
                    "type": "postback",
                    "title": "運動學",
                    "payload":"DEVELOPER_DEFINED" 
                },
                {
                    "type": "postback",
                    "title": "力學",
                    "payload": "DEVELPER_DEFINED"
                }]
        responese = send_button_message(sender_id, button, "順便標記一下!")

        return 1
        #elf.go_back()
    def on_enter_waiting(sel, event, count):
        sender_id = event['sender']['id']
        send_text_message(sender_id, "等我一下唷!")

    def on_enter_check(self, event, count):
        responese = send_text_message(temp, "這樣懂了嗎??如果懂得話就回答懂, 不懂就不要裝懂, 直接回答不懂, 我不會生氣")

    def on_enter_produces(self, event, count):
        print("produce")
        sender_id = event['sender']['id']
        produce_word()
        f = open("output.txt","r")
        send_text_message(sender_id, f.read())
        send_text_message(sender_id, "type finish")

    def on_exit_label(self, event, count):
        print('Leaving label')

    def on_enter_ans(self, event, count):
        send_text_message(temp, "這樣懂了嗎??如果懂得話就回答懂, 不懂就不要裝懂, 直接回答不懂, 我不會生氣")
