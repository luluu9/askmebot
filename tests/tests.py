import unittest
import sys, os


class TestQuestions(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestQuestions, self).__init__(*args, **kwargs)
        import askme
        self.testQuestions = askme.Questions(myPath + "\\" + "test_data.json")

    def test_data_import(self):
        q = self.testQuestions.questions
        self.assertEqual(q[0], "First question")
        self.assertEqual(q[-1], "Last question")


if __name__ == '__main__':
    myPath = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(myPath + '\\..\\src')  # required for using from askmebot/ directory
    unittest.main()