<?php

function playGame() {
    $numberToGuess = rand(0, 10);
    $livesRemaining = 3;
    echo "You have " . $livesRemaining . " lives. Good luck!\n";

    while($livesRemaining > 0) {
        echo "Enter a number: ";
        $num = (int)trim(fgets(STDIN));
        
        if ($num == $numberToGuess) {
            echo "You won!\n";
            break;
        }

        $livesRemaining--;

        if ($livesRemaining == 0) {
            echo "Sorry. You lose!\n";
            break;
        }

        echo "Try again! You have " . $livesRemaining . " lives remaining.\n";
    }
}

playGame();

?>
