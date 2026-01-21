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


def save_result(fullname, email, score, passed, all_fn, success, fail):
    
    if passed:
        results = []
        
        # read all lines
        if os.path.exists(success):
            with open(success, "r", encoding="utf-8") as f:
                for line in f:
                    if "-" in line:
                        name, sc = line.strip().split("-")
                        results.append((name, int(sc)))
                       
        # add new line and sort lines 
        results.append((fullname, score))
        results.sort(key=lambda x: x[1], reverse=True)
        #ssave lines
        with open(success, "w", encoding="utf-8") as f:
            for name, sc in results:
                f.write(f"{name}-{sc}\n")

    else:
        lines = []
        # read all lines
        if os.path.exists(fail):
            with open(fail, "r", encoding="utf-8") as f:
                lines = f.readlines()
        # add new line and sort
        lines.append(fullname + "\n")
        lines.sort()
        #save lines
        with open(fail, "w", encoding="utf-8") as f:
            for line in lines:
                f.write(line)
            
    with open(all_fn, "a", encoding="utf-8") as f:
        f.write(f"{fullname},{score},{email}\n")
 

def send_email(score, name, email, passed):
    email_subject = "TEST TULEMUS"
    sender_adress = "kirill.fedulin22@gmail.com"
    email_password = "???"
    email_stmp = "smtp.gmail.com"
    
    message = f"Tere {name}!\nSinu õigete vastuste arv: {score}"
    if passed:
        message = message + "\nSa sooritasid testi edukalt."
    else:
        message = message + "\nKahjuks testi ei sooritatud edukalt."
    
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


def send_report(success_fn, all_fn):
    sender_adress = "kirill.fedulin22@gmail.com"
    email_password = "???"
    email_stmp = "smtp.gmail.com"

    try:
        success_users = []
        if os.path.exists(success_fn):
            with open(success_fn, "r", encoding="utf-8") as f:
                success_users =  [line.split('-')[0] for line in f]
            
        result = []
        best_score = 0
        best_user = ""
        with open(all_fn, "r", encoding="utf-8") as f:
            for line in f:
                full_name, score, email = line.strip().split(",")
                msg = f"{full_name} - {score} õigesti - {email} -"
                if full_name in success_users:
                    result.append(f"{msg} - SOBIS")
                else:
                    result.append(f"{msg} - EI SOBINUD")
                if int(score) > best_score:
                    best_score = int(score)
                    best_user = full_name
                        
        
        print("\nTulemused: ")
        for r in result:
            print(r)

        body = f"""
Tere!

Tänased küsimustiku tulemused:

{"\n".join(result)}

Parim vastaja: {best_user} ({best_score} õigesti)

Lugupidamisega,  
Küsimustiku Automaatprogramm
        """
        print(body)

        message = EmailMessage()
        message["Subject"] = "TESTI RAPORT"
        message["From"] = sender_adress
        message["To"] = "tootaja@firma.ee"
        message.set_content(body)
    
        with smtplib.SMTP_SSL(email_stmp, 465) as smtp:
            smtp.login(sender_adress, email_password)
            smtp.send_message(message)  

        print("Raport saadetud!")
    except Exception as e:
        print(f"Report ei saadanud! {e}")


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
   
   
def get_all_users(all_fn): 
    results = []
    if os.path.exists(all_fn):
        with open(all_fn, "r", encoding="utf-8") as f:
            for line in f:
                results.append(line.split(",")[0])
    return results


def reset_files(*files):
    for file in files:
        try:
            os.remove(file) 
        except:
            continue
            

def input_fullname():
    while True:
        fullname = input("Palun sisestage oma nimi ja perekonnanimi: ").strip()
        parts = fullname.split()
        if len(parts) < 2:
            print("Palun sisestage nii eesnimi kui perekonnanimi!")
            continue
        return fullname

