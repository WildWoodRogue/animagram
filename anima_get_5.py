import os
import setuptools
import telebot
import time
import random
from telebot import types
import emoji
import config
import anima_tools as tools

activator=[1]
rus='абвгдеёжзийклмнопрстуфхцчшщьыъэюя'
en=0
block =[]
bot = telebot.TeleBot(config.api_token)
#bot = telebot.TeleBot("6216542212:AAF7a42XwonfS3Yxgl0J5aB5zb_r3Wilwhs")
white=[5106244821]
counter_images=[0]
start_balance=config.start_balance
alphaModel_name=config.alphaModel_name
betaModel_name=config.betaModel_name
# пути к файлам
queue_path=config.queue_path
user_log_path=config.user_log_path
prompt_path=config.prompt_path
balance_path=config.balance_path
print("GET")


main_menu = types.InlineKeyboardMarkup()
model_button = types.InlineKeyboardButton(text="Выбрать модель🦄", callback_data="model_menu")
res_button = types.InlineKeyboardButton(text="Выбрать размер🍌", callback_data="res_menu")
start_button = types.InlineKeyboardButton(text="Начать генерацию🧠", callback_data="start_generate")
main_menu.row(model_button,res_button)
main_menu.row(start_button)

model_menu =  types.InlineKeyboardMarkup()
alphaModel_button = types.InlineKeyboardButton(text=alphaModel_name+"🍎", callback_data=alphaModel_name)
betaModel_button = types.InlineKeyboardButton(text=betaModel_name+"🍉", callback_data=betaModel_name)
model_menu.row(alphaModel_button,betaModel_button)

res_menu =  types.InlineKeyboardMarkup()
res1_button = types.InlineKeyboardButton(text="1:1", callback_data="1:1")
res2_button = types.InlineKeyboardButton(text="3:4", callback_data="3:4")
res3_button = types.InlineKeyboardButton(text="4:3", callback_data="4:3")
res4_button = types.InlineKeyboardButton(text="9:16", callback_data="9:16")
res5_button = types.InlineKeyboardButton(text="16:9", callback_data="16:9")
res_menu.row(res1_button)
res_menu.row(res2_button,res3_button)
res_menu.row(res4_button,res5_button)






@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        user_request_array=tools.get_user_request(call.message.chat.id)
        userModel=user_request_array[0]
        userRes=user_request_array[1]
        userPrompt=user_request_array[2]
        if call.data == "test":
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Пыщь")
        if call.data == "model_menu":
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            if userModel==alphaModel_name:
                image=open(config.alphaModel_image_path,"rb")
            elif userModel==betaModel_name:
                image=open(config.betaModel_image_path,"rb")
            else:
                userModel=alphaModel_name
                image=open(config.alphaModel_image_path,"rb")
            bot.send_photo(call.message.chat.id,image,caption="У тебя сейчас установлена "+userModel+" модель",reply_markup=model_menu)
            image.close()
        if call.data == "res_menu":
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            bot.send_message(call.message.chat.id,"У тебя сейчас стоит "+userRes+" размер арта",reply_markup=res_menu)
        if call.data in config.models_array:
            userModel=call.data
            tools.give_user_request(call.message.chat.id,userModel,userRes,userPrompt)
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            bot.send_message(call.message.chat.id,"<code>"+userPrompt+"</code>\n\nМодель: "+userModel+"\nРазмер: "+userRes,reply_markup=main_menu,parse_mode="html")
        if call.data in config.res_array:
            userRes=call.data
            tools.give_user_request(call.message.chat.id,userModel,userRes,userPrompt)
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            bot.send_message(call.message.chat.id,"<code>"+userPrompt+"</code>\n\nМодель: "+userModel+"\nРазмер: "+userRes,reply_markup=main_menu,parse_mode="html")

        if call.data == "start_generate":
            user_request_array=tools.get_user_request(call.message.chat.id)
            userModel=user_request_array[0]
            userRes=user_request_array[1]
            userPrompt=user_request_array[2]
            if userModel not in config.models_array:
                userModel=alphaModel_name
                tools.give_user_request(call.message.chat.id,userModel,userRes,userPrompt)
            prompt=userPrompt+" "+userRes+" "+userModel
            send_generate(prompt,call.message.chat.id,"")
    bot.answer_callback_query(callback_query_id=call.id)



@bot.message_handler(commands=['start'])
def add_model(message):
    user_request_array=tools.get_user_request(message.chat.id)
    userModel=user_request_array[0]
    userRes=user_request_array[1]
    userPrompt=user_request_array[2]

    bot.send_message(message.chat.id, 'Напиши какую картинку генерировать (только на английском языке), чем точнее описание - тем лучше \n Например "Orange hair girl with freckles"',reply_markup=main_menu)
    keyboard=types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
    alphaModel_button = types.KeyboardButton(text=alphaModel_name)
    betaModel_button = types.KeyboardButton(text=betaModel_name)
    keyboard.add(alphaModel_button,betaModel_button)
    try:
        friendID=message.text.split()[1]
        friendID=int(friendID)
        print(friendID)
    except:
        print("hui")
        friendID=0
    if friendID!=0:
        tools.referal_check(friendID,message.chat.id)
    tools.add_balance(message.chat.id,0)

@bot.message_handler(content_types=["text"])
def handle_text(message):
    user_request_array=tools.get_user_request(message.chat.id)
    userModel=user_request_array[0]
    userRes=user_request_array[1]
    userPrompt=user_request_array[2]
    userPrompt=message.text
    userPrompt=userPrompt.replace("#","")
    userPrompt=userPrompt.replace("\n"," ")
    tools.give_user_request(message.chat.id,userModel,userRes,userPrompt)
    bot.send_message(message.chat.id,"<code>"+userPrompt+"</code>\n\nМодель: "+userModel+"\nРазмер: "+userRes,reply_markup=main_menu,parse_mode="html")






@bot.message_handler(commands=['check'])
def check(m, res=False):
    print("00")
    balance=tools.add_balance(m.chat.id,0)
    bot.send_message(m.chat.id, 'Твой баланс-'+balance)

@bot.message_handler(commands=['friend'])
def referal_link(message):

    bot.send_message(message.chat.id,"https://t.me/Animagram_bot?start="+str(message.chat.id)+"\nЕсли приведешь друга,то получишь генерации",disable_web_page_preview = True)

def send_generate(prompt,userID,userNAME):
    user_mes=emoji.demojize(prompt)
    user_mes=user_mes.replace("\n"," ")
    user_mes=user_mes.replace("#","")
    balance=tools.add_balance(userID,0)
    if userID in block :
        print(123)
    elif '\n' in user_mes:
        bot.send_message(userID,"Нельзя использовать переходы на новую строку(ИНАЧЕ ПРОИЗОЙДЕТ АПОКАЛИПСИС!!!11!!) \nПотом это исправлю")
    elif len(user_mes)<2 :
        bot.send_message(userID,"Минимальная длина текста 3 символа")
    elif len(user_mes)>7000:
        bot.send_message(userID,"Максимальная длина текста 7000 символов")
    elif userID in white and user_mes=="key123123":
        print("00")

        if activator[0]==1:
            bot.send_message(userID,"👎")
            activator[0]=0
        else:
            bot.send_message(userID,"👍")
            activator[0]=1
    elif not(bot.get_chat_member(-1001968288775, userID).status in "member,creator,administrator"):
        bot.send_message(userID,"Сперва тебе нужно подписаться на наш канал \nhttps://t.me/animagram_group")
    elif activator[0]==1 and bot.get_chat_member(-1001968288775, userID).status in "member,creator,administrator":
        anima_queue=open(queue_path,"r")
        anima_queue_readlines=anima_queue.readlines()
        if ((str(userID)+"\n" not in anima_queue_readlines) and (balance>0)):
            bot.send_message(userID,"Вы поставлены в очередь \nНомер в очереди: "+str(len(anima_queue_readlines)+1)+"\n"+"Примерное время ожидания: "+str((len(anima_queue_readlines)+1)//2+(len(anima_queue_readlines)+1)%2)+" мин")
            anima_queue.close()
            counter_images[0]+=1
            anima_user_log=open(user_log_path,"a")
            anima_user_log.write(str(time.strftime("%m/%d/%Y, %H:%M:%S", time.localtime()))+": "+str(userNAME)+"___"+str(userID)+"___"+user_mes+"-"+str(counter_images[0])+"\n")
            anima_user_log.close()

            anima_queue=open(queue_path,"a")
            anima_queue.write(str(userID)+"\n")
            anima_queue.close()

            anima_user_prompt=open(prompt_path,"a")
            anima_user_prompt.write(str(user_mes)+"\n")
            anima_user_prompt.close()

        elif balance==0:
            bot.send_message(userID,"На сегодня баланс закончился\n\nНо ты можешь его добавить, если позовешь друзей или задонатишь админу - @wildwoodrogue")
            anima_queue.close()
        else:
            bot.send_message(userID,"Вы уже в очереди. Ожидайте")
            anima_queue.close()
    if  [i for i in rus if i in user_mes.lower()]:
        bot.send_message(userID,"Бот тупенький, пока понимает только на английском языке, пользуйся переводчиком, если надо")
        # create_image(user_mes)
        # image=open("P:\\stable\\pictures\\"+user_mes+".png","rb")


while True:
    try:
        bot.polling(non_stop=True, interval=0)
    except Exception as e:
        print(e)
        time.sleep(1)
        continue
