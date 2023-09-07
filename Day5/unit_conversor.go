package main

import (
	"fmt"
)

func displayCategories(categories map[string]string) string {
	fmt.Println("Please select a category:")
	for key, value := range categories {
		fmt.Println(key, ".", value)
	}
	fmt.Print("\nYour choice: ")
	var choice string
	fmt.Scanln(&choice)
	return choice
}

func displayUnits(units map[string][]string, chosenCategory string) int {
	fmt.Printf("\nYou have chosen %s. Please select a unit:\n", chosenCategory)
	for i, unit := range units[chosenCategory] {
		fmt.Println(i+1, ".", unit)
	}
	fmt.Print("\nYour choice: ")
	var choice int
	fmt.Scan(&choice)
	return choice
}

func getConversionValue(fromUnit, toUnit string, value float64) float64 {
	conversionFactors := map[string]map[string]float64{
		// Length
		"Meter (m)": {
			"Kilometer (km)": 0.001,
			"Centimeter (cm)": 100,
			"Millimeter (mm)": 1000,
			"Inch (in)": 39.3701,
			"Foot (ft)": 3.28084,
			"Yard (yd)": 1.09361,
			"Mile (mi)": 0.000621371,
		},
		"Kilometer (km)": {"Meter (m)": 1000},
		"Centimeter (cm)": {"Meter (m)": 0.01},

		// Mass
		"Kilogram (kg)": {
			"Gram (g)": 1000,
			"Milligram (mg)": 1000000,
			"Pound (lb)": 2.20462,
			"Ounce (oz)": 35.274,
		},
		"Gram (g)": {
			"Kilogram (kg)": 0.001,
			"Milligram (mg)": 1000,
		},

		// Time - (ToDo)

		// Temperature - (ToDo)

		// Area
		"Square meter (m²)": {
			"Square kilometer (km²)": 0.000001,
			"Square centimeter (cm²)": 10000,
		},
		"Square kilometer (km²)": {"Square meter (m²)": 1000000},

		// Volume
		"Liter (L)": {
			"Milliliter (mL)": 1000,
			"Cubic meter (m³)": 0.001,
			"Gallon (gal)": 0.264172,
			"Pint (pt)": 2.11338,
		},
		"Milliliter (mL)": {"Liter (L)": 0.001},

		// Speed
		"Meter per second (m/s)": {
			"Kilometer per hour (km/h)": 3.6,
			"Mile per hour (mph)": 2.23694,
		},
		"Kilometer per hour (km/h)": {"Meter per second (m/s)": 0.277778},

		// Currency, Energy, and Pressure (ToDo)
	}

	if factor, ok := conversionFactors[fromUnit][toUnit]; ok {
		return value * factor
	}
	return -1
}


func main() {
	categories := map[string]string{
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

	units := map[string][]string{
		"Length":       {"Meter (m)", "Kilometer (km)", "Centimeter (cm)", "Millimeter (mm)", "Inch (in)", "Foot (ft)", "Yard (yd)", "Mile (mi)"},
		"Mass":        {"Kilogram (kg)", "Gram (g)", "Milligram (mg)", "Ton (t)", "Pound (lb)", "Ounce (oz)"},
		"Time":        {"Second (s)", "Minute (min)", "Hour (hr)", "Day (d)"},
		"Temperature": {"Celsius (°C)", "Fahrenheit (°F)", "Kelvin (K)"},
		"Area":        {"Square meter (m²)", "Square kilometer (km²)", "Square centimeter (cm²)", "Acre (ac)", "Hectare (ha)"},
		"Volume":      {"Liter (L)", "Milliliter (mL)", "Cubic meter (m³)", "Gallon (gal)", "Pint (pt)"},
		"Speed":       {"Meter per second (m/s)", "Kilometer per hour (km/h)", "Mile per hour (mph)"},
		"Currency":    {"Dollar (USD)", "Euro (EUR)", "Pound Sterling (GBP)", "Yen (JPY)"},
		"Energy":      {"Joule (J)", "Calorie (cal)", "Kilojoule (kJ)", "Kilocalorie (kcal)"},
		"Pressure":    {"Pascal (Pa)", "Kilopascal (kPa)", "Megapascal (MPa)", "Bar (bar)", "Atmosphere (atm)"},
	}

	chosenCategoryKey := displayCategories(categories)
	chosenCategory, ok := categories[chosenCategoryKey]
	if !ok {
		fmt.Println("Invalid choice. Program terminated.")
		return
	}

	chosenUnitIndex := displayUnits(units, chosenCategory) - 1
	if chosenUnitIndex < 0 || chosenUnitIndex >= len(units[chosenCategory]) {
		fmt.Println("Invalid choice. Program terminated.")
		return
	}
	chosenUnit := units[chosenCategory][chosenUnitIndex]

	toUnitIndex := displayUnits(units, chosenCategory) - 1
	if toUnitIndex < 0 || toUnitIndex >= len(units[chosenCategory]) {
		fmt.Println("Invalid choice. Program terminated.")
		return
	}
	toUnit := units[chosenCategory][toUnitIndex]

	var value float64
	fmt.Printf("\nPlease enter the value you want to convert from %s to %s: ", chosenUnit, toUnit)
	fmt.Scan(&value)

	convertedValue := getConversionValue(chosenUnit, toUnit, value)
	if convertedValue == -1 {
		fmt.Println("Sorry, this conversion is not supported in this program.")
	} else {
		fmt.Printf("\n%.2f %s is equal to %.2f %s\n", value, chosenUnit, convertedValue, toUnit)
	}
}
