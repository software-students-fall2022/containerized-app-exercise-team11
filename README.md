[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-c66648af7eb3fe8bc4f294546bfd86ef473780cde1dea487d3c4ff354943c9ae.svg)](https://classroom.github.com/online_ide?assignment_repo_id=9354868&assignment_repo_type=AssignmentRepo)
# Containerized App Exercise

![BadgeWebClientTest](https://github.com/software-students-fall2022/containerized-app-exercise-team11/actions/workflows/workflow.yml/badge.svg) ![BadgeMLTest](https://github.com/software-students-fall2022/containerized-app-exercise-team11/actions/workflows/ml_workflow.yml/badge.svg)

## Description
This project will allow the user to have their speech translated in near real-time. The user speaks into their microphone, their speech is transcribed into text, and that text is translated. The translation is then available for the user to view through the web app.

## Instructions for Use
Please run the below commands in a terminal on your system to install and run these programs. Before you begin, please [ensure Docker is installed on your system](https://docs.docker.com/engine/install/). Also, please [ensure ffmpeg is installed on your system](https://ffmpeg.org/download.html).

### Step 1: Clone Repository
First, clone this repository onto your system:
```
git clone https://github.com/software-students-fall2022/containerized-app-exercise-team11.git
```
### Step 2: Create & Set Up Virtual Environment
Next, navigate to the machine learning folder:
```
cd machine-learning-client
```
Create a python virtual environment:
```
python -m venv .venv
```
Next, you will have to activate the virtual environment. This step will differ on different operating systems. Conventionally, on UNIX-like systems (Mac and Linux), the command to do this will be:
```
source venv/bin/activate
```
On Windows, the activate script is conventionally `.venv\Scripts\Activate.ps1`. If your activation script is located there, use this command in PowerShell:
```
.\.venv\Scripts\Activate.ps1
```
After your virtual environment has been activated, install dependencies needed for the machine learning client:
```
pip install -r requirements.txt
```
### Step 3: Start Docker Containers
In a seperate terminal window, in the root directory of the project, start the docker containers for the web app and MongoDB database by using:
```
docker compose up
```
If you receive permissions errors, use `sudo` in front of the above command if on Mac or Linux, or use an elevated PowerShell terminal to run the command if on Windows.

### Step 4: Run Machine Learning Client
In the original terminal window, run the following command to start the Machine Learning Client:
```
python -m translator
```

### Step 5: Instructions for Program Use
After starting the machine learning client, type in the number of seconds you want to record for. Then press Enter. Once you press Enter, the program will start recording using the default microphone on your system.
Once the recording has stopped, you will be presented with options on what language you want the program to translate your speech into, if any. Make a selection, then press enter.

Navigate to <http://localhost:5000> to view the most recent translation, as well as data about your speech.

Navigate to <http://localhost:5000/history> to view all the translations you have ever done.

If you have any more translations you would like to do, you may repeat these steps. Otherwise, follow the instructions below to exit the program.

### Step 6: Exiting the Program
To exit the machine learning client, enter anything non-numeric into the machine learning client when it asks for a recording length.

To exit the web app, use `Ctrl+C` in the terminal or exit the window it is running in.

## Team 11 Members:
[Michael Ma](https://github.com/mma01us)
[David Adler](https://github.com/dov212)
[Harrison Douglass](https://github.com/hpdouglass)
[Sneheel Sarangi](https://github.com/Xarangi)
[Bruce Wu](https://github.com/bxw201)
[Brandon Chao](https://github.com/Sciao)
[Khalifa AlFalasi](https://github.com/Khalifa-AlFalasi)
