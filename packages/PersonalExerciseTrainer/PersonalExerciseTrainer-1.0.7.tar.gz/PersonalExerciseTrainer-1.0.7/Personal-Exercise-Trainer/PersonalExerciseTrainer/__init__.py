import datetime
import time
import webbrowser
import pyautogui
import platform
import importlib

class Exercise:
    def data():
        while True:
            print('Welcome to your Personal Exercise Trainer\n')
            print('Please follow the following format while giving your slots or time:-')
            print('Point no.1 --> Your timings will always be in 24-hours (HH:MM) format 12-hour format is not acceptable')
            print('Point no.2 --> Maximum slots available are 4')
            print('Point no.3 --> Your timings will always be greater than your current time')
            print('Point no.4 --> Your timings will always be in ascending order for ex - (14:20 , 14:40) ')
            print('Point no.5 --> Same timings or slots are not allowed for example - (14:20 , 14:20) are not allowed')
            print('Point no.6 --> No spaces are allowed before and after the time slot\n')
            our_slots = Exercise.requirements()
            validated_list = Exercise.validate(our_slots)
            if validated_list ==True:
                print(validated_list)
                continue
            else:
                break
        global var
        var = our_slots
        return our_slots

    def requirements():
        my_list =[]
        count = 0
        while True:
            count +=1
            data = input(f'Please enter your {count}st slot------>')
            my_list.append(data)
            if len(my_list) == 4:
                break				
            else:
                continue
        return my_list

    def validate(slot):
        if type(slot) == list and  slot == sorted(slot):
            try:
                for n in range(len(slot)):
                    datetime.datetime.strptime(slot[n] , "%H:%M")
            except:
                print('Please check your inputs they are not in requested formatte HH:MM ')
                return True
            try:
                for check in slot:
                    Current_time = time.strftime("%H:%M")
                    t1 = datetime.datetime.strptime(Current_time , "%H:%M")
                    t2 = datetime.datetime.strptime(str(check) , "%H:%M")
                    delta_time = t2 - t1
                    module_type = datetime.datetime.strptime(str(delta_time),"%H:%M:%S" )
                    str_type = str(module_type)
                    hour = int(str_type[11:13])  * 3600
                    min = int(str_type[14:16])  * 60
                    if hour + min > 0 :
                        pass
                    else:
                        print('Please check your inputs your slot time is equal to current time')
                        return True
            except:
                print(' Please check your inputs your slot time are not greater than current time')
                return True       
        else:
            print('Please check your inputs it is not in ascending order')
            return True

    def time_diff(user_input):
        #for Exercise in user_input:
        if type(user_input)!= list:
            url = Exercise.link_selector()
            Current_time = time.strftime("%H:%M")
            t1 = datetime.datetime.strptime(Current_time , "%H:%M")
            t2 = datetime.datetime.strptime(str(user_input) , "%H:%M")  # problem 
            delta_time = t2 - t1
            print('Delta Time = ',delta_time)
            module_type = datetime.datetime.strptime(str(delta_time),"%H:%M:%S" )
            result = str(module_type)
            #print(result)
            hour = int(result[11:13])  * 3600
            min = int(result[14:16])  * 60
            total = hour + min
            # print(total)
            time.sleep(total)
            user_OS = platform.system()
            if user_input in url:
                if user_OS == 'Windows':
                    a=url[user_input]
                    webbrowser.open(a)
                    time.sleep(40)
                    pyautogui.hotkey('ctrl', 'shift', 'w')
            if user_input in url:
               if user_OS == 'Darwin':
                    a=url[user_input]
                    webbrowser.open(a)
                    time.sleep(40)
                    pyautogui.hotkey('command', 'shift', 'w')
        else:
            return ('Data is not excepted in list')  
        return True


    def link_selector():
        my_playlist=["https://youtu.be/oGvcrsxXikU",
        "https://youtu.be/ljAsrDbPWWE",
        "https://youtu.be/nrF-d7LqS2o",
        "https://www.youtube.com/watch?v=igXdzA2Kwno"]
        res = dict(zip(var,my_playlist))
        return res


    def Exercise1():
        """This Exercise will count only when both your hands are vertically straight up"""
        try:    
            importlib.import_module('PersonalExerciseTrainer.EX1')
        except:
            pass
        return True


    def Exercise2():
        """ This Exercise will count only when both arms are Horizontally straight"""
        try:    
            importlib.import_module('PersonalExerciseTrainer.EX2')
        except:
            pass
        return True

    def Exercise3():
        """This Exercise will only count when Left arm is horizontally straight"""
        try:    
            importlib.import_module('PersonalExerciseTrainer.EX3')
        except:
            pass
        return True

    def Exercise4():
        """This Exercise will only count when Right arm is horizontally straight"""
        try:    
            importlib.import_module('PersonalExerciseTrainer.EX4')
        except:
            pass
        return True


