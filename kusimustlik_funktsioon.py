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
        for l in f:
            l = l.strip()
            if not l:
                continue
            if ":" not in l:
                print(f"Viga failis! {l}")
                continue
            q, a = l.split(":", 1)
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
        lastname = "user"
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
    return score

def sort_by_score(success="oiged.txt"):
    if not os.path.exists(success):
        return
    
    with open(success, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
        lines.sort(key=lambda x: int(x.split(":", 1)[1]), reverse=True)        
        
    with open(success, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")

        
def sort_by_name(fail="valed.txt"):
    if not os.path.exists(fail):
        return
    
    with open(fail, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    lines = [line for line in lines if ":" in line]
    lines.sort(key=lambda x: x.split(":", 1)[0])

    with open(fail, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")



def save_result(fullname, score, passed, all_fn, success, fail):
    email = generation_email(fullname)
    line = f"{fullname}:{score}\n"
    
    if passed:
        with open(success, "a", encoding="utf8") as f:
            f.write(line)
        sort_by_score(success)
    else:
        with open(fail, "a", encoding="utf8") as f:
            f.write(line)
        sort_by_name(fail)
    
    with open(all_fn, "a", encoding="utf-8") as f:
        f.write(f"{fullname}, {score}, {email}\n")
    
 

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
    
    msg = EmailMessage()
    msg["Subject"] = email_subject
    msg["From"] = sender_adress
    msg["To"] = email
    msg.set_content(message)
    
    try:
        with smtplib.SMTP_SSL(email_stmp, 465) as smtp:
            smtp.login(sender_adress, email_password)
            smtp.send_message(msg) 
        print(f"Email saadetud! {email}")
    except Exception as e:
        print(f"Email was not sent error{e}")


def send_report(success_fn, fail_fn):
    sender_adress = "kirill.fedulin22@gmail.com"
    email_password = "???"
    email_stmp = "smtp.gmail.com"
    
    best_user = ""
    best_score = -1
    
    if os.path.exists(success_fn):
        with open(success_fn, "r", encoding="utf-8") as f:
                for i, line in  enumerate(f, start=1):
                    line = line.strip()
                    if ":" not in line:
                        continue
                    if ":" not in line:
                        continue
                    fullname, score = line.split(":")
                    score = int(score)
                    print(f"{i}. {fullname} - {score} - {generation_email(fullname)} - SOBIB")
                    
                    if score > best_score:
                        best_score = score
                        best_user = fullname
                        
    if os.path.exists(fail_fn):
        with open(fail_fn, "r", encoding="utf-8") as f:
                for i, line in enumerate(f, start=1):
                    fullname, score = line.strip().split(":")
                    print(f"{i}. {fullname} - {score} - {generation_email(fullname)} - EI SOBINUD")
                    
        print(f"\nParim kasutaja: {best_user} ({best_score} oigesti!)")
    
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
   
   
   
   
def is_unique_name(fullname, all_fn):
    fullname_norm = fullname.strip().lower()
    
    if not os.path.exists(all_fn):
        return True
      
    with open(all_fn, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            parts = line.split(":")
            existing_name = parts[0].strip().lower()
            if existing_name == fullname_norm:
                return False
    return True


def reset_files(*files):
    for file in files:
        with open(file, "w", encoding="utf-8") as f:
            f.write("") 
