from tkinter import ttk
from tkinter import *

import sqlite3

# Main program
class Product:

    db_name = 'Wharehouse.db'

    def __init__(self, windows):
        self.wind = windows
        self.wind.title('Almacen de Electronicos')
    # Main container
        frame = LabelFrame(self.wind, text='Ingreso de productos')
        frame.grid(row=0, column=0, columnspan=3, pady=20)
    # Input product, price
        Label(frame, text='Producto: ').grid(row=1, column=0)
        self.product = Entry(frame)
        self.product.focus()
        self.product.grid(row=1, column=1)
        Label(frame, text='Precio: ').grid(row=2, column=0)
        self.price = Entry(frame)
        self.price.grid(row=2, column=1)
    # Buttons  Add, Update, Delete
        ttk.Button(frame, text='Agregar', command=self.add_product).grid(row=3, columnspan=2, sticky=W + E)
        ttk.Button(frame, text='Actualizar', command=self.update_product).grid(row=4, columnspan=2, sticky=W + E)
        ttk.Button(frame, text='Eliminar', command=self.delete_product).grid(row=5, columnspan=2, sticky=W + E)
    # Products: Table, Header
        self.tree = ttk.Treeview(height=10, columns=2)
        self.tree.grid(row=4, column=0, columnspan=2)
        self.tree.heading('#0', text='Producto', anchor=CENTER)
        self.tree.heading('#1', text='Precio', anchor=CENTER)
        self.get_product()
     # Output message
        self.message = Label(text='', fg='green')
        self.message.grid(row=3, column=0, columnspan=2, sticky=W + E)
    # dB validation insert data
    def validation(self):
        return len(self.product.get()) != 0 and len(self.price.get()) != 0
    # dB Conection
    def run_query(self, query, parameters=()):
        with sqlite3.connect(self.db_name) as conx:
            cursor = conx.cursor()
            result = cursor.execute(query, parameters)
            conx.commit()
        return result
    # dB Query product
    def get_product(self):
        # Cleaning table
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        # Query data
        query = 'SELECT * FROM products ORDER BY product DESC '
        db_rows = self.run_query(query)
        for row in db_rows:
            self.tree.insert('', 0, text=row[1], values=row[2])
    # dB Add produrct
    def add_product(self):
        if self.validation():
            query = 'INSERT INTO products VALUES(NULL, ?, ?)'
            parameters = (self.product.get(), self.price.get())
            self.run_query(query, parameters)
            self.message['text'] = 'Producto: {}, agregado correctamente'.format(self.product.get())
            self.product.delete(0, END)
            self.price.delete(0, END)
        else:
            self.message['text'] = 'Se requiere precio y producto para agregar'
        self.get_product()
    # dB Delete product
    def delete_product(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]
        except IndexError as e:
            self.message['text'] = 'Selecciona un registro, para eliminar'
            return
        self.message['text'] = ''
        product = self.tree.item(self.tree.selection())['text'] # name
        query = 'DELETE FROM products WHERE product = ?'
        self.run_query(query, (product, ))
        self.message['text'] = 'Registro: {}, borrado exitosamente.'.format(product)
        self.get_product()
    # db Update product
    def update_product(self
                      
                      ):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'Selecciona un registro, para actualizar'
            return
        product = self.tree.item(self.tree.selection())['text'] #name
        price = self.tree.item(self.tree.selection())['values'][0] # old_price
        self.edit_wind = Toplevel()
        self.edit_wind.title('Actualización de productos')
    # Old Product
        Label(self.edit_wind, text='Producto: ').grid(row=0, column=1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = product), state='readonly').grid(row = 0, column = 2)
    # New Product
        Label(self.edit_wind, text='Nuevo: ').grid(row = 1, column = 1)
        new_product = Entry(self.edit_wind)
        new_product.grid(row=1, column = 2)
    # Old Price
        Label(self.edit_wind, text='Precio: ').grid(row=2, column=1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = price), state='readonly').grid(row = 2, column = 2)
    # New Price
        Label(self.edit_wind, text='Nuevo: ').grid(row = 3, column = 1)
        new_price = Entry(self.edit_wind)
        new_price.grid(row = 3, column = 2)
    # Button edit produtc
        Button(self.edit_wind, text='Actualizar', command = lambda: self.edit_records(new_product.get(), product, new_price.get(), price)).grid(row = 4, column = 2, sticky = W + E)
    # Edti produtcs
    def edit_records(self, new_product, product,  new_price, price):
        query = 'UPDATE products SET product = ?, price = ? WHERE product = ? AND price = ?'
        parameters = (new_product, new_price, product, price)
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.message['text'] = 'Registro: {}, actualizado correctamente.'.format(product)
        self.get_product()

if __name__ == "__main__":
    windows = Tk()
    application = Product(windows)
    windows.mainloop()
