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

    def get_question(self, topic=None, question_id=None):
        if len(self.free) == 0:
            print("No more questions! Resetting queue")
            self.free = list(self.questions.keys())
        if question_id:
            if question_id in self.questions:
                return self.questions[question_id]
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
            return self.questions[randomQuestionId]
    
    def update_data(self):
        self.data = {
            "questions": self.questions,
            "topics": self.topics
        }
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

    def add_question(self, question, topic=None):
        if question:
            # it can be better if we change questions from Dict to List
            # then it will be able to index questions on the fly 
            new_q_id = str(max(map(int, self.questions.keys())) + 1)
            self.questions[new_q_id] = question
            if topic in self.topics:
                self.topics[topic].append(new_q_id)
            self.update_data()
            return "Added question " + new_q_id
        return "No question given!"
                

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith(ask_command):
        context = message.content.split(ask_command)[1].strip()
        if context.startswith("add"): # add question
            question = context.split("add")[-1].strip()
            result = q.add_question(question)
            await message.channel.send(result)
        elif context.startswith("id"): # select question by id
            question_id = context.split("id")[-1].strip()
            result = q.get_question(question_id=question_id)
            await message.channel.send(result)
        else: # return question (by topic if given)
            topic = message.content.split(ask_command)[-1].strip()
            question = q.get_question(topic)
            await message.channel.send(question)

q = Questions()
client.run(os.environ['TOKEN'])


# TODO:
# - add questions by chat ✔
# - manage topics
# - list questions
# - handle free questions in better way (?) // what about theme questions
