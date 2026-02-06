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
# GUI Class
# =====================

class CalculatorGUI:
    """
    Graphical User Interface Class - Handles all tkinter-related components
    This class is responsible for creating and managing the calculator's visual interface,
    including the window, display screen, buttons, colors, and user interactions.
    """
    
    def __init__(self):
        """
        Initialize the Calculator GUI
        This method sets up all the essential components of the calculator interface:
        1. Define color scheme for buttons
        2. Create the main window
        3. Create the display screen
        4. Initialize the calculation engine
        5. Create all calculator buttons
        """
        
        # =====================
        # Button color definitions
        # =====================
        
        self.NUMBER_COLOR = "#ff8fcf"   # Pink color for number buttons (0-9 and decimal point)
        self.OP_COLOR = "#4da6ff"       # Blue color for operator buttons (+, -, ×, ÷, functions)
        self.EQUAL_COLOR = "#1e90ff"    # Darker blue color specifically for the '=' button
        self.TEXT_COLOR = "white"       # White text color for all button labels
        
        # =====================
        # Initialize GUI components in sequence
        # =====================
        
        # Step 1: Create and configure the main calculator window
        self.setup_window()
        
        # Step 2: Create the display screen where expressions and results appear
        self.create_display()
        
        # Step 3: Initialize the calculation engine and connect it to the display
        self.engine = CalculatorEngine(self.display)
        
        # Step 4: Create all calculator buttons (numbers, operators, functions)
        self.create_buttons()
    
    
    # =====================
    # Window setup method
    # =====================
    
    def setup_window(self):
        """
        Create and configure the main calculator window
        
        This method initializes the root tkinter window with specific properties:
        - Sets the window title to "Scientific Calculator"
        - Defines fixed dimensions (380x625 pixels) for consistent layout
        - Disables window resizing to maintain button alignment and spacing
        """
        
        # Create the main tkinter window object
        self.root = tk.Tk()
        
        # Set the title that appears in the window's title bar
        self.root.title("Scientific Calculator")
        
        # Set fixed window dimensions: 380 pixels wide × 625 pixels tall
        # These dimensions are optimized for all buttons to fit properly
        self.root.geometry("380x625")
        
        # Disable window resizing to keep the calculator layout fixed
        # This prevents buttons from becoming misaligned if user tries to resize
        self.root.resizable(False, False)
    
    
    # =====================
    # Display creation method
    # =====================
    
    def create_display(self):
        """
        Create the calculator's display screen (Entry widget)
        
        The display screen shows:
        - Mathematical expressions as the user types them
        - Final calculation results after pressing '='
        - Error messages if invalid expressions are entered
        
        Properties:
        - Large font (Arial, 24pt) for easy readability
        - Right-aligned text (like traditional calculators)
        - Positioned at the top of the calculator spanning all 4 columns
        """
        
        # Create an Entry widget to serve as the calculator's display screen
        self.display = tk.Entry(
            self.root,                  # Parent widget (main window)
            font=("Arial", 24),         # Large font for better visibility
            justify="right",            # Right-align text (standard calculator behavior)
            bd=10                       # Border width of 10 pixels for visual separation
        )
        
        # Position the display screen in the grid layout:
        # - Row 1 (leaving row 0 empty for potential future use)
        # - Column 0, spanning across all 4 columns
        # - Padding: 10 pixels on all sides
        self.display.grid(row=1, column=0, columnspan=4, padx=10, pady=10)
    
    
    # =====================
    # Button creation helper method (with hover effect)
    # =====================
    
    def create_button(self, text, r, c, cmd, bg, colspan=1):
        """
        Create a styled calculator button with hover effect
        
        This method creates individual buttons for the calculator with:
        - Custom colors based on button type (number/operator)
        - Hover effect (shadow appears when mouse enters button area)
        - Consistent size and styling across all buttons
        - Grid-based positioning for organized layout
        
        Parameters:
        -----------
        text : str
            The label displayed on the button (e.g., "7", "+", "sin")
        r : int
            Row position in the grid layout
        c : int
            Column position in the grid layout
        cmd : function
            Function to execute when button is clicked
        bg : str
            Background color in hex format (e.g., "#ff8fcf")
        colspan : int, optional
            Number of columns the button should span (default: 1)
            Used for buttons like '=' which spans 4 columns
        
        Returns:
        --------
        button : tk.Button
            The created button object
        """
        
        # =====================
        # Create the button widget
        # =====================
        
        button = tk.Button(
            self.root,                     # Parent widget (main window)
            text=text,                     # Text label displayed on the button
            font=("Arial", 14, "bold"),    # Font: Arial, size 14, bold for clarity
            width=6,                       # Button width (in character units)
            height=2,                      # Button height (in character units)
            highlightbackground=bg,        # Background color (differs for numbers vs operators)
            activebackground=bg,           # Keep same color when button is pressed
            relief="flat",                 # Flat appearance (modern, minimalist style)
            borderwidth=0,                 # Remove default border for cleaner look
            command=cmd                    # Function to execute when clicked
        )
        
        # =====================
        # Hover effect implementation
        # =====================
        # These functions create a visual feedback when mouse hovers over button
        # This improves user experience by showing which button will be pressed
        
        def on_enter(event):
            """
            Mouse enters button area → add raised shadow effect
            This gives visual feedback that the button is interactive
            """
            button.config(relief="raised")
        
        def on_leave(event):
            """
            Mouse leaves button area → remove shadow (return to flat)
            Button returns to its normal flat appearance
            """
            button.config(relief="flat")
        
        # Bind the hover functions to mouse events:
        # <Enter> event triggers when mouse cursor enters button area
        # <Leave> event triggers when mouse cursor exits button area
        button.bind("<Enter>", on_enter)
        button.bind("<Leave>", on_leave)
        
        # =====================
        # Position button in the grid layout
        # =====================
        
        button.grid(
            row=r,              # Row position in grid
            column=c,           # Column position in grid
            columnspan=colspan, # Number of columns to span (1 for most buttons, 4 for '=')
            padx=6,             # Horizontal padding (6 pixels space between buttons)
            pady=6,             # Vertical padding (6 pixels space between buttons)
            sticky="nsew"       # Stretch button to fill entire grid cell (north-south-east-west)
        )
        
        return button
    
    
    # =====================
    # Input handling methods
    # =====================
    
    def press(self, value):
        """
        Insert a value into the display screen
        
        This method is called when user clicks number or operator buttons.
        It appends the clicked value to the end of the current expression.
        
        Parameters:
        -----------
        value : str
            The character to insert (number, operator, or function name)
        
        Example:
        --------
        If display shows "5+3" and user clicks "2", display becomes "5+32"
        """
        self.display.insert(tk.END, value)
    
    
    def clear_all(self):
        """
        Clear the entire display screen and reset last answer (AC button)
        
        AC stands for "All Clear" - it performs a complete reset:
        - Deletes all text from the display screen
        - Resets the last_answer variable in the calculation engine
        
        This is typically used when starting a completely new calculation
        or when user wants to clear everything and start fresh.
        """
        # Delete all characters from the display (from position 0 to END)
        self.display.delete(0, tk.END)
        
        # Reset the last answer stored in the engine (used by Ans button)
        self.engine.last_answer = ""
    
    
    def clear_entry(self):
        """
        Clear the last entry (number or function) - C button
        
        This is a "smart delete" that removes:
        - Complete function names (sin(, cos(, log(, etc.) as one unit
        - OR the last single character if not a function
        
        This is more user-friendly than deleting character by character
        when dealing with mathematical functions.
        
        Example:
        --------
        Display: "5+sin("
        After C button: "5+"  (removes entire "sin(" not just the "(")
        """
        # Get current text from display
        text = self.display.get()
        
        # Check if the text ends with any known function name
        # If found, remove the entire function as one unit
        for func in ["asin(", "acos(", "atan(", "sin(", "cos(", "tan(", "log("]:
            if text.endswith(func):
                # Delete from (text length - function length) to END
                # This removes the complete function name
                self.display.delete(len(text)-len(func), tk.END)
                return  # Exit after removing function
        
        # If no function found and text exists, remove just the last character
        if text:
            self.display.delete(len(text)-1, tk.END)
    
    
    def delete_last(self):
        """
        Delete the last entered character from the display (DEL button)
        
        This method removes only the last single character, regardless of
        whether it's part of a number, operator, or function name.
        
        Implementation:
        - Get current text
        - Delete everything from display
        - Re-insert text without the last character
        
        Example:
        --------
        Display: "sin(45)"
        After DEL: "sin(4"
        """
        # Get the current text from display
        text = self.display.get()
        
        # Clear the entire display
        self.display.delete(0, tk.END)
        
        # Re-insert the text without the last character (text[:-1] means all except last)
        self.display.insert(0, text[:-1])
    
    
    def insert_pi(self):
        """
        Insert the mathematical constant π (pi) into the display
        
        When the π button is pressed, this method inserts the numerical
        value of pi (approximately 3.14159265359) into the expression.
        
        The value is obtained from Python's math.pi constant which provides
        high precision (typically 15-17 decimal places).
        
        Example:
        --------
        User clicks: "2" → "×" → "π"
        Display shows: "2×3.141592653589793"
        """
        # Insert the value of pi at the end of current expression
        # math.pi provides the most accurate value available in Python
        self.display.insert(tk.END, str(math.pi))
    
    
    def power(self):
        """
        Insert the power/exponent operator (^) into the display
        
        This allows users to calculate exponents (powers).
        The ^ symbol will later be converted to Python's ** operator
        during calculation.
        
        Examples:
        ---------
        2^3 → calculates as 2**3 → result: 8
        5^2 → calculates as 5**2 → result: 25
        """
        # Insert the ^ symbol which represents exponentiation
        # This will be converted to ** during expression evaluation
        self.display.insert(tk.END, "^")
    
    
    # =====================
    # Button creation method (creates all calculator buttons)
    # =====================
    
    def create_buttons(self):
        """
        Create all calculator buttons in organized rows
        
        This method systematically creates every button on the calculator
        in a logical order, organizing them by function:
        
        1. Control buttons (AC, C, DEL, ÷)
        2. Number pad (7-9, 4-6, 1-3, 0)
        3. Basic operators (×, -, +)
        4. Special buttons (decimal point, comma, power)
        5. Scientific functions (√, π, parentheses)
        6. Trigonometric functions (sin, cos, tan, and their inverses)
        7. Logarithm and Ans buttons
        8. Equals button
        
        Each button is color-coded:
        - Pink (NUMBER_COLOR) for digits
        - Blue (OP_COLOR) for operators and functions
        - Dark blue (EQUAL_COLOR) for equals button
        """
        
        # =====================
        # Row 2: Top control buttons
        # =====================
        # These buttons control the display and basic division
        
        self.create_button("AC", 2, 0, self.clear_all, self.OP_COLOR)
        # AC (All Clear): Clears entire display and resets last answer
        
        self.create_button("C", 2, 1, self.clear_entry, self.OP_COLOR)
        # C (Clear Entry): Removes last entry (smart delete for functions)
        
        self.create_button("DEL", 2, 2, self.delete_last, self.OP_COLOR)
        # DEL (Delete): Removes only the last single character
        
        self.create_button("÷", 2, 3, lambda: self.press("÷"), self.OP_COLOR)
        # Division operator: ÷ symbol (will be converted to / during calculation)
        
        
        # =====================
        # Rows 3-5: Number pad and basic operators
        # =====================
        # Standard calculator layout: 7-8-9, 4-5-6, 1-2-3
        # Each row includes its corresponding operator (×, -, +)
        
        # Define button layout as list of tuples: (text, row, column)
        buttons = [
            ("7",3,0), ("8",3,1), ("9",3,2), ("×",3,3),  # Row 3
            ("4",4,0), ("5",4,1), ("6",4,2), ("-",4,3),  # Row 4
            ("1",5,0), ("2",5,1), ("3",5,2), ("+",5,3),  # Row 5
        ]
        
        # Loop through each button definition and create it
        for text, r, c in buttons:
            if text.isdigit():
                # If button is a digit (0-9), use pink NUMBER_COLOR
                self.create_button(text, r, c, lambda x=text: self.press(x), self.NUMBER_COLOR)
            else:
                # If button is an operator (×, -, +), use blue OP_COLOR
                self.create_button(text, r, c, lambda x=text: self.press(x), self.OP_COLOR)
        
        
        # =====================
        # Row 6: Zero, decimal point, comma, and power
        # =====================
        
        self.create_button("0", 6, 0, lambda: self.press("0"), self.NUMBER_COLOR)
        # Zero button: Uses pink color like other numbers
        
        self.create_button(".", 6, 1, lambda: self.press("."), self.NUMBER_COLOR)
        # Decimal point: Allows entry of decimal numbers (e.g., 3.14)
        
        self.create_button(",", 6, 2, lambda: self.press(","), self.OP_COLOR)
        # Comma: Used in functions like √(3,27) for nth root
        
        self.create_button("xʸ", 6, 3, self.power, self.OP_COLOR)
        # Power button: Inserts ^ symbol for exponentiation (x to the power of y)
        
        
        # =====================
        # Row 7: Roots, constants, and parentheses
        # =====================
        
        self.create_button("√", 7, 0, lambda: self.press("√"), self.OP_COLOR)
        # Square root symbol: Can be used as √25 or √(3,27) for nth root
        
        self.create_button("π", 7, 1, self.insert_pi, self.OP_COLOR)
        # Pi constant: Inserts the value of π (approximately 3.14159...)
        
        self.create_button("(", 7, 2, lambda: self.press("("), self.OP_COLOR)
        # Opening parenthesis: For grouping expressions and function arguments
        
        self.create_button(")", 7, 3, lambda: self.press(")"), self.OP_COLOR)
        # Closing parenthesis: Completes grouped expressions
        
        
        # =====================
        # Row 8: Trigonometric functions and logarithm
        # =====================
        # All trigonometric functions work with degrees (not radians)
        
        self.create_button("sin", 8, 0, lambda: self.press("sin("), self.OP_COLOR)
        # Sine function: Calculates sine of an angle in degrees
        # Example: sin(30) → 0.5
        
        self.create_button("cos", 8, 1, lambda: self.press("cos("), self.OP_COLOR)
        # Cosine function: Calculates cosine of an angle in degrees
        # Example: cos(60) → 0.5
        
        self.create_button("tan", 8, 2, lambda: self.press("tan("), self.OP_COLOR)
        # Tangent function: Calculates tangent of an angle in degrees
        # Example: tan(45) → 1.0
        
        self.create_button("log", 8, 3, lambda: self.press("log("), self.OP_COLOR)
        # Logarithm base 10: Calculates log₁₀(x)
        # Example: log(100) → 2.0
        
        
        # =====================
        # Row 9: Inverse trigonometric functions and Ans button
        # =====================
        # Inverse trig functions return angles in degrees
        
        self.create_button("asin", 9, 0, lambda: self.press("asin("), self.OP_COLOR)
        # Inverse sine (arcsin): Returns angle whose sine is the input
        # Example: asin(0.5) → 30 degrees
        
        self.create_button("acos", 9, 1, lambda: self.press("acos("), self.OP_COLOR)
        # Inverse cosine (arccos): Returns angle whose cosine is the input
        # Example: acos(0.5) → 60 degrees
        
        self.create_button("atan", 9, 2, lambda: self.press("atan("), self.OP_COLOR)
        # Inverse tangent (arctan): Returns angle whose tangent is the input
        # Example: atan(1) → 45 degrees
        
        self.create_button("Ans", 9, 3, self.engine.insert_ans, self.OP_COLOR)
        # Ans (Answer) button: Inserts the result of the last calculation
        # Useful for chaining calculations without retyping results
        
        
        # =====================
        # Row 10: Equals button (spans all 4 columns)
        # =====================
        
        self.create_button("=", 10, 0, self.engine.calculate, self.EQUAL_COLOR, colspan=4)
        # Equals button: Triggers calculation of the expression
        # - Spans across all 4 columns for easy access
        # - Uses darker blue color (EQUAL_COLOR) to stand out
        # - Calls engine.calculate() to evaluate the expression
    
    
    # =====================
    # Application run method
    # =====================
    
    def run(self):
        """
        Start the calculator application
        
        This method starts the tkinter main event loop, which:
        - Displays the calculator window
        - Listens for user interactions (button clicks, keyboard input)
        - Keeps the application running until user closes the window
        
        This is the final method called after all setup is complete.
        The program will remain in this loop until the window is closed.
        """
        self.root.mainloop()

# =====================
# Run the application
# =====================
if __name__ == "__main__":
    app = CalculatorGUI()
    app.run()





