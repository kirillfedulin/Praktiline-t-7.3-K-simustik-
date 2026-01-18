import os

def load_questions(questions_file="kusimused.txt", answers_file="vastused.txt"):
    kus_vas = {}
    if not os.path.exists(questions_file) or not os.path.exists(answers_file):
        return kus_vas
    
    with open(questions_file, encoding="utf8") as file_questions, open(answers_file, encoding="utf8") as file_answers:
        questions = [line.strip() for line in file_questions if line.strip()]
        answers - [line.strip() for line in file_answers if line.strip()]

    if len(question) != len(answers):
        print("kusimuste ja vastuse arv ei uhti!")
        min_len = min(len(questions), len(answers))
        question = question[:min_len]
        answers = answers[:min_len]

    kus_vas = dict(zip(questions, answers))
    return kus_vas