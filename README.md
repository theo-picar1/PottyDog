# PottyDog 
## What is PottyDog❔
<div align="center">
    <img src="./server/static/images/happy_dog.png" width="200">
</div>

PottyDog is a tool that combines hardware and software that will allow you to know whether or not your dog is waiting by the door to go out and potty, with the help of an easy-to-use UI and easy-to-setup device!

**Note:** new features will still be implemented for this project, but development will slow down.

## Website 🌐
<img src="./server/static/images/website-certificate.png">

You can check out the website here: https://pottydog.online

**Note:** As this is an early version, you will not be able to track your dog without the device AND the correct permissions. This will be addressed in a future version!

## Technologies Used 🧑‍💻

<div style="display: flex; align-items: center; gap: 10px">
    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/python/python-original.svg" width="50"/>
    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/javascript/javascript-original.svg" width="50"/>
    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/html5/html5-original.svg" width="50"/>
    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/css3/css3-original.svg" width="50"/>
    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/bootstrap/bootstrap-original.svg" width="60"/>
    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/mysql/mysql-original.svg" width="50"/>
    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/flask/flask-original.svg" width="60"/>
    <img src="./server/static/images/pubnub-logo.png" width="100">
    <img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/amazonwebservices/amazonwebservices-original-wordmark.svg" width="55"/>
</div>
<br>

- Languages: Python, JavaScript, HTML, CSS, BootStrap, MySQL DB
- Framework: Flask
- Other: PubNub, Amazon Web Services 

## Hardware Setup 👷
- **PIR Sensor** for motion detection from heat emitting objects, like pets and people

<img src="./server/static/images/pir-sensor.png" width="350" />

- **Raspberry Pi 400 Model B** for processing sensor input and managing device behaviour

<img src="./server/static/images/raspberry-pi4.png" width="350" />

- **Buzzer** as an auditory cue that the device is on and ready to go

<img src="./server/static/images/piezo-buzzer.png" width="350"/>

- **Fritzing diagram** of hardware connections

<img src="./server/static/images/PottyDog Fritz Diagram.jpg">

## System Architecture 🌉
<img src="./server/static/images/pottydog-architecture.png">

## Features Implemented ✅
- Live motion detection that updates the UI immediately based on motion type (basic motion, no motion, staying motion)
- Logging in and registering, with passwords securely stored with Bcrypt password hashing
- Logging potty activity (pee, poop, both, other) with the option to add a note to it and view it in a separate page
- Basic profile editing for username and dog's name
- Main dashboard to show motion status, potty activity count for the day, and the last recorded potty activity

## Features to be Implemented 📋
- Google login
- Dynamically add new devices for different dog owners
- Video footage if dog is by the door (may be difficult)
- Edit and delete potty logs in the activity page
- Add and delete users in admin dashboard 
- Allow multiple users to use the same device
- Create a page that gives a tutorial on how to use a device

## Website Preview
<img src="./server/static/images/pottydog-landing.png">
<img src="./server/static/images/pottydog-dashboard.png">
<img src="./server/static/images/pottydog-activities.png">
<img src="./server/static/images/pottydog-admin-dashboard.png">