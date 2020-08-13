from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from face_recognition_app import  login_manager

class User(UserMixin):
    """
    Create an Employee table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'employees'

    id = 1
    email = 'admin@admin.ia'
    first_name = 'Admin'
    last_name = 'Admin'
    password_hash = generate_password_hash('password')
    is_admin = False
    is_active = True

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User: {}>'.format(self.email)

# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    user = User()
    user.email='admin@admin'
    user.is_admin=True
    user.is_active=True
    user.id=1

    return user
