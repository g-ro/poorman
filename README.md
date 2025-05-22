# PoorMan v0.1

A lightweight, cross-platform desktop application for testing REST APIs, similar to Postman. Built with Python and Tkinter.

## Features

- Send HTTP requests (GET, POST, PUT, DELETE, etc.)
- Configure request parameters, headers, and body
- Support for different body types (raw, JSON, form data)
- Authentication support (Basic, Bearer Token, OAuth 1.0, OAuth 2.0)
- Save and load request configurations
- Pretty-print JSON responses
- SSL/TLS support with option to ignore certificate verification

## Project Structure

```
poorman/
├── README.md
├── LICENSE
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── version.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── request_model.py
│   │   └── response_model.py
│   ├── views/
│   │   ├── __init__.py
│   │   ├── main_window.py
│   │   ├── request_panel.py
│   │   ├── response_panel.py
│   │   └── components/
│   │       ├── __init__.py
│   │       └── tree_view.py
│   ├── controllers/
│   │   ├── __init__.py
│   │   └── request_controller.py
│   └── services/
│       ├── __init__.py
│       ├── request_service.py
│       └── storage_service.py
```

## Architecture

The application follows the Model-View-Controller (MVC) pattern with additional service layers:

- **Models**: Data structures for requests and responses
- **Views**: UI components and layouts
- **Controllers**: Handle user interactions and coordinate between views and services
- **Services**: Core business logic for HTTP requests, authentication, and storage

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/poorman.git
   cd poorman
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python src/main.py
   ```

## Dependencies

- Python 3.7+
- requests
- requests-oauthlib
- urllib3
- tkinter (usually comes with Python)



## Author

Rohit Gupta

## Version History

- 0.1 (2024-01) - Initial release
  - Basic HTTP request functionality
  - Authentication support
  - Request saving/loading
  - JSON response formatting

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by Postman (https://www.postman.com/)
- Built with Python and Tkinter
- Uses the excellent `requests` library 