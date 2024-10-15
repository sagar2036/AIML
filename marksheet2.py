import tkinter as tk
from tkinter import messagebox
from fpdf import FPDF

class MarksheetPortal:
    def __init__(self, root):
        self.root = root
        self.root.title("Marksheet Portal")
        self.root.geometry("600x400")
        self.current_frame = None
        
        # Store student info and marks
        self.student_info = {}
        self.subject_marks = {}
        
        # Initialize the first page (Introduction)
        self.show_intro_page()
        
    def switch_frame(self, new_frame_class):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = new_frame_class(self)
        self.current_frame.pack(fill='both', expand=True)
        
    def show_intro_page(self):
        self.switch_frame(IntroPage)
        
    def show_login_page(self):
        self.switch_frame(LoginPage)
    
    def show_subject_input_page(self):
        self.switch_frame(SubjectInputPage)
    
    def show_marks_display_page(self):
        self.switch_frame(MarksDisplayPage)
    
    def show_marksheet_page(self):
        self.switch_frame(MarksheetPage)
    
    def generate_pdf(self):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        pdf.cell(200, 10, txt="Marksheet", ln=True, align="C")
        pdf.cell(200, 10, txt=f"Student Name: {self.student_info['name']}", ln=True, align="L")
        pdf.cell(200, 10, txt=f"Class: {self.student_info['class']}", ln=True, align="L")
        pdf.cell(200, 10, txt=f"Roll No: {self.student_info['roll_no']}", ln=True, align="L")

        # Table header
        pdf.cell(40, 10, "Subject", 1, 0, 'C')
        pdf.cell(40, 10, "Marks", 1, 1, 'C')

        # Adding subject marks to PDF
        for subject, mark in self.subject_marks.items():
            pdf.cell(40, 10, subject, 1)
            pdf.cell(40, 10, str(mark), 1)
            pdf.cell(0, 10, '', 0, 1)  # New line

        # Calculate total, average, and result
        total_marks = sum(self.subject_marks.values())
        avg_marks = total_marks / len(self.subject_marks)
        result = "Pass" if avg_marks >= 35 else "Fail"
        result_in_words = "Pass" if result == "Pass" else "Fail"

        # Display total, average, and result in the PDF
        pdf.cell(40, 10, "Total Marks:", 1)
        pdf.cell(40, 10, str(total_marks), 1)
        pdf.cell(0, 10, '', 0, 1)  # New line
        
        pdf.cell(40, 10, "Average Marks:", 1)
        pdf.cell(40, 10, f"{avg_marks:.2f}", 1)
        pdf.cell(0, 10, '', 0, 1)  # New line

        pdf.cell(40, 10, "Result:", 1)
        pdf.cell(40, 10, result_in_words, 1)
        pdf.cell(0, 10, '', 0, 1)  # New line

        # Save the PDF
        pdf.output("marksheet.pdf")
        messagebox.showinfo("Success", "Marksheet downloaded as PDF")

# Frame classes for different pages
class IntroPage(tk.Frame):
    def __init__(self, controller):
        tk.Frame.__init__(self, controller.root, bg="#d3f3ff")  # Light blue background
        self.controller = controller
        
        label = tk.Label(self, text="Welcome to the Marksheet Portal", font=('Arial', 18), bg="#d3f3ff")
        label.pack(pady=50)
        
        next_btn = tk.Button(self, text="login", command=controller.show_login_page)
        next_btn.pack(pady=20)

class LoginPage(tk.Frame):
    def __init__(self, controller):
        tk.Frame.__init__(self, controller.root, bg="#ffcccb")  # Light red background
        self.controller = controller
        
        tk.Label(self, text="Login", font=('Arial', 18), bg="#ffcccb").pack(pady=20)
        
        tk.Label(self, text="Username", bg="#ffcccb").pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack(pady=5)
        
        tk.Label(self, text="Password", bg="#ffcccb").pack()
        self.password_entry = tk.Entry(self, show='*')
        self.password_entry.pack(pady=5)
        
        login_btn = tk.Button(self, text="Login", command=self.login)
        login_btn.pack(pady=20)
        
        prev_btn = tk.Button(self, text="Previous", command=controller.show_intro_page)
        prev_btn.pack(pady=20)
    
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if username == "admin" and password == "2024":
            self.controller.show_subject_input_page()
        else:
            messagebox.showerror("Error", "Invalid username or password")

class SubjectInputPage(tk.Frame):
    def __init__(self, controller):
        tk.Frame.__init__(self, controller.root, bg="#ffe5b4")  # Light orange background
        self.controller = controller
        
        tk.Label(self, text="Enter Student Information", font=('Arial', 16), bg="#ffe5b4").pack(pady=20)
        
        tk.Label(self, text="Name", bg="#ffe5b4").pack()
        self.name_entry = tk.Entry(self)
        self.name_entry.pack(pady=5)
        
        tk.Label(self, text="Class", bg="#ffe5b4").pack()
        self.class_entry = tk.Entry(self)
        self.class_entry.pack(pady=5)
        
        tk.Label(self, text="Roll No", bg="#ffe5b4").pack()
        self.roll_no_entry = tk.Entry(self)
        self.roll_no_entry.pack(pady=5)
        
        tk.Label(self, text="Enter Marks for Subjects", font=('Arial', 14), bg="#ffe5b4").pack(pady=10)
        self.subject_entries = {}
        subjects = ["Math", "English", "Science", "History", "Geography"]
        for subject in subjects:
            tk.Label(self, text=subject, bg="#ffe5b4").pack()
            entry = tk.Entry(self)
            entry.pack(pady=5)
            self.subject_entries[subject] = entry
        
        submit_btn = tk.Button(self, text="Submit", command=self.submit)
        submit_btn.pack(pady=20)
        
        prev_btn = tk.Button(self, text="Previous", command=controller.show_login_page)
        prev_btn.pack(pady=10)
    
    def submit(self):
        self.controller.student_info['name'] = self.name_entry.get()
        self.controller.student_info['class'] = self.class_entry.get()
        self.controller.student_info['roll_no'] = self.roll_no_entry.get()
        
        for subject, entry in self.subject_entries.items():
            try:
                self.controller.subject_marks[subject] = int(entry.get())
            except ValueError:
                messagebox.showerror("Error", f"Invalid marks for {subject}")
                return
        
        self.controller.show_marks_display_page()

class MarksDisplayPage(tk.Frame):
    def __init__(self, controller):
        tk.Frame.__init__(self, controller.root, bg="#cce5ff")  # Light blue background
        self.controller = controller
        
        student_info = controller.student_info
        subject_marks = controller.subject_marks
        
        tk.Label(self, text="Review Student Information", font=('Arial', 16), bg="#cce5ff").pack(pady=20)
        
        tk.Label(self, text=f"Name: {student_info['name']}", bg="#cce5ff").pack(pady=5)
        tk.Label(self, text=f"Class: {student_info['class']}", bg="#cce5ff").pack(pady=5)
        tk.Label(self, text=f"Roll No: {student_info['roll_no']}", bg="#cce5ff").pack(pady=5)
        
        tk.Label(self, text="Marks:", bg="#cce5ff").pack(pady=10)
        for subject, marks in subject_marks.items():
            tk.Label(self, text=f"{subject}: {marks}", bg="#cce5ff").pack(pady=5)
        
        generate_btn = tk.Button(self, text="Get Marksheet", command=controller.show_marksheet_page)
        generate_btn.pack(pady=20)
        
        prev_btn = tk.Button(self, text="Previous", command=controller.show_subject_input_page)
        prev_btn.pack(pady=10)

class MarksheetPage(tk.Frame):
    def __init__(self, controller):
        tk.Frame.__init__(self, controller.root)
        
        student_info = controller.student_info
        subject_marks = controller.subject_marks
        
        tk.Label(self, text="Marksheet", font=('Arial', 16)).pack(pady=20)

        tk.Label(self, text=f"Name: {student_info['name']}", bg="#cce5ff").pack(pady=5)
        tk.Label(self, text=f"Class: {student_info['class']}", bg="#cce5ff").pack(pady=5)
        tk.Label(self, text=f"Roll No: {student_info['roll_no']}", bg="#cce5ff").pack(pady=5)
        
        total_marks = sum(subject_marks.values())
        avg_marks = total_marks / len(subject_marks)
        result = "Pass" if avg_marks >= 35 else "Fail"
        
        tk.Label(self, text="").pack(pady=5)
        
        table_frame = tk.Frame(self)
        table_frame.pack()
        
        # Create header row
        headers = ["Subject", "Marks"]
        for i, header in enumerate(headers):
            header_label = tk.Label(table_frame, text=header, relief="solid", width=15, font=("Arial", 12))
            header_label.grid(row=0, column=i, padx=10, pady=5)
        
        # Create rows for subjects and marks
        for row_idx, (subject, marks) in enumerate(subject_marks.items(), start=1):
            subject_label = tk.Label(table_frame, text=subject, relief="solid", width=15)
            subject_label.grid(row=row_idx, column=0, padx=10, pady=5)
            
            marks_label = tk.Label(table_frame, text=marks, relief="solid", width=15)
            marks_label.grid(row=row_idx, column=1, padx=10, pady=5)
        
        # Display total, average, and result in table format
        total_row = row_idx + 1
        tk.Label(table_frame, text="Total", relief="solid", width=15).grid(row=total_row, column=0, padx=10, pady=5)
        tk.Label(table_frame, text=total_marks, relief="solid", width=15).grid(row=total_row, column=1, padx=10, pady=5)
        
        avg_row = total_row + 1
        tk.Label(table_frame, text="Average", relief="solid", width=15).grid(row=avg_row, column=0, padx=10, pady=5)
        tk.Label(table_frame, text=f"{avg_marks:.2f}", relief="solid", width=15).grid(row=avg_row, column=1, padx=10, pady=5)
        
        result_row = avg_row + 1
        tk.Label(table_frame, text="Result", relief="solid", width=15).grid(row=result_row, column=0, padx=10, pady=5)
        tk.Label(table_frame, text=result, relief="solid", width=15).grid(row=result_row, column=1, padx=10, pady=5)
        
        download_btn = tk.Button(self, text="Download PDF", command=controller.generate_pdf)
        download_btn.pack(pady=20)
        
        prev_btn = tk.Button(self, text="Previous", command=controller.show_marks_display_page)
        prev_btn.pack(pady=10)


# Main application setup
if __name__ == "__main__":
    root = tk.Tk()
    app = MarksheetPortal(root)
    root.mainloop()
