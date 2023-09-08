def display_categories(categories):
    print("Please select a category:")
    for key, value in categories.items():
        print(f"{key}. {value}")
    return input("\nYour choice: ")

def display_units(units, chosen_category):
    print(f"\nYou have chosen {chosen_category}. Please select a unit:")
    for index, unit in enumerate(units[chosen_category], 1):
        print(f"{index}. {unit}")
    return input("\nYour choice: ")

def get_conversion_value(from_unit, to_unit, value):
    # Conversion logic will go here
    conversion_factors = {
        ("Meter (m)", "Kilometer (km)"): 0.001,
        ("Kilometer (km)", "Meter (m)"): 1000,
        ("Centimeter (cm)", "Meter (m)"): 0.01,
        ("Meter (m)", "Centimeter (cm)"): 100,
        # You can add more conversion factors here
    }

    factor = conversion_factors.get((from_unit, to_unit))
    if factor is not None:
        return value * factor
    else:
        return "Conversion not supported"

def main():
    categories = {
        "1": "Length",
        "2": "Mass",
        "3": "Time",
        "4": "Temperature",
        "5": "Area",
        "6": "Volume",
        "7": "Speed",
        "8": "Currency",
        "9": "Energy",
        "10": "Pressure",
    }

    units = {
        "Length": ["Meter (m)", "Kilometer (km)", "Centimeter (cm)", "Millimeter (mm)", "Inch (in)", "Foot (ft)", "Yard (yd)", "Mile (mi)"],
        "Mass": ["Kilogram (kg)", "Gram (g)", "Milligram (mg)", "Ton (t)", "Pound (lb)", "Ounce (oz)"],
        "Time": ["Second (s)", "Minute (min)", "Hour (hr)", "Day (d)"],
        "Temperature": ["Celsius (°C)", "Fahrenheit (°F)", "Kelvin (K)"],
        "Area": ["Square meter (m²)", "Square kilometer (km²)", "Square centimeter (cm²)", "Acre (ac)", "Hectare (ha)"],
        "Volume": ["Liter (L)", "Milliliter (mL)", "Cubic meter (m³)", "Gallon (gal)", "Pint (pt)"],
        "Speed": ["Meter per second (m/s)", "Kilometer per hour (km/h)", "Mile per hour (mph)"],
        "Currency": ["Dollar (USD)", "Euro (EUR)", "Pound Sterling (GBP)", "Yen (JPY)"],
        "Energy": ["Joule (J)", "Calorie (cal)", "Kilojoule (kJ)", "Kilocalorie (kcal)"],
        "Pressure": ["Pascal (Pa)", "Kilopascal (kPa)", "Megapascal (MPa)", "Bar (bar)", "Atmosphere (atm)"]
    }

    # Display categories and get user's choice
    chosen_category_key = display_categories(categories)
    chosen_category = categories.get(chosen_category_key, "Invalid choice")

    if chosen_category == "Invalid choice":
        print("Invalid choice. Program terminated.")
        return

    # Display units for the chosen category and get user's choice
    chosen_unit_index = display_units(units, chosen_category)
    chosen_unit = units[chosen_category][int(chosen_unit_index) - 1] if 0 < int(chosen_unit_index) <= len(units[chosen_category]) else "Invalid choice"

    if chosen_unit == "Invalid choice":
        print("Invalid choice. Program terminated.")
        return

    # Continue with the logic to perform unit conversion
    to_unit_index = display_units(units, chosen_category)
    to_unit = units[chosen_category][int(to_unit_index) - 1] if 0 < int(to_unit_index) <= len(units[chosen_category]) else "Invalid choice"

    if to_unit == "Invalid choice":
        print("Invalid choice. Program terminated.")
        return

    # Get the value the user wants to convert
    value = float(input(f"\nPlease enter the value you want to convert from {chosen_unit} to {to_unit}: "))

    # Perform the conversion
    converted_value = get_conversion_value(chosen_unit, to_unit, value)

    if converted_value == "Conversion not supported":
        print("Sorry, this conversion is not supported in this program.")
    else:
        print(f"\n{value} {chosen_unit} is equal to {converted_value} {to_unit}")

if __name__ == "__main__":
    main()
