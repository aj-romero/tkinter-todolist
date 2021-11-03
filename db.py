from tkinter import *
import sqlite3

root = Tk()
root.title('Tk to-do list')
root.geometry('500x500')

conn = sqlite3.connect('todo.db')

c = conn.cursor()

c.execute("""
        CREATE TABLE if not exists todo(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            CREATED_AT TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            description TEXT NOT NULL,
            completed BOOLEAN NOT NULL
            );
        """)

conn.commit()

def remove(id):
    def _remove():
        c.execute("DELETE FROM todo WHERE id = ?", (id,))
        conn.commit()
        render_todos()
    return _remove

def complete(id):
    def _complete(): #currying! retrasando la ejecucion de la funcion
        todo = c.execute("SELECT * FROM todo WHERE id = ?",(id,)).fetchone()
        c.execute("UPDATE todo SET completed = ? WHERE id = ?",(not todo[3],id))
        conn.commit()
        render_todos()
    return _complete
    

def render_todos():
    rows = c.execute(" SELECT * FROM todo").fetchall()
    
    for widget in frame.winfo_children():
        widget.destroy()

    for i in range(0, len(rows)):
        id = rows[i][0]
        completed = rows[i][3]
        description = rows[i][2]
        color = '#555555' if completed else '#ffffff'
        cl = Checkbutton(frame, text = description,fg = color, width = 42, anchor = 'w', command=complete(id))
        cl.grid(row = i, column = 0, sticky = 'w')
        
        btn = Button(frame, text = 'Del', command = remove(id))
        btn.grid(row = i, column = 1)
        cl.select() if completed else cl.deselect()


def addTodo():
    todo = e.get()
    if todo:
        c.execute("""
                INSERT INTO todo(description, completed) VALUES(?,?)
            """,(todo, False))
        conn.commit()
        e.delete(0,END)
        render_todos()
    else:
        pass

l = Label(root, text = 'Tarea')
l.grid(row = 0, column = 0)

e = Entry(root, width = 40)
e.grid(row = 0, column = 1)

btn = Button(root, text = 'ADD', command = addTodo)
btn.grid(row = 0 , column = 2)

frame = LabelFrame(root, text = 'My Tasks', padx = 5, pady = 5)
frame.grid(row = 1, column = 0, columnspan = 3, sticky = 'nswe', padx = 5)

e.focus()
root.bind('<Return>', lambda x: addTodo())

render_todos()


root.mainloop()
