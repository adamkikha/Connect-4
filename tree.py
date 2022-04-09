from concurrent.futures import thread
from threading import Thread
import tkinter
from PIL import ImageTk, Image
from tkinter import Frame, Label, Tk
from graphviz import Digraph


# responsible for drawing trees
class Tree:
    
    # seperate thread for tree window mainloop
    class drawer(Thread):
        def __init__(self,tk : Tk,img):
            super().__init__()
            self.tk = tk
            self.img = img
            
        def run(self) -> None:
            while True:
                self.tk.update()
                self.tk.update_idletasks()
    
    # class variable with a refrence for current tree window
    current_tk = None
    
    def __init__(self, states):
        self.graph = Digraph()
        self.png_name = 'states_tree'
        self.extension = 'png'
        self.create_tree(states)
        self.save_tree()
        
    # creates tree from parent map
    def create_tree(self,dic : dict):
        for parent , value in dic.items():
            label = "min\n"+value[0]
            if value[2]:
                label = "max\n"+value[0]
            self.graph.node(parent,label)
            for child in value[1]:
                # self.graph.node(child[2],child[0])
                self.graph.edge(parent,child[2],child[1])
    
    # saves the graph in an image    
    def save_tree(self):
        self.graph.format = self.extension
        tree = self.graph.unflatten(stagger=3)
        tree.render(self.png_name)
    
    # displays the tree in a seperate window
    def display(self,image_name):
        tree_screen = tkinter.Toplevel()
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
        thread = Tree.drawer(tree_screen,img)
        thread.start()   
    