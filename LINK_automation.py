#!/usr/bin/env python
# coding: utf-8

import pyautogui as pyag
pyag.PAUSE = 1
import subprocess
import time
import logging
from tkinter import Tk
from tkinter import filedialog 

import os
import pathlib


def mouse_tracker():
    for i in range(4):
        print(pyag.position())
        time.sleep(4)

class Cryostat:
    """Automated cryostat control - keyboard and mouse input simulated to use with Linkam's LINK Software.
   
    Notes
    -----
    You find the docs of pyautogui here: https://pyautogui.readthedocs.io/en/latest/
    If you want to stop the automation: Slam mouse pointer into one of the screen corners.
    
    """
    def __init__(self,exe_path):
        """Initializes LINK program and connects to cryostat."""
        try:
            self.connected = False
            self.LINKpath = exe_path
            
        except Exception as err:
            logging.error(f"Unexpected {err=} during execution of __init__ function: {type(err)=}")
            raise
    
    # def find_file(self,file_name, directory_name):
    #     files_found = []
    #     for path, subdirs, files in os.walk(directory_name):
    #         for name in files:
    #             if(file_name == name):
    #                 file_path = os.path.join(path,name)
    #                 files_found.append(file_path)
    #     return files_found
    
    def define_picture_path(self):
        """Methode to retrieve the screenshot folder.
        
        Returns
        -------
        None
        
        Notes
        -----
        These screenshots have to be done every time the Computer changes. 
        TBV: Even changing the Computer's monitor might lead to errors.
        
        If some items on the screenshots are not found, redo the screenshots and name them as their predecessors.
        
        """
        root = Tk() # Creates master window for tkinters filedialog window
        root.withdraw() # Hides master window
        picturepath = pathlib.Path(filedialog.askdirectory(title = 'Choose the LINK screenshot folder'))
        return picturepath
    
    # def open_LINK(self):
    #     """ methode to open LINK program """
    #     subprocess.Popen(['C:\\Program Files\\Linkam Scientific\\LINK\\LINK.exe'])
    #     return None

    def connect(self,):
        """Methode to connect T96 controller to LINK.
        
        Returns
        ------
        """ 

        try:
            
            subprocess.Popen(self.LINKpath) #'C:\\Program Files\\Linkam Scientific\\LINK\\LINK.exe'
            self.picturepath = self.define_picture_path()
            
            pyag.confirm('Confirm that the LINK software has started, is open in front of you and you are ready for pyautogui to take over the mouse.')
            controller_menu = pyag.locateOnScreen(str(self.picturepath / 'controller-menu.png') ,confidence=0.9)
            pyag.moveTo(controller_menu)
            pyag.click(controller_menu, clicks = 1 ,button='left')
            time.sleep(1)
            pyag.move(0,30)
            pyag.click(clicks=1, button='left')
            time.sleep(2)
            
            if pyag.locateOnScreen(str(self.picturepath / 'Temp_logo.png') ,confidence=0.9):
                self.connected = True
                pyag.confirm('Mouse is free to use')
                
            return self.connected, self.picturepath
            
        except Exception as err:
            logging.error(f"Unexpected {err=} during execution of connect function: {type(err)=}")
            raise


    def import_lpf(self,filename):
        """Methode to import parameters via profile file.
        
        Parameters
        ----------
        filename: string, required
            name of LINK's profile file
        
        Notes
        -----
        Give ONLY filename, not path
        
        """
        try:
            file_menu = pyag.locateOnScreen(str(self.picturepath / 'file-menu.png') ,confidence=0.9)
            pyag.click(file_menu, clicks = 1 ,button='left')
            pyag.move(10,25)
            profile_menu = pyag.locateOnScreen(str(self.picturepath / 'Profile_file-button.png') ,confidence=0.9)
            pyag.click(profile_menu, clicks = 1 ,button='left')
            pyag.write(filename)
            pyag.press('enter')
        
        except Exception as err:
            logging.error(f"Unexpected {err=} during execution of import_lpf methode: {type(err)=}")
            raise


    def export_lpf(self,filename):
        """Methode to save cryo parameter to .lpf file.
        """
        try:
            file_menu = pyag.locateOnScreen(str(self.picturepath / 'file-menu.png') ,confidence=0.9)
            pyag.click(file_menu, clicks = 1 ,button='left')
            pyag.move(10,40)
            profile_menu = pyag.locateOnScreen(str(self.picturepath / 'Profile_file-button.png') ,confidence=0.9)
            pyag.click(profile_menu, clicks = 1 ,button='left')
            pyag.write(filename.split('.')[0] + '.lpf')
            pyag.press('enter')
            
        except Exception as err:
            logging.error(f"Unexpected {err=} during execution of export_lpf methode: {type(err)=}")
            raise
            
    def set_parameter(self,a,b,c): #40 pixels down is the enter
        """ methode to set manually the parameter of one ramp cycle """
        array0 = [a,b,c] # Import via csv file 
        array = [self.picturepath / 'rate_logo.png',self.picturepath / 'limit_logo.png',self.picturepath / 'time_logo.png']#'pictures\lnp-speed_logo.png']
        try:
            for parameter,picture in list(zip(array0,array)):
                item = pyag.locateOnScreen(str(picture) ,confidence=0.9)
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
        if direction == True:
            item = pyag.locateOnScreen(str(self.picturepath / 'next_cycle.png') ,confidence=0.9)
            pyag.click(item, clicks = 1 ,button='left')
        if direction == False:
            item = pyag.locateOnScreen(str(self.picturepath / 'last_cycle.png') ,confidence=0.9)
            pyag.click(item, clicks = 1 ,button='left')
        return None

    def go_to_first_ramp_cycle(self,number_ramp_cycles):
        """
        """
        try:
            for i in range(number_ramp_cycles):
                if not pyag.locateOnScreen(str(self.picturepath / 'ramp-1_logo.png') ,confidence=0.9):
                    self.change_ramp_cycle(False)
                else: break
                
        except Exception as err:
            logging.error(f"Unexpected {err=} during execution of go_to_first_ramp_cycle methode: {type(err)=}")
            raise
    
    def set_start_cycle(self):
        """methode to set the current ramp as start ramp
        """
        pyag.locateOnScreen(str(self.picturepath / 'ramp-1_logo.png') ,confidence=0.9)
    
    def multiple_ramps(self,number_ramp_cycles,*args):
        """ methode to set parameter for multiple ramp cycles """ 
        try:
            ramp_cycle = 0 
            parameter = args[0] # First [0] strips the args environment away
            for i in range(number_ramp_cycles):
                rate = parameter[0][0]        
                temperature = parameter[0][1] # [0][1] = First row second item
                duration = parameter[0][2]    # [0][2] = First row third item
                parameter = parameter[1:] # Move on to second row 
                self.set_parameter(rate,temperature,duration)
                ramp_cycle += 1
                self.change_ramp_cycle(ramp_cycle < number_ramp_cycles)
                
            self.go_to_first_ramp_cycle(number_ramp_cycles)
                
        except KeyboardInterrupt:
            print('\n')

    
    
    def move_temperature_line(self):
        """ methode to display current cryostat temperature """
        item = pyag.locateOnScreen(str(self.picturepath / 'temperature_line.png') ,confidence=0.9)
        pyag.moveTo(item)
        pyag.drag(300,0,2,button='left')
        return None

    def start_measurement(self):
        """ methode to start measurement """
        item = pyag.locateOnScreen(str(self.picturepath / ('start_button.png')) ,confidence=0.9)
        pyag.click(item, clicks = 1 ,button='left')
        time.sleep(1)
        self.click_ok()

    def click_ok(self):
        item = pyag.locateOnScreen(str(self.picturepath / ('OK_button.png')) ,confidence=0.9)
        pyag.click(item, clicks = 1 ,button='left')

        #pyag.write('enter')
        
    def stop_measurement(self):
        """methode to stop measurement"""
        item = pyag.locateOnScreen(str(self.picturepath / ('stop_button.png')) ,confidence=0.9)
        pyag.click(item, clicks = 1 ,button='left')
        

        
    def close_results(self,):
        """method to close temperature window. """
        item = pyag.locateOnScreen(str(self.picturepath / ('results_x_button.png')) ,confidence=0.9)
        pyag.click(item, clicks = 1 ,button='left')
        
    def open_minimized_LINK(self):
        """ methode to open minimized LINK window """
        try:
            logging.info('Reopening LINK window')
            bar = pyag.locateOnScreen(str(self.picturepath / 'LINK_logo.png'),confidence=0.9)
            pyag.click(bar ,button='left')
            time.sleep(2)

            #start_button = pyag.locateOnScreen('pictures\start_button.png',confidence=0.8)
            #print(start_button)
            #pyag.click(start_button, button='left',duration=3)
            #print(pyag.position())
        except KeyboardInterrupt:
            print('Process was cancelled')

