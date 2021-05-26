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

help_message = f"""
- {ask_command}: asks random question
- {ask_command}: [topic]: asks random question about topic
- {ask_command}: add [question]: adds question to list
- {ask_command}: list [page]: lists questions on page x
- {ask_command}: topics: lists available topics
- {ask_command}: topic [topic]: lists question about topic
- {ask_command}: set [question_id] [topic]: sets question to topic
- {ask_command}: unset [question_id] [topic]: unsets question from topic
"""


class Questions:
    def __init__(self, datafile):
        self.datafile = datafile
        self.questions = []
        self.topics = {}
        data = self.load_data(datafile)
        if data:
            self.questions = data['questions']
            self.topics = {topic: list(map(int, indexes)) for topic, indexes in data['topics'].items()}
        self.free = [i for i in range(len(self.questions))]  # id of questions that were not used

    def load_data(self, datafile):
        try:
            with open(datafile, 'r', encoding="utf-8") as f:
                return json.load(f)
        except Exception as error:
            if os.path.exists(datafile):
                print("Can't open data.json file")
                raise error
            else:
                return None

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
                random_question_id = int(random.choice(self.topics[topic])) - 1
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
        with open(self.datafile, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def add_question(self, question, topic=None):
        if question:
            self.questions.append(question)
            question_id = len(self.questions)
            if topic in self.topics:
                self.topics[topic].append(question_id)
            self.free.append(question_id)
            self.update_data()
            return "Added question with id " + str(question_id)
        return "No question given!"
    
    def remove_question(self, remove_id):
        if 0 < remove_id and remove_id <= len(self.questions):
            self.questions.pop(remove_id-1)
            # indexes are rearranged so clean up dirt
            index_to_del = len(self.questions) + 1
            if index_to_del in self.free:
                self.free.remove(index_to_del)
            for topic, questions_ids in self.topics.items():
                if remove_id in questions_ids:
                    self.topics[topic].remove(remove_id)
                # deincrement each question with id above id to remove
                for index, question_id in enumerate(questions_ids):
                    if question_id > remove_id:
                        self.topics[topic][index] -= 1
            self.update_data()
            return "Successfully removed question " + str(remove_id)
        else:
            return "Bad id to remove: " + str(remove_id)

    def get_questions(self, page, amount_on_page=10):
        start = (page-1)*amount_on_page
        stop = page*amount_on_page
        questions_list = self.questions[start:stop]
        if len(questions_list) == 0:
            return ["No questions on this page!"]
        return questions_list
    
    def get_questions_amount(self):
        return len(self.questions)
    
    def get_topic_list(self):
        return [topic for topic in self.topics]

    def get_topic_questions(self, topic):
        if topic in self.topics:
            return [self.questions[q-1] for q in self.topics[topic]]
        else:
            return ["Topic not in the database!"]
    
    def set_topic(self, question_id, topic):
        if topic in self.topics:
            if question_id in self.topics[topic]:
                return "Question already in the topic list!"
            if question_id < 1 or question_id > len(self.questions):
                return f"Invalid question id, choose between 1 and {len(self.questions)}"
            self.topics[topic].append(question_id)
            self.update_data()
            return f"Question {question_id} set to the topic {topic}"
        else:
            self.topics[topic] = [question_id]
            self.update_data()
            return f"Added topic {topic} and set {question_id} there"

    def unset_topic(self, question_id, topic):
        if topic in self.topics:
            if question_id in self.topics[topic]:
                self.topics[topic].remove(question_id)
                self.update_data()
                return f"Question {question_id} removed from the topic {topic}"
            return "Question not in the topic list!"
        else:
            return "Topic not in the database!"
    
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
        elif context.startswith("remove"):
            await remove_question(message, context)
        elif context.startswith("id"):  # select question by id
            await select_by_id(message, context)
        elif context.startswith("list"):  # get list of questions
            await list_questions(message, context)
        elif context.startswith("topics"):
            await print_topics(message, context)
        elif context.startswith("topic"):
            await print_topic(message, context)
        elif context.startswith("set"):
            await set_topic(message, context)
        elif context.startswith("unset"):
            await unset_topic(message, context)
        elif context.startswith("help"):
            await help(message, context)
        else:  # return question (by topic if given)
            await return_question(message, context)


async def add_question(message, context):
    question = context.split("add", maxsplit=1)[-1].strip()
    result = q.add_question(question)
    await message.channel.send(result)


async def remove_question(message, context):
    question_id = int(context.split("remove")[-1].strip())
    result = q.remove_question(question_id)
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


async def print_topics(message, context):
    topics_list = q.get_topic_list()
    topics_str = "\n".join(["- " + topic for topic in topics_list])
    await message.channel.send(topics_str)


async def print_topic(message, context):
    topic = context.split("topic")[-1].strip()
    topic_questions = q.get_topic_questions(topic) 
    questions_str = "\n".join([str(i) + ". " + q for i, q in enumerate(topic_questions, start=1)])
    await message.channel.send(questions_str)


async def set_topic(message, context):
    args = context.split("set")[-1].split()
    question_id = int(args[0])
    topic = args[1]
    result = q.set_topic(question_id, topic)
    await message.channel.send(result)


async def unset_topic(message, context):
    args = context.split("set")[-1].split()
    question_id = int(args[0])
    topic = args[1]
    result = q.unset_topic(question_id, topic)
    await message.channel.send(result)


async def help(message, context):
    await message.channel.send(help_message)


if __name__ == "__main__":
    q = Questions(datafile)
    client.run(os.environ['TOKEN'])


# TODO:
# - add questions by chat ✔
# - handle questions ids better ✔
# - list questions ✔
# - remove questions by chat ✔
# - manage topics ✔
# - add help ✔
# - check indexes when setting question id to topic ✔
# - ensure indexes is passed as int to topics variable ✔
# - modify database to run simultaneously on many servers at once 
# - list questions by topic in one function (?)
# - handle free questions in better way (?) // what about theme questions
# - add multiple questions by chat at once


# KNOWN BUGS:
# - if keyword add in add question message, content is eaten (if someone types !askme add added) in db it figures as "ed") ✔