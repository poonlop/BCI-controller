# This file is undone
# To-Do LIST
# 1. This function is valid only {'action': 'neutral', 'power': 0.0, 'time': 1677401626.2411} this format
#    -> We have to write some command that extract only this format data 
# 2. This function haven't used for real time yet so we need to test it.

import json

def direction(file_name): 
    file = open(str(file_name),'r')
    data = file.readlines()
    use_data = data[1:100]
    # You can modify for proper command
    for x in use_data :
    #convert to dictionary format using json.loads()
        x = json.loads(x.replace("'", '"'))
        if x['action'] == 'push' and  x['power'] > 0.5: 
            print('turn left')
        else: 
            print('running')


direction("test2.json")