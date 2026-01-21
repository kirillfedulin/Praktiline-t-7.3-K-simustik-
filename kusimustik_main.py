from kusimustlik_funktsioon import *

questions_answers = "kusimused_vastused.txt"
all_fn = "koik.txt"
success_fn = "oiged.txt"
fail_fn = "valed.txt"


N = 3
M = 3
tries = 0
score = 0
while True: 
    menu = input("\nVali tegevus:\n1. Alustada testi 2. Uut kusimust 3. Valja\n \nSissesta valik (1/2/3): ")
    if menu == "1":
        fullname = input_fullname()
        users = get_all_users(all_fn)
        tries = len(users)
        if fullname in users:
            print("See nimi on juba olemas! Palun sisesta teine nimi. ")
            continue
        print(tries)
        email = generation_email(fullname)
        questions = load_questions(questions_answers)
        score = take_questions(fullname, questions, N)
        passed = score > N/2
        save_result(fullname, email, score, passed, all_fn, success_fn, fail_fn)
        send_email(score, fullname, email, passed)
        
        tries += 1
        if tries >= M:
            send_report(success_fn, all_fn)
            reset_files(success_fn, fail_fn, all_fn)
            break
        
    elif menu == "2":
        add_question(questions_answers)
    elif menu == "3":
        print("Head aega!")
        break
