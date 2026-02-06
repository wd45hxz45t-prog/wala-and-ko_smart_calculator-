# Import tkinter to build the graphical user interface (GUI):
import tkinter as tk

# Import math to perform mathematical operations such as roots and trigonometric functions:
import math

# Import re (Regular Expressions) to detect and transform mathematical patterns
# such as square roots and scientific functions into valid Python expressions:
import re


# =====================
# Calculation Engine Class
# =====================

class CalculatorEngine:
    """
    Calculator Engine Class - Handles all mathematical calculations
    
    This class is responsible for:
    - Processing mathematical expressions entered by the user
    - Converting calculator symbols into Python-compatible operators
    - Handling advanced functions (roots, trigonometry, logarithms)
    - Storing the last calculated result for the Ans button
    - Displaying results or error messages on the screen
    """
    
    def __init__(self, display):
        """
        Initialize the Calculator Engine
        
        Parameters:
        -----------
        display : tk.Entry
            Reference to the calculator's display screen widget
            This allows the engine to read input and show results
        
        Attributes:
        -----------
        self.display : tk.Entry
            The display screen where expressions and results appear
        self.last_answer : str
            Stores the most recent calculation result
            Used by the "Ans" button to recall previous answers
        """
        self.display = display      # Reference to the display screen
        self.last_answer = ""       # Initialize empty (no previous calculation yet)
    
    
    # =====================
    # Main calculation method
    # =====================
    
    def calculate(self):
        """
        Evaluate the mathematical expression entered by the user
        
        This method performs the complete calculation process:
        1. Retrieves the expression from the display screen
        2. Converts calculator symbols to Python operators
        3. Transforms mathematical functions using regex
        4. Evaluates the final expression
        5. Displays the result or an error message
        
        Supported operations:
        ---------------------
        - Basic arithmetic: +, -, ×, ÷
        - Exponents: x^y (converted to x**y)
        - Square roots: √25 or √(25)
        - Nth roots: √(n,x) means nth root of x
        - Trigonometry: sin, cos, tan (input in degrees)
        - Inverse trig: asin, acos, atan (output in degrees)
        - Logarithm: log(x) base 10
        
        Error handling:
        ---------------
        If any error occurs during calculation (invalid syntax, 
        division by zero, domain errors, etc.), the display shows "Error"
        """
        try:
            # =====================
            # Step 1: Get expression from display
            # =====================
            
            # Retrieve the current text from the display screen
            # This is what the user has typed (e.g., "5×3+√25")
            expr = self.display.get()
            
            
            # =====================
            # Step 2: Replace calculator symbols with Python operators
            # =====================
            
            # Convert multiplication symbol × to Python's *
            # Convert division symbol ÷ to Python's /
            # Example: "5×3÷2" becomes "5*3/2"
            expr = expr.replace("×", "*").replace("÷", "/")
            
            
            # =====================
            # Step 3: Handle exponentiation (power)
            # =====================
            
            # Convert power symbol ^ into Python's exponent operator **
            # Example: "2^3" becomes "2**3" which evaluates to 8
            expr = expr.replace("^", "**")
            
            
            # =====================
            # Step 4: Handle general nth root format √(n,x)
            # =====================
            
            # Regex pattern breakdown for general root format √(n, x):
            # √\(        : matches the '√' symbol followed by an opening parenthesis
            # \s*        : matches any optional whitespace (spaces/tabs)
            # ([^,]+)    : captures the first number (n = root degree) before the comma
            #              [^,]+ means "one or more characters that are NOT a comma"
            # \s*,\s*    : matches the comma separating the numbers, with optional spaces
            # ([^)]+)    : captures the second number (x = number to take root of)
            #              [^)]+ means "one or more characters that are NOT a closing parenthesis"
            # \s*\)      : matches any optional whitespace before the closing parenthesis
            #
            # Replacement: (\2 ** (1/\1))
            # Mathematical formula: nth root of x = x^(1/n)
            # \2 refers to the second captured group (x)
            # \1 refers to the first captured group (n)
            #
            # Example:
            # √(3,27) → (27 ** (1/3)) → 3.0 (cube root of 27)
            # √(2,16) → (16 ** (1/2)) → 4.0 (square root of 16)
            
            expr = re.sub(
                r'√\(\s*([^,]+)\s*,\s*([^)]+)\s*\)',
                r'(\2 ** (1/\1))',
                expr
            )
            
            
            # =====================
            # Step 5: Handle square root format √25 or √(25)
            # =====================
            
            # Regex pattern breakdown for square root format √number:
            # √\(?       : matches the '√' symbol, optionally followed by opening parenthesis
            #              \(? means "zero or one opening parenthesis"
            # ([0-9.]+)  : captures the number itself
            #              [0-9.]+ means "one or more digits or decimal points"
            #              This allows both integers (25) and decimals (25.5)
            # \)?        : optionally matches a closing parenthesis after the number
            #
            # Replacement: math.sqrt(\1)
            # Converts to Python's square root function
            # \1 refers to the captured number
            #
            # This pattern allows flexible input:
            # √25   → math.sqrt(25)   → 5.0
            # √(25) → math.sqrt(25)   → 5.0
            # √9.5  → math.sqrt(9.5)  → 3.082...
            
            expr = re.sub(
                r'√\(?([0-9.]+)\)?',
                r'math.sqrt(\1)',
                expr
            )
            
            
            # =====================
            # Step 6: Handle trigonometric functions (input in degrees)
            # =====================
            
            # Python's math.sin, math.cos, math.tan work with radians
            # But calculators typically use degrees for user convenience
            # So we convert: degrees → radians → calculate → result
            
            # Sine function: sin(angle_in_degrees)
            # Pattern: sin\(([^)]+)\) captures everything inside sin(...)
            # Replacement: math.sin(math.radians(\1))
            # Example: sin(30) → math.sin(math.radians(30)) → 0.5
            expr = re.sub(r'sin\(([^)]+)\)', r'math.sin(math.radians(\1))', expr)
            
            # Cosine function: cos(angle_in_degrees)
            # Example: cos(60) → math.cos(math.radians(60)) → 0.5
            expr = re.sub(r'cos\(([^)]+)\)', r'math.cos(math.radians(\1))', expr)
            
            # Tangent function: tan(angle_in_degrees)
            # Example: tan(45) → math.tan(math.radians(45)) → 1.0
            expr = re.sub(r'tan\(([^)]+)\)', r'math.tan(math.radians(\1))', expr)
            
            
            # =====================
            # Step 7: Handle inverse trigonometric functions (output in degrees)
            # =====================
            
            # Python's math.asin, math.acos, math.atan return radians
            # But we want to display the result in degrees
            # So we convert: calculate in radians → convert to degrees → result
            
            # Inverse sine (arcsin): asin(value) returns angle in degrees
            # Pattern: asin\(([^)]+)\) captures the value inside asin(...)
            # Replacement: math.degrees(math.asin(\1))
            # Example: asin(0.5) → math.degrees(math.asin(0.5)) → 30.0 degrees
            expr = re.sub(r'asin\(([^)]+)\)', r'math.degrees(math.asin(\1))', expr)
            
            # Inverse cosine (arccos): acos(value) returns angle in degrees
            # Example: acos(0.5) → math.degrees(math.acos(0.5)) → 60.0 degrees
            expr = re.sub(r'acos\(([^)]+)\)', r'math.degrees(math.acos(\1))', expr)
            
            # Inverse tangent (arctan): atan(value) returns angle in degrees
            # Example: atan(1) → math.degrees(math.atan(1)) → 45.0 degrees
            expr = re.sub(r'atan\(([^)]+)\)', r'math.degrees(math.atan(\1))', expr)
            
            
            # =====================
            # Step 8: Handle logarithm function (base 10)
            # =====================
            
            # Regex pattern breakdown for logarithm function log(x):
            # log\(      : matches the literal text 'log('
            # ([^)]+)    : captures everything inside the parentheses (the argument x)
            #              [^)]+ means "one or more characters that are NOT a closing parenthesis"
            # \)         : matches the closing parenthesis
            #
            # Replacement: math.log10(\1)
            # Converts the user input log(x) into Python's math.log10(x)
            # This calculates the logarithm base 10
            #
            # Mathematical note: log₁₀(x) answers "10 to what power equals x?"
            #
            # Examples:
            # log(100)  → math.log10(100)  → 2.0   (because 10² = 100)
            # log(1000) → math.log10(1000) → 3.0   (because 10³ = 1000)
            # log(10)   → math.log10(10)   → 1.0   (because 10¹ = 10)
            
            expr = re.sub(r'log\(([^)]+)\)', r'math.log10(\1)', expr)
            
            
            # =====================
            # Step 9: Evaluate the final expression
            # =====================
            
            # At this point, all calculator symbols and functions have been
            # converted to valid Python code. Now we can safely evaluate it.
            # 
            # Example transformation:
            # User input:  "sin(30)+√25×2"
            # After step 2-8: "math.sin(math.radians(30))+math.sqrt(25)*2"
            # Evaluation: 0.5 + 5.0 * 2 = 10.5
            
            result = eval(expr)
            
            
            # =====================
            # Step 10: Save the result for the Ans button
            # =====================
            
            # Store the result as a string in last_answer
            # This allows the user to recall this result later using the "Ans" button
            # Example: If user calculates "5+3" = 8, then "Ans×2" = 16
            self.last_answer = str(result)
            
            
            # =====================
            # Step 11: Display the result on screen
            # =====================
            
            # Clear the current display (remove the expression)
            self.display.delete(0, tk.END)
            
            # Insert the calculated result
            # The result appears in the same place where the expression was
            self.display.insert(0, result)
        
        
        except:
            # =====================
            # Error handling
            # =====================
            
            # If ANY error occurs during the calculation process, we catch it here
            # Possible errors include:
            # - SyntaxError: Invalid mathematical expression (e.g., "5++3")
            # - ZeroDivisionError: Division by zero (e.g., "5÷0")
            # - ValueError: Invalid domain for functions (e.g., "√(-1)" or "log(-5)")
            # - NameError: Undefined variable or function
            # - TypeError: Wrong type of argument
            
            # Clear the display
            self.display.delete(0, tk.END)
            
            # Show generic "Error" message to the user
            # We use a generic message rather than showing technical error details
            # to keep the interface simple and user-friendly
            self.display.insert(0, "Error")
    
    
    # =====================
    # Insert previous answer method
    # =====================
    
    def insert_ans(self):
        """
        Insert the last calculated answer into the current expression
        
        This method is called when the user presses the "Ans" button.
        It retrieves the last calculation result and inserts it at the
        current cursor position in the display.
        
        Use case:
        ---------
        User calculates: 5 + 3 = 8
        Then types: 2 ×
        Then presses: Ans
        Display shows: 2 × 8
        
        If no previous calculation exists:
        -----------------------------------
        last_answer is an empty string "", so nothing is inserted
        This prevents errors when Ans is pressed before any calculation
        """
        # Insert the last answer at the end of the current expression
        # tk.END means "insert at the end of whatever is currently displayed"
        # If last_answer is empty, nothing visible happens (empty string inserted)
        self.display.insert(tk.END, self.last_answer)


# =====================
# GUI window setup
# =====================

# Create the main calculator window
root = tk.Tk()
root.title("Scientific Calculator")
root.geometry("380x625")

#Disable window resizing to keep the calcilater layout fixed : 
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
# Button color definitions
# =====================

NUMBER_COLOR = "#ff8fcf"   # Pink color for number buttons
OP_COLOR = "#4da6ff"       # Blue color for operator buttons
EQUAL_COLOR = "#1e90ff"    # Darker blue for '=' button
TEXT_COLOR = "white"       # Text color for all buttons


# =====================
# Button creation helper (Styled buttons with hover effect)
# =====================

# Creates a styled calculator button with custom colors,
# optional column span, and hover (mouse-over) shadow effect
def btn(text, r, c, cmd, bg, fg, colspan=1):

    # Create the button widget
    button = tk.Button(
        root,
        text=text,                     # Text displayed on the button
        font=("Arial", 14, "bold"),    # Font style for better visibility
        width=6,                       # Button width
        height=2,                      # Button height
        highlightbackground=bg,        # Background color (numbers / operators)
       
                
        activebackground=bg,           # Keep same color when pressed
        relief="flat",                 # Flat style for modern look
        borderwidth=0,                 # Remove default border
        command=cmd                    # Function executed when button is clicked
    )

    # =====================
    # Hover effect (mouse-over shadow effect)
    # =====================

    # Mouse enters button → add shadow
    def on_enter(event):
        button.config(relief="raised")

    # Mouse leaves button → remove shadow
    def on_leave(event):
        button.config(relief="flat")

    # Bind hover events
    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)

    # =====================
    # Button placement on the grid
    # =====================

    button.grid(
        row=r,
        column=c,
        columnspan=colspan,
        padx=6,
        pady=6,
        sticky="nsew"
    )

    return button

 
# =====================
# Top control buttons
# =====================

btn("AC", 2, 0, clear_all, OP_COLOR, TEXT_COLOR)
btn("C", 2, 1, clear_entry, OP_COLOR, TEXT_COLOR)
btn("DEL", 2, 2, delete_last, OP_COLOR, TEXT_COLOR)
btn("÷", 2, 3, lambda: press("÷"), OP_COLOR, TEXT_COLOR)



# =====================
# Numbers and basic operations
# =====================

buttons = [
    ("7",3,0), ("8",3,1), ("9",3,2), ("×",3,3),
    ("4",4,0), ("5",4,1), ("6",4,2), ("-",4,3),
    ("1",5,0), ("2",5,1), ("3",5,2), ("+",5,3),
]

for text, r, c in buttons:
    if text.isdigit() or text == ".":
        btn(text, r, c, lambda x=text: press(x), NUMBER_COLOR, TEXT_COLOR)
    else:
        btn(text, r, c, lambda x=text: press(x), OP_COLOR, TEXT_COLOR)


# =====================
# Bottom row (zero, decimal, comma, equals)
# =====================

btn("0", 6, 0, lambda: press("0"), NUMBER_COLOR, TEXT_COLOR)
btn(".", 6, 1, lambda: press("."), NUMBER_COLOR, TEXT_COLOR)
btn(",", 6, 2, lambda: press(","), OP_COLOR, TEXT_COLOR)
btn("=", 10, 0, engine.calculate, EQUAL_COLOR, TEXT_COLOR, colspan=4)


# =====================
# Roots, constants, and brackets
# =====================

btn("√", 7, 0, lambda: press("√"), OP_COLOR, TEXT_COLOR)
btn("π", 7, 1, insert_pi, OP_COLOR, TEXT_COLOR)
btn("(", 7, 2, lambda: press("("), OP_COLOR, TEXT_COLOR)
btn(")", 7, 3, lambda: press(")"), OP_COLOR, TEXT_COLOR)




# =====================
# Scientific functions
# =====================
btn("sin", 8, 0, lambda: press("sin("), OP_COLOR, TEXT_COLOR)
btn("cos", 8, 1, lambda: press("cos("), OP_COLOR, TEXT_COLOR)
btn("tan", 8, 2, lambda: press("tan("), OP_COLOR, TEXT_COLOR)
btn("log", 8, 3, lambda: press("log("), OP_COLOR, TEXT_COLOR)

btn("asin", 9, 0, lambda: press("asin("), OP_COLOR, TEXT_COLOR)
btn("acos", 9, 1, lambda: press("acos("), OP_COLOR, TEXT_COLOR)
btn("atan", 9, 2, lambda: press("atan("), OP_COLOR, TEXT_COLOR)
btn("Ans", 9, 3, engine.insert_ans, OP_COLOR, TEXT_COLOR)

# ======== ADDED (Power button) ========
btn("xʸ", 6, 3, power, OP_COLOR, TEXT_COLOR)
# =====================================



# =====================
# Run the application
# =====================

if __name__ == "__main__":
    root.mainloop()





