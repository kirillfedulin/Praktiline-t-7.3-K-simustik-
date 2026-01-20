import os
import random
import smtplib
from email.message import EmailMessage
import json
from numpy import append

def load_questions(questions_answers):
    kus_vas = {}

    if os.path.exists(questions_answers):
        with open(questions_answers, "r", encoding="utf8") as f:
            kus_vas = json.load(f)
            
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
    return name, score


def save_result(name, score, correct_answers = "oiged.json", wrong_answers = "valed.json"):
    with open(correct_answers, "w", encoding="utf-8") as f:
         f.write(json.dumps(correct_answers, ensure_ascii=False, indent=4))
         f.write(f"{name}: {score} oiget vastust\n")
    
    with open(wrong_answers, "w", encoding="utf-8") as f:
         f.write(json.dumps(wrong_answers, ensure_ascii=False, indent=4))
         f.write(f"{name}: {score} valesti vastust\n")


def send_email(score, name, email):
    email_subject = "TEST TULEMUS"
    sender_adress = "kirill.fedulin22@gmail.com"
    email_password = "???"
    email_stmp = "smtp.gmail.com"
    
    message = f"Tere {name}!\n\nSinu test tulemus: {score}/3"
    if score == 3:
        message = message + "\n\nPalju õnne! Sa sooritasid testi edukalt."
    else:
        message = message + "\n\nKui sooritasid testi edukalt, palju õnne!\n"
    
    print(message)
    
    email = EmailMessage()
    email["Subject"] = email_subject
    email["From"] = sender_adress
    email["To"] = email
    email.set_content(message)
    
    try:
        with smtplib.SMTP_SSL(email_stmp, 465) as smtp:
            smtp.login(sender_adress, email_password)
            smtp.send_message(message) 
        print(f"Email saadetud! {email}")
    except Exception as e:
        print(f"Email was not sent error{e}")


def generate_report(sender_adress, email_password, email_stmp):
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


def add_question(questions_answers):
   question = input("Sisesta uus küsimus: ")
   answer = input("Sisesta õige vastus: ")

   if question == "" or answer == "":
        print("Küsimus ja vastus ei tohi olla tühjad.")
        return
   print(f"{question}: {answer}\n")

   kus_vas = load_questions(questions_answers)
   kus_vas[question] = answer
   with open(questions_answers, "w", encoding="utf-8") as f:
         f.write(json.dumps(kus_vas, ensure_ascii=False, indent=4))

   print("Uus küsimus lisatud!")