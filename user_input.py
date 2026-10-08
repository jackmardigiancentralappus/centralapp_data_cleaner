def ask_choice(question, choices, default=None):
    while True:
        answer = input(question).strip().lower() or default
        if answer in choices:
            return answer
        print(f"  Please enter one of: {', '.join(choices)}")

def ask_yes_no(question, default="y"):
    return ask_choice(question, ["y", "n"], default) == "y"

def ask_number(question, minimum=1, maximum=None, default=None):
    while True:
        answer = input(question).strip() or default
        if answer is not None and str(answer).isdigit():
            number = int(answer)
            if number >= minimum and (maximum is None or number <= maximum):
                return number
        print("  Please enter a valid number.")

def ask_text(question, default=None):

    answer = input(question).strip() or default
    confirmation = ask_choice(f"Please confirm {answer} is correct (Y/N)", ["y", "n"])
    if confirmation == "y":
        return answer
    else:
        final_answer = ask_text(question, default)
        return final_answer

