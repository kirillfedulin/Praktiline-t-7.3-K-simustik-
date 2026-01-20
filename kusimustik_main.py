from kusimustlik_funktsioon import *

while True:
    questions_answers = "kusimused_vastused.json"
    menu = input("\nVali tegevus:\n1. Alustada testi 2. Uut kusimust 3. Valja\n \nSissesta valik (1/2/3): ")
    if menu == "1":
        fullname = input("Palun sisestage oma nimi: ")
        email = generation_email(fullname)
        name = fullname.strip().split()[0]
        questions = load_questions(questions_answers)
        N = 3
        score = take_questions(name, questions, N)
        save_result(name, score, correct_answers = "oiged.json", wrong_answers = "valed.json")
        send_email(score, name, email)
    elif menu == "2":
        add_question(questions_answers)
    elif menu == "3":
        print("Head aega!")
        break
