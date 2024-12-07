Lamport Clock Simulator
=======================

A Python-based simulator for demonstrating and experimenting with Lamport's Logical Clock algorithm. This project provides both backend functionality for logical clocks and a graphical user interface (GUI) to visualize and interact with the simulation.

Features
--------

*   Simulate multiple processes, each with its own logical clock.
    
*   Trigger local events to increment a process's clock.
    
*   Transmit and receive messages between processes with proper clock synchronization.
    
*   Capture snapshots of the current states of all processes.
    
*   User-friendly graphical interface built with Tkinter.
    

Prerequisites
-------------

*   Python 3.7 or higher
    
*   Required libraries:
    
    *   tkinter (comes pre-installed with Python)
        

Installation
------------

1.  bashCopy codegit clone https://github.com/rohankayastha1/Lamport-clock-simulator.git
    
2.  bashCopy codecd Lamport-clock-simulator
    
3.  bashCopy codepython lamport-simulation.py
    

How to Use
----------

1.  **Start the Simulation**:
    
    *   Enter the number of processes you want to simulate in the input box and click **"Create Processes"**.
        
2.  **Trigger Local Events**:
    
    *   Click **"Local Event"** for any process to increment its clock.
        
3.  **Send Messages**:
    
    *   Click **"Send Message"** for a process to send a message to one or more recipient processes.
        
    *   Select the recipients in the dialog box and confirm the message.
        
4.  **Receive Messages**:
    
    *   Click **"Receive Message"** for a process to process a pending message from the message queue.
        
5.  **Capture Snapshot**:
    
    *   Click **"Take Snapshot"** to view the current clock values of all processes.
        


Understanding the Code
----------------------

### Logical Clock

Each process is represented by a logical clock that:

*   Increments on local events.
    
*   Increments and transmits its value during message sending.
    
*   Synchronizes with received clock values during message reception.
    

### GUI

The Tkinter-based interface provides an interactive way to:

*   Manage processes.
    
*   Trigger events and simulate message exchanges.
    
*   Display snapshots of the system state.
    

Future Improvements
-------------------

*   Add support for vector clocks.
    
*   Display a visual representation of message exchanges.
    
*   Allow saving and loading snapshots.
    

About
-------

This project is a part of academic subject project 


Author
------

Rohan Kayastha KaluwarEmail: rohankayastha111@gmail.comGitHub: [rohankayastha1](https://github.com/rohankayastha1)
