import tkinter as tk

class ArrayStack:
    def __init__(self): self.stack = []

    def size(self): return len(self.stack)
    
    def is_empty(self): return self.size() == 0
    
    def push(self, item): self.stack.append(item)

    def pop(self): 
        if self.is_empty(): return None
        return self.stack.pop(-1)
    
    def peek(self): 
        if self.is_empty(): return None
        return self.stack[-1]
    
class ArrayQueue:
    def __init__(self): self.queue = []

    def size(self): return len(self.queue)
    
    def is_empty(self): return self.size() == 0
    
    def enqueue(self, item): self.queue.append(item)

    def dequeue(self): 
        if self.is_empty(): return None
        return self.queue.pop(0)
    
    def peek(self): 
        if self.is_empty(): return None
        return self.queue[0]
    
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
    
class LinkedListStack:
    def __init__(self):
        self.top = None
        self.len = 0

    def size(self): return self.len
    
    def is_empty(self): return self.top is None
    
    def push(self, item):
        new_node = Node(item)
        new_node.next = self.top
        self.top = new_node
        self.len += 1

    def pop(self):
        if self.is_empty(): return None
        popped_value = self.top.value
        self.top = self.top.next
        self.len -= 1
        return popped_value

    def peek(self):
        if self.is_empty(): return None
        return self.top.value
    
class LinkedListQueue:
    def __init__(self):
        self.front = self.rear = None
        self.len = 0

    def size(self): return self.len
        
    def is_empty(self): return self.front is None
        
    def enqueue(self, item):
        new_node = Node(item)
        if self.rear is not None: 
            self.rear.next = new_node
        else: 
            self.front = new_node
        self.rear = new_node
        self.len += 1

    def dequeue(self):
        if self.is_empty(): return None
        dequeued_value = self.front.value
        self.front = self.front.next
        self.len -= 1
        if self.front is None: self.rear = None
        return dequeued_value

    def peek(self): 
        if self.is_empty(): return None
        return self.front.value

class Dish:
    def __init__(self, name, category, price):
        self.name = name
        self.category = category
        self.price = price

class RestaurantSystem:
    def __init__(self):
        self.menu = []
        self.categories = ["Rice meals", "Noodles", "Drinks"]

        self.cart = []

        self.back_stack = ArrayStack()
        self.order_queue = ArrayQueue()

        self.current_screen = "home"
        self.current_category = None

        self.next_order_id = 1
        self.current_order = None

    # -------------------------
    # Basic helper methods
    # -------------------------

    def clear_window(self, root):
        for widget in root.winfo_children(): widget.destroy()

    def add_dish_to_menu(self, name, category, price):
        self.menu.append(Dish(name, category, price))

    def get_dishes_by_category(self, category):
        dishes = []
        for dish in self.menu:
            if dish.category == category: dishes.append(dish)
        return dishes
    
    def save_current(self):
        self.back_stack.push({'screen': self.current_screen, 'category': self.current_category})

    def go_back(self, root):
        if self.back_stack.is_empty(): return
        previous = self.back_stack.pop()
        self.go_to(root, previous['screen'], previous['category'], save_history=False)

    def go_to (self, root, screen, category=None, save_history=True):
        if save_history: self.save_current()

        if screen == "home": self.show_home(root)
        elif screen == "customer": self.show_customer_interface(root)
        elif screen == "categories": self.show_categories(root)
        elif screen == "dishes": self.show_dishes(root, category)
        elif screen == "cart": self.show_cart(root)
        
    # -------------------------
    # Home screen
    # -------------------------

    def show_home(self, root):
        self.clear_window(root)
        self.current_screen = "home"
        self.current_category = None

        tk.Label(root, text='You are a').pack()
        tk.Button(root, text='Customer', command=lambda: self.go_to(root, 'customer')).pack()
        tk.Button(root, text="Restaurant Staff", command=lambda: self.show_staff_interface(root)).pack()

    # -------------------------
    # Customer home screen
    # -------------------------

    def show_customer_interface(self, root):
        self.clear_window(root)
        self.current_screen = 'customer'
        self.current_category = None

        tk.Button(root, text='Menu', command=lambda: self.go_to(root, 'categories')).pack()
        tk.Button(root, text='Cart', command=lambda: self.go_to(root, 'cart')).pack()
        tk.Button(root, text='Back', command=lambda: self.go_back(root)).pack()

    # -------------------------
    # Categories screen
    # -------------------------

    def show_categories(self, root):
        self.clear_window(root)
        self.current_screen = 'categories'
        self.current_category = None

        for category in self.categories:
            tk.Button(root, text=f'{category}', command=lambda c=category: self.go_to(root, 'dishes', c)).pack()
        tk.Button(root, text='Back', command=lambda: self.go_back(root)).pack()
        
    # -------------------------
    # Dishes screen
    # -------------------------

    def show_dishes(self, root, category):
        self.clear_window(root)
        self.current_screen = "dishes"
        self.current_category = category

        tk.Label(root, text=f'{category}').grid(row=0, column=0)
        dishes = self.get_dishes_by_category(category)

        row = 1
        for dish in dishes:
            tk.Label(root, text=f'{dish.name} - {dish.price} VND').grid(row=row, column=0)
            tk.Button(root, text='Add to cart', command=lambda d=dish: self.show_add_to_cart(d)).grid(row=row, column=1)
            row += 1
        tk.Button(root, text='Cart', command=lambda: self.go_to(root, 'cart')).grid(row=row, column=0)
        tk.Button(root, text='Back', command=lambda: self.go_back(root)).grid(row=row, column=1)
        
    # -------------------------
    # Add to cart popup
    # -------------------------

    def show_add_to_cart(self, dish):
        popup = tk.Toplevel()
        popup.title("Add to Cart")
        popup.geometry("200x150")

        quantity = tk.IntVar(value=1)
        def increase(): quantity.set(quantity.get() + 1)
        def decrease(): 
            if quantity.get() > 1: quantity.set(quantity.get() - 1)

        tk.Label(popup, text=f'{dish.name} - {dish.price}').grid(row=0, column=0)
        tk.Label(popup, textvariable=quantity).grid(row=0, column=2)
        tk.Button(popup, text='+', command=increase).grid(row=0, column=1)
        tk.Button(popup, text='-', command=decrease).grid(row=0, column=3)

        tk.Label(popup, text="Note").grid(row=1, column=0) 
        note_entry = tk.Entry(popup)
        note_entry.grid(row=2, column=0)

        note_stack = ArrayStack()
        note_stack.push('')
        note_entry.bind('<KeyRelease-space>', lambda event: note_stack.push(note_entry.get().strip()))

        def undo_text():
            if note_stack.size() <= 1: 
                note_entry.delete(0, tk.END)
                return
            note_stack.pop()
            note_entry.delete(0, tk.END)
            note_entry.insert(tk.INSERT, note_stack.peek())
        tk.Button(popup, text='Undo', command=undo_text).grid(row=2, column=1)

        def confirm():
            self.cart.append({'dish': dish, 'quantity': quantity.get(), 'note': note_entry.get()})
            popup.destroy()
        tk.Button(popup, text='OK', command=confirm).grid(row=3, column=0)

    # -------------------------
    # Cart screen
    # -------------------------

    def show_cart(self, root):
        self.clear_window(root)
        self.current_screen = "cart"
        self.current_category = None

        def remove_from_cart(index):
            del self.cart[index]
            self.show_cart(root)

        tk.Label(root, text='Dish').grid(row=0, column=0)
        tk.Label(root, text='Qty').grid(row=0, column=1)
        tk.Label(root, text='Note').grid(row=0, column=2)
        tk.Label(root, text='Subtotal').grid(row=0, column=3)

        if len(self.cart) == 0: 
            tk.Label(root, text="Cart is empty.").grid(row=1, column=0)
            button_row = 2
        else:
            total = 0
            row = 1
            for index, item in enumerate(self.cart):
                dish, quantity, note = item['dish'], item['quantity'], item['note']
                subtotal = dish.price * quantity
                total += subtotal

                tk.Label(root, text=dish.name).grid(row=row, column=0)
                tk.Label(root, text=quantity).grid(row=row, column=1)
                tk.Label(root, text=note).grid(row=row, column=2)
                tk.Label(root, text=subtotal).grid(row=row, column=3)
                tk.Button(root, text='Remove', command=lambda i=index: remove_from_cart(i)).grid(row=row, column=4)
                row += 1

            tk.Label(root, text=f'Total: {total} VND').grid(row=row, column=0)
            tk.Button(root, text='Confirm order', command=lambda: self.confirm_order(root)).grid(row=row+1, column=0)
            button_row = row+2

        tk.Button(root, text='Back', command=lambda: self.go_back(root)).grid(row=button_row, column=0)

    # -------------------------
    # Confirm order
    # -------------------------

    def confirm_order(self, root):
        order = {'id': self.next_order_id, 'items': self.cart.copy()}
        self.order_queue.enqueue(order)
        self.cart.clear()
        self.show_cart(root)
        self.next_order_id += 1

        popup = tk.Toplevel()
        popup.geometry("200x150")
        tk.Label(popup, text=f"Order #{order['id']} has been sent to the restaurant.").pack()
        tk.Button(popup, text='OK', command=popup.destroy).pack()
        
    # -------------------------
    # Restaurant staff interface
    # -------------------------

    def show_staff_interface(self, root):
        self.clear_window(root)
        tk.Button(root, text='Next order', command=lambda: self.prepare_next_order(root)).pack()
        tk.Button(root, text='Back', command=lambda: self.go_to(root, 'home')).pack()

    def prepare_next_order(self, root):
        self.clear_window(root)
        if self.order_queue.is_empty():
            tk.Label(root, text='No order waiting.').grid(row=0, column=0)
            tk.Button(root, text='Back', command=lambda: self.show_staff_interface(root)).grid(row=0, column=1)
            return
        
        next_order = self.order_queue.dequeue()
        tk.Label(root, text=f"Order #{next_order['id']}").grid(row=0, column=0)
        tk.Label(root, text='Dish').grid(row=1, column=0)
        tk.Label(root, text='Qty').grid(row=1, column=1)
        tk.Label(root, text='Note').grid(row=1, column=2)

        row = 2
        for index, item in enumerate(next_order['items']):
            dish, quantity, note = item['dish'], item['quantity'], item['note']
            tk.Label(root, text=dish.name).grid(row=row, column=0)
            tk.Label(root, text=quantity).grid(row=row, column=1)
            tk.Label(root, text=note).grid(row=row, column=2)
            row += 1
        tk.Button(root, text='Done', command=lambda: self.show_staff_interface(root)).grid(row=row, column=0)

def main():
    system = RestaurantSystem()
    system.add_dish_to_menu("Chicken Rice", "Rice meals", 45000)
    system.add_dish_to_menu("Beef Rice", "Rice meals", 55000)
    system.add_dish_to_menu("Beef Noodles", "Noodles", 50000)
    system.add_dish_to_menu("Seafood Noodles", "Noodles", 60000)
    system.add_dish_to_menu("Iced Tea", "Drinks", 15000)
    system.add_dish_to_menu("Milk Tea", "Drinks", 30000)

    root = tk.Tk()
    root.geometry('400x300')
    root.title('Restaurant Application')
    system.show_home(root)
    root.mainloop()

main()
    





        


        
    
    

    
    
