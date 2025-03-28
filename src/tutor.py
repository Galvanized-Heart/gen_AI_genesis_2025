from utils import make_persistent
from helper import Helper
from quiz import Quiz
from concept import Concept


class Tutor:
    helper: Helper
    quizzer: Quiz
    summary_path: str
    concepts_path: str
    document_path: str

    def __init__(self, summary_path, concepts_path, document_path, language):
        self.language = language
        summary_prompt = f"Summarize the following content into easy to follow core concepts in {language}"
        concepts_prompt = f"Extract the core concepts and list the names of the concepts each on a new line in {language}"
        self.summary_path = make_persistent(summary_prompt, document_path, summary_path)
        self.concepts_path = make_persistent(concepts_prompt, document_path, concepts_path)
        self.concepts = []

        try:
            with open(self.concepts_path, "r") as f:
                con_names = f.readlines()
                for i in range(len(con_names)):
                    con_names[i] = con_names[i].strip()
                    self.concepts.append(Concept(con_names[i], self.summary_path))
        except FileNotFoundError:
            print(f"Error: Concepts file not found at {self.concepts_path}")
            self.concepts = []

    def user_question(self, question_prompt):
        # Asks tutor agent a clarification question in helper mode
        self.helper = Helper(self.summary_path, language=self.language)
        return self.helper.get_advice(question_prompt)

    def make_quiz(self):
        self.quiz = Quiz(self.concepts)

    def get_quiz_questions(self, num=5):
        return self.quiz.choose_ques(num)

    def check_quiz_answers(self, answers):
        return self.quiz.check_answers(answers)

    def print_summary(self):
        try:
            with open(self.summary_path, 'r') as f:
                print(f.read())
        except FileNotFoundError:
            print(f"Error: Summary file not found at {self.summary_path}")

    def print_concepts(self):
        try:
            with open(self.concepts_path, 'r') as f:
                print(f.read())
        except FileNotFoundError:
            print(f"Error: Concepts file not found at {self.concepts_path}")
