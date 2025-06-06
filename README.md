# Travel Database Application

This is a comprehensive travel management web application built with Flask that helps users explore, plan, and book travel experiences. The application features:

- **Travel Destination Catalog**: Browse through various travel destinations including Kashmir, Udaipur, Kerala, Shimla, Bali, and Vietnam
- **Detailed Itineraries**: View customized itineraries for different budget levels (budget, mid-range, and luxury)
- **User Management**: Secure user registration, login, and password recovery system
- **Booking System**: Integrated booking functionality for travel packages
- **Email Notifications**: Automated email system for booking confirmations and password recovery
- **Search Functionality**: Search for destinations and travel packages
- **Responsive Design**: User-friendly interface accessible on various devices

The application uses SQL Server for data storage and includes email functionality for notifications. It's designed to help travelers plan their trips with detailed information about destinations, pricing, and day-by-day itineraries.

## Prerequisites

- Python 3.x
- SQL Server
- ODBC Driver for SQL Server
- Git (optional, for cloning the repository)

## Setup Instructions

1. **Clone the repository** (if using Git):
   ```bash
   git clone <repository-url>
   cd travel_database_app
   ```

2. **Create and activate a virtual environment**:
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # Linux/Mac
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure the application**:
   - Open `config.py`
   - Update the database connection string with your SQL Server details:
     ```python
     DB_CONNECTION = "Driver={SQL Server};Server=YOUR_SERVER;Database=TravelDB;Trusted_Connection=yes;"
     ```
   - Update the email settings if needed:
     ```python
     MAIL_SERVER = 'smtp.gmail.com'
     MAIL_PORT = 587
     MAIL_USE_TLS = True
     MAIL_USERNAME = 'your-email@gmail.com'
     MAIL_PASSWORD = 'your-app-password'
     ```

## Running the Application

1. **Activate the virtual environment** (if not already activated):
   ```bash
   # Windows
   .\venv\Scripts\activate

   # Linux/Mac
   source venv/bin/activate
   ```

2. **Start the Flask application**:
   ```bash
   python app.py
   ```

3. **Access the application**:
   - Open your web browser
   - Navigate to `http://localhost:5000`

## Project Structure

- `app.py` - Main application file
- `config.py` - Configuration settings
- `requirements.txt` - Python dependencies
- `templates/` - HTML templates
- `static/` - Static files (CSS, JavaScript, images)
- `venv/` - Virtual environment directory

## Troubleshooting

1. **Database Connection Issues**:
   - Ensure SQL Server is running
   - Verify the connection string in `config.py`
   - Check if the ODBC driver is installed

2. **Email Issues**:
   - Verify email credentials in `config.py`
   - For Gmail, ensure you're using an App Password if 2FA is enabled

3. **Module Not Found Errors**:
   - Ensure you're in the virtual environment
   - Run `pip install -r requirements.txt` again

## Support

For any issues or questions, please contact the development team.
