from diffusers import StableDiffusionPipeline, EulerDiscreteScheduler, StableDiffusionLatentUpscalePipeline
from diffusers.models import AutoencoderKL
import torch
from diffusers import AutoencoderKL
import os
import setuptools
import safetensors
from diffusers import DDIMScheduler
from transformers import CLIPFeatureExtractor
import telebot
import time
import random
from PIL import Image
from xformers.ops import MemoryEfficientAttentionFlashAttentionOp

import anima_config as config
start_balance="15"
queue_path="P:\\stable\\anima_queue.txt"
user_log_path="P:\\stable\\anima_user_log.txt"
prompt_path="P:\\stable\\anima_user_prompt.txt"
balance_path="P:\\stable\\anima_users_balance.txt"
activator=[1]
queue=[]
block =[]
bot = telebot.TeleBot('')
white=[5106244821]
counter_images=[0]
height=960
width=960

vaePath = r"P:\downloads\kl-f8-anime2.vae.pt"
vae = AutoencoderKL.from_pretrained(r"P:\diffuse", torch_dtype=torch.float16).to("cuda")

betaModel = r"C:\Users\QWW\.cache\huggingface\hub\models--stablediffusionapi--dark-sushi-mix\snapshots\428762d28ef61df6353a361c24e2dd5ac27730ec" #10/10
alphaModel=r"C:\Users\QWW\.cache\huggingface\hub\models--qww12332122--qwwsomething\snapshots\1afea868a36a69a1c05c6dd708d44e1d6e45172e"


alpha = StableDiffusionPipeline.from_pretrained(alphaModel,custom_pipeline="lpw_stable_diffusion", torch_dtype=torch.float16,safety_checker=None,vae=vae)
alpha.scheduler = DDIMScheduler.from_config(alpha.scheduler.config)
alpha = alpha.to("cuda")
alpha.enable_xformers_memory_efficient_attention()
alpha.enable_attention_slicing()#УМЕНЬШАЕТ ЗАТРАТЫ ВИДЕОПАМЯТИ КАПЕЦ КАК СИЛЬНО!!!!!!!!
alpha.enable_xformers_memory_efficient_attention()
alpha.load_textual_inversion(r"P:\downloads\verybadimagenegative_v1.2-6400.pt")



beta = StableDiffusionPipeline.from_pretrained(betaModel,custom_pipeline="lpw_stable_diffusion", torch_dtype=torch.float16,safety_checker=None,vae=vae)
beta.scheduler = DDIMScheduler.from_config(beta.scheduler.config)
beta = beta.to("cuda")
beta.enable_xformers_memory_efficient_attention()
beta.enable_attention_slicing()#УМЕНЬШАЕТ ЗАТРАТЫ ВИДЕОПАМЯТИ КАПЕЦ КАК СИЛЬНО!!!!!!!!
beta.enable_xformers_memory_efficient_attention()
beta.load_textual_inversion(r"P:\downloads\verybadimagenegative_v1.2-6400.pt")




negative_prompt=""
negative_prompt="nude,porn,hentai,nude someone,vagina,nipples,nipple,dick,penis,pussy"
negative_prompt='((((child porn)))),(((loli))),(((((child))))),((((shota)))),((((kid)))),((((kids)))),((((lolicon)))),((((shotacon)))),(((unnecessary faces))),(((unnecessary legs))),(((worst pose))),(((extra legs))), (((extra hands))),((extra fingers)),((((extra faces)))),without any clothes,(((little nude boy))),error,(worst quality:1.7), conjoined fingers, (((deformed fingers))),(((worst quality eyes))),(((deformed eyes))),(low quality, worst quality:1.7),(((bad anatomy))),(extra limbs:1.5),((long body part)),(poorly drawn face:1.5),(mutated fingers:1.7),(veryBadImageNegative_v1.2-6400:0.9)'
print("GIVE")

def bicubic_resize(image, size):
    return image.resize(size, resample=Image.BICUBIC)

def create_image(prompt,user_id):
    generator_int=random.randint(0,999999)
    #generator_int=1
    generator = torch.Generator("cuda").manual_seed(generator_int) #  random.randint(0,999999)
    if "16:9" in prompt:
        prompt=prompt.replace("16:9","")
        height=720
        width=1280
    elif "9:16" in prompt:
        prompt=prompt.replace("9:16","")
        height=1280
        width=720
    elif "1:1" in prompt:
        prompt=prompt.replace("1:1","")
        height=960
        width=960
    else:
        height=960
        width=960
    if "mixpro" in prompt:
        prompt=prompt.replace("mixpro","")
        image = alpha("a "+prompt,guidance_scale=7, num_inference_steps=20, height=height, width=width, negative_prompt=negative_prompt,generator=generator).images[0]
    elif "darksushi" in prompt:
        prompt=prompt.replace("darksushi","")
        image = beta("a "+prompt,guidance_scale=7, num_inference_steps=20, height=height, width=width, negative_prompt=negative_prompt,generator=generator).images[0]
    else:
        image = alpha("a "+prompt,guidance_scale=7, num_inference_steps=20, height=height, width=width, negative_prompt=negative_prompt,generator=generator).images[0]

    torch.cuda.empty_cache()
    counter_images[0]+=1

    image.save("P:\\stable\\pictures\\"+str(user_id)+"__"+str(counter_images[0])+".png")
    image=open("P:\\stable\\pictures\\"+str(user_id)+"__"+str(counter_images[0])+".png","rb")
    im=Image.open("P:\\stable\\pictures\\"+str(user_id)+"__"+str(counter_images[0])+".png")
    width, height = im.size
    new_size = (width * 2, height * 2)
    image2=bicubic_resize(im,new_size)
    image2.save("P:\\stable\\pictures\\"+str(user_id)+"__"+str(counter_images[0])+"hd"+".png")
    image2=open("P:\\stable\\pictures\\"+str(user_id)+"__"+str(counter_images[0])+"hd"+".png","rb")

    try:
        bot.send_photo(user_id,image)
        bot.send_document(user_id,image2)
    except:
        print("ERROR")
    image.close()
    image2.close()


while True:
    anima_queue_file=open(queue_path,"r")
    anima_user_prompt_file=open(prompt_path,"r")
    anima_queue=anima_queue_file.readlines()
    anima_user_prompt=anima_user_prompt_file.readlines()
    anima_queue_file.close()
    anima_user_prompt_file.close()

    if len(anima_queue)>0 and len(anima_user_prompt)>0:
        user_id=anima_queue[0]
        user_id=user_id.replace('\n','',1)
        user_id=str(user_id)
        user_id=int(user_id)
        print(user_id)
        prompt=anima_user_prompt[0]
        prompt=prompt.lower()
        prompt=prompt.replace('\n','',1)
        print(prompt)
        create_image(prompt,user_id)
        print(1)
        anima_queue_file=open(queue_path,"r")
        anima_user_prompt_file=open(prompt_path,"r")
        anima_queue=anima_queue_file.readlines()
        anima_user_prompt=anima_user_prompt_file.readlines()
        anima_queue_file.close()
        anima_user_prompt_file.close()
        anima_user_prompt.pop(0)
        anima_queue.pop(0)
        anima_queue="".join(anima_queue)
        anima_user_prompt="".join(anima_user_prompt)
        anima_queue_file=open(queue_path,"w")
        anima_user_prompt_file=open(prompt_path,"w")
        anima_queue_file.write(anima_queue)
        anima_user_prompt_file.write(anima_user_prompt)
        anima_user_prompt_file.close()
        anima_queue_file.close()

        users_balances_lines=open(balance_path,"r")
        users_balances=users_balances_lines.readlines()
        users_balances_lines.close()
        users=[]
        balances=[]
        for i in users_balances:
            lines_user=i.split(",")
            users.append(lines_user[0])
            balances.append((lines_user[1])[:-1])
        if str(user_id) not in users:
            users.append(str(user_id))
            balances.append(start_balance)
        user_index=users.index(str(user_id))
        balance=int(balances[user_index])
        balance-=1
        balances[user_index]=str(balance)
        file_write_users=""
        for i in range(0,len(users)):
            file_write_users+=users[i]+","+balances[i]+"\n"
        users_balances_lines=open(balance_path,"w")
        users_balances_lines.write(file_write_users)
        users_balances_lines.close()
        try:
            bot.send_message(user_id,'Твой баланс-'+str(balance))
        except:
            print("user block us")
        donateInt=random.randint(0,17)
        if donateInt==10:
            try:
                bot.send_message(user_id,'Если будут какие-то ошибки, пиши -@wildwoodrogue')
            except:
                print("user block us")
        elif str(donateInt) in "8 9 1 2":
            try:
                bot.send_message(user_id,"Если тебе понравился мой бот, то ты можешь поддержать его развитие денюжкой \nhttps://qiwi.com/n/WILDWOODROGUE - QIWI \n4279380697148247 - сбер \n2200700472181907 - tinkoff \nP1095666540 - payeer \nДенюжки пойдут на покупку видеокарты, что сделает арты в разы лучше")
            except:
                print("user block us")
        elif donateInt==11:
            try:
                bot.send_message(user_id,"Если не получается сгенерировать нужную картинку с первого раза - попробуй еще несколько раз, через 3-5 раз у тебя должно получиться")
            except:
                print("user block us")
        elif donateInt==12:
            try:
                bot.send_message(user_id,"Проверяй запрос на грамматические ошибки, иначе они могут привести к совсем другой генерации")
            except:
                print("user block us")
        elif donateInt==13:
            try:
                bot.send_message(user_id,"У нас постоянно проходят конкурсы на лучший арт, так же есть призы\nhttps://t.me/competitionAnimagram")
            except:
                print("user block us")
        elif donateInt==14:
            try:
                bot.send_message(user_id,"/check - узнаешь свой баланс\n/friend - создать ссылку для друга\n/start - если что-то сломалось")
            except:
                print("user block us")
        elif donateInt==15:
            try:
                bot.send_message(user_id,"Если пригласишь друзей, то получишь генераций\nТвоя ссылка\nhttps://t.me/Animagram_bot?start="+str(user_id))
            except:
                print("user block us")
        elif donateInt==16:
            try:
                bot.send_message(user_id,"Пс, есть местечко, где мы выкладываем свои арты и просто болтаем https://t.me/animagram_chill")
            except:
                print("user block us")

















while True:
    try:
        bot.polling(non_stop=True, interval=0)
    except Exception as e:
        print(e)
        time.sleep(1)
        continue
