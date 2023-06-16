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
from telebot import types
import time
import random
from PIL import Image
from xformers.ops import MemoryEfficientAttentionFlashAttentionOp
import config
import anima_tools as tools
start_balance=config.start_balance
queue_path=config.queue_path
user_log_path=config.user_log_path
prompt_path=config.prompt_path
balance_path=config.balance_path
activator=[1]
queue=[]
block =[]
bot = telebot.TeleBot(config.api_token)
white=[5106244821]
counter_images=[0]
height=960
width=960
alphaModel_name=config.alphaModel_name
betaModel_name=config.betaModel_name

vaePath = r"P:\downloads\kl-f8-anime2.vae.pt"
vae = AutoencoderKL.from_pretrained(r"P:\diffuse", torch_dtype=torch.float16).to("cuda")

betaModel = r"C:\Users\QWW\.cache\huggingface\hub\models--stablediffusionapi--dark-sushi-mix\snapshots\428762d28ef61df6353a361c24e2dd5ac27730ec" #10/10
alphaModel=r"P:\safetensorTodiffusers"


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

main_menu = types.InlineKeyboardMarkup()
model_button = types.InlineKeyboardButton(text="Выбрать модель🦄", callback_data="model_menu")
res_button = types.InlineKeyboardButton(text="Выбрать размер🍌", callback_data="res_menu")
start_button = types.InlineKeyboardButton(text="Начать генерацию🧠", callback_data="start_generate")
main_menu.row(model_button,res_button)
main_menu.row(start_button)



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
    elif "3:4" in prompt:
        prompt=prompt.replace("3:4","")
        height=1024
        width=768
    elif "4:3" in prompt:
        prompt=prompt.replace("4:3","")
        height=768
        width=1024
    else:
        height=960
        width=960
    if alphaModel_name in prompt:
        prompt=prompt.replace(alphaModel_name,"")
        image = alpha("a "+prompt,guidance_scale=7, num_inference_steps=20, height=height, width=width, negative_prompt=negative_prompt,generator=generator).images[0]
    elif betaModel_name in prompt:
        prompt=prompt.replace(betaModel_name,"")
        image = beta("a "+prompt,guidance_scale=7, num_inference_steps=20, height=height, width=width, negative_prompt=negative_prompt,generator=generator).images[0]
    else:
        image = alpha("a "+prompt,guidance_scale=7, num_inference_steps=20, height=height, width=width, negative_prompt=negative_prompt,generator=generator).images[0]

    torch.cuda.empty_cache()
    counter_images[0]+=1

    image.save("P:\\stable\\pictures\\"+str(user_id)+"__"+str(counter_images[0])+".png")
    image=open("P:\\stable\\pictures\\"+str(user_id)+"__"+str(counter_images[0])+".png","rb")

    try:
        user_request_array=tools.get_user_request(user_id)
        userModel=user_request_array[0]
        userRes=user_request_array[1]
        userPrompt=user_request_array[2]
        bot.send_document(user_id,image,caption="<code>"+userPrompt+"</code>\nМодель: "+userModel+"\nРазмер: "+userRes,parse_mode="html",reply_markup=main_menu)
        balance=tools.add_balance(user_id,-1)
    except:
        print("ERROR")
    image.close()


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


        balance=tools.add_balance(user_id,0)
        try:
            bot.send_message(user_id,'Твой баланс-'+str(balance))
        except:
            print("user block us")



while True:
    try:
        bot.polling(non_stop=True, interval=0)
    except Exception as e:
        print(e)
        time.sleep(1)
        continue
