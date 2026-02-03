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

