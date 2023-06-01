Getting Started
=====================

Prerequisites
-------------

Hardware: 
`````````
The core setup consists of a 

- computer
- light source
- monochromator
- two filter wheels
- chopper
- pre-amplifier
- lock-in amplifier
- sample holder

For further details refer to our Hardware section :ref:`Hardware`. 

Since the initial start of the sEQE setup the AFMD group has succeeded in integrating and automating a cryostat into the sEQE setup for temperature dependant sEQE measurements. For further information please contact Ming Zhu whos email is on the AFMD webpage.

Software 
````````

Proprietary Software:
:::::::::::::::::::::

- Lock-in Amplifier: LabOne by Zurich Instruments which can be downloaded for free at `Zurich Instruments download center <https://www.zhinst.com/europe/en/support/download-center>`_

Add-on:

- Cryostate: LINK by Linkam Scientific which has to be bought from `Linkam Scientific <https://www.linkam.co.uk/>`_

Free software:
::::::::::::::

- Working Python installation - setup was written in python 3.9 on Ubuntu. Afterwards it was made Windows compatible and is now mainly running under windows. 

What is Python ? And how do I install it ? Important questions whos answers you find under `<https://www.python.org/about/gettingstarted/>`_ . 
 
- Python packages mentioned in the according requirement files - there is one for Windows users and one for Linux users. 

We want to point out the `python microscope package <https://python-microscope.org/>`_ which we use to control the Thorlabs filter wheel. It was written by amazing people, go check out their current projects ! 



Installation
------------

0. Setup a virtual environment - why ? Great question, see `<https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/>`_ 

1. Log into the virtual environment and clone the git repository from `<https://github.com/AFMD/sEQE-Setup>`_ 

2. Choose according to your operating system the suitable requirements file and install dependencies via: 

    `pip install -r requirements_file.txt`


