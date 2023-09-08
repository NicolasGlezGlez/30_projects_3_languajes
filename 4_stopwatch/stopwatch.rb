def main
    puts "Stopwatch started (Press Enter to stop)"
    counter = 0
    running = true
  
    # Thread for the stopwatch
    timer_thread = Thread.new do
      while running
        sleep(0.01)
        counter += 100
  
        mins, restSecs = counter.divmod(60000)
        secs, millis = restSecs.divmod(1000)
        time_format = format("Elapsed Time: %02d:%02d:%03d", mins, secs, millis)
  
        print "\r#{time_format}"
      end
    end
  
    # Thread to wait for user input
    input_thread = Thread.new do
      gets
      running = false
    end
  
    # Wait for both threads to complete
    timer_thread.join
    input_thread.join
  
    puts "\nStopwatch stopped."
  end
  
main  # Call the main function to start the game
  