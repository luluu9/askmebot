## Bot description
This bot is used to socialize with friends on Discord servers. Ask yourselves questions and have a fun!

#### Features
- ask a random question ✔
- add/remove questions using a Discord chat ✔
- list pages of questions ✔
- choose a theme of the questions ✔
- manage questions' topics by chat ✔
- ~~handle many servers at once~~ ❌
- ~~add multiple questions by chat at once~~ ❌

If you have some good ideas, write to me!

#### Requirements
- Python 3 (tested on Python 3.9.4)
- Discord Bot account and token: you can look [here](https://www.freecodecamp.org/news/create-a-discord-bot-with-python/) for this
- Installed modules from requirements.txt

#### Installation
To use this bot on your own follow instructions:
- download this repository by `git pull https://github.com/luluu9/askmebot` or Code -> Download ZIP button and extract it
- open terminal in downloaded directory
- install requirements by typing `pip -r install requirements.txt`
- export a variable TOKEN in terminal/Powershell/cmd:
  - Terminal: `export TOKEN={your Discord Bot token}`
  - Powershell: not supported now
  - cmd: `set TOKEN={your Discord Bot token}`
- [optionally] generate a data.json file with questions and topics with `py data.py` (look *How to use* paragraph for more information)
- run bot by using `py askme.py`

#### How to use
Firstly, you may want to generate a list of questions. In this repository you have included list of some Polish questions in the *questions.txt* file. Currently, you have to write down questions on your own to questions.txt file. I will be working on bringing some basic funny questions to the repository. 
Then, run the *data.py* file to generate a *data.json* file that contains informations about questions. 

You can also add questions by Discord chat by typing *!askme add [question]*.

After that, all you have to do is to run the *askme.py* script and type *!askme* command on Discord chat. 
Type *!askme help* to get a list about supported commands. 

You can change *!askme* to whatever command you want. Just edit *ask_command* variable in *askme.py* file.

#### Known bugs
- Currently none