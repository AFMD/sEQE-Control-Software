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
    If you want to stop the automation: "Slam" mouse pointer into one of the screen corners.
    
    nomenclature:
    LINK: name of the Linkam Scientific's software for operating their cryostat.
    ramp cycle: multiple (temperature) rows connected to cover the whole temperature range of interest for this measurement. 
    (temperature) row: a specific temperature change with a given rate [degrees C/min], a given final temperature [degrees C], a holding time [h:m:s] and lnp-speed [?]. 
    lnp-speed: the speed with which liquid nitrogen is pumped into the sample chamber.
    
    """
    def __init__(self,exe_path):
        try:
            self.connected = False
            self.LINKpath = exe_path
            
        except Exception as err:
            logging.error(f"Unexpected {err=} during execution of __init__ function: {type(err)=}")
    
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
        picturepath : PosixPath
            Operating system independent path description to LINK automation screenshots
            
        Raises
        ------
        TypeError
            If tkinter.filedialog gets cancelled and does not return a PosixPath object
        
        Notes
        -----
        These screenshots have to be done every time the computer changes. 
        Carefull: even changing the computer's monitor might lead to errors.
        
        If some items on the screenshots are not found, redo the screenshots and name them as their predecessors.
        
        """
        try:
            root = Tk() # Creates master window for tkinters filedialog window
            root.withdraw() # Hides master window
            
            picturepath = pathlib.Path(filedialog.askdirectory(title = 'Choose the LINK screenshot folder'))
            
            if not picturepath == '':
                return picturepath
            
            else: 
                logging.error('Empty picturepath - please choose a folder path again')
        except Exception as err:
            logging.error(f"Unexpected {err=} during execution of define_picture_path function:" + '\n' + f"{type(err)=}")
            
    # def open_LINK(self):
    #     """ methode to open LINK program """
    #     subprocess.Popen(['C:\\Program Files\\Linkam Scientific\\LINK\\LINK.exe'])
    #     return None

    def connect(self,):
        """Methode connecting T96 controller to LINK via USB.
        
        Returns
        ------
        self.connected : bool
            True if LINK software up and USB connection successful, False by default
            
        self.picturepath : PosixPath
             Operating system independent path description to LINK automation screenshots now as class attribute

        Notes
        -----
        This methode opens LINK, uses the screenshots in picturepath to locate necessary buttons on the screen and automatically 
        connect to the T96 controller via USB.
        
        """ 

        try:
            
            subprocess.Popen(self.LINKpath) #'C:\\Program Files\\Linkam Scientific\\LINK\\LINK.exe'
            self.picturepath = self.define_picture_path()
            
            user_input = pyag.alert('Confirm that the LINK software has started, is open in front of you and you are ready for pyautogui to take over the mouse.')
            if user_input == 'OK':
                controller_menu = pyag.locateOnScreen(str(self.picturepath / 'controller-menu.png') ,confidence=0.9)
                pyag.moveTo(controller_menu)
                pyag.click(controller_menu, clicks = 1 ,button='left')
                time.sleep(1)
                pyag.move(0,30)
                pyag.click(clicks=1, button='left')
                time.sleep(2)
            
                if pyag.locateOnScreen(str(self.picturepath / 'Temp_logo.png') ,confidence=0.9):
                    self.connected = True
                    pyag.alert('Mouse is free to use')
                
                return self.connected, self.picturepath
            
            else: self.logger.info('Confitm')
            
        except OSError as err:
            logging.error(f'{err=} during execution of connect methode: {type(err)=}' + '\n' + 'screenshot objects were not found on the screen.')
        
        except TypeError as err:
            logging.error(f'{err=} during execution of connect methode: {type(err)=}' + '\n' + 'filepath choice got canceled')
        
            
        except Exception as err:
            logging.error(f"Unexpected {err=} during execution of connect function:" + '\n' + f"{type(err)=}")


    def import_lpf(self,filename):
        """Methode to import cryostat parameters into LINK via LINK profile file.
        
        Parameters
        ----------
        filename: string, required
            name of LINK's profile file
        
        Notes
        -----
        Give ONLY filename, not path
        LINK profile file ending: .lpf
        
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
            logging.error(f"Unexpected {err=} during execution of import_lpf methode:" + '\n' + f"{type(err)=}")


    def export_lpf(self,filename):
        """Methode to save LINK cryo parameter to .lpf file in LINK.
        
        Parameters
        ----------
        filename: string, required
            name of LINK's profile file
        
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
            logging.error(f"Unexpected {err=} during execution of export_lpf methode:" + '\n' + f"{type(err)=}")
            
            
    def set_parameter(self,ramp_rate,final_temperature,holding_time): #40 pixels down is the enter
        """Methode to set manually the parameter of one ramp row in LINK.
        
        Parameters
        ----------
        ramp_rate : float
            degree Celsius per minute change in chamber
            
        final_temperature : float 
            final temperature after temperature ramp 
            
        holding_time : int 
            total time for cryostat to hold the temperature
        
        Notes
        -----
        Automatically sets the liquid nitrogen pump speed (lnp-speed) to "auto". 
        
        """
        try:
            array0 = [ramp_rate,final_temperature,holding_time] # Import via csv file 
            array = [self.picturepath / 'rate_logo.png',self.picturepath / 'limit_logo.png',self.picturepath / 'time_logo.png']
            for parameter,picture in list(zip(array0,array)):
                item = pyag.locateOnScreen(str(picture) ,confidence=0.9)
                pyag.moveTo(item)
                pyag.move(0,20)
                pyag.click(button='left')
                pyag.write(f'{parameter}')
                pyag.press('enter')
            lnp_speed = pyag.locateOnScreen(str(self.picturepath / 'lnp-speed_logo.png') ,confidence=0.9)
            pyag.moveTo(lnp_speed)
            pyag.move(0,20)
            pyag.click(button='left')
            auto_button = pyag.locateOnScreen(str(self.picturepath / 'auto_button.png') ,confidence=0.9)
            pyag.click(auto_button, clicks = 1 ,button='left')
            pyag.press('enter')

        except Exception as err:
            logging.error(f"Unexpected {err=} during execution of set_parameter methode:" + '\n' + f"{type(err)=}")

    def change_ramp_cycle(self,direction):
        """Methode to change ramp row in LINK.
        
        Parameters
        ----------
        direction : bool 
            True for move on temperature row up, False for one row down
            
        
        """
        try:
            if direction == True:
                item = pyag.locateOnScreen(str(self.picturepath / 'next_cycle.png') ,confidence=0.9)
                pyag.click(item, clicks = 1 ,button='left')
            if direction == False:
                item = pyag.locateOnScreen(str(self.picturepath / 'last_cycle.png') ,confidence=0.9)
                pyag.click(item, clicks = 1 ,button='left')
        
        except Exception as err:
            logging.error(f"Unexpected {err=} during execution of change_ramp_cycle:" + '\n' + f"{type(err)=}")        

    def go_to_first_ramp_cycle(self,number_ramp_cycles):
        """Methode to move back to first row in LINK. 
        
        Parameters
        ----------
        number_ramp_cycles : int
            number of rows in this specific ramp cycle 
        """
        try:
            for i in range(number_ramp_cycles):
                if not pyag.locateOnScreen(str(self.picturepath / 'ramp-1_logo.png') ,confidence=0.9):
                    self.change_ramp_cycle(False)
                else: break
                
        except Exception as err:
            logging.error(f"Unexpected {err=} during execution of go_to_first_ramp_cycle methode:" + '\n' + f"{type(err)=}")
    
    def set_start_cycle(self):
        """Methode to set the current row as start of ramp cycle.
        
        Notes
        -----
        LINK does not automatically start the next temperature row if you stop the current holding time, and move up in the ramp cycle. 
        The user has to specify the current row as the next "start row" by pressing on the "ramp logo" and click on "set start row"
        
        """
        try: 
            item = pyag.locateOnScreen(str(self.picturepath / 'ramp_logo.png') ,confidence=0.9)
            pyag.click(item, clicks = 1 ,button='left')
            item = pyag.locateOnScreen(str(self.picturepath / 'set_start_row_button.png') ,confidence=0.9)
            pyag.click(item, clicks = 1 ,button='left')
            
        except Exception as err:
            logging.error(f"Unexpected {err=} during execution of set_start_cycle methode:" + '\n' + f"{type(err)=}")
        
    def multiple_ramps(self,number_ramp_cycles,*args):
        """Methode to set parameter for multiple temperature rows.
        
        Parameters
        ----------
        number_ramp_cycles : int
            number of rows in this specific ramp cycle
            
        args : list 
            
        
        """ 
        try:
            ramp_cycle = 0 
            parameter = args[0] # First [0] strips the args environment away
            user_input = pyag.alert('Confirm that the LINK window is visible and you are ready for pyautogui to take over the mouse.')
            if user_input == 'OK': 
                for i in range(number_ramp_cycles):
                    rate = parameter[0][0]        
                    temperature = parameter[0][1] # [0][1] = First row second item
                    duration = parameter[0][2]    # [0][2] = First row third item
                    parameter = parameter[1:] # Move on to second row 
                    self.set_parameter(rate,temperature,duration)
                    ramp_cycle += 1
                    self.change_ramp_cycle(ramp_cycle < number_ramp_cycles)

                self.go_to_first_ramp_cycle(number_ramp_cycles)
                
            else:
                self.logger.info('Could not confirm LINK window for multiple_ramps methode - please try again')

        except Exception as err:
            logging.error(f"Unexpected {err=} during execution of multiple_ramps methode:" + '\n' + f"{type(err)=}")
    
    
    def move_temperature_line(self):
        """Methode to display current cryostat temperature."""
        try: 
            item = pyag.locateOnScreen(str(self.picturepath / 'temperature_line.png') ,confidence=0.9)
            pyag.moveTo(item)
            pyag.drag(300,0,2,button='left')
            
        except Exception as err:
            logging.error(f"Unexpected {err=} during execution of move_temperature_line methode:" + '\n' + f"{type(err)=}")
            
    def start_measurement(self):
        """Methode to start measurement."""
        
        try:
            item = pyag.locateOnScreen(str(self.picturepath / ('start_button.png')) ,confidence=0.9)
            pyag.click(item, clicks = 1 ,button='left')
            time.sleep(1) # Wait for popup window
            self.click_ok()
        
        except Exception as err:
            logging.error(f"Unexpected {err=} during execution of start_measurement methode:" + '\n' + f"{type(err)=}")        

    def click_ok(self):
        """Methode to click 'OK' button."""
        
        try: 
            item = pyag.locateOnScreen(str(self.picturepath / ('OK_button.png')) ,confidence=0.9)
            pyag.click(item, clicks = 1 ,button='left')
            
        except Exception as err:
            logging.error(f"Unexpected {err=} during execution of click_ok methode:" + '\n' + f"{type(err)=}")        
        
    def stop_measurement(self):
        """Methode to stop measurement."""
        
        try:
            item = pyag.locateOnScreen(str(self.picturepath / ('stop_button.png')) ,confidence=0.9)
            pyag.click(item, clicks = 1 ,button='left')

        except Exception as err:
            logging.error(f"Unexpected {err=} during execution of stop_measurement methode:" + '\n' + f"{type(err)=}")            

    def close_results(self,):
        """Method to close temperature window."""
        
        try:
            item = pyag.locateOnScreen(str(self.picturepath / ('results_x_button.png')) ,confidence=0.9)
            pyag.click(item, clicks = 1 ,button='left')
            
        except Exception as err:
            logging.error(f"Unexpected {err=} during execution of close_results methode:" + '\n' + f"{type(err)=}")
        
    def open_minimized_LINK(self):
        """Methode to open minimized LINK window."""
        
        try:
            logging.info('Reopening LINK window')
            bar = pyag.locateOnScreen(str(self.picturepath / 'LINK_logo.png'),confidence=0.9)
            pyag.click(bar ,button='left')
            time.sleep(2)

        except KeyboardInterrupt:
            print('Process was cancelled')

