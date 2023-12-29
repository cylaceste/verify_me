from verify_me_db.database import Database


def add_initial_users(db: Database):
    db.add_entry('users', (111, 'Chieko', '1234-05-06', 'lacestec@gmail.com', 101))
    db.add_entry('users', (112, 'Bob Smith', '1985-09-23', 'bob@example.com', 102))
    db.add_entry('images', (101, 'https://example.com/chieko.jpg'))
    db.add_entry('images', (102, 'https://example.com/bob.jpg'))


def create_database():
    return Database()


def run_airport_scenario(db: Database):
    '''
    Run through a scenario where I use verify_me to print a boarding pass, sit at a bar, and board an airplane.
    '''
    print(f"I, Chieko, arrive at the airport and head to my airline's help desk to print a boarding pass\n."
          f"'Hi, please give me your passport'. Says the cs agent. 'I forgot my passport but I have verify_me', "
          f"I say. I open the verify_me app and select 'Flight' and click 'Generate Verification'. \n'My code is: ",
          end='')

    print_boarding_pass_verification = db.generate_verification(111, 'Flight')

    print(f"{print_boarding_pass_verification}'.\n The cs agent scans my code and it pulls up the following "
          f"information: \n\n{db.get_verification(print_boarding_pass_verification)}\n\n'Cool beans, the photo matches "
          f"and also I was able to find your flight. Here's your boarding pass!")

    print(f"I sit down at an airport bar for a snack and the waiter asks to see if my ID. I feel apprehensive about "
          f"giving people my real name when they don't need it, so I use the verify_me app, which only exposes "
          f"whether I'm of drinking age or not. 'Here is my verify_me code: ", end='')

    bar_verification = db.generate_verification(111, 'Bar')

    print(f"{bar_verification}'. The waiter scans my code and gets the following information:"
          f"\n\n{db.get_verification(bar_verification)}\n\n 'Cool beans, the photo matches and it says you're of "
          f"drinking age.")

    print(f"My flight arrives and I try to board with the same verification code from earlier but it's "
          f"expired (NOT IMPLEMENTED). So I generate a new one: ", end='')

    boarding_verification = db.generate_verification(111, 'Flight')

    print(f"{boarding_verification}. This ID works and the boarding agent sees: "
          f"\n\n{db.get_verification(bar_verification)}, compares the photo against my face, and my name against the "
          f"boarding pass.")


def main():
    db = create_database()
    add_initial_users(db)
    run_airport_scenario(db)


if __name__ == "__main__":
    main()
