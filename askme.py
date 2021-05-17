import discord
import os 
import json
import random

client = discord.Client()

# questions:
# id1: question; id2:...

# topics:
# topic: [id1, id2]...

# already_asked:
# [id1, id2]

ask_command = "!askme"


class Questions:
    def __init__(self):
        try:
            with open('data.json', 'r', encoding="utf-8") as f:
                data = json.load(f)
        except Exception as error:
            print("Can't open data.json file")
            raise error

        self.questions = data['questions']
        self.topics = data['topics']
        self.free = list(self.questions.keys()) # id of questions that were not used 

    def get_question(self, topic=None):
        if len(self.free) == 0:
            print("No more questions! Resetting queue")
            self.free = list(self.questions.keys())
        if topic:
            if topic in self.topics:
                randomQuestionId = random.choice(self.topics[topic])
                try:
                    self.free.remove(randomQuestionId)
                except ValueError: # it can happen if someone firstly pull question that is in topic list 
                    pass
                return self.questions[randomQuestionId]
            else:
                print('No topic in the database:', topic)
                return "No " + topic + " in the database!"
        else:
            randomQuestionId = random.choice(self.free)
            self.free.remove(randomQuestionId)
            return self.questions[randomQuestionId])
        


@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith(ask_command):
        topic = message.content.split(ask_command)[-1].strip()
        question = q.get_question(topic)
        await message.channel.send(question)

q = Questions()
client.run(os.environ['TOKEN'])
