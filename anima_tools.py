import config

start_balance=config.start_balance
queue_path=config.queue_path
user_log_path=config.user_log_path
prompt_path=config.prompt_path
balance_path=config.balance_path
start_balance=config.start_balance
alphaModel_name=config.alphaModel_name
betaModel_name=config.betaModel_name
balance_path_reserve=config.balance_path_reserve
request_path=config.request_path

#work
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
    users_balances_lines_reserve=open(balance_path_reserve,"w")
    users_balances_lines_reserve.write(file_write_users)
    users_balances_lines_reserve.close()
    return balance

#work
def balance_new():
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
    users_balances_lines_reserve=open(balance_path_reserve,"w")
    users_balances_lines_reserve.write(file_write_users)
    users_balances_lines_reserve.close()


#work
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
        add_balance(friendID,start_balance)


#work
def add_user_in_request(userID):
    file_request=open(request_path,"r")
    request_lines=file_request.readlines()
    file_request.close()
    users_id_array=[]
    users_model_array=[]
    users_resolution_array=[]
    users_prompt_array=[]
    if len(request_lines)>0:
        for i in request_lines:
            line_request=i.split("#")
            user_id=line_request[0]
            user_model=line_request[1]
            user_resolution=line_request[2]
            user_prompt=line_request[3]
            user_prompt=user_prompt[:-1]

            users_id_array.append(user_id)
            users_model_array.append(user_model)
            users_resolution_array.append(user_resolution)
            users_prompt_array.append(user_prompt)


    if str(userID) not in users_id_array:
        users_id_array.append(str(userID))
        users_model_array.append(alphaModel_name)
        users_prompt_array.append("Orange hair girl")
        users_resolution_array.append("1:1")
    file_string=""
    for i in range(0,len(users_id_array)):
        file_string=file_string+users_id_array[i]+"#"+users_model_array[i]+"#"+users_resolution_array[i]+"#"+users_prompt_array[i]+"\n"
    file_request=open(request_path,"w")
    file_request.write(file_string)
    file_request.close()


def get_user_request(userID):
    add_user_in_request(userID)
    file_request=open(request_path,"r")
    request_lines=file_request.readlines()
    file_request.close()
    users_id_array=[]
    users_model_array=[]
    users_resolution_array=[]
    users_prompt_array=[]
    for i in request_lines:
        line_request=i.split("#")

        user_id=line_request[0]
        user_model=line_request[1]
        user_resolution=line_request[2]
        user_prompt=line_request[3]
        #user_prompt=user_prompt[:-1]
        if str(userID)==user_id:
            return [user_model,user_resolution,user_prompt]
def give_user_request(userID,userModel,userResolution,userPrompt):
    add_user_in_request(userID)
    file_request=open(request_path,"r")
    request_lines=file_request.readlines()
    file_request.close()
    users_id_array=[]
    users_model_array=[]
    users_resolution_array=[]
    users_prompt_array=[]

    if len(request_lines)>0:
        for i in request_lines:
            line_request=i.split("#")
            user_id=line_request[0]
            user_model=line_request[1]
            user_resolution=line_request[2]
            user_prompt=line_request[3]
            user_prompt=user_prompt[:-1]
            if user_id==str(userID):
                user_id=str(userID)
                user_model=userModel
                user_resolution=userResolution
                user_prompt=userPrompt
                user_prompt=user_prompt[:-1]
            users_id_array.append(user_id)
            users_model_array.append(user_model)
            users_resolution_array.append(user_resolution)
            users_prompt_array.append(user_prompt)

    file_string=""
    for i in range(0,len(users_id_array)):
        file_string=file_string+users_id_array[i]+"#"+users_model_array[i]+"#"+users_resolution_array[i]+"#"+users_prompt_array[i]+"\n"
    file_request=open(request_path,"w")
    file_request.write(file_string)
    file_request.close()
