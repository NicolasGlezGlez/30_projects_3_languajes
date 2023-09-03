package main

import (
	"fmt"
	"errors"
)

func perform_operation(op string, num1 float64, num2 float64) (float64, error) {
	switch op {
	case "+":
		return num1 + num2, nil
	case "-":
		return num1 - num2, nil
	case "*":
		return num1 * num2, nil
	case "/":
		if num2 == 0 {
			return 0, errors.New("Cannot divide by zero")
		}
		return num1 / num2, nil
	default:
		return 0, errors.New("Invalid operator")
	}
}

func main()  {
	fmt.Println("Enter the first number: ")
	var num1 float64
    fmt.Scanln(&num1)

	fmt.Println("Enter an operator (+, -, *, /): ")
	var op string
	fmt.Scanln(&op)

	fmt.Println("Enter the second number: ")
	var num2 float64
	fmt.Scanln(&num2)

	result, err := perform_operation(op,float64(num1),float64(num2))

	if err != nil {
		fmt.Println("Error: ", err)
	}else{
		fmt.Println("Result: ", result)
	}

	
}