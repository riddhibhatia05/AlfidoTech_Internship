import json
from datetime import datetime
import tkinter as tk
from tkinter import messagebox


class TodoListGUI:
    def __init__(self, master):
        self.master = master
        master.title("To-Do List")

        self.tasks = []

        self.task_label = tk.Label(master, text="Task:")
        self.task_label.grid(row=0, column=0, sticky="w")

        self.task_entry = tk.Entry(master)
        self.task_entry.grid(row=0, column=1, padx=5, pady=5)

        self.add_button = tk.Button(master, text="Add Task", command=self.add_task)
        self.add_button.grid(row=0, column=2, padx=5, pady=5)

        self.tasks_listbox = tk.Listbox(master, width=50)
        self.tasks_listbox.grid(row=1, columnspan=3, padx=5, pady=5)

        self.delete_button = tk.Button(master, text="Delete Task", command=self.delete_task)
        self.delete_button.grid(row=2, column=0, padx=5, pady=5)

        self.complete_button = tk.Button(master, text="Mark as Completed", command=self.mark_completed)
        self.complete_button.grid(row=2, column=1, padx=5, pady=5)

        self.priority_label = tk.Label(master, text="Priority:")
        self.priority_label.grid(row=3, column=0, sticky="w")

        self.priority_entry = tk.Entry(master)
        self.priority_entry.grid(row=3, column=1, padx=5, pady=5)

        self.search_label = tk.Label(master, text="Search:")
        self.search_label.grid(row=4, column=0, sticky="w")

        self.search_entry = tk.Entry(master)
        self.search_entry.grid(row=4, column=1, padx=5, pady=5)

        self.search_button = tk.Button(master, text="Search", command=self.search_task)
        self.search_button.grid(row=4, column=2, padx=5, pady=5)

        self.load_tasks()

    def add_task(self):
        task = self.task_entry.get()
        priority = self.priority_entry.get()
        if task:
            self.tasks.append({'task': task, 'priority': priority, 'completed': False})
            self.update_tasks_listbox()
            self.task_entry.delete(0, tk.END)
            self.priority_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Please enter a task.")

    def delete_task(self):
        selected_index = self.tasks_listbox.curselection()
        if selected_index:
            del self.tasks[selected_index[0]]
            self.update_tasks_listbox()

    def mark_completed(self):
        selected_index = self.tasks_listbox.curselection()
        if selected_index:
            self.tasks[selected_index[0]]['completed'] = True
            self.update_tasks_listbox()

    def search_task(self):
        keyword = self.search_entry.get().lower()
        if keyword:
            search_result = [task['task'] for task in self.tasks if keyword in task['task'].lower()]
            if search_result:
                messagebox.showinfo("Search Result", "\n".join(search_result))
            else:
                messagebox.showinfo("Search Result", "No tasks found.")

    def update_tasks_listbox(self):
        self.tasks_listbox.delete(0, tk.END)
        for task in self.tasks:
            status = "Completed" if task['completed'] else "Pending"
            self.tasks_listbox.insert(tk.END, f"{task['task']} - Priority: {task['priority']}, Status: {status}")

    def load_tasks(self):
        try:
            with open("tasks.json", 'r') as f:
                self.tasks = json.load(f)
            self.update_tasks_listbox()
        except FileNotFoundError:
            messagebox.showwarning("Warning", "No tasks file found.")

    def save_tasks(self):
        with open("tasks.json", 'w') as f:
            json.dump(self.tasks, f)
        messagebox.showinfo("Info", "Tasks saved successfully.")


def main():
    root = tk.Tk()
    todo_list_gui = TodoListGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
