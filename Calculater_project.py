# Import tkinter to build the graphical user interface (GUI):
import tkinter as tk

# Import math to perform mathematical operations such as roots and trigonometric functions:
import math

# Import re (Regular Expressions) to detect and transform mathematical patterns
# such as square roots and scientific functions into valid Python expressions:
import re


# =====================
# Calculation class
# =====================

class CalculatorEngine:

    def __init__(self, display):
        self.display = display
        self.last_answer = ""


    # =====================
    # Calculation function
    # =====================

    # Evaluates the mathematical expression entered by the user
    def calculate(self):
        try:
            expr = self.display.get()

            # Replace calculator symbols with Python operators
            expr = expr.replace("×", "*").replace("÷", "/")

            # ======== ADDED (Power handling) ========
            # Convert power symbol ^ into Python exponent operator **
            expr = expr.replace("^", "**")
            # =======================================

            # Handle general root format √(n,x):
                # Regex breakdown for general root format √(n, x):
    #  √\(      : matches the '√' symbol followed by an opening parenthesis
    #  \s*      :matches any optional whitespace before or after
    # ([^,]+)   : captures the first number (n) before the comma
    # \s*,\s*   : matches the comma separating the numbers, allowing spaces around it
    # ([^)]+)   :captures the second number (x) after the comma
    #  \s*\)    :matches any optional whitespace before the closing parenthesis

            expr = re.sub(
                r'√\(\s*([^,]+)\s*,\s*([^)]+)\s*\)',
                r'(\2 ** (1/\1))',
                expr
            )

            # Handle square root format √25:
                # Regex breakdown for square root format √number:
    #  √\(?       : matches the '√' symbol, optionally followed by an opening parenthesis
    #  ([0-9.]+)  : captures the number itself (can include decimal points)
    #  \)?        : optionally matches a closing parenthesis after the number
    # This allows the user to write both √25 and √(25), and both will be
    # correctly converted to math.sqrt(25) for evaluation in Python
            expr = re.sub(
                r'√\(?([0-9.]+)\)?',
                r'math.sqrt(\1)',
                expr
            )

            # Trigonometric functions (input in degrees)
            expr = re.sub(r'sin\(([^)]+)\)', r'math.sin(math.radians(\1))', expr)
            expr = re.sub(r'cos\(([^)]+)\)', r'math.cos(math.radians(\1))', expr)
            expr = re.sub(r'tan\(([^)]+)\)', r'math.tan(math.radians(\1))', expr)

            # Inverse trigonometric functions (output in degrees)
            expr = re.sub(r'asin\(([^)]+)\)', r'math.degrees(math.asin(\1))', expr)
            expr = re.sub(r'acos\(([^)]+)\)', r'math.degrees(math.acos(\1))', expr)
            expr = re.sub(r'atan\(([^)]+)\)', r'math.degrees(math.atan(\1))', expr)

            # Logarithmic function (base 10)
            # Regex breakdown for logarithm function log(x):
    # log\(       : matches the 'log(' literal in the input
    # ([^)]+)    : captures everything inside the parentheses (the argument x)
    # \)          : matches the closing parenthesis
    #
    # Replacement: math.log10(\1)
    # Converts the user input log(x) into Python's math.log10(x),
    #   which calculates the logarithm base 10.
    #
    # Example:
    # log(100) :math.log10(100) → 2: 
            
            expr = re.sub(r'log\(([^)]+)\)', r'math.log10(\1)', expr)

            # Evaluate the final expression
            result = eval(expr)

            # Save the result for the Ans button
            self.last_answer = str(result)

            # Display the result
            self.display.delete(0, tk.END)
            self.display.insert(0, result)

        except:
            # Display error message if calculation fails
            self.display.delete(0, tk.END)
            self.display.insert(0, "Error")

    def insert_ans(self):
        self.display.insert(tk.END, self.last_answer)
        


# =====================
# Input handling functions
# =====================

# Inserts the pressed button value into the display screen
def press(value):
    display.insert(tk.END, value)

# Clears the entire display screen
def clear_all():
    display.delete(0, tk.END)

# Clears the current entry (same as AC for simplicity)
def clear_entry():
    display.delete(0, tk.END)

# Deletes the last entered character from the display
def delete_last():
    text = display.get()
    display.delete(0, tk.END)
    display.insert(0, text[:-1])

# Inserts the value of pi (π) into the display
def insert_pi():
    display.insert(tk.END, str(math.pi))

# ======== ADDED (Power function) ========
# Inserts the power symbol (^) into the display for exponent calculations
def power():
    display.insert(tk.END, "^")
# =======================================



# =====================
# GUI window setup
# =====================

# Create the main calculator window
root = tk.Tk()
root.title("Scientific Calculator")
root.geometry("380x720")
root.resizable(False, False)

# Entry widget used as the calculator display screen
display = tk.Entry(
    root,
    font=("Arial", 24),
    justify="right",
    bd=10
)
display.grid(row=1, column=0, columnspan=4, padx=10, pady=10)

engine = CalculatorEngine(display)


# =====================
# Button creation helper
# =====================

# Creates and places a button on the calculator grid
def btn(text, r, c, cmd):
    tk.Button(
        root,
        text=text,
        font=("Arial", 14),
        width=6,
        height=2,
        command=cmd
    ).grid(row=r, column=c, padx=4, pady=4)
    
    
    
 
# =====================
# Top control buttons
# =====================

btn("AC", 2, 0, clear_all)
btn("C", 2, 1, clear_entry)
btn("DEL", 2, 2, delete_last)
btn("÷", 2, 3, lambda: press("÷"))



# =====================
# Numbers and basic operations
# =====================

buttons = [
    ("7",3,0), ("8",3,1), ("9",3,2), ("×",3,3),
    ("4",4,0), ("5",4,1), ("6",4,2), ("-",4,3),
    ("1",5,0), ("2",5,1), ("3",5,2), ("+",5,3),
]

for text, r, c in buttons:
    btn(text, r, c, lambda x=text: press(x))


# =====================
# Bottom row (zero, decimal, comma, equals)
# =====================

btn("0", 6, 0, lambda: press("0"))
btn(".", 6, 1, lambda: press("."))
btn(",", 6, 2, lambda: press(","))
btn("=", 10, 3, engine.calculate)


# =====================
# Roots, constants, and brackets
# =====================

btn("√", 7, 0, lambda: press("√"))
btn("π", 7, 1, insert_pi)
btn("(", 7, 2, lambda: press("("))
btn(")", 7, 3, lambda: press(")"))



# =====================
# Scientific functions
# =====================

btn("sin", 8, 0, lambda: press("sin("))
btn("cos", 8, 1, lambda: press("cos("))
btn("tan", 8, 2, lambda: press("tan("))
btn("log", 8, 3, lambda: press("log("))

btn("asin", 9, 0, lambda: press("asin("))
btn("acos", 9, 1, lambda: press("acos("))
btn("atan", 9, 2, lambda: press("atan("))
btn("Ans", 9, 3, engine.insert_ans)

# ======== ADDED (Power button) ========
btn("xʸ", 6, 3, power)
# =====================================
   
    




