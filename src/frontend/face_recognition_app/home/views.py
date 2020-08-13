from flask import abort, render_template
from flask_login import current_user, login_required

from . import home

@home.route('/')
def homepage():
    """
    Render the homepage template on the / route
    """
    return render_template('home/index.html', title="Welcome")

@home.route('/welcome')
@login_required
def welcome():
    """
    Render the welcome template on the /welcome route
    """
    return render_template('home/welcome.html', title="Welcome ")


@home.route('/test2')
def test2():
    """
    [temporary] Render the test homepage template on the /test2 route
    """
    return render_template('home/index-attempt-to-fix-footer.html', title="Test2")

