import discord
import os 
import json
import random
from math import ceil

client = discord.Client()

# questions:
# [question1, question2...]

# topics:
# topic: [id1, id2]...

# already_asked:
# [id1, id2]

directory = os.path.dirname(__file__)

ask_command = "!askme"
datafile = directory + "\\data.json"


class Questions:
    def __init__(self, datafile):
        data = self.load_data(datafile)
        self.questions = data['questions']
        self.topics = data['topics']
        self.free = [i for i in range(len(self.questions))]  # id of questions that were not used

    def load_data(self, datafile):
        try:
            with open(datafile, 'r', encoding="utf-8") as f:
                return json.load(f)
        except Exception as error:
            print("Can't open data.json file")
            raise error

    def get_question(self, topic=None, question_id=None):
        if len(self.free) == 0:
            print("No more questions! Resetting the queue")
            self.free = [i for i in range(len(self.questions))]
        if question_id is not None:
            if 1 <= question_id <= len(self.questions):
                return self.questions[question_id - 1]
            return f"Invalid id, range from 1 to {len(self.questions)}"
        if topic:
            if topic in self.topics:
                random_question_id = int(random.choice(self.topics[topic]))
                try:
                    self.free.remove(random_question_id)
                except ValueError:  # it can happen if someone firstly pull question that is in topic list
                    pass
                return self.questions[random_question_id]
            else:
                print('No topic in the topic database:', topic)
                return "No " + topic + " in the topic database!"
        else:
            random_question_id = random.choice(self.free)
            self.free.remove(random_question_id)
            return self.questions[random_question_id]
    
    def update_data(self):
        data = {
            "questions": self.questions,
            "topics": self.topics
        }
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def add_question(self, question, topic=None):
        if question:
            self.questions.append(question)
            question_id = len(self.questions)
            if topic in self.topics:
                self.topics[topic].append(question_id)
            self.update_data()
            return "Added question with id " + str(question_id)
        return "No question given!"
    
    def get_questions(self, page, amount_on_page=10):
        start = (page-1)*amount_on_page
        stop = page*amount_on_page
        questions_list = self.questions[start:stop]
        if len(questions_list) == 0:
            return ["No questions on this page!"]
        return questions_list
    
    def get_questions_amount(self):
        return len(self.questions)
                

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith(ask_command):
        context = message.content.split(ask_command)[1].strip()
        if context.startswith("add"):  # add question
            await add_question(message, context)
        elif context.startswith("id"):  # select question by id
            await select_by_id(message, context)
        elif context.startswith("list"):  # get list of questions
            await list_questions(message, context)
        else:  # return question (by topic if given)
            await return_question(message, context)


async def add_question(message, context):
    question = context.split("add")[-1].strip()
    result = q.add_question(question)
    await message.channel.send(result)


async def select_by_id(message, context):
    question_id = int(context.split("id")[-1].strip())
    result = q.get_question(question_id=question_id)
    await message.channel.send(result)


async def list_questions(message, context):
    amount = 10
    page = context.split("list")[-1].strip()
    if page:
        page = int(page)
        result = q.get_questions(page, amount)
        questions_list = ""
        start = (page-1)*amount+1
        for i, question in enumerate(result, start=start):
            questions_list += f"{i}. {question}\n"
        await message.channel.send(questions_list)
    else:
        await message.channel.send(f"Choose page from 1 to {ceil(q.get_questions_amount()/amount)}")


async def return_question(message, context):
    topic = message.content.split(ask_command)[-1].strip()
    question = q.get_question(topic)
    await message.channel.send(question)


if __name__ == "__main__":
    q = Questions(datafile)
    client.run(os.environ['TOKEN'])


# TODO:
# - add questions by chat ✔
# - handle questions ids better ✔
# - list questions ✔
# - manage topics
# - handle free questions in better way (?) // what about theme questions
