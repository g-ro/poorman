import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Dict

from models.request_model import RequestModel
from views.components.tree_view import EditableTreeView

class RequestPanel:
    def __init__(self, parent: ttk.Frame, on_send: Callable[[RequestModel], None]):
        self.parent = parent
        self.on_send = on_send
        self.request_controller = None  # Will be set by MainWindow
        
        # Create main frame
        self.frame = ttk.LabelFrame(parent, text="Request", padding="5")
        
        # URL Frame
        url_frame = ttk.Frame(self.frame)
        url_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # HTTP Method dropdown
        ttk.Label(url_frame, text="Method:").pack(side=tk.LEFT, padx=(0, 5))
        self.method_var = tk.StringVar(value="GET")
        method_combo = ttk.Combobox(url_frame, textvariable=self.method_var, 
                                  values=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"],
                                  state="readonly", width=10)
        method_combo.pack(side=tk.LEFT, padx=(0, 10))
        
        # URL Entry
        ttk.Label(url_frame, text="URL:").pack(side=tk.LEFT, padx=(0, 5))
        self.url_var = tk.StringVar()
        url_entry = ttk.Entry(url_frame, textvariable=self.url_var, width=50)
        url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        # Send button
        ttk.Button(url_frame, text="Send", command=self.on_send_click).pack(side=tk.LEFT)
        
        # Create notebook for request details
        notebook = ttk.Notebook(self.frame)
        notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Parameters tab
        params_frame = ttk.Frame(notebook)
        self.params_tree = EditableTreeView(params_frame, ["Key", "Value", "Description"], "Parameter")
        notebook.add(params_frame, text="Params")
        
        # Headers tab
        headers_frame = ttk.Frame(notebook)
        self.headers_tree = EditableTreeView(headers_frame, ["Key", "Value", "Description"], "Header")
        notebook.add(headers_frame, text="Headers")
        
        # Body tab
        body_frame = ttk.Frame(notebook)
        self.create_body_tab(body_frame)
        notebook.add(body_frame, text="Body")
        
        # Auth tab
        auth_frame = ttk.Frame(notebook)
        self.create_auth_tab(auth_frame)
        notebook.add(auth_frame, text="Auth")
    
    def create_body_tab(self, parent: ttk.Frame):
        """Create the body configuration tab"""
        # Body type selection
        type_frame = ttk.Frame(parent)
        type_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(type_frame, text="Body Type:").pack(side=tk.LEFT, padx=(0, 10))
        
        self.body_type_var = tk.StringVar(value="none")
        body_types = [("None", "none"), ("Raw", "raw"), ("Form Data", "form"), ("JSON", "json")]
        
        for text, value in body_types:
            ttk.Radiobutton(type_frame, text=text, variable=self.body_type_var, 
                          value=value, command=self.on_body_type_change).pack(side=tk.LEFT, padx=(0, 10))
        
        # Body content frame
        self.body_content_frame = ttk.Frame(parent)
        self.body_content_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Raw/JSON text area
        self.body_text = tk.Text(self.body_content_frame, height=10, wrap=tk.WORD)
        
        # Form data tree view
        self.form_tree = EditableTreeView(self.body_content_frame, ["Key", "Value", "Type"], "Form Field")
        
        self.on_body_type_change()
    
    def create_auth_tab(self, parent: ttk.Frame):
        """Create the authentication configuration tab"""
        # Auth type selection
        type_frame = ttk.Frame(parent)
        type_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(type_frame, text="Auth Type:").pack(side=tk.LEFT, padx=(0, 10))
        
        self.auth_type_var = tk.StringVar(value="none")
        auth_types = [("None", "none"), ("Basic Auth", "basic"), ("Bearer Token", "bearer"),
                     ("OAuth 1.0", "oauth1"), ("OAuth 2.0", "oauth2")]
        
        for text, value in auth_types:
            ttk.Radiobutton(type_frame, text=text, variable=self.auth_type_var,
                          value=value, command=self.on_auth_type_change).pack(side=tk.LEFT, padx=(0, 10))
        
        # Auth content frame
        self.auth_content_frame = ttk.Frame(parent)
        self.auth_content_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Basic Auth frame
        self.basic_auth_frame = ttk.LabelFrame(self.auth_content_frame, text="Basic Authentication", padding="10")
        self.basic_username_var = tk.StringVar()
        self.basic_password_var = tk.StringVar()
        
        ttk.Label(self.basic_auth_frame, text="Username:").grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        ttk.Entry(self.basic_auth_frame, textvariable=self.basic_username_var).grid(row=0, column=1, sticky=tk.W, pady=(0, 5))
        
        ttk.Label(self.basic_auth_frame, text="Password:").grid(row=1, column=0, sticky=tk.W)
        ttk.Entry(self.basic_auth_frame, textvariable=self.basic_password_var, show="*").grid(row=1, column=1, sticky=tk.W)
        
        # Bearer Token frame
        self.bearer_auth_frame = ttk.LabelFrame(self.auth_content_frame, text="Bearer Token", padding="10")
        self.bearer_token_var = tk.StringVar()
        
        ttk.Label(self.bearer_auth_frame, text="Token:").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(self.bearer_auth_frame, textvariable=self.bearer_token_var, width=50).grid(row=0, column=1, sticky=tk.W)
        
        # OAuth 1.0 frame
        self.oauth1_frame = ttk.LabelFrame(self.auth_content_frame, text="OAuth 1.0", padding="10")
        self.oauth1_vars = {}
        
        oauth1_fields = [
            ("Consumer Key:", "oauth1_consumer_key"),
            ("Consumer Secret:", "oauth1_consumer_secret"),
            ("Access Token:", "oauth1_access_token"),
            ("Token Secret:", "oauth1_token_secret")
        ]
        
        for i, (label, var_name) in enumerate(oauth1_fields):
            ttk.Label(self.oauth1_frame, text=label).grid(row=i, column=0, sticky=tk.W, pady=(0, 5))
            self.oauth1_vars[var_name] = tk.StringVar()
            ttk.Entry(self.oauth1_frame, textvariable=self.oauth1_vars[var_name], width=40).grid(
                row=i, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # OAuth 2.0 frame
        self.oauth2_frame = ttk.LabelFrame(self.auth_content_frame, text="OAuth 2.0", padding="10")
        self.oauth2_vars = {}
        
        oauth2_fields = [
            ("Client ID:", "oauth2_client_id"),
            ("Client Secret:", "oauth2_client_secret"),
            ("Access Token URL:", "oauth2_token_url"),
            ("Authorization URL:", "oauth2_auth_url"),
            ("Redirect URI:", "oauth2_redirect_uri"),
            ("Scope:", "oauth2_scope")
        ]
        
        for i, (label, var_name) in enumerate(oauth2_fields):
            ttk.Label(self.oauth2_frame, text=label).grid(row=i, column=0, sticky=tk.W, pady=(0, 5))
            self.oauth2_vars[var_name] = tk.StringVar()
            ttk.Entry(self.oauth2_frame, textvariable=self.oauth2_vars[var_name], width=40).grid(
                row=i, column=1, sticky=(tk.W, tk.E), pady=(0, 5))
        
        # OAuth 2.0 buttons
        oauth2_btn_frame = ttk.Frame(self.oauth2_frame)
        oauth2_btn_frame.grid(row=len(oauth2_fields), column=0, columnspan=2, pady=(10, 0))
        
        ttk.Button(oauth2_btn_frame, text="Get Authorization URL", 
                  command=self.on_get_oauth2_auth_url).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(oauth2_btn_frame, text="Get Access Token", 
                  command=self.on_get_oauth2_token).pack(side=tk.LEFT)
        
        self.on_auth_type_change()
    
    def on_body_type_change(self):
        """Handle body type change"""
        for widget in self.body_content_frame.winfo_children():
            widget.pack_forget()
        
        body_type = self.body_type_var.get()
        if body_type in ["raw", "json"]:
            self.body_text.pack(fill=tk.BOTH, expand=True)
        elif body_type == "form":
            self.form_tree.frame.pack(fill=tk.BOTH, expand=True)
    
    def on_auth_type_change(self):
        """Handle authentication type change"""
        for widget in self.auth_content_frame.winfo_children():
            widget.pack_forget()
        
        auth_type = self.auth_type_var.get()
        if auth_type == "basic":
            self.basic_auth_frame.pack(fill=tk.X)
        elif auth_type == "bearer":
            self.bearer_auth_frame.pack(fill=tk.X)
        elif auth_type == "oauth1":
            self.oauth1_frame.pack(fill=tk.X)
        elif auth_type == "oauth2":
            self.oauth2_frame.pack(fill=tk.X)
    
    def on_send_click(self):
        """Handle send button click"""
        request = self.get_request()
        self.on_send(request)
    
    def get_request(self) -> RequestModel:
        """Get current request configuration"""
        # Get parameters
        params = {}
        for key, value, _ in self.params_tree.get_items():
            if key:
                params[key] = value
        
        # Get headers
        headers = {}
        for key, value, _ in self.headers_tree.get_items():
            if key:
                headers[key] = value
        
        # Get body data
        body_type = self.body_type_var.get()
        body_content = ""
        form_data = {}
        
        if body_type in ["raw", "json"]:
            body_content = self.body_text.get("1.0", tk.END).strip()
        elif body_type == "form":
            for key, value, _ in self.form_tree.get_items():
                if key:
                    form_data[key] = value
        
        # Get auth data
        auth_type = self.auth_type_var.get()
        auth_data = {}
        
        if auth_type == "basic":
            auth_data = {
                "username": self.basic_username_var.get(),
                "password": self.basic_password_var.get()
            }
        elif auth_type == "bearer":
            auth_data = {"token": self.bearer_token_var.get()}
        elif auth_type == "oauth1":
            auth_data = {
                "consumer_key": self.oauth1_vars["oauth1_consumer_key"].get(),
                "consumer_secret": self.oauth1_vars["oauth1_consumer_secret"].get(),
                "access_token": self.oauth1_vars["oauth1_access_token"].get(),
                "token_secret": self.oauth1_vars["oauth1_token_secret"].get()
            }
        elif auth_type == "oauth2":
            auth_data = {
                "client_id": self.oauth2_vars["oauth2_client_id"].get(),
                "client_secret": self.oauth2_vars["oauth2_client_secret"].get(),
                "token_url": self.oauth2_vars["oauth2_token_url"].get(),
                "auth_url": self.oauth2_vars["oauth2_auth_url"].get(),
                "redirect_uri": self.oauth2_vars["oauth2_redirect_uri"].get(),
                "scope": self.oauth2_vars["oauth2_scope"].get()
            }
        
        return RequestModel(
            method=self.method_var.get(),
            url=self.url_var.get(),
            params=params,
            headers=headers,
            body_type=body_type,
            body_content=body_content,
            form_data=form_data,
            auth_type=auth_type,
            auth_data=auth_data
        )
    
    def set_request(self, request: RequestModel):
        """Set request configuration"""
        self.method_var.set(request.method)
        self.url_var.set(request.url)
        
        # Set parameters
        self.params_tree.clear()
        for key, value in request.params.items():
            self.params_tree.add_items([(key, value, "")])
        
        # Set headers
        self.headers_tree.clear()
        for key, value in request.headers.items():
            self.headers_tree.add_items([(key, value, "")])
        
        # Set body
        self.body_type_var.set(request.body_type)
        self.on_body_type_change()
        
        if request.body_type in ["raw", "json"]:
            self.body_text.delete("1.0", tk.END)
            self.body_text.insert("1.0", request.body_content)
        elif request.body_type == "form":
            self.form_tree.clear()
            for key, value in request.form_data.items():
                self.form_tree.add_items([(key, value, "text")])
        
        # Set auth
        self.auth_type_var.set(request.auth_type)
        self.on_auth_type_change()
        
        if request.auth_type == "basic":
            self.basic_username_var.set(request.auth_data.get("username", ""))
            self.basic_password_var.set(request.auth_data.get("password", ""))
        elif request.auth_type == "bearer":
            self.bearer_token_var.set(request.auth_data.get("token", ""))
        elif request.auth_type == "oauth1":
            for key, var_name in [
                ("consumer_key", "oauth1_consumer_key"),
                ("consumer_secret", "oauth1_consumer_secret"),
                ("access_token", "oauth1_access_token"),
                ("token_secret", "oauth1_token_secret")
            ]:
                self.oauth1_vars[var_name].set(request.auth_data.get(key, ""))
        elif request.auth_type == "oauth2":
            for key, var_name in [
                ("client_id", "oauth2_client_id"),
                ("client_secret", "oauth2_client_secret"),
                ("token_url", "oauth2_token_url"),
                ("auth_url", "oauth2_auth_url"),
                ("redirect_uri", "oauth2_redirect_uri"),
                ("scope", "oauth2_scope")
            ]:
                self.oauth2_vars[var_name].set(request.auth_data.get(key, ""))
    
    def on_get_oauth2_auth_url(self):
        """Handle getting OAuth2 authorization URL"""
        client_id = self.oauth2_vars["oauth2_client_id"].get()
        auth_url = self.oauth2_vars["oauth2_auth_url"].get()
        redirect_uri = self.oauth2_vars["oauth2_redirect_uri"].get()
        scope = self.oauth2_vars["oauth2_scope"].get()
        
        if not all([client_id, auth_url, redirect_uri]):
            messagebox.showerror("Error", "Please fill in Client ID, Authorization URL, and Redirect URI")
            return
        
        # Get authorization URL through controller
        auth_url = self.request_controller.setup_oauth2(client_id, redirect_uri, scope)
        if auth_url:
            messagebox.showinfo("Authorization URL", f"Please visit this URL to authorize:\n\n{auth_url}")
    
    def on_get_oauth2_token(self):
        """Handle getting OAuth2 access token"""
        dialog = tk.Toplevel(self.parent)
        dialog.title("Enter Authorization Code")
        dialog.geometry("500x120")
        dialog.transient(self.parent)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Authorization Code:").pack(pady=10)
        code_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=code_var, width=60).pack(pady=5)
        
        def get_token():
            code = code_var.get().strip()
            if not code:
                messagebox.showerror("Error", "Please enter authorization code")
                return
            
            client_secret = self.oauth2_vars["oauth2_client_secret"].get()
            token_url = self.oauth2_vars["oauth2_token_url"].get()
            
            if self.request_controller.get_oauth2_token(code, client_secret, token_url):
                dialog.destroy()
                messagebox.showinfo("Success", "Access token obtained successfully!")
        
        ttk.Button(dialog, text="Get Token", command=get_token).pack(pady=10) 