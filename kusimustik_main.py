from kusimustlik_funktsioon import *

while True:
    menu = input("\nVali tegevus:\n1. Alustada testi 2. Uut kusimust 3. Valja\n \nSissesta valik (1/2/3): ")
    if menu == "1":
        fullname = input("Palun sisestage oma nimi: ")
        email = generation_email(fullname)
        name = fullname.strip().split()[0]
        questions = load_questions("kusimused.txt", "vastused.txt")
        N = 3
        score = take_questions(name, questions, N)
        send_email("", "", "", "", score, name)
    elif menu == "2":
        add_question("kusimused.txt", "vastused.txt")
    elif menu == "3":
        print("Head aega!")
        break
