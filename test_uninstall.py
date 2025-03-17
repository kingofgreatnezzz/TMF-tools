import time
import os

# File to save countdown state
countdown_file = "countdown_state.txt"

# The file you want to delete
file_to_delete = "C:\Users\king\Downloads\wallpae"  
# Function to read the remaining countdown time from a file
def read_countdown():
    if os.path.exists(countdown_file):
        with open(countdown_file, "r") as f:
            return int(f.read().strip())
    else:
        # 28 days in seconds
        return 28 * 24 * 60 * 60

# Function to save the remaining countdown time to a file
def save_countdown(countdown):
    with open(countdown_file, "w") as f:
        f.write(str(countdown))

# Countdown loop
countdown_seconds = read_countdown()

print("Starting the countdown...")

while countdown_seconds > 0:
    days_left = countdown_seconds // (24 * 60 * 60)
    hours_left = (countdown_seconds % (24 * 60 * 60)) // 3600
    minutes_left = (countdown_seconds % 3600) // 60
    seconds_left = countdown_seconds % 60
    print(f"Time left: {days_left} days, {hours_left} hours, {minutes_left} minutes, {seconds_left} seconds", end="\r")
    time.sleep(1)

    countdown_seconds -= 1
    save_countdown(countdown_seconds)

# Delete the file after countdown
print("\nTime's up! Deleting the file...")

if os.path.exists(file_to_delete):
    os.remove(file_to_delete)
    print(f"File {file_to_delete} has been deleted successfully.")
else:
    print(f"File {file_to_delete} does not exist.")

# Clean up by deleting the countdown file after completion (optional)
os.remove(countdown_file)
