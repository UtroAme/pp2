def guess(num,randomNum,trys=1):
    if num == randomNum:
        print(f"Good job, {name}! You guessed my number in {trys} guesses!")
        return
    else:
        if num > randomNum:
            print("Your guess is too hight")
        else:
            print("Your guess is too low")

        print("Take a guess.")
        num = int(input())
        trys += 1

        guess(num, randomNum,trys)