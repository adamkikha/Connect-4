from concurrent.futures import thread
from threading import Thread
from PIL import ImageTk, Image
from tkinter import Frame, Label, Tk
from graphviz import Digraph



class Tree:
    class drawer(Thread):
        def __init__(self):
            super().__init__()
            self.tk = Tree.current_tk
            
        def run(self) -> None:
            self.tk.mainloop()
    
    current_tk = None
    def __init__(self, states):
        self.graph = Digraph()
        self.png_name = 'states_tree'
        self.extension = 'png'
        self.create_tree(states)
        self.save_tree()
        
    def create_tree(self,dic : dict):
        print(len(dic.items()))
        for parent , value in dic.items():
            self.graph.node(parent,value[0])
            for child in value[1]:
                self.graph.node(child[2],child[0])
                self.graph.edge(parent,child[2],child[1])
    
    def display(self,image_name):
        if Tree.current_tk is not None:
            Tree.current_tk.destroy()
        tree_screen = Tk()
        tree_screen.title("State Tree")
        tree_image = Image.open(image_name)
        tkimage = ImageTk.PhotoImage(tree_image)
        image_height = tkimage.height()
        image_width = tkimage.width()

        tree_screen.geometry(str(image_width) + "x" + str(image_height))
        frame = Frame(tree_screen, width = image_width, height = image_height)
        frame.pack()
        frame.place(anchor='center', relx=0.5, rely=0.5)
        frame.pack()
        img = ImageTk.PhotoImage(tree_image)
        label = Label(frame, image = img)
        label.pack()
        tree_screen.update()
        tree_screen.deiconify()
        Tree.current_tk = tree_screen
        thread = Tree.drawer()
        thread.start()   
        
    def save_tree(self):
        self.graph.format = self.extension
        tree = self.graph.unflatten(stagger=20)
        tree.render(self.png_name)
