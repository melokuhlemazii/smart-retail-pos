import os
from app import create_app, db

app = create_app()

if __name__ == '__main__':
    # Development
    debug = os.getenv('FLASK_ENV') == 'development'
    app.run(debug=debug, host='0.0.0.0', port=int(os.getenv('PORT', 5000)))



