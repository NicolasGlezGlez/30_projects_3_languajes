package main

import (
	"fmt"
	"time"
)

func main() {
	fmt.Println("Stopwatch started")
	counter := 0
	running := true

	go func() {
		for running {
			time.Sleep(10 * time.Millisecond) // 10 milliseconds
			counter += 100

			mins, restSecs := counter/60000, counter%60000
			secs, millis := restSecs/1000, restSecs%1000
			timeFormat := fmt.Sprintf("\rElapsed Time: %02d:%02d:%03d", mins, secs, millis)
			fmt.Print(timeFormat)
		}
	}()

	fmt.Println("\nPress 'Enter' to stop...")
	fmt.Scanln()
	running = false
	fmt.Println("\nStopwatch stopped")
}
