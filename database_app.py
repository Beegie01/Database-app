import sqlite3 as sq, tkinter as tk, pandas as pd
from tkinter import ttk, messagebox, scrolledtext

sq.paramstyle = 'named'
root = tk.Tk()
root.title('Database app')
root.geometry('600x400')
root.resizable(width=False, height=True)

# create new database or connect to existing database
conn = sq.connect('table.db')

# create cursor
c = conn.cursor()

frame = tk.Frame(root)
frame.grid(row=1, columnspan=4)
frame.rowconfigure(list(range(9)), weight=1)
frame.columnconfigure(list(range(4)), weight=1)

# execute commands - query the database
# c.execute('''CREATE TABLE addresses (
#             first_name text,
#             last_name text,
#             address text,
#             city text,
#             state text,
#             zip_code integer
#             )''')

# commit changes
conn.commit()

def add_rec(event):
    win = tk.Toplevel(root)
    win.title('Edit Record')
    win.geometry('500x500')
    win.resizable(width=False, height=True)

    frame = tk.Frame(win)
    frame.grid(row=0)

    # connect to database - table
    dbase = sq.connect('table.db')

    c = dbase.cursor()
    # create text entry boxes and labels
    tk.Label(frame, text='First Name:').grid(row=0)
    fn = tk.Entry(frame, width=30, relief='sunken', bd=3)
    fn.grid(row=0, column=1, padx=30)

    tk.Label(frame, text='Last Name:').grid(row=1)
    ln = tk.Entry(frame, width=30, relief='sunken', bd=3)
    ln.grid(row=1, column=1)

    tk.Label(frame, text='Address:').grid(row=2)
    addr = tk.Entry(frame, width=30, relief='sunken', bd=3)
    addr.grid(row=2, column=1)

    tk.Label(frame, text='City:').grid(row=3)
    city = tk.Entry(frame, width=30, relief='sunken', bd=3)
    city.grid(row=3, column=1)

    tk.Label(frame, text='State:').grid(row=4)
    state = tk.Entry(frame, width=30, relief='sunken', bd=3)
    state.grid(row=4, column=1)

    tk.Label(frame, text='Zipcode:').grid(row=5)
    zipcode = tk.Entry(frame, width=30, relief='sunken', bd=3)
    zipcode.grid(row=5, column=1)

    submit_btn = tk.Button(frame, text='SUBMIT', bg='green', fg='white', command=lambda: submit(event=None, old_window=win,
                                     entries=[fn, ln, addr, city, state, zipcode]))
    submit_btn.grid(row=6, columnspan=3, ipadx=120)

    tk.Button(frame, text='CANCEL', fg='red', bg='white', command=win.destroy).grid(row=7, columnspan=3, ipadx=120)

    # binding events
    fn.bind('<Return>', lambda event: ln.focus())
    ln.bind('<Return>', lambda event: addr.focus())
    addr.bind('<Return>', lambda event: city.focus())
    city.bind('<Return>', lambda event: state.focus())
    state.bind('<Return>', lambda event: zipcode.focus())
    zipcode.bind('<Return>', lambda event: submit_btn.focus())
    submit_btn.bind('<Return>', lambda event: submit(event=None, old_window=win,
                                     entries=[fn, ln, addr, city, state, zipcode]))
    submit_btn.bind('<Enter>', lambda event: submit_btn.config(bg='white'))  # when mouse hovers, button color changes to white
    submit_btn.bind('<Leave>', lambda event: submit_btn.config(bg='green'))  # when mouse leaves, button color returns to green

# create submit function
def submit(event, old_window: tk.Toplevel, entries: list):
    '''
    to submit and save enteries into addresses table
    in the table database
    :param event:
    :return:
    '''
    fn, ln, addr, city, state, zipcode = entries  # list of entries

    # connect to database - table.db
    dbase = sq.connect('table.db')

    # establish cursor to execute query
    c = dbase.cursor()

    # query tables in connected database
    c.execute('INSERT INTO addresses VALUES (:fname, :lname, :address, :city, :state, :zipcode)',
             {
                'fname': fn.get().capitalize(),
                'lname': ln.get().capitalize(),
                'address': addr.get().title(),
                'city': city.get().title(),
                'state': state.get().title(),
                'zipcode': zipcode.get()
             })

    if not(messagebox.askyesno(message=f'Do You Want To Insert record:\n'
                                       f'First name: {fn.get().capitalize()},\n'
                                       f'Last name: {ln.get().capitalize()}\n'
                                       f'Address: {addr.get().title()}\n'
                                       f'City: {city.get().title()}\n'
                                       f'State: {state.get().title()}\n'
                                       f'Zipcode: {zipcode.get()}?')):  # user decides not to save changes
        messagebox.showinfo(message='Deletion Aborted!')
        # close database
        dbase.close()
        old_window.destroy()  # edit window is destroyed
        return add_rec(event=None)

    # save changes made to database
    dbase.commit()

    # close database
    dbase.close()

    # clear the entry boxes
    fn.delete(0, 'end')
    ln.delete(0, 'end')
    addr.delete(0, 'end')
    city.delete(0, 'end')
    state.delete(0, 'end')
    zipcode.delete(0, 'end')

def show_rec(event):
   win = tk.Toplevel(root)
   win.title('Database Viewer')
   win.geometry('600x300')
   win.resizable(width=False, height=True)

   frame = tk.Frame(win)
   frame.grid(row=0)
   # frame.rowconfigure(list(range(5)))
   # frame.columnconfigure(list(range(5)))

   # connect to database
   dbase = sq.connect('table.db')

   # cursor for commands
   c = dbase.cursor()

   # query the database
   c.execute('''SELECT *, oid
            FROM addresses
   ''')
   q = c.fetchall()  # list of tuples - records
   # print(q)
   current_rec = []
   record = 'id,\tfirst_name,\tlast_name,\taddress,\tcity,\tstate,\tzipcode\n'
   for rec in q:
      fname, lname, addr, city, state, zipcode, oid = rec  # unpack the record
      current_rec.append({'first_name': fname, 'last_name': lname, 'address': addr, 'city': city, 'state': state, 'zipcode': zipcode})
      record += f'{oid},\t{fname},\t{lname},\t{addr[:6]},\t{city},\t{state},\t{zipcode}\n'
   df = pd.DataFrame(current_rec)
   print(df)
   tk.Label(frame, text=record).grid(row=0, columnspan=5, sticky='nsew')

   tk.Button(frame, text='Close Window', bg='red', fg='white', command=win.destroy).grid(row=4, ipadx=200)

   # close database
   dbase.close()

def updater(old_window, entries, selected_id):
   # print(entries)
   fname, lname, addr, city, state, zipcode = entries

   dbase = sq.connect('table.db')

   c = dbase.cursor()

   c.execute('''UPDATE addresses SET 
            first_name = ?,
            last_name = ?,
            address = ?,
            city = ?,
            state = ?,
            zip_code = ?
            WHERE oid = ?''',
             [
                fname.capitalize(),
                lname.capitalize(),
                addr.title(),
                city.title(),
                state.title(),
                zipcode,
                selected_id
              ])

   if not(messagebox.askyesno(message='Do You Want To Save Changes?')):  # user decides not to save changes
      messagebox.showinfo(message='Changes Not Saved!')
      return old_window.destroy()  # edit window is destroyed

   dbase.commit()
   messagebox.showinfo(message='Changes Saved!')

   dbase.close()
   old_window.destroy()

def edited(old_window, selected_id):
   old_window.destroy()

   win = tk.Toplevel(root)
   win.title('Edit Record')
   win.geometry('400x500')
   win.resizable(width=False, height=True)

   frame = tk.Frame(win)
   frame.grid(row=0)

   dbase = sq.connect('table.db')

   c = dbase.cursor()

   c.execute(f'SELECT * FROM addresses WHERE oid={selected_id}')
   q = c.fetchall()
   print(q)
   for rec in q:
      f, l, a, c, s, z = rec

   # create text entry boxes and labels
   tk.Label(frame, text='First Name:').grid(row=0)
   fn = tk.Entry(frame, width=30, relief='sunken', bd=3)
   fn.insert(0, f)
   fn.grid(row=0, column=1, padx=30)

   tk.Label(frame, text='Last Name:').grid(row=1)
   ln = tk.Entry(frame, width=30, relief='sunken', bd=3)
   ln.insert(0, l)
   ln.grid(row=1, column=1)

   tk.Label(frame, text='Address:').grid(row=2)
   addr = tk.Entry(frame, width=30, relief='sunken', bd=3)
   addr.insert(0, a)
   addr.grid(row=2, column=1)

   tk.Label(frame, text='City:').grid(row=3)
   city = tk.Entry(frame, width=30, relief='sunken', bd=3)
   city.insert(0, c)
   city.grid(row=3, column=1)

   tk.Label(frame, text='State:').grid(row=4)
   state = tk.Entry(frame, width=30, relief='sunken', bd=3)
   state.insert(0, s)
   state.grid(row=4, column=1)

   tk.Label(frame, text='Zipcode:').grid(row=5)
   zipcode = tk.Entry(frame, width=30, relief='sunken', bd=3)
   zipcode.insert(0, z)
   zipcode.grid(row=5, column=1)

   tk.Button(frame, text='SAVE', bg='green', fg='white',
             command=lambda: updater(win, entries=[fn.get(), ln.get(), addr.get(), city.get(), state.get(), zipcode.get()], selected_id=selected_id)).grid(row=6, columnspan=3, ipadx=120)
   tk.Button(frame, text='CANCEL', fg='red', bg='white', command=win.destroy).grid(row=7, columnspan=3, ipadx=120)

def edit_rec(event):
   win = tk.Toplevel(root)
   win.title('Edit Record')
   win.geometry('800x500')
   win.resizable(width=False, height=True)

   frame = tk.Frame(win)
   frame.grid(row=0)

   # connect to database - table
   dbase = sq.connect('table.db')

   c = dbase.cursor()

   c.execute('SELECT *, oid FROM addresses')
   q = c.fetchall()
   # print(q)
   st = scrolledtext.ScrolledText(frame, bg='brown', fg='white', width=95)
   st.grid(row=0, columnspan=5, pady=4, sticky='nsew')
   st.insert('end', 'ID;\tFIRST_NAME;\tLAST_NAME;\tADDRESS;\tCITY;\tSTATE;\tZIPCODE\n\n')
   r_ids = []
   for rec in q:
      fn, ln, addr, c, s, z, oid = rec
      r_ids.append(oid)
      st.insert('end', f'{oid};\t{fn};\t{ln};\t{addr};\t{c};\t{s};\t{z}\n')

   st.config(state='disabled')
   st.bind('<Enter>', lambda event: st.focus)

   tk.Label(frame, text='Edit Row ID:').grid(row=1, sticky='e')
   editCbox = ttk.Combobox(frame, width=3, values=r_ids, state='readonly')
   editCbox.set(r_ids[0])
   editCbox.grid(row=1, column=1, sticky='w')

   tk.Button(frame, text='Edit', bg='purple', fg='white', command=lambda: edited(win, editCbox.get())).grid(row=1, ipadx=20, column=2, sticky='w')

   tk.Button(frame, text='CANCEL', bg='red', fg='white', command=win.destroy).grid(row=2, column=0, columnspan=3, ipadx=300)

   dbase.commit()
   dbase.close()

def deleted(old_window, selected_id):
    # db connection
    dbase = sq.connect('table.db')
    # cursor to run query
    c = dbase.cursor()
    # run delete query
    c.execute(f'DELETE from addresses WHERE oid={selected_id}')

    if not(messagebox.askyesno(message=f'Do You Want To Delete record {selected_id}?')):  # user decides not to save changes
        messagebox.showinfo(message='Deletion Aborted!')
        # close database
        dbase.close()
        old_window.destroy()  # edit window is destroyed
        return delete_rec(event=None)

    # save changes to database
    dbase.commit()
    # close database
    dbase.close()
    # notification of deletion
    messagebox.showinfo(message=f'Record {selected_id} Has Been Deleted')
    old_window.destroy()

    delete_rec(event=None)

def delete_rec(event):
   # unique window for deletion
   win = tk.Toplevel(root)
   win.title('Delete Record')
   win.geometry('600x300')
   win.resizable(width=False, height=True)

   frame = tk.Frame(win)
   frame.grid(row=0)

   # connect to database
   dbase = sq.connect('table.db')
   # cursor
   c = dbase.cursor()

   # query the database
   c.execute('''SELECT *, oid
               FROM addresses
      ''')
   q = c.fetchall()  # list of tuples - records
   # print(q)
   current_rec = []
   record = 'id,\tfirst_name,\tlast_name,\taddress,\tcity,\tstate,\tzipcode\n'
   for rec in q:
      fname, lname, addr, city, state, zipcode, oid = rec  # unpack the record
      # current_rec.append(
      #    {'first_name': fname, 'last_name': lname, 'address': addr, 'city': city, 'state': state, 'zipcode': zipcode})
      record += f'{oid},\t{fname},\t{lname},\t{addr[:6]},\t{city},\t{state},\t{zipcode}\n'
   # df = pd.DataFrame(current_rec)
   # print(df)
   tk.Label(frame, text=record).grid(row=0, rowspan=3, columnspan=5, sticky='nsew')

   # list of available row ids
   c.execute('SELECT oid from addresses')
   r_ids = [*c.fetchall()]
   print(r_ids)

   # create a delete entry and label
   tk.Label(frame, text='Select Row ID:').grid(row=5, sticky='e')
   dCbox = ttk.Combobox(frame, width=5, state='readonly', values=r_ids)
   dCbox.set(r_ids[0])
   dCbox.grid(row=5, column=1, sticky='w')

   # query database
   tk.Button(frame, text='Delete', fg='red', command=lambda: deleted(win, dCbox.get())).grid(row=5, column=2, sticky='w')

   tk.Button(frame, text='Close Window', bg='red', fg='white', command=win.destroy).grid(row=6, columnspan=5, pady=2, ipadx=200)

   win.bind_class('tk.Button', '<Enter>', lambda event: tk.Button.config(bg='yellow'))
   win.bind_class('tk.Button', '<Leave>', lambda event: tk.Button.config(bg='SystemButtonFace'), add='+')

   # save changes to database
   dbase.commit()

   # close database
   dbase.close()

def on_enter2(event):
   query_btn.config(bg='yellow')

def on_leave2(event):
   query_btn.config(bg='brown')

# submit button
add_btn = tk.Button(frame, text='Add Record To Database', bg='green', fg='black', command=lambda: add_rec(event=None))
add_btn.grid(row=6, columnspan=2, padx=10, pady=10, ipadx=100)

query_btn = tk.Button(frame, text='Show Records', bg='purple', fg='black', command=lambda: show_rec(event=None))
query_btn.grid(row=7, columnspan=2, padx=10, pady=10, ipadx=120)

edit_btn = tk.Button(frame, text='Edit Records', bg='purple', fg='black', command=lambda: edit_rec(event=None))
edit_btn.grid(row=9, columnspan=2, padx=10, pady=10, ipadx=120)

del_btn = tk.Button(frame, text='Delete Records', bg='red', fg='black', command=lambda: delete_rec(event=None))
del_btn.grid(row=11, columnspan=2, padx=10, pady=10, ipadx=120)

query_btn.bind('<Enter>', on_enter2)
query_btn.bind('<Leave>', on_leave2)
edit_btn.bind('<Enter>', lambda event: edit_btn.config(bg='yellow'))
edit_btn.bind('<Leave>', lambda event: edit_btn.config(bg='purple'))
del_btn.bind('<Enter>', lambda event: del_btn.config(bg='yellow'))
del_btn.bind('<Leave>', lambda event: del_btn.config(bg='red'))


# close connection
conn.close()

root.mainloop()