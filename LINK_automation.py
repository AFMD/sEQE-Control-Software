#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pyautogui as pyag
pyag.PAUSE = 1
import subprocess
import time
import logging
from tkinter import Tk
from tkinter import filedialog 

import os
import pathlib


# In[19]:



def mouse_tracker():
    for i in range(4):
        print(pyag.position())
        time.sleep(4)

class CryostatControl:
    """Automated cryostat control - keyboard and mouse input simulated to use with Linkam's LINK Software.
        You find the docs of pyautogui here: https://pyautogui.readthedocs.io/en/latest/
        If you want to stop the methods: Slam mouse pointer into one of the screen corners. 
    """
    def __init__(self,file_name,directory_name):
        """opens LINK program and connects to cryostat"""
        try:
            subprocess.Popen(self.find_file(file_name,pathlib.Path(directory_name))) #'C:\\Program Files\\Linkam Scientific\\LINK\\LINK.exe'
            self.picturepath = self.define_picture_path()
            time.sleep(15) #give LINK time to be found and started
            self.connect_USB()
            
            
        except Exception as err:
            logging.error(f"Unexpected {err=} during execution of setParameters function: {type(err)=}")
            raise
    
    def find_file(self,file_name, directory_name):
        files_found = []
        for path, subdirs, files in os.walk(directory_name):
            for name in files:
                if(file_name == name):
                    file_path = os.path.join(path,name)
                    files_found.append(file_path)
        return files_found
    
    def define_picture_path(self):
        root = Tk() # Creates master window for tkinters filedialog window
        root.withdraw() # Hides master window
        picturepath = pathlib.Path(filedialog.askdirectory())
        return picturepath
    
    # def open_LINK(self):
    #     """ methode to open LINK program """
    #     subprocess.Popen(['C:\\Program Files\\Linkam Scientific\\LINK\\LINK.exe'])
    #     return None

    def connect_USB(self):
        """ methode to connect T96 controller to LINK """ 
        array = [#'pictures\controller-menu.png',
            #'pictures/connect_USB-button.png',
            'pictures/popup_ok-button.png','pictures/popup_ok-button2.png']
        try:
            controller_menu = pyag.locateOnScreen(str(self.picturepath / 'controller-menu.png') ,confidence=0.9)
            pyag.moveTo(controller_menu)
            pyag.click(controller_menu, clicks = 1 ,button='left')
            time.sleep(1)
            pyag.move(0,30)
            pyag.click(clicks=1, button='left')
            # for picture in array:
            #     if pyag.locateOnScreen(picture, confidence=0.9) == True:
            #         item = pyag.locateOnScreen(picture ,confidence=0.9)
            #         pyag.click(item, clicks = 1 ,button='left')
            #     else: None
        
        # except 'ImageNotFoundException':
        #     logging.error('Cant find the "connect" button - check whether screenshot is correctly found')

            

        except KeyboardInterrupt:
            print('\n')
        return None

    def import_parameter_file(self,filename):
        """ methode to import parameters via profile file 
            Give ONLY filename to methode, not path
        """
        file_menu = pyag.locateOnScreen(picturepath + '/file-menu.png' ,confidence=0.8)
        pyag.click(file_menu, clicks = 1 ,button='left')
        pyag.move(10,25)
        profile_menu = pyag.locateOnScreen('pictures/Profile_file-button.png' ,confidence=0.8)
        pyag.click(profile_menu, clicks = 1 ,button='left')
        pyag.write(filename)
        pyag.press('enter')
        return None


    def set_parameter(self,a,b,c): #40 pixels down is the enter
        """ methode to set manually the parameter of one ramp cycle """
        array0 = [a,b,c]
        array = ['pictures/rate_logo.png','pictures\limit_logo.png','pictures/time_logo.png']#'pictures\lnp-speed_logo.png']
        try:
            for parameter,picture in list(zip(array0,array)):
                item = pyag.locateOnScreen(picture ,confidence=0.8)
                pyag.moveTo(item)
                pyag.move(0,20)
                pyag.click(button='left')
                pyag.write(f'{parameter}')
                pyag.press('enter')
        except KeyboardInterrupt:
            print('\n')
        return None

    def change_ramp_cycle(self,direction):
        """ methode to change ramp cycle """
        array = ['pictures/ramp_down.png','pictures/ramp_up.png'] 
        if direction == True:
            item = pyag.locateOnScreen('pictures/ramp_up.png' ,confidence=0.8)
            pyag.click(item, clicks = 1 ,button='left')
        if direction == False:
            item = pyag.locateOnScreen('pictures/ramp_down.png' ,confidence=0.8)
            pyag.click(item, clicks = 1 ,button='left')
        return None

    def multiple_ramps(self,number_ramp_cycles,*args):
        """ methode to set parameter for multiple ramp cycles """ 
        try:
            ramp_cycle = 0
            #for i in range(number_ramp_cycles):
                #change_ramp_cycle(False)
            for i in range(number_ramp_cycles):
                rate = args[0]
                temperature = args[1]
                duration = args[2]
                args = args[3:]
                self.set_parameter(rate,temperature,duration)
                ramp_cycle += 1
                self.change_ramp_cycle(ramp_cycle < number_ramp_cycles)
                print(ramp_cycle)
            for i in range(ramp_cycle-2):
                self.change_ramp_cycle(False)
        except KeyboardInterrupt:
            print('\n')

    def move_temperature_line(self):
        """ methode to display current cryostat temperature """
        item = pyag.locateOnScreen('pictures/temperature-line.png' ,confidence=0.9)
        pyag.moveTo(item)
        pyag.drag(300,0,2,button='left')
        return None

    def start_measurement(self):
        """ methode to start measurement """
        item = pyag.locateOnScreen('pictures/start_button.png' ,confidence=0.8)
        pyag.click(item, clicks = 1 ,button='left')
        time.sleep(1)
        pyag.write('enter')

    def open_minimized_LINK(self):
        """ methode to open minimized LINK window """
        try:
            logging.info('Reopening LINK window')
            bar = pyag.locateOnScreen(picturepath + '\LINK_logo.png',confidence=.9)
            pyag.click(bar ,button='left')
            time.sleep(2)

            #start_button = pyag.locateOnScreen('pictures\start_button.png',confidence=0.8)
            #print(start_button)
            #pyag.click(start_button, button='left',duration=3)
            #print(pyag.position())
        except KeyboardInterrupt:
            print('Process was cancelled')
    
# def main():
#     LINK = CryostatControl()

#     LINK.open_LINK()
#     time.sleep(10)
#     #LINK.open_minimized_LINK()
#     LINK.connect_USB()
#     time.sleep(3)
#     time.sleep(2)
#     LINK.multiple_ramps(2,20,20,20,10,10,10)
#     #LINK.import_parameter_file('test.lpf')
#     time.sleep(3)
#     LINK.move_temperature_line()
#     LINK.start_measurement()

# if __name__ == "__main__": 
#     main()


# In[25]:


root = Tk() # Creates master window for tkinters filedialog window
root.withdraw() # Hides master window
picturepath = filedialog.askdirectory()
print(picturepath)


# In[ ]:


# LINK = CryostatControl()

# LINK.open_LINK()
# time.sleep(10)
# #LINK.open_minimized_LINK()
# LINK.connect_USB()
# time.sleep(3)
# time.sleep(2)
# #LINK.multiple_ramps(2,20,20,20,10,10,10)
# LINK.import_parameter_file('test.lpf')
# time.sleep(3)
# LINK.move_temperature_line()
# LINK.start_measurement()


# In[ ]:


#open_LINK()
#time.sleep(10)
# connect_USB()
# set_parameter(10,30,30)
# time.sleep(1)
# move_temperature_line()
# change_ramp_cycle(True)
# set_parameter(10,35,20)
# start_measurement()


# In[ ]:


# open_minimized_LINK()
# multiple_ramps(3,10,10,10,20,20,20,30,30,30)


# In[ ]:


#print(list(range(3)))


# In[ ]:


#from LINK_automation import CryostatControl

def main():
    LINK = CryostatControl()

    LINK.open_LINK()
    time.sleep(10)
    #LINK.open_minimized_LINK()
    LINK.connect_USB()
    time.sleep(3)
    time.sleep(2)
    LINK.multiple_ramps(2,20,20,20,10,10,10)
    #LINK.import_parameter_file('test.lpf')
    time.sleep(3)
    LINK.move_temperature_line()
    LINK.start_measurement()

if __name__ == "__main__":
    main()


# In[17]:


LINK = CryostatControl('LINK.exe','C:/Program Files/')

#LINK.find_file('LINK.exe',pathlib.Path('C:/Program Files/'))

