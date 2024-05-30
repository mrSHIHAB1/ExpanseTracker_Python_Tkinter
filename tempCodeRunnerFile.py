import tkinter as tk
from tkinter import messagebox
from customtkinter import *
from PIL import Image, ImageTk
from datetime import datetime
from collections import defaultdict
from tkcalendar import DateEntry
import pyrebase
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
firebaseConfig = {
  #Firebase realtime datbase link
};
firebase=pyrebase.initialize_app(firebaseConfig)
db=firebase.database()

class LoginForm(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Login Form")
        self.geometry("800x550+200+50")
        self.configure(bg='white')
        self.resizable(width=False, height=False)
        self.create_login_widgets()

    def create_login_widgets(self):
        image_path = "pythonProject/banner.png"  
        image = Image.open(image_path)
        image.thumbnail((450, 550))
        photo = ImageTk.PhotoImage(image)
        frame = tk.Frame(self, bg="white", width=450, height=550,highlightthickness=0,borderwidth=0)
        frame.pack_propagate(0)
        frame.pack(side='left')
        label = tk.Label(frame, image=photo,highlightthickness=0,borderwidth=0)
        label.image = photo  
        label.pack(pady=40)
        self.label_name=tk.Label(self,text="Personal Finance Manager",bg=self.cget('bg'), font=("Arial", 18,'bold'), fg="VioletRed4")
        self.label_name.place(x=60,y=355)
        self.label_name = tk.Label(self, text="Sign In",bg=self.cget('bg'), font=("Arial", 23), fg="VioletRed4").pack(pady=10)
        self.label_name = tk.Label(self, text="                           ",bg=self.cget('bg'),).pack(pady=20)
        self.label_name = tk.Label(self, text="Email:",bg=self.cget('bg'), font=("Arial", 13), fg="VioletRed4")
        self.label_name.place(x=470,y=90)
        
        self.entry_name = tk.Entry(self,width=50,highlightbackground="VioletRed3", highlightcolor="VioletRed4", highlightthickness=1)
        self.entry_name.pack(pady=5,ipady=6)
        self.label_name = tk.Label(self, text="                           ",bg=self.cget('bg'),).pack(pady=10)
        self.label_password = tk.Label(self, text="Password:",bg=self.cget('bg'), font=("Arial", 13), fg="VioletRed4")
        self.label_password.place(x=470,y=173)
        self.entry_password = tk.Entry(self, show="*",width=50, highlightbackground="VioletRed3", highlightcolor="VioletRed4", highlightthickness=1)
        self.entry_password.pack(pady=5,ipady=6)
        self.label_name = tk.Label(self, text="                           ",bg=self.cget('bg'),).pack(pady=10)
        self.button_login = tk.Button(self, text="Sign In", command=self.login,width=40 ,bg="VioletRed3", fg="white")
        self.button_login.pack(pady=5)
        self.label_password = tk.Label(self, text="or",bg=self.cget('bg'), font=("Arial", 10), fg="VioletRed4").pack(padx=5)
        self.button_signup = tk.Button(self, text="Sign Up", command=self.signup,width=40 ,bg="VioletRed3", fg="white")
        self.button_signup.pack(pady=5)

    def login(self):
        global current_user_email
        nameo = self.entry_name.get()
        username = nameo.split('@')[0]
        password = self.entry_password.get()
        users_data = db.child("Users").get()
       

        
        if users_data.val():
                flag=0
                for user_key, user_value in users_data.val().items():
                    if user_value.get('Email') == username and user_value.get('Password') == password:
                        flag=1
                        current_user_email = username
                        self.show_ok_page()
                if flag==0:
                    messagebox.showerror("Error", "No User found with this email and password")
                    
                        
                    
                
        else:
             messagebox.showerror("Error", "No User")
                 
        

    def signup(self):
        self.destroy()
        signup_form = SignUpForm()
        signup_form.mainloop()

    def show_ok_page(self):
        self.destroy()
        ok_page = OkPage()
        ok_page.mainloop()

class SignUpForm(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Sign Up Form")
        self.geometry("800x550+200+50")
        self.configure(bg='white')
        self.create_signup_widgets()
        self.db_stream = db.child("Users").child(current_user_email).child("display_text").stream(self.update_display)

    def create_signup_widgets(self):
        image_path = "pythonProject/Signup.png" 
        image = Image.open(image_path)
        image.thumbnail((450, 550))
        photo = ImageTk.PhotoImage(image)
        frame = tk.Frame(self, bg="white", width=450, height=550,highlightthickness=0,borderwidth=0)
        frame.pack_propagate(0)
        frame.pack(side='left')
        label = tk.Label(frame, image=photo,highlightthickness=0,borderwidth=0)
        label.image = photo  
        label.pack(pady=60)
        
        self.label_name = tk.Label(self, text="Sign Up",bg=self.cget('bg'), font=("Arial", 23), fg="VioletRed4").pack(pady=10)
        self.label_name = tk.Label(self, text="                           ",bg=self.cget('bg'),).pack(pady=20)

        self.label_name = tk.Label(self, text="Name:",bg=self.cget('bg'), font=("Arial", 13), fg="VioletRed4")
        self.label_name.place(x=470,y=83)
        self.entry_name = tk.Entry(self,width=50,highlightbackground="VioletRed3", highlightcolor="VioletRed4", highlightthickness=1)
        self.entry_name.place(x=470, y=108, height=25)

        self.label_phone = tk.Label(self, text="Phone:",bg=self.cget('bg'), font=("Arial", 13), fg="VioletRed4")
        self.label_phone.place(x=470, y=150)
        self.entry_phone = tk.Entry(self,width=50,highlightbackground="VioletRed3", highlightcolor="VioletRed4", highlightthickness=1)
        self.entry_phone.place(x=470, y=175, height=25) 

        self.label_email = tk.Label(self, text="Email:",bg=self.cget('bg'), font=("Arial", 13), fg="VioletRed4")
        self.label_email.place(x=470, y=217)
        self.entry_email = tk.Entry(self,width=50,highlightbackground="VioletRed3", highlightcolor="VioletRed4", highlightthickness=1)
        self.entry_email.place(x=470, y=242, height=25)


        self.label_password = tk.Label(self, text="Password:",bg=self.cget('bg'), font=("Arial", 13), fg="VioletRed4")
        self.label_password.place(x=470, y=285)
        self.entry_password = tk.Entry(self, show="*",width=50,highlightbackground="VioletRed3", highlightcolor="VioletRed4", highlightthickness=1)
        self.entry_password.place(x=470, y=310, height=25)

        self.label_name = tk.Label(self, text="                           ",bg=self.cget('bg'),).pack(pady=20)
        self.button_register = tk.Button(self, text="Register", command=self.register,width=40 ,bg="VioletRed3", fg="white")
        self.button_register.place(x=475,y=370)

        self.button_back = tk.Button(self, text="Back to Login", command=self.back_to_login,width=40 ,bg="VioletRed3", fg="white")
        self.button_back.place(x=475,y=410)

    def register(self):
       name = self.entry_name.get()
       phone = self.entry_phone.get()
       email = self.entry_email.get()
       password = self.entry_password.get()
       username = email.split('@')[0]
    
       if name==''or phone==''or email=='' or password=='':
         messagebox.showerror("Error", "Please Fill up the form completly")
         return
       users_data = db.child("Users").get()
       if users_data.val():
           for user_key, user_value in users_data.val().items():
               if user_value.get('Email') == username:
                   messagebox.showerror("Error", "Email already exists. Please choose another email.")
                   return
    
       
       user = {'Name': name, 'Phone': phone, 'Email': username, 'Password': password,}
       db.child('Users').push(user)
       messagebox.showinfo("Success", "User registered successfully.")
       self.back_to_login()
    

    def back_to_login(self):
        self.destroy()
        login_form = LoginForm()
        login_form.mainloop()

class OkPage(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("OK Page")
        self.geometry("800x550+200+50")
        self.create_ok_widgets()
        self.db_stream = db.child("Users").child("display_text").stream(self.update_display)
        global current_user_email
        current_sum = db.child("Users").child(current_user_email).child("sum_value").get().val()
        if current_sum is None:
            current_sum = 0
        self.display_text.delete('1.0', tk.END)
        self.display_text.insert(tk.END, current_sum)
    def create_ok_widgets(self):
        global current_user_email
        sum_value = db.child("Users").child(current_user_email).child("sum_value").get().val()

        left_frame = tk.Frame(self, bg="white", width=150, height=550, highlightthickness=0, borderwidth=0)
        left_frame.pack_propagate(0) 
        left_frame.pack(side='left')

       
        bold_font = ("Arial", 12, "bold")

    
        self.button_dashboard = tk.Button(left_frame, text="Dashboard", width=40, height=3, bg="VioletRed3", fg="white", font=bold_font, command=self.show_visual)
        self.button_dashboard.pack(pady=5)
        self.button_visual = tk.Button(left_frame, text="Transaction", width=40, height=3, bg="VioletRed3", fg="white", font=bold_font, command=self.show_dashboard)
        self.button_visual.pack(pady=5)
        self.button_signin = tk.Button(left_frame, text="Calculator", width=40, height=3, bg="VioletRed3", fg="white", font=bold_font, command=self.show_signin)
        self.button_signin.pack(pady=5)
        self.button_signout = tk.Button(left_frame, text="Sign Out", width=15, height=2, bg="VioletRed3", fg="white", font=bold_font, command=self.signout)
        self.button_signout.place(x=0, y=499)
        self.button_sgraph = tk.Button(left_frame, text="Visual", width=15, height=2, bg="VioletRed3", fg="white", font=bold_font, command=self.sgraph)
        self.button_sgraph.place(x=0, y=250)

       
        self.right_frame = tk.Frame(self, bg="white", highlightthickness=0, borderwidth=0)
        self.right_frame.pack(fill="both", expand=True)

     
        self.visual_frame = tk.Frame(self.right_frame, bg="lightSkyBlue1", highlightthickness=0, borderwidth=0)
        self.create_visual_widgets()

        self.signin_frame = tk.Frame(self.right_frame, bg="lightSkyBlue1", highlightthickness=0, borderwidth=0)
        self.show_dashboard_frame=tk.Frame(self.right_frame, bg="lightSkyBlue1", highlightthickness=0, borderwidth=0)
        self.sgraph_frame = tk.Frame(self.right_frame, bg="lightSkyBlue1", highlightthickness=0, borderwidth=0)
        
        
        


    def create_visual_widgets(self):
        
        image_path = "pythonProject/B2.png"   
        image = tk.PhotoImage(file=image_path)  
        image_label = tk.Label(self.visual_frame, image=image, bg="lightSkyBlue1")
        image_label.image = image  
        image_label.place(x=1, y=5)
        self.display_text = tk.Text(self.visual_frame, height=2, width=8, font=("Arial", 52), bd=3,bg="green3",fg="white")
        self.display_text.place(x=220, y=21)
        input_label = tk.Label(self.visual_frame, text="Amonut", font=("Arial", 12), bg="lightSkyBlue1")
        input_label.place(x=280,y=255)
        input_label = tk.Label(self.visual_frame, text="Note", font=("Arial", 12), bg="lightSkyBlue1")
        input_label.place(x=500,y=255)
        date_label = tk.Label(self.visual_frame, text="Date", font=("Arial", 12), bg="lightSkyBlue1")
        date_label.place(x=80,y=255)
        self.input_entry1 = DateEntry(self.visual_frame, width=24,height=1, background='darkblue',foreground='white', borderwidth=3)
        self.input_entry1.place(x=10, y=284)
    
       
        
        
        self.input_entry2 = tk.Entry(self.visual_frame, font=("Arial", 12), bd=3)
        self.input_entry2.place(x=230,y=280)
        self.input_entry3 = tk.Entry(self.visual_frame, font=("Arial", 12), bd=3)
        self.input_entry3.place(x=450,y=280)
        self.input_entry4 = DateEntry(self.visual_frame, width=24,height=1, background='darkblue',foreground='white', borderwidth=3)
        self.input_entry4.place(x=10,y=424)
        
        
        self.input_entry5 = tk.Entry(self.visual_frame, font=("Arial", 12), bd=3)
        self.input_entry5.place(x=230,y=420)
        self.input_entry6 = tk.Entry(self.visual_frame, font=("Arial", 12), bd=3)
        self.input_entry6.place(x=450,y=420)
        update_button = tk.Button(self.visual_frame, text="Deposit", width=10, bg="VioletRed3", fg="white", font=("Arial", 12, "bold"), command=self.update_display)
        update_button.place(x=265,y=320)
        remove_button = tk.Button(self.visual_frame, text="Withdraw", width=10, bg="VioletRed3", fg="white", font=("Arial", 12, "bold"), command=self.remove_value)
        remove_button.place(x=265,y=460)
    def signout(self):
        
        self.destroy()

       
        login_form = LoginForm()
        login_form.mainloop()
    def show_dashboard(self):
       
        self.hide_frames()
        self.show_dashboard_frame.pack(fill="both", expand=True)
    
        
        if hasattr(self, "table_frame"):
            
            self.update_table_content()
        else:
           
            self.create_table()
    
    def create_table(self):
       
        self.table_frame = tk.Frame(self.show_dashboard_frame,bg="lightSkyBlue1")
        self.table_frame.pack(fill="both", expand=True)
    
        
        history_label = tk.Label(self.table_frame, text="Transaction History", font=("Arial", 16), bg="lightSkyBlue1")
        history_label.pack(pady=20)
    
        
        table_container = tk.Frame(self.table_frame)
        table_container.pack(fill="both", expand=True,padx=40)
    
       
        self.scrollbar = tk.Scrollbar(table_container, orient="vertical")
        self.scrollbar.pack(side="right", fill="y")
    
        
        self.canvas = tk.Canvas(table_container, yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
    
      
        self.scrollbar.config(command=self.canvas.yview)
    
       
        self.inner_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")
    
        
        def on_configure(event):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
        
        self.inner_frame.bind("<Configure>", on_configure)
    
        
        headers = ["Type", "Date", "Note", "Amount"]
        for i, header in enumerate(headers):
            tk.Label(self.inner_frame, text=header, font=("Arial", 20, "bold"), bg="lightSkyBlue1", borderwidth=1, relief="solid").grid(row=0, column=i, padx=5, pady=5, sticky="nsew")
    
        
        self.display_table_data()
    
        
        self.table_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    
    def update_table_content(self):
       
        for widget in self.inner_frame.winfo_children():
            widget.destroy()
    
       
        headers = ["Type", "Date", "Note", "Amount"]
        for i, header in enumerate(headers):
            tk.Label(self.inner_frame, text=header, font=("Arial", 20, "bold"), bg="lightSkyBlue1", borderwidth=2, relief="solid").grid(row=0, column=i, padx=5, pady=5, sticky="nsew")
    
        
        self.display_table_data()
    
        
        self.table_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
    
    def display_table_data(self):
       
       global current_user_email  

       updates_data = db.child("Users").child(current_user_email).child("updates").get().val()
       withdraws_data = db.child("Users").child(current_user_email).child("withdraws").get().val()   
       all_data = {}
       if updates_data:
           all_data.update(updates_data)
       if withdraws_data:
           all_data.update(withdraws_data)   
       if all_data:
           for i, (key, value) in enumerate(all_data.items(), start=1):
               data_type = "Deposit" if key in updates_data else "Withdraw"
               bag_color = "green" if data_type == "Deposit" else "red"
               tk.Label(self.inner_frame, text=data_type, bg=bag_color, borderwidth=1, width=20, height=2,
                        relief="solid").grid(row=i, column=0, padx=5, pady=5, sticky="nsew")
               tk.Label(self.inner_frame, text=value["date"], bg="white", borderwidth=1, relief="solid").grid(row=i,
                                                                                                                column=1,
                                                                                                                padx=5,
                                                                                                                pady=5,
                                                                                                                sticky="nsew")
               tk.Label(self.inner_frame, text=value["note"], bg="white", borderwidth=1, width=20,
                        relief="solid").grid(row=i, column=2, padx=5, pady=5, sticky="nsew")
               tk.Label(self.inner_frame, text=value["input_value"], bg="white", borderwidth=1,
                        relief="solid").grid(row=i, column=3, padx=5, pady=5, sticky="nsew")   
       
           
                     
    def show_visual(self):
       
        self.hide_frames()
        self.visual_frame.pack(fill="both", expand=True)

    def update_display(self):
       
        global current_user_email 
      
        input_number = self.input_entry2.get()
        date = self.input_entry1.get()
        note = self.input_entry3.get()
      
        current_sum = db.child("Users").child(current_user_email).child("sum_value").get().val()
      
        if current_sum:
            new_sum = int(current_sum) + int(input_number)
        else:
            new_sum = int(input_number)
      
        update_id = datetime.now().strftime("%Y%m%d%H%M%S%f")
      
        data = {
            "input_value": input_number,
            "date": date,
            "note": note
        }
      
        db.child("Users").child(current_user_email).update({"sum_value": new_sum})
        db.child("Users").child(current_user_email).child("updates").child(update_id).set(data)
      
        self.display_text.delete('1.0', tk.END)
        self.display_text.insert(tk.END, new_sum)
      
        self.input_entry1.delete(0, tk.END)
        self.input_entry2.delete(0, tk.END)
        self.input_entry3.delete(0, tk.END)
    def remove_value(self):
        global current_user_email
        input_number = self.input_entry5.get()
        date = self.input_entry4.get()
        note = self.input_entry6.get()

        try:
            current_sum = db.child("Users").child(current_user_email).child("sum_value").get().val()

            if current_sum:
                new_sum = int(current_sum) - int(input_number)
            else:
                new_sum = 0

            withdrawal_id = datetime.now().strftime("%Y%m%d%H%M%S%f")

            withdrawal_data = {
                "date": date,
                "note": note,
                "input_value": input_number
            }

            db.child("Users").child(current_user_email).child("withdraws").child(withdrawal_id).set(withdrawal_data)
            db.child("Users").child(current_user_email).update({"sum_value": new_sum})

            self.display_text.delete('1.0', tk.END)
            self.display_text.insert(tk.END, new_sum)

            self.input_entry5.delete(0, tk.END)
            self.input_entry4.delete(0, tk.END)
            self.input_entry6.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Invalid Value!")
    def sgraph(self):
       self.hide_frames()
       self.sgraph_frame.pack(fill="both", expand=True)
       
       global current_user_email
       updates_data = db.child("Users").child(current_user_email).child("updates").get().val()
       withdraws_data = db.child("Users").child(current_user_email).child("withdraws").get().val()
       
       updates_transactions = defaultdict(int)
       withdraws_transactions = defaultdict(int)

       if updates_data:
           for key, update in updates_data.items():
               date = update['date']
               amount = int(update['input_value'])
               updates_transactions[date] += amount

       if withdraws_data:
           for key, withdraw in withdraws_data.items():
               date = withdraw['date']
               amount = int(withdraw['input_value'])
               withdraws_transactions[date] += amount
       
       all_dates = sorted(set(updates_transactions.keys()).union(set(withdraws_transactions.keys())))
       
       update_amounts = [updates_transactions[date] for date in all_dates]
       withdraw_amounts = [withdraws_transactions[date] for date in all_dates]
       
       x = np.arange(len(all_dates))
       width = 0.35  
       
       fig, ax = plt.subplots(figsize=(10, 5))
       bars1 = ax.bar(x - width/2, update_amounts, width, label='Deposits', color='blue')
       bars2 = ax.bar(x + width/2, withdraw_amounts, width, label='Withdraws', color='red')
       
       ax.set_xlabel('Date')
       ax.set_ylabel('Amount')
       ax.set_title('Transactions Over Time')
       ax.set_xticks(x)
       ax.set_xticklabels(all_dates, rotation=45)
       ax.legend()
       
    
       for i, rect in enumerate(bars1):
           height = rect.get_height()
           ax.text(rect.get_x() + rect.get_width()/2., height, update_amounts[i],
                   ha='center', va='bottom')
       
       for i, rect in enumerate(bars2):
           height = rect.get_height()
           ax.text(rect.get_x() + rect.get_width()/2., height, withdraw_amounts[i],
                   ha='center', va='bottom')
       
       for widget in self.sgraph_frame.winfo_children():
           widget.destroy()
       
       canvas = FigureCanvasTkAgg(fig, master=self.sgraph_frame)
       canvas.draw()
       canvas.get_tk_widget().pack(fill="both", expand=True)
    def show_signin(self):
        
        self.hide_frames()
        self.signin_frame.pack(fill="both", expand=True)

       
        calculator_frame = tk.Frame(self.signin_frame, bg="black")
        calculator_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

       
        bold_font = ("Arial", 14, "bold")

       
        result_var = tk.StringVar()
        result_entry = tk.Entry(calculator_frame, textvariable=result_var, font=("Arial", 14), justify="right", bd=5)
        result_entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        
        buttons = [
            ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("/", 1, 3),
            ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("*", 2, 3),
            ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("-", 3, 3),
            ("0", 4, 0), ("C", 4, 1), ("=", 4, 2), ("+", 4, 3),
        ]

        def on_button_click(text):
            if text == "C":
                result_var.set("")
            elif text == "=":
                try:
                    result = eval(result_var.get())
                    result_var.set(result)
                except:
                    messagebox.showerror("Error", "Invalid Expression!")
            else:
                current_text = result_var.get()
                result_var.set(current_text + text)

        for (text, row, column) in buttons:
            button = tk.Button(calculator_frame, text=text, font=("Arial", 14), width=5, height=2, command=lambda t=text: on_button_click(t))
            button.grid(row=row, column=column, padx=5, pady=5, sticky="nsew")

    def hide_frames(self):
        
        if hasattr(self, 'show_dashboard_frame'):
            self.show_dashboard_frame.pack_forget()
        
        self.visual_frame.pack_forget()
        self.signin_frame.pack_forget()
        self.sgraph_frame.pack_forget()


if __name__ == "__main__":
    login_form = LoginForm()
    login_form.mainloop()
