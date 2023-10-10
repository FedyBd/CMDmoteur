import tkinter as tk
import cx_Oracle
import os
import requests
class MyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MioT")

        # Premier cadre (première page)
        self.frame1 = tk.Frame(self.root)
        self.frame1.pack()

        self.label1 = tk.Label(self.frame1, text="Login page ", font=("Helvetica", 16), fg="blue")
        self.label1.pack(pady=5)

        # Input fields for Connexion
        self.empty_label = tk.Label(self.frame1, text="Username")
        self.empty_label.pack()
        self.username_entry = tk.Entry(self.frame1, width=20)
        self.username_entry.pack()
        self.empty_label = tk.Label(self.frame1, text="Password")
        self.empty_label.pack()
        self.password_entry = tk.Entry(self.frame1, show="*", width=20)  # Masking password with "*"
        self.password_entry.pack()

        self.button1 = tk.Button(self.frame1, text="Log in", command=self.authenticate_user)
        self.button1.pack(pady=5)
        # Empty label
        self.empty_label = tk.Label(self.frame1, text="", fg="red")
        self.empty_label.pack()


        # Deuxième cadre (deuxième page)
        self.frame2 = tk.Frame(self.root)
        self.label2 = tk.Label(self.frame2, text="Motor Panel ", font=("Helvetica", 16), fg="blue")
        # Create the main container frame to hold the first two buttons
        self.button_container = tk.Frame(self.frame2)
        self.button21 = tk.Button(self.button_container, text="ON", fg="green", command=move_forward)
        self.button22 = tk.Button(self.button_container, text="OFF", fg="red", command=stop_motor)
        self.button2 = tk.Button(self.frame2, text="Log out", command=self.goto_page1)


    def goto_page2(self) :
        # Clear the username and password fields
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        # Cacher le premier cadre et afficher le deuxième
        self.frame1.pack_forget()
        self.frame2.pack()
        self.label2.pack(pady=5)
        self.button_container.pack(pady=25)
        self.button21.pack(side='left')
        self.button22.pack(side='left')
        self.button2.pack(pady=25)


    def goto_page1(self):
        # Cacher le deuxième cadre et afficher le premier
        self.frame2.pack_forget()
        self.label1.pack()
        self.button1.pack()
        self.frame1.pack()


    def authenticate_user(self):
        # Get the entered username and password
        entered_username = self.username_entry.get()
        entered_password = self.password_entry.get()

        # Replace these values with your actual connection details
        host = 'localhost'
        port = '1521'
        sid = 'xe'

        db_username = os.environ.get('DB_USERNAME')
        db_password = os.environ.get('DB_PASSWORD')
        user = db_username
        password = db_password

        # Construct the connection string
        dsn = cx_Oracle.makedsn(host, port, sid=sid)

        # Connect to the Oracle database
        conn = cx_Oracle.connect(user=user, password=password, dsn=dsn)

        # Create a cursor to execute SQL queries
        cursor = conn.cursor()

        # Query the database for the entered username
        query = "SELECT username, mdp FROM auth WHERE username = :entered_username"
        cursor.execute(query, entered_username=entered_username)
        result = cursor.fetchone()

        # Close the cursor and the database connection
        cursor.close()
        conn.close()

        # Check if the username exists in the database and if the entered password matches the stored password
        if result is not None and result[1] == entered_password:
            print("Successful authentication!")
            self.goto_page2()  # Move to the second page after successful authentication
        else:
            self.empty_label.config(text="Authentication failed! Please try again.", fg="red")


# Define the base URL of your Raspberry Pi's web server
#WE NEED TO MAKE SURE OF THE PI URL, WE USED ADVANCED IP SCANNER :

raspberry_pi_url = "http://192.168.1.16:5000"

# Function to make HTTP request to move the motor forward
def move_forward():
    requests.get(f"{raspberry_pi_url}/forward")

# Function to make HTTP request to stop the motor
def stop_motor():
    requests.get(f"{raspberry_pi_url}/stop")
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x300")
    app = MyApp(root)
    root.mainloop()
