import os
import random
import smtplib
from email.message import EmailMessage
from numpy import append

def save_qna(filename, qna):
    with open(filename, "w", encoding="utf8") as f:
        for q, a in qna.items():
            f.write(f"{q}:{a}\n")    
    

def load_qna(filename):
    res = {}
    with open(filename, "r", encoding="utf8") as f:
        for l in f.readlines():
            q, a = l.split(":")
            res[q] = a
    return res


def load_questions(questions_answers):
    kus_vas = {}

    if os.path.exists(questions_answers):
        kus_vas = load_qna(questions_answers)
            
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


def take_questions(fullname, questions, N):
    score = 0
    print(f"\nTere {fullname}! Vasta palun kusimustele!\n")
    all_questions = list(questions.items())
    random.shuffle(all_questions)       
    selected_questions = all_questions[:N]  
    for question, correct_answer in selected_questions:
        user_answer = input(f"{question} ")
        if user_answer.strip().lower() == correct_answer.strip().lower():            
            score += 1
    return fullname, score


def save_result(name, score, passed, all_fn, success, fail):
    if passed:
        with open(success, "w", encoding="utf8") as f:
            f.write(f"{name}:{score}\n").sort(score)
    else:
        with open(fail, "w", encoding="utf8") as f:
            f.write(f"{name}:{score}\n").sort(name)
    
    with open(all_fn, "w", encoding="utf-8") as f:
        f.write(name, score, generation_email())
    
 

def send_email(score, name, email, passed):
    email_subject = "TEST TULEMUS"
    sender_adress = "kirill.fedulin22@gmail.com"
    email_password = "???"
    email_stmp = "smtp.gmail.com"
    
    message = f"Tere {name}!\n\nSinu test tulemus: {score}/3"
    if passed:
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


def send_report(success_fn, fail_fn, all_fn):
    sender_adress = "kirill.fedulin22@gmail.com"
    email_password = "???"
    email_stmp = "smtp.gmail.com"
    
    best_user = ""
    fullnames = []
    answer = []
    
    if os.path.exists(success_fn):
        with open(success_fn, "r", encoding="utf-8") as f:
            first_line = f.readline().strip()
            if first_line:
                best_user = first_line
                
    if os.path.exists(all_fn):
        with open(all_fn, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split(",")
                    fullname = parts[0] + " " + parts[1]
                    fullnames.append(fullname)
                    
    if os.path.exists(success_fn):
        with open(success_fn, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split(":")
                    answer.append(parts[1])
                    
    if os.path.exists(fail_fn):
        with open(fail_fn, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    parts = line.split(":")
                    answer.append(parts[1]) 
                    
    if fullnames in success_fn:
            for i, in enumerate(starts=1):
                print(f"{i}. {fullnames} - {answer} oigesti - {generation_email} - SOBIS")
    else:
            for i, in enumerate(starts=1):
                print(f"{i}. {fullnames} - {answer} oigesti - {generation_email} - EI SOBINUD")
    
    print(f"Parim kasutaja: {best_user} ({answer} oigesti)")
    
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
   save_qna(questions_answers, kus_vas)
   print("Uus küsimus lisatud!")