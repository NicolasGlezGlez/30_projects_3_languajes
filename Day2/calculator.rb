def main
    puts "Enter the first number: "
    input1 = gets.chomp
  
    unless numeric?(input1)
      puts "That's not a valid number."
      return
    end
  
    num1 = input1.to_f
  
    puts "Enter an operator (+,-,*,/): "
    op = gets.chomp
  
    puts "Enter another number: "
    input2 = gets.chomp
  
    unless numeric?(input2)
      puts "That's not a valid number."
      return
    end
  
    num2 = input2.to_f
  
    result = perform_operation(op, num1, num2)
  
    if result == "Wrong Operator"
      puts result
    else
      puts "The result is: #{result}"
    end
  end
  
  def perform_operation(op, num1, num2)
    case op
    when "+"
      num1 + num2
    when "-"
      num1 - num2
    when "*"
      num1 * num2
    when "/"
      if num2 == 0
        "Cannot divide by zero"
      else
        num1 / num2
      end
    else
      "Wrong Operator"
    end
  end
  
  def numeric?(string)
    true if Float(string) rescue false
  end
  
main
  