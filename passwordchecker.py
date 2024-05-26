import threading
import requests
import hashlib
import tkinter as tk
from tkinter import messagebox, ttk

# Global variable for the password entry field

password_entry = None

def requests_api_data(query_string):
	"""
    Function to request data from the API.
    query_string: The first 5 characters of the SHA-1 hashed password.
    Returns the response from the API.
    """
	url = 'https://api.pwnedpasswords.com/range/' + query_string
	try:
		res = requests.get(url)
		# If the request was not successful, raise an error:
		if res.status_code != 200:
			raise RuntimeError(f'Error fetching: {res.status_code}, check the api and try again.')
		return res
	except Exception as e:
		messagebox.showerror("Error", f"An error occurred: {str(e)}")

def get_password_leaks_count(hashes, hash_to_check):
	"""
    Function to get the count of password leaks.
    hashes: The response from the API.
    hash_to_check: The rest of the SHA-1 hashed password.
    Returns the count of password leaks.
    """
	# Split the response into lines and then split each line into hash and count:
	hashes = (line.split(':') for line in hashes.text.splitlines())
	# Iterate over the hashes, if the hash matches the one we're checking, return the count
	for h, count in hashes:
		if h == hash_to_check:
			return count
	return 0

def pwned_api_check(password):
	"""
    Function to check if a password has been hacked.
    password: The password to check.
    Returns the count of password leaks.
    """
	# Hash the password using SHA-1
	sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
	# Split the hash into the first 5 characters and the rest
	first5_char, tail = sha1password[:5], sha1password[5:]
	# Request data from the API using the first 5 characters of the hash
	response = requests_api_data(first5_char)
	# Get the count of password leaks using the response and the rest of the hash
	return get_password_leaks_count(response, tail)

def check_password():
	"""
	Check the strength of a password using the Have I Been Pwned API.

	This function gets the password from the entry field, starts a new thread 
	to run the callback function, which calls the `pwned_api_check` function to 
	check if the password has been compromised. Finally, it displays a message 
	box with the result.

	Args:
		None

	Returns:
		None
	"""
	# Get the password from the entry field
	password = password_entry.get()
	# If the password is empty, show an error message
	if not password:
		messagebox.showerror("Error", "Password cannot be empty.")
		return

	# Disable the check button and set the status label to "Checking..."
	check_button.config(state=tk.DISABLED)
	status_label.config(text="Checking...")

	def callback():
		count = pwned_api_check(password)
		password_entry.delete(0, 'end')  # Clear the password variable
		if count:
			messagebox.showinfo("Password Check", f'Your password was found {count} times... You should probably change your password!')
		else:
			messagebox.showinfo("Password Check", 'Your password was NOT found. Carry on!')
		check_button.config(state=tk.NORMAL)  # Enable the check button
		status_label.config(text="")  # clear the status label

	threading.Thread(target=callback).start()  # Start a new thread to run the callback function

# Create the GUI
root = tk.Tk()
root.title("Password Checker")

frame = tk.Frame(root)
frame.pack(padx = 20, pady = 20)

label = tk.Label(frame, text = "Enter your password:")
label.grid(row = 0, column = 0)

password_entry = tk.Entry(frame, show = "*")
password_entry.grid(row = 0, column = 1)

check_button = tk.Button(frame, text = "Check Password", command = check_password)
check_button.grid(row = 1, column = 0, columnspan = 2)

progress_bar = ttk.Progressbar(frame, mode = 'indeterminate')
progress_bar.grid(row = 3, column = 0, columnspan = 2)

def start_progress():
	progress_bar.start()

def stop_progress():
	progress_bar.stop()
	progress_bar['value'] = 100

check_button.config(command = lambda: [start_progress(), check_password(), stop_progress()])

status_label = tk.Label(frame, text = "")
status_label.grid(row = 2, column = 0, columnspan = 2)

root.mainloop()