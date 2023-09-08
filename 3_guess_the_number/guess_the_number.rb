def main
    lives_remaining = 3
    number_to_guess = rand(0..10)
  
    puts "Secret number generated. Guess it!"
  
    while lives_remaining > 0
      puts "#{lives_remaining} lives remaining"
      puts "Enter a number: "
      num = gets.chomp.to_i  # Convert input to integer
  
      if num == number_to_guess
        puts "You've won!"
        break
      else
        puts "Incorrect. Try again."
        lives_remaining -= 1
      end
    end
  
    if lives_remaining == 0
      puts "You've lost. The number was #{number_to_guess}."
    end
  end
  
main  # Call the main function to start the game
  