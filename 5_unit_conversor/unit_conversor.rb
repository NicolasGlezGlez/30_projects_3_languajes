def display_categories(categories)
    puts "Please select a category:"
    categories.each do |key, value|
      puts "#{key}. #{value}"
    end
    gets.chomp
  end
  
  def display_units(units, chosen_category)
    puts "\nYou have chosen #{chosen_category}. Please select a unit:"
    units[chosen_category].each_with_index do |unit, index|
      puts "#{index + 1}. #{unit}"
    end
    gets.chomp.to_i
  end
  
  def get_conversion_value(from_unit, to_unit, value)
    conversion_factors = {
      "Meter (m)" => {
        "Kilometer (km)" => 0.001,
        "Centimeter (cm)" => 100,
        "Millimeter (mm)" => 1000,
        "Inch (in)" => 39.3701,
        "Foot (ft)" => 3.28084,
        "Yard (yd)" => 1.09361,
        "Mile (mi)" => 0.000621371
      },
      "Kilogram (kg)" => {
        "Gram (g)" => 1000,
        "Milligram (mg)" => 1000000,
        "Pound (lb)" => 2.20462,
        "Ounce (oz)" => 35.274
      },
      # ... (include more conversion factors ToDo)
    }
  
    factor = conversion_factors.dig(from_unit, to_unit)
    return value * factor if factor
    -1  # return -1 if conversion not found
  end
  
  def main
    categories = {
      "1" => "Length",
      "2" => "Mass",
      # ... (include other categories ToDo)
    }
  
    units = {
      "Length" => ["Meter (m)", "Kilometer (km)", "Centimeter (cm)", "Millimeter (mm)"],
      "Mass" => ["Kilogram (kg)", "Gram (g)", "Milligram (mg)", "Pound (lb)"],
      # ... (include units for other categories ToDo)
    }
  
    chosen_category_key = display_categories(categories)
    chosen_category = categories[chosen_category_key]
  
    chosen_unit_index = display_units(units, chosen_category)
    chosen_unit = units[chosen_category][chosen_unit_index - 1]
  
    puts "\nYou have chosen #{chosen_unit}. Select another unit to convert to:"
    to_unit_index = display_units(units, chosen_category)
    to_unit = units[chosen_category][to_unit_index - 1]
  
    print "\nPlease enter the value you want to convert: "
    value = gets.chomp.to_f
  
    converted_value = get_conversion_value(chosen_unit, to_unit, value)
  
    if converted_value == -1
      puts "Sorry, this conversion is not supported in this program."
    else
      puts "\n#{value} #{chosen_unit} is equal to #{converted_value} #{to_unit}"
    end
  end
  
  main
  