import os
import setuptools
import telebot
import time
import random
queue_path="P:\\stable\\anima_queue.txt"
user_log_path="P:\\stable\\anima_user_log.txt"
prompt_path="P:\\stable\\anima_user_prompt.txt"
balance_path="P:\\stable\\anima_users_balance.txt"
start_balance="15"
users_balances_lines=open(balance_path,"r")
users_balances=users_balances_lines.readlines()
users=[]
balances=[]
for i in users_balances:
    lines_user=i.split(",")
    users.append(lines_user[0])
    if int((lines_user[1])[:-1])<int(start_balance):
        balances.append(start_balance)
    else:
        balances.append((lines_user[1])[:-1])
file_write_users=''
for i in range(0,len(users)):
    file_write_users+=users[i]+","+balances[i]+"\n"
users_balances_lines=open(balance_path,"w")
users_balances_lines.write(file_write_users)
users_balances_lines.close()
