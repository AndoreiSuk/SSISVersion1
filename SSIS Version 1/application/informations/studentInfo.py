import tkinter as tk
import ttkbootstrap as ttk
from ..database import programs, students

class StudentInfo(ttk.Toplevel):
    def __init__(self, master, mode: str, data: dict=None):
        super().__init__(master=master)
        self.data = data # Store original data for comparison during edit
        self.mode = mode
        self.transient(master)
        window_width = 380
        window_height = 500
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        self.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
        self.title('New Student' if mode == 'new' else 'Edit Student Information')
        form_frame = ttk.Frame(self, padding=20)
        form_frame.pack(fill='both', expand=True)
        ttk.Label(form_frame, text="STUDENT ID (YYYY-NNNN)", font=('Default', 10)).pack(pady=(0,5), anchor='w')
        self.id_entry = ttk.Entry(form_frame)
        self.id_entry.pack(padx=0, fill='x', pady=(0,10))
        ttk.Label(form_frame, text="FIRST NAME", font=('Default', 10)).pack(pady=(0,5), anchor='w')
        self.firstname_entry = ttk.Entry(form_frame)
        self.firstname_entry.pack(padx=0, fill='x', pady=(0,10))
        ttk.Label(form_frame, text="LAST NAME", font=('Default', 10)).pack(pady=(0,5), anchor='w')
        self.lastname_entry = ttk.Entry(form_frame)
        self.lastname_entry.pack(padx=0, fill='x', pady=(0,10))
        ttk.Label(form_frame, text="SEX", font=('Default', 10)).pack(pady=(0,5), anchor='w')
        self.sex_values = ["No Selection", "Male", "Female", "Prefer not to say"]
        self.sex_option = ttk.Combobox(form_frame, values=self.sex_values, state='readonly')
        self.sex_option.pack(fill='x', padx=0, pady=(0,10))
        ttk.Label(form_frame, text="PROGRAM", font=('Default', 10)).pack(pady=(0,5), anchor='w')
        
        all_programs_data = programs.get_all()
        program_codes_list = ["No Selection"]
        if isinstance(all_programs_data, list):
            for program in all_programs_data:
                college_code = str(program.get("COLLEGE", "")).strip()
                if college_code and college_code.lower() not in ['nan', 'none', '']:
                    program_id = program.get("ID")
                    if program_id and str(program_id).strip():
                        program_codes_list.append(str(program_id))
        self.program_ids_list = list(dict.fromkeys(program_codes_list))
        self.program_option = ttk.Combobox(form_frame, values=self.program_ids_list, state='readonly')
        
        self.program_option.pack(fill='x', padx=0, pady=(0,10))
        ttk.Label(form_frame, text="YEAR LEVEL", font=('Default', 10)).pack(pady=(0,5), anchor='w')
        self.year_level_values = ["No Selection", "First Year", "Second Year", "Third Year", "Fourth Year"]
        self.yearlevel_option = ttk.Combobox(form_frame, values=self.year_level_values, state='readonly')
        self.yearlevel_option.pack(fill='x', padx=0, pady=(0,20))
        self.buttons_frame = ttk.Frame(form_frame)
        self.create_button = ttk.Button(self.buttons_frame, text="Create" if mode == 'new' else 'Save Changes', width=15, bootstyle="success" if mode == 'new' else "primary", command=self.create_button_callback)
        self.create_button.pack(side='left', fill='x', expand=True, padx=(0,5), ipady=3)
        self.cancel_button = ttk.Button(self.buttons_frame, text="Cancel", width=15, bootstyle="secondary", command=self.destroy)
        self.cancel_button.pack(side='right', fill='x', expand=True, padx=(5,0), ipady=3)
        self.buttons_frame.pack(side='bottom', padx=0, pady=(10,0), fill='x')

        if self.data is not None:
            self.id_entry.insert(0, self.data.get('ID',''))
            self.firstname_entry.insert(0, self.data.get("FIRSTNAME",''))
            self.lastname_entry.insert(0, self.data.get("LASTNAME",''))
            sex_val_from_data = str(self.data.get("SEX", "")).strip()
            set_sex_value = "No Selection"
            if sex_val_from_data:
                if sex_val_from_data in self.sex_values:
                    set_sex_value = sex_val_from_data
                else:
                    for val in self.sex_values:
                        if val.lower() == sex_val_from_data.lower():
                            set_sex_value = val
                            break
            self.sex_option.set(set_sex_value)
            program_val_from_data = str(self.data.get("PROGRAM", "")).strip()
            set_program_value = "No Selection"
            if program_val_from_data:
                if program_val_from_data in self.program_ids_list:
                    set_program_value = program_val_from_data
                else:
                    for val in self.program_ids_list:
                        if val.lower() == program_val_from_data.lower():
                            set_program_value = val
                            break
            self.program_option.set(set_program_value)
            year_level_val_from_data = str(self.data.get("YEAR LEVEL", "")).strip()
            set_year_level_value = "No Selection"
            if year_level_val_from_data:
                if year_level_val_from_data in self.year_level_values:
                    set_year_level_value = year_level_val_from_data
                else:
                    for val in self.year_level_values:
                        if val.lower() == year_level_val_from_data.lower():
                            set_year_level_value = val
                            break
            self.yearlevel_option.set(set_year_level_value)
        else:
            self.sex_option.set("No Selection")
            self.program_option.set("No Selection")
            self.yearlevel_option.set("No Selection")
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
        ok_button = ttk.Button(button_frame, text='Ok', width=10, command=toplevel.destroy, bootstyle="primary")
        ok_button.pack()
        toplevel.grab_set()

    def create_button_callback(self):
        stud_id = self.id_entry.get().strip()
        firstname = self.firstname_entry.get().strip()
        lastname = self.lastname_entry.get().strip()
        sex = self.sex_option.get()
        program_code = self.program_option.get()
        year_level = self.yearlevel_option.get()
        selected_sex = sex if sex != "No Selection" else ""
        selected_program = program_code if program_code != "No Selection" else ""
        selected_year_level = year_level if year_level != "No Selection" else ""
        if not (len(stud_id) == 9 and stud_id[4] == '-' and stud_id[:4].isdigit() and stud_id[5:].isdigit()):
            return self.dialog("Invalid Student ID format.\nExpected: YYYY-NNNN (e.g., 2023-0001)", "Input Error")
        current_data = {
            "ID": stud_id,
            "FIRSTNAME": firstname,
            "LASTNAME": lastname,
            "SEX": selected_sex,
            "PROGRAM": selected_program,
            "YEAR LEVEL": selected_year_level
        }
        if self.mode == 'new':
            if students.check(stud_id):
                return self.dialog("This Student ID already exists!! Please Try Again.", "Update Error")
            students.insert_one(current_data)
            self.dialog(f"Successfully created the Student: #{stud_id}", "Success!!!")
            if hasattr(self.master, 'current_student_sort_option'):
                self.master.current_student_sort_option = None
            if hasattr(self.master, 'refresh_student_table'): self.master.refresh_student_table()
            self.destroy()
        else: # self.mode == 'edit'
            original_stud_id = self.data.get('ID', '').strip() # Get the original ID
            changed = False
            if self.data:
                if original_stud_id.lower() != stud_id.lower():
                    changed = True
                elif self.data.get('FIRSTNAME', '') != firstname:
                    changed = True
                elif self.data.get('LASTNAME', '') != lastname:
                    changed = True
                elif self.data.get('SEX', '') != selected_sex:
                    changed = True
                elif self.data.get('PROGRAM', '') != selected_program:
                    changed = True
                elif self.data.get('YEAR LEVEL', '') != selected_year_level:
                    changed = True
            else:
                changed = True
            if not changed:
                return self.dialog("No changes were made. Please try again.", "Information")
            success = students.edit(original_id=original_stud_id, new_data=current_data)
            if success:
                self.dialog(f"Successfully updated the Student: #{stud_id}", "Success")
                if hasattr(self.master, 'refresh_student_table'): self.master.refresh_student_table()
                self.destroy()
            else:
                self.dialog(f"Failed to update Student: #{stud_id}'. It might be that the new ID already exists for another record or original ID was not found.", "Error")