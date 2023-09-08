package main

import (
	"fmt"
	"math/rand"
)

func play_game(lives_remaining int)(bool, error)  {
	var number_to_guess int = rand.Intn(10)
	println("You have ", lives_remaining, " lives. Good luck!")
	for lives_remaining > 0{
		println("Enter the number: ")
		var num int
		_, err := fmt.Scanln(&num)
		if err != nil {
			println("That's not a valid number! Please try again.")
			continue // Skip the rest of the loop and start from the beginning
		}

		if num == number_to_guess {
			println("You won!")
			
			return true, nil
		}
		lives_remaining -= 1
		if lives_remaining == 0 {
			print("Sorry. You lose!")
			break
		}
        print("Try again! You have ", lives_remaining, " lives remaining.")
	}
	return false, nil

}

func main(){
	var lives_remaining int = 3
    play_game(lives_remaining)
}