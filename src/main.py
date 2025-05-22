import tkinter as tk
from tkinter import ttk
from views.main_window import MainWindow

def main():
    """Main function to run the application"""
    root = tk.Tk()
    
    # Set application icon and style
    try:
        root.tk.call('wm', 'iconphoto', root._w, tk.PhotoImage())
    except:
        pass
    
    # Configure style
    style = ttk.Style()
    try:
        style.theme_use('clam')
    except:
        pass
    
    # Create and run the application
    app = MainWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main() 