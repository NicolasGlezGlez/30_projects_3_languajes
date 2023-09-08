<?php

function perform_operation($operator, $num1, $num2) {
    switch ($operator) {
        case "+":
            return $num1 + $num2;
        case "-":
            return $num1 - $num2;
        case "*":
            return $num1 * $num2;
        case "/":
            if ($num2 == 0) {
                return "Error: Division by zero";
            }
            return $num1 / $num2;
        default:
            return "Error: Invalid operator";
    }
}

while (true) {
    echo "Enter the first number: ";
    $num1 = trim(fgets(STDIN));
    if (!is_numeric($num1)) {
        echo "Invalid input. Please enter a number.\n";
        continue;
    }

    echo "Enter an operator (+, -, *, /): ";
    $operator = trim(fgets(STDIN));

    echo "Enter the second number: ";
    $num2 = trim(fgets(STDIN));
    if (!is_numeric($num2)) {
        echo "Invalid input. Please enter a number.\n";
        continue;
    }

    $result = perform_operation($operator, $num1, $num2);
    echo "Result: $result\n";

    echo "Would you like to perform another operation? (y/n): ";
    $continue = trim(fgets(STDIN));
    if ($continue !== 'y') {
        break;
    }
}
?>
