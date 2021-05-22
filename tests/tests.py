import unittest
import sys, os
import json


class TestQuestions(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestQuestions, self).__init__(*args, **kwargs)
        import askme
        self.testQuestions = askme.Questions(myPath + "\\" + "test_data.json")
        self.assertQuestions = ["First question", "Second question", "Last question"]
        self.assertTopics = {"first": [1], "others": [2, 3]}
    
    def test_data_import(self):
        q = self.testQuestions.questions
        self.assertEqual(q, self.assertQuestions)
    
    def test_get_question(self):
        q =  self.testQuestions.get_question()
        self.assertIn(q, self.assertQuestions)

    def test_no_free_questions(self):
        # it's good if prints "No more questions!"
        for i in range(len(self.assertQuestions) + 1):
            q =  self.testQuestions.get_question()
            self.assertIn(q, self.assertQuestions)
    
    def test_get_question_by_id(self):
        q = self.testQuestions.get_question(question_id=1)
        self.assertIn(q, self.assertQuestions[0])

    def test_get_question_by_topic(self):
        q = self.testQuestions.get_question(topic="first")
        self.assertEqual(q, "First question")
    
    def test_get_question_by_invalid_topic(self):
        q = self.testQuestions.get_question(topic="invalid_topic")
        self.assertEqual(q, "No invalid_topic in the topic database!")

    def test_add_empty_question(self):
        r = self.testQuestions.add_question("")
        self.assertEqual(r, "No question given!")

    def test_add_question(self):
        r = self.testQuestions.add_question("Added question")
        self.assertEqual(r, "Added question with id " + str(len(self.assertQuestions)+1))
    
    def test_remove_question(self):
        self.testQuestions.questions.append("To delete")
        current_questions = self.testQuestions.questions
        id_to_remove = len(current_questions)
        r = self.testQuestions.remove_question(id_to_remove)
        self.assertEqual(r, "Successfully removed question " + str(id_to_remove))
        self.assertEqual(current_questions, self.assertQuestions)
        self.assertNotIn("To delete", self.testQuestions.questions)
        self.assertNotIn(id_to_remove, self.testQuestions.free)

    def test_remove_question_invalid_id(self):
        invalid_id = len(self.testQuestions.questions) + 1
        r = self.testQuestions.remove_question(invalid_id)
        self.assertEqual(r, "Bad id to remove: " + str(invalid_id))
    
    def test_remove_question_check_topics(self):
        self.testQuestions.questions.append("To delete")
        current_questions = self.testQuestions.questions
        id_to_remove = len(current_questions)
        self.testQuestions.topics["to_del"] = [id_to_remove]
        self.testQuestions.remove_question(id_to_remove)
        self.assertEqual(self.testQuestions.topics["to_del"], [])
    
    def test_set_existing_topic(self):
        self.testQuestions.set_topic(1, "others")
        testTopic = self.assertTopics
        testTopic["others"].append(1)
        self.assertEqual(self.testQuestions.topics, testTopic)
        self.testQuestions.topics = self.assertTopics

    def test_set_topic_to_invalid_id(self):
        invalid_id = len(self.testQuestions.questions) + 1
        r = self.testQuestions.set_topic(invalid_id, "others")
        self.assertEqual(self.testQuestions.topics, self.assertTopics)
        self.assertEqual(r, "Invalid question id, choose between 1 and " + str((invalid_id - 1)))

    def test_unset_topic(self):
        id_to_unset = self.assertTopics["others"][0]
        assert_topic = self.assertTopics["others"][1:]
        r = self.testQuestions.unset_topic(id_to_unset, "others")
        self.assertEqual(self.testQuestions.topics["others"], assert_topic)
        self.assertEqual(r, f"Question {id_to_unset} removed from the topic others")

    def test_unset_invalid_topic(self):
        id_to_unset = 1
        assert_topic = "invalid_topic"
        r = self.testQuestions.unset_topic(id_to_unset, assert_topic)
        self.assertEqual(self.testQuestions.topics, self.assertTopics)

    def test_unset_invalid_id(self):
        r = self.testQuestions.unset_topic(1, "others")
        self.assertEqual(self.testQuestions.topics["others"], self.assertTopics["others"])

    def test_get_questions(self):
        r = self.testQuestions.get_questions(1)
        self.assertEqual(r, self.assertQuestions)

    def test_get_questions_bad_page(self):
        r = self.testQuestions.get_questions(99)
        self.assertEqual(r, ["No questions on this page!"])
    
    def test_get_questions_custom_number(self):
        r = self.testQuestions.get_questions(1, amount_on_page=2)
        self.assertEqual(r, self.assertQuestions[:2])
    
    def test_get_questions_amount(self):
        r = self.testQuestions.get_questions_amount()
        self.assertEqual(r, len(self.assertQuestions))


def clear_test_data():
    questions = ["First question", "Second question", "Last question"]
    topics = {"first": [1], "others": [2, 3]}
    data = {
        "questions": questions,
        "topics": topics
    }
    with open(myPath + "\\" + "test_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


if __name__ == '__main__':
    myPath = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(myPath + '\\..\\src')  # required for using from askmebot/ directory
    unittest.main(exit=False)
    clear_test_data()