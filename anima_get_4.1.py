import os
import setuptools
import telebot
import time
import random
from telebot import types
import emoji
activator=[1]
rus='абвгдеёжзийклмнопрстуфхцчшщьыъэюя'
en=0
block =[]
bot = telebot.TeleBot('')
white=[5106244821]
counter_images=[0]
start_balance="15"
models=["darksuski","mixpro"]
# пути к файлам
queue_path="P:\\stable\\anima_queue.txt"
user_log_path="P:\\stable\\anima_user_log.txt"
prompt_path="P:\\stable\\anima_user_prompt.txt"
balance_path="P:\\stable\\anima_users_balance.txt"
print("GET")

# добавить баланс пользователю
def add_balance(userID,count_balance):
    users_balances_lines=open(balance_path,"r")
    users_balances=users_balances_lines.readlines()
    users_balances_lines.close()
    users=[]
    balances=[]
    for i in users_balances:
        lines_user=i.split(",")
        users.append(lines_user[0])
        balances.append((lines_user[1])[:-1])
    if str(userID) not in users:
        users.append(str(userID))
        balances.append(start_balance)
    user_index=users.index(str(userID))
    balance=int(balances[user_index])
    balance+=count_balance
    balances[user_index]=str(balance)
    file_write_users=""
    for i in range(0,len(users)):
        file_write_users+=users[i]+","+balances[i]+"\n"
    users_balances_lines=open(balance_path,"w")
    users_balances_lines.write(file_write_users)
    users_balances_lines.close()

# проверить реферальную ссылку и добавить баланс
def referal_check(friendID,userID):
    users_balances_lines=open(balance_path,"r")
    users_balances=users_balances_lines.readlines()
    users_balances_lines.close()
    users=[]
    balances=[]
    for i in users_balances:
        lines_user=i.split(",")
        users.append(lines_user[0])
        balances.append((lines_user[1])[:-1])
    if str(userID) not in users:
        add_balance(friendID,15)

# добавление пользователя в базу данных
def if_user_in_balance(userID):
    users_balances_lines=open(balance_path,"r")
    users_balances=users_balances_lines.readlines()
    users_balances_lines.close()
    users=[]
    balances=[]
    for i in users_balances:
        lines_user=i.split(",")
        users.append(lines_user[0])
        balances.append((lines_user[1])[:-1])
    if str(userID) not in users:
        users.append(str(userID))
        balances.append(start_balance)
    user_index=users.index(str(userID))
    balance=balances[user_index]
    #bot.send_message(message.chat.id, 'Твой баланс-'+balance)
    file_write_users=''
    for i in range(0,len(users)):
        file_write_users+=users[i]+","+balances[i]+"\n"
    users_balances_lines=open(balance_path,"w")
    users_balances_lines.write(file_write_users)
    users_balances_lines.close()


@bot.message_handler(commands=['start'])
def add_model(message):
    bot.send_message(message.chat.id, 'Напишите какую картинку генерировать (только на английском языке), чем точнее описание - тем лучше \nМожешь посмотреть в интернете различные prompt, это поможет тебе с генерацией \n\n Например "Orange hair girl with freckles"\n\nP.s у тебя только 10 артов в день\n\nТакже есть 2 стиля: darksushi, mixpro - добавь их в запрос и получишь картинку в таком стиле')
    keyboard=types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
    alphaModel_button = types.KeyboardButton(text='mixpro')
    betaModel_button = types.KeyboardButton(text='darksushi')
    keyboard.add(alphaModel_button,betaModel_button)
    print(message.text.split())
    try:
        print(message.text.split())
        friendID=message.text.split()[1]
        friendID=int(friendID)
        print(friendID)
    except:
        print("hui")
        friendID=0
    if friendID!=0:
        referal_check(friendID,message.chat.id)
    if_user_in_balance(message.chat.id)
    msg=bot.send_message(message.chat.id,"Выбери модель", reply_markup=keyboard)
    bot.register_next_step_handler(msg, add_resolution,message.text)


@bot.message_handler(commands=['check'])
def check(m, res=False):
    print("00")
    users_balances_lines=open(balance_path,"r")
    users_balances=users_balances_lines.readlines()
    users=[]
    balances=[]
    for i in users_balances:
        lines_user=i.split(",")
        users.append(lines_user[0])
        balances.append((lines_user[1])[:-1])
    if str(m.chat.id) not in users:
        users.append(str(m.chat.id))
        balances.append(start_balance)
    user_index=users.index(str(m.chat.id))
    balance=balances[user_index]
    file_write_users=''
    for i in range(0,len(users)):
        file_write_users+=users[i]+","+balances[i]+"\n"
    users_balances_lines=open(balance_path,"w")
    users_balances_lines.write(file_write_users)
    users_balances_lines.close()
    bot.send_message(m.chat.id, 'Твой баланс-'+balance)

@bot.message_handler(commands=['friend'])
def referal_link(message):
    keyboard=types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
    begin_button = types.KeyboardButton(text='/begin')
    keyboard.add(begin_button)
    bot.send_message(message.chat.id,"https://t.me/Animagram_bot?start="+str(message.chat.id)+"\nЕсли приведешь друга,то получишь генерации", reply_markup=keyboard)

@bot.message_handler(commands=['begin'])
def add_model(message):
    keyboard=types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
    alphaModel_button = types.KeyboardButton(text='mixpro')
    betaModel_button = types.KeyboardButton(text='darksushi')
    keyboard.add(alphaModel_button,betaModel_button)
    msg=bot.send_message(message.chat.id,"Выбери модель", reply_markup=keyboard)
    bot.register_next_step_handler(msg, add_resolution,message.text)

def add_resolution(message,value):
    keyboard=types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
    res1_button = types.KeyboardButton(text='16:9')
    res2_button = types.KeyboardButton(text='9:16')
    res3_button = types.KeyboardButton(text='1:1')
    keyboard.add(res3_button,res2_button,res1_button)
    msg=bot.send_message(message.chat.id,"Выбери разрешение", reply_markup=keyboard)
    bot.register_next_step_handler(msg, add_prompt,message.text)

def add_prompt(message,value):
    keyboard=types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
    msg=bot.send_message(message.chat.id,"Введи запрос", reply_markup=telebot.types.ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, send_to_send,value+' '+message.text)

def send_to_send(message,value):
    prompt=value+" "+message.text
    print(prompt)
    send_generate(prompt,message.chat.id,message.from_user.username)

def send_generate(prompt,userID,userNAME):
    user_mes=emoji.demojize(prompt)
    user_mes=user_mes.replace("\n"," ")
    users_balances_lines=open(balance_path,"r")
    users_balances=users_balances_lines.readlines()
    users_balances_lines.close()
    users=[]
    balances=[]
    for i in users_balances:
        lines_user=i.split(",")
        users.append(lines_user[0])
        balances.append((lines_user[1])[:-1])
    if str(userID) not in users:
        users.append(str(userID))
        balances.append(start_balance)
    user_index=users.index(str(userID))
    balance=int(balances[user_index])
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
        if ((str(userID)+"\n" not in anima_queue_readlines) and (str(userID) in users) and (balance>0)):
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

            file_write_users=''
            for i in range(0,len(users)):
                file_write_users+=users[i]+","+balances[i]+"\n"
            users_balances_lines=open(balance_path,"w")
            users_balances_lines.write(file_write_users)
            users_balances_lines.close()
        elif balance==0:
            bot.send_message(userID,"На СЕГОДНЯ баланс закончился\n\nНо ты можешь его добавить, если задонатишь админу - @wildwoodrogue")
            anima_queue.close()
        else:
            bot.send_message(userID,"Вы уже в очереди. Ожидайте")
            anima_queue.close()
    if  [i for i in rus if i in user_mes.lower()]:
        bot.send_message(userID,"Бот тупенький, пониает только на английском языке, пользуйся переводчиком, если надо")
        # create_image(user_mes)
        # image=open("P:\\stable\\pictures\\"+user_mes+".png","rb")
    keyboard=types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
    begin_button = types.KeyboardButton(text='/begin')
    keyboard.add(begin_button)
    msg=bot.send_message(userID,"'/begin' - чтобы снова генерировать изображения", reply_markup=keyboard)


while True:
    try:
        bot.polling(non_stop=True, interval=0)
    except Exception as e:
        print(e)
        time.sleep(1)
        continue
