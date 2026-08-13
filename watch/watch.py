match_in = input("Enter your text: ").strip().lower()


match match_in:
    case "slytherin":
        print("You have slytherin..You are going to be a great wizard but may not be a good person.")
    case "gryffindor":
        print("You have gryffindor..You are brave and courageous.")
    case "hufflepuff":
        print("You have hufflepuff..You are loyal and hardworking.")
    case "ravenclaw":
        print("You have ravenclaw..You are intelligent and wise.")
    case _:
        print("You have entered an invalid house name.")