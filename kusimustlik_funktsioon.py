import os
import random
import smtplib
from email.message import EmailMessage



def load_questions(questions_answers="kusimused_vastused.txt"):
    kus_vas = {}

    if not os.path.exists(questions_answers):
        return kus_vas

    with open(questions_answers, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            if ":" in line:
                question, answer = line.split(":", 1)
                kus_vas[question.strip()] = answer.strip()

    return kus_vas



def generation_email(fullname):
    parts = fullname.strip().split()
    if len(parts) >= 2:
        firstname, lastname = parts[0].lower(), parts[-1].lower()
    else:
        firstname = parts[0].lower()
        while True:
            lastname = input("Palun sisestage oma perekonnanimi: ").strip().lower()
            if lastname:
                break
    return f"{firstname}.{lastname}@example.com"



def take_questions(name, questions, N):
    print(f"\nTere {name}! Vasta palun kusimustele!\n")
    all_questions = list(questions.items())
    random.shuffle(all_questions)       
    selected_questions = all_questions[:N]
    score = 0
    for question, correct_answer in selected_questions:
        user_answer = input(f"{question} ")
        if user_answer.strip().lower() == correct_answer.strip().lower():
            score += 1
    return score


def save_result(correct_answers, wrong_answers):
    with open("oiged.txt", "w", encoding="utf8") as f:
       for name, score in correct_answers:
           f.write(f"{name}: {score} oiget vastust\n")
    
    with open("valed.txt", "w", encoding="utf8") as f:
       for name, score in wrong_answers:
           f.write(f"{name}: {score} valesti vastust\n")



def send_email(email_subject, sender_adress, email_password, email_stmp, score, name):
    email_subject = "TEST TULEMUS"
    sender_adress = "kirill.fedulin22@gmail.com"
    email_passwrod = "mbec buaz lxco hkpk"
    email_stmp = "smtp.gmail.com"
    
    if score == 3:
        print(f"Tere {name} !")
        print(f"Sinu õigete vastuste arv: {score}")
        print("Sa sooritasid testi edukalt!")
    else:
        print(f"Tere {name} !")
        print(f"Sinu õigete vastuste arv: {score}")
        print("Kahjuks testi ei sooritatud edukalt.")
    
    message = EmailMessage()
    message["Subject"] = email_subject
    message["From"] = sender_adress
    message["To"] = generation_email(name)
    if score == 3:
        message.set_content(f"Tere {name}!\n\nSinu test tulemus: {score}/3\n\nPalju õnne! Sa sooritasid testi edukalt.")
    else:
        message.set_content(f"Tere {name}!\n\nSinu test tulemus: {score}/3\n\nKui sooritasid testi edukalt, palju õnne!\n")
    
    with smtplib.SMTP_SSL(email_stmp, 465) as smtp:
        smtp.login(sender_adress, email_passwrod)
        smtp.send_message(message) 
    print("Email saadetud!")



def generate_report(sendr_adress, email_password, email_stmp):
    sender_adress = "kirill.fedulin22@gmail.com"
    email_password = "mbec buaz lxco hkpk"
    email_stmp = "smtp.gmail.com"
    
    best_user = ""
    
    if os.path.exists("oiged.txt"):
        with open("oiged.txt", "r", encoding="utf-8") as f:
            first_line = f.readline().strip()
            if first_line:
                best_user = first_line
    
    message = EmailMessage()
    message["Subject"] = "TESTI RAPORT"
    message["From"] = sender_adress
    message["To"] = "tootaja@firma.ee"
    message.set_content(f"Parim kasutaja: \n{best_user}")
    
    with smtplib.SMTP_SSL(email_stmp, 465) as smtp:
        smtp.login(sender_adress, email_password)
        smtp.send_message(message)  

    print("Raport saadetud!")


def add_question(questions_file="kusimused.txt", answers_file="vastused.txt"):
    new_question = input("Sisesta uus küsimus: ").strip()
    new_answer = input("Sisesta õige vastus: ").strip()
    
    with open(questions_file, "a", encoding="utf8") as q_file, open(answers_file, "a", encoding="utf8") as a_file:
        q_file.write(new_question + "\n")
        a_file.write(new_answer + "\n")
    
    print("Uus küsimus ja vastus on lisatud.")

    
    