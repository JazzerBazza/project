from application import app
from flask import render_template, g, flash, redirect, url_for, request
import pymysql




def connect_db():
    return pymysql.connect(
        user = 'root', password = 'password', database = 'Cohort4',
        autocommit = True, charset = 'utf8mb4',
        cursorclass = pymysql.cursors.DictCursor)



def get_db():
    '''Opens a new database connection per request.'''
    if not hasattr(g, 'db'):
        g.db = connect_db()
    return g.db

@app.teardown_appcontext
def close_db(error):
    '''Closes the database connection at the end of request.'''
    if hasattr(g, 'db'):
        g.db.close()


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM Customer WHERE username = %s AND password = %s', (Username, Password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['Username'] = account['Username']
            # Redirect to home page
            return 'Logged in successfully!'
        else:
            # Account doesn't exist or username/password incorrect
            msg = 'Incorrect username/password!'
    return render_template('login.html', msg='')



@app.route('/')
def home_page():
    return render_template('home.html', title='Skys The Limit Store')


@app.route('/products', methods=['GET', 'POST'])
def products1():
    """ Display Products Page    """
    cursor = get_db().cursor()
    cursor.execute("SELECT Product_id, image, Product_name, Gender, Price from products order by Product_id asc")
    result = cursor.fetchall()
    app.logger.info(result)
    return render_template(
                'products.html',
                title="Products Page",
                description="Check out our great products",
                records=result
    )

@app.route('/products/<int:id>')
def product_display(id):
    app.logger.info(id)
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM products WHERE Product_id=%s ", id)
    result = cursor.fetchone()
    app.logger.info(result)
    return render_template(
                'item.html',
                title="Third database query - using products template, passing parameter to query",
                description=f"Another db query with parameter from url: Product_id={id}.",
                records=result
    )

@app.route('/product/delete/<int:id>')
def customer_delete(id):
    """ Fourth route. Param for deleting from Actor table
    """
    app.logger.info(id)
    cursor = get_db().cursor()
    cursor.execute("DELETE FROM customer WHERE customer_id=%s ",id)
    message=f"Deleted product id {id}"
    app.logger.info(message)
    flash(message)
    return redirect(url_for('home'))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    """ Admin Inventory Page    """
    cursor = get_db().cursor()
    cursor.execute("SELECT Product_id, Product_name, Gender, Price, Quantity_Small, Quantity_Medium, Quantity_Large, Quantity_Xlarge from products order by Product_id asc")
    result = cursor.fetchall()
    app.logger.info(result)
    return render_template(
                'admin.html',
                title="Admin Page",
                description="Stock Inventory",
                records=result
    )

@app.route('/about')
def about():
    return render_template(
        'about.html',
        title="About Us",
        description="We are a group of 4 brought together from different regions of Sky Home Service",
        names=['Barrie', 'Rob', 'Sean', 'Zee']
    )



