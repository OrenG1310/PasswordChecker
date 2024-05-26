import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from utils import generate_password, calculate_strength

class PasswordCheckerGUI:
    def __init__(self, check_password_func):
        self.root = ThemedTk(theme = "arc")
        self.root.title("Password Checker")
        self.root.bind("<Return>", self.start_check) # Bind the Enter key to the start_check method

        frame = tk.Frame(self.root)
        frame.pack(padx = 40, pady = 40)

        label = tk.Label(frame, text = "Enter your password:", font = ("Helvetica", 12))
        label.grid(row = 0, column = 0)

        # Add an entry field to enter the password
        self.password_entry = tk.Entry(frame, show = "*", font = ("Helvetica", 12))
        self.password_entry.grid(row = 0, column = 1, padx = 5, pady = 0)
        self.password_entry.bind('<KeyRelease>', self.update_strength) # Bind the KeyRelease event to the update_strength method
        
        # Add a checkbox to toggle password visibility
        self.show_password_var = tk.IntVar()
        show_password_checkbox = tk.Checkbutton(frame, text = "Show Password", variable = self.show_password_var, command = self.toggle_password_visibility, font = ("Helvetica", 12))
        show_password_checkbox.grid(row = 0, column = 2, pady = 0)

        # Create a custom style for the strength bar
        self.progress_style = ttk.Style()
        self.progress_style.theme_use('default')
        self.progress_style.configure("strength.Horizontal.TProgressbar", background = 'teal', thickness = 12)

        # Add a label to show the strength of the password
        self.strength_label = tk.Label(frame, text = "Password Strength:", font = ("Helvetica", 10))
        self.strength_label.grid(row = 1, column = 0, pady = 10)

        # Add a progress bar to show the strength of the password
        self.strength_bar = ttk.Progressbar(frame, style = "strength.Horizontal.TProgressbar", mode = 'determinate', length = 185)
        self.strength_bar.grid(row = 1, column = 1, pady = 10)

        # Add a 'Copy to Clipboard' button
        self.copy_button = tk.Button(frame, text = "Copy to Clipboard", command = self.copy_to_clipboard, font = ("Helvetica", 12))
        self.copy_button.grid(row = 1, column = 2, pady = 10)
        
        # Add a 'Check Password' button
        self.check_button = tk.Button(frame, text = "Check Password", command = self.start_check, font = ("Helvetica", 12))
        self.check_button.grid(row = 2, column = 1, pady = 10)

        # Add a 'Generate Password' button
        self.generate_button = tk.Button(frame, text = "Generate New Password", command = self.generate_and_set_password, font = ("Helvetica", 12))
        self.generate_button.grid(row = 2, column = 2, padx = 100, pady = 10)

        # Add a progress bar to show the progress of the password check
        self.progress_bar = ttk.Progressbar(frame, style = "strength.Horizontal.TProgressbar", mode = 'indeterminate', length = 175)
        self.progress_bar.grid(row = 3, column = 1, pady = 10)

        # Add a label to show the status of the password check
        self.status_label = tk.Label(frame, text = "", font = ("Helvetica", 12), fg = "red")
        self.status_label.grid(row = 4, column = 1, pady = 10)

        # Set the check_password_func callback function
        self.check_password_func = check_password_func


    def toggle_password_visibility(self):
        """
        Toggles the visibility of the password in the password entry field.

        If the show_password_var is True, the password will be displayed as plain text.
        If the show_password_var is False, the password will be displayed as asterisks.

        Args:
            None

        Returns:
            None
        """
        if self.show_password_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")


    def copy_to_clipboard(self):
        """
        Copies the password from the password entry field to the clipboard.

        This method retrieves the password from the password entry field, clears the clipboard,
        appends the password to the clipboard, and updates the status label to indicate that
        the password has been copied.

        Args:
            None

        Returns:
            None
        """
        password = self.password_entry.get()
        self.root.clipboard_clear()
        self.root.clipboard_append(password)
        self.status_label.config(text="Password copied to clipboard!", fg='green')


    def generate_and_set_password(self):
        """
        Generates a new password and sets it in the password entry field.
        """
        new_password = generate_password(12)
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, new_password)
        self.update_strength()


    def update_strength(self, event = None):
        """
        Update the strength of the password and display it on the progress bar.

        Args:
            event (Event, optional): The event that triggered the update. Defaults to None.
        """
        password = self.password_entry.get()
        if not password:
            self.strength_bar['value'] = 0
            return

        strength = calculate_strength(password)
        self.strength_bar['value'] = strength * 100

        # Change the color of the progress bar based on the strength
        if strength < 0.3:
            self.progress_style.configure("strength.Horizontal.TProgressbar", background='red')
        elif strength < 0.6:
            self.progress_style.configure("strength.Horizontal.TProgressbar", background='yellow')
        else:
            self.progress_style.configure("strength.Horizontal.TProgressbar", background='green')


    def start_check(self, event = None):
        """
        Starts the password checking process.

        Args:
            event (Event, optional): The event that triggered the method. Defaults to None.
        """
        password = self.password_entry.get()
        
        if password == '':
            self.status_label.config(text = "Please enter a password!")
            return
        
        self.progress_bar.start()
        self.check_password_func(password)
        
        self.progress_bar.stop()
        self.progress_bar['value'] = 100
        self.reset_gui()


    def reset_gui(self):
        """
        Resets the GUI by clearing the password entry field, status label, and progress bar.
        """
        self.password_entry.delete(0, tk.END) # Clear the password entry field
        self.status_label.config(text = "") # Clear the status label
        self.progress_bar['value'] = 0 # Reset the progress bar


    def run(self):
        self.root.mainloop()