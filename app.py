from flask import Flask
from flask_cors import CORS
from db_config import init_mysql

app = Flask(__name__)
CORS(app)

# Initialize MySQL
mysql = init_mysql(app)
app.config['MYSQL_OBJ'] = mysql

# Import and register blueprints
from routes.auth_routes import auth_bp
from routes.donor_routes import donor_bp
from routes.recipient_routes import recipient_bp
from routes.admin_routes import admin_bp
from routes.general_routes import general_bp
from routes.register_routes import register_bp   

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(donor_bp, url_prefix='/api/donor')
app.register_blueprint(recipient_bp, url_prefix='/api/recipient')
app.register_blueprint(admin_bp, url_prefix='/api/admin')
app.register_blueprint(general_bp, url_prefix='/api')
app.register_blueprint(register_bp)  

if __name__ == '__main__':
    app.run(debug=True)
