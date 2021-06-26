## Setting up a Windows Development environment 

 

Howdoi can be used on Windows, MacOS and Linux etc. But the development environment can only be set up in a Linux or Mac. To set up the development environment in Windows, follow the following steps: 

### Install WSL

WSL is Windows Subsystem for Linux. It offers Linux interoperability in Windows and allows users to set up a virtual environment. 

If you do not have WSL set up, follow the steps in this [tutorial](https://www.windowscentral.com/install-windows-subsystem-linux-windows-10) 

### Setting up the virtual environment

After setting up WSL, go to the directory where you want to set up Howdoi. Open the Command Prompt here and enter the following to enter the WSL environment. 

``` bash
bash 
``` 

Now you are using the Linux-compatible kernel on Windows and can set up a virtual environment. 

### Clone the git repository

```bash
$ git clone https://github.com/gleitz/howdoi.git 
``` 

Setup and activate a virtual environment: 

``` bash
$ python3 -m venv .venv 
$ source .venv/bin/activate 
``` 

Make sure you have pip installed, if not, enter: 

``` bash
$ sudo apt install python3-pip 
``` 

Go to the project directory and install requirements: 

``` bash
$ cd howdoi 
$ pip install -r requirements.txt 
``` 

> if howdoi does not process queries after this command, make sure your PATH variables for Python and Pip are set correctly in Windows environment variables.  

### Test run

Check to see if everything has been set-up correctly: 

```  bash
pip install howdoi 
howdoi  print hello world
``` 

 

 

 