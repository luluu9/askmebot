import unittest
import sys, os
import json


class TestQuestions(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestQuestions, self).__init__(*args, **kwargs)
        import askme
        self.testQuestions = askme.Questions(myPath + "\\" + "test_data.json")
        self.assertQuestions = ["First question", "Second question", "Last question"]
    
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
        q =  self.testQuestions.get_question(question_id=1)
        self.assertIn(q, self.assertQuestions[0])

    # TODO
    # def test_get_question_by_topic(self):

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

    def test_remove_question_bad_id(self):
        bad_id = len(self.testQuestions.questions) + 1
        r = self.testQuestions.remove_question(bad_id)
        self.assertEqual(r, "Bad id to remove: " + str(bad_id))
    
    # TODO
    # def test_remove_question_check_topics(self):

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
    topics = {}
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