import tkinter as tk
import ttkbootstrap as ttk
from ..database import programs, colleges, students

class ProgramInfo(tk.Toplevel):
    def __init__(self, master, mode: str, data: dict = None):
        super().__init__(master=master)
        self.mode = mode
        self.data = data
        self.transient(master)
        window_width = 350
        window_height = 300
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        self.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
        self.title('New Program' if mode == 'new' else 'Edit Program Information')
        form_frame = ttk.Frame(self, padding=20)
        form_frame.pack(fill='both', expand=True)
        ttk.Label(form_frame, text="PROGRAM CODE", font=('Default', 10)).pack(pady=(0,5), anchor='w')
        self.id_entry = ttk.Entry(form_frame)
        self.id_entry.pack(padx=0, fill='x', pady=(0,10))
        ttk.Label(form_frame, text="PROGRAM NAME", font=('Default', 10)).pack(pady=(0,5), anchor='w')
        self.name_entry = ttk.Entry(form_frame)
        self.name_entry.pack(padx=0, fill='x', pady=(0,10))
        ttk.Label(form_frame, text="COLLEGE", font=('Default', 10)).pack(pady=(0,5), anchor='w')
        college_ids_list = [cid for cid in colleges.get_college_ids() if cid]
        if "No Selection" not in college_ids_list:
            college_ids_list.insert(0, "No Selection")
        self.college_option = ttk.Combobox(form_frame, values=college_ids_list, state='readonly')
        self.college_option.pack(fill='x', padx=0, pady=(0,20))
        self.buttons_frame = ttk.Frame(form_frame)
        self.create_button = ttk.Button(self.buttons_frame, text="Create" if mode == 'new' else 'Save Changes', width=15, bootstyle="success" if mode == 'new' else "primary", command=self.create_button_callback)
        self.create_button.pack(side='left', fill='x', expand=True, padx=(0,5), ipady=3)
        self.cancel_button = ttk.Button(self.buttons_frame, text="Cancel", width=15, bootstyle="secondary", command=self.destroy)
        self.cancel_button.pack(side='right', fill='x', expand=True, padx=(5,0), ipady=3)
        self.buttons_frame.pack(side='bottom', padx=0, pady=(10,0), fill='x')

        if self.data is not None:
            self.id_entry.insert(0, self.data.get('ID', ''))
            self.name_entry.insert(0, self.data.get("NAME", ''))
            current_college = self.data.get("COLLEGE", "No Selection")
            if current_college in college_ids_list:
                self.college_option.set(current_college)
            else:
                found_match = False
                for cid_val in college_ids_list:
                    if cid_val.lower() == current_college.lower():
                        self.college_option.set(cid_val)
                        found_match = True
                        break
                if not found_match:
                    self.college_option.set("No Selection")
        else:
            self.college_option.set("No Selection")
        self.grab_set()

    def dialog(self, text, title="Message"):
        toplevel = ttk.Toplevel(self)
        toplevel.title(title)
        toplevel.transient(self)
        window_width = 350
        window_height = 180
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        toplevel.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
        outer_frame = ttk.Frame(toplevel)
        outer_frame.pack(expand=True, fill='both', padx=10, pady=10)
        msg_label = ttk.Label(outer_frame, text=text, wraplength=window_width-60, justify='center', anchor='center')
        msg_label.pack(expand=True, fill='both', pady=(0,15))
        button_frame = ttk.Frame(outer_frame)
        button_frame.pack(side='bottom', pady=(0,5))
        ok_button = ttk.Button(button_frame, text='OK', width=10, command=toplevel.destroy, bootstyle="primary")
        ok_button.pack()
        toplevel.grab_set()

    def create_button_callback(self):
        prog_id = self.id_entry.get().strip()
        name = self.name_entry.get().strip()
        college_val = self.college_option.get()
        selected_college = college_val if college_val != "No Selection" else ""
        current_data = {"ID": prog_id, "NAME": name, "COLLEGE": selected_college}

        if not prog_id or not name:
            return self.dialog("Program Code and Program Name are required.", "Input Error")

        if self.mode == 'new':
            if programs.check(prog_id):
                return self.dialog("This Program code already exists!!!", "Please try again.")
            programs.insert_one(current_data)
            self.dialog(f"Successfully created the Program: {prog_id}", "Success!!!")
            if hasattr(self.master, 'current_program_sort_option'):
                self.master.current_program_sort_option = None
        else: # self.mode == 'edit'
            original_prog_id = self.data.get('ID', '').strip()

            if self.data and original_prog_id.lower() == prog_id.lower() and self.data.get('NAME', '') == name and self.data.get('COLLEGE', '') == selected_college:
                return self.dialog("No changes were made. Please try again.", "Information")

            if original_prog_id.lower() != prog_id.lower():
                if programs.check(prog_id):
                    return self.dialog(f"The New Program Code you entered already exists.", "Error")

                all_students_data = students.get_all()
                for s in all_students_data:
                    if isinstance(s, dict) and str(s.get("PROGRAM", "")).strip().lower() == original_prog_id.lower():
                        s["PROGRAM"] = prog_id
                        students.edit(original_id=s['ID'], new_data=s)
                
                programs.edit(original_prog_id, current_data)
                self.dialog(f"Successfully updated the Program.", "Success")

            else:
                success = programs.edit(original_id=original_prog_id, new_data=current_data)
                if success:
                    self.dialog(f"Successfully updated the Program: {prog_id}", "Success")
                else:
                    self.dialog(f"Failed to update Program '{prog_id}'.", "Error")

        if hasattr(self.master, 'refresh_program_table'): self.master.refresh_program_table()
        if hasattr(self.master, 'refresh_student_table'): self.master.refresh_student_table()
        self.destroy()