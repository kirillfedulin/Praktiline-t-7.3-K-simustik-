import os

def load_questions(question_file="kusimused.txt", answer_file="vastused.txt"):
    kus_vas = {}
    if not os.path.exsist(question_file) or not os.path.exsist(answer_file)
        return kus_vas
    
    with open(question_file, encoding="utf8") as file_question, open(answer_file, encoding="utf8") as file_answer:
        