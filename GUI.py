import tkinter as tk
from PIL import Image, ImageTk
from formal_eq import *

# Create a window
window = tk.Tk()
window.title("ROBDD")
window.geometry("400x200")  # set the window dimensions to 400x200 pixels

#!test Case #1:
#( ( a & b ) | ( b & c ) ) | ( a & c )  
#( a & b ) | ( c & ( a ^ b ) )


#!test Case #2:
#( a & b ) | ( ! a & c )  
# ( a & b ) | (  b & c )


# Create two input entries with labels
tk.Label(window, text="Input 1:").grid(row=0, column=0)
input1_entry = tk.Entry(window)
input1_entry.grid(row=0, column=1)

tk.Label(window, text="Input 2:").grid(row=1, column=0)
input2_entry = tk.Entry(window)
input2_entry.grid(row=1, column=1)

# Define a function to print the input values
def Run_BtnFunc():
    input_str = input1_entry.get()
    input_str_2 = input2_entry.get()
    # #input_str = " ( ( ! a & ( ! b & ! c ) ) | ( a & b ) )  | ( b & c ) \n"
    # input_str = " a & ( b & c ) \n"
    # input_str_2 = " ( a | 0 ) & ( b & c ) \n" # another function to test the eq checking
   
    
    Order=('a','b','c') # you should extracted the var from the input string or ask the user to enter the order he/she wants
    index=0
    input_tokens = input_str.split()
    input_tokens=search_for_one_zero(input_tokens)
    parsetree, index = parse(input_tokens)
    print(parsetree)
    start,index=BDDNode.ConstructBDD(parsetree,Order)
    start=BDDNode.BDDRed(start)
    
    index=0
    input_tokens = input_str_2.split()
    input_tokens=search_for_one_zero(input_tokens)
    parsetree_2, index = parse(input_tokens)
    start_2,index=BDDNode.ConstructBDD(parsetree_2,Order)
    start_2=BDDNode.BDDRed(start_2)
    print(parsetree_2)
    
    if BDDNode.check_Eq(start,start_2):
        print("The two circuits are equivalent")
        message = "The two circuits are equivalent"

    else:
        print("The two circuits are NOT equivalent")
        message = "The two circuits are NOT equivalent"

    result_label.config(text=message)  # update the label with the message

    bdd = graphviz.Digraph()
    bdd.node(str(start), label = start.GetName(), shape="circle")
    bdd = BDDNode.display_BDD(start,bdd)
    bdd.render("Circuit 1", format="png")
    
    bdd = graphviz.Digraph()
    bdd.node(str(start_2), label = start_2.GetName(), shape="circle")
    bdd = BDDNode.display_BDD(start_2,bdd)
    bdd.render("Circuit 2", format="png")
        

# Create a button to print the input values
print_button = tk.Button(window, text="Run", command=Run_BtnFunc)
print_button.grid(row=2, column=0)

# Define a function to display an image
def display_image1():
    image = Image.open("Circuit 1.png")
    image.show()

# Define a function to display an image
def display_image2():
    image = Image.open("Circuit 2.png")
    image.show()

# Create a button to display an image
image_button = tk.Button(window, text="Display Image Circuit 1", command=display_image1)
image_button.grid(row=2, column=1)

# Create a button to display an image
image_button = tk.Button(window, text="Display Image Circuit 2", command=display_image2)
image_button.grid(row=4, column=1)

# Create a label to display the result message
result_label = tk.Label(window, text="", font=("Arial", 16))
result_label.grid(row=3, column=0, columnspan=2)

# Start the GUI

window.mainloop()
