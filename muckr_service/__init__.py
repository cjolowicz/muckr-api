import flask
import flask_sqlalchemy
import flask_restless

if flask_restless.__version__ == '0.17.0':
    # flask_restless swallows its own only use of ValidationError, replacing the
    # error message "Model does not have field '{0}'" with "Could not determine
    # specific validation errors".

    import flask_restless.views

    def _extract_validation_error_message(exception):
        try:
            left, _ = str(exception).rsplit("'", 1)
            _, fieldname = left.rsplit("'", 1)
            return {fieldname: str(exception)}
        except ValueError:
            return None

    def extract_error_messages(exception):
        rv = _extract_error_messages(exception)
        if rv is None and isinstance(exception, flask_restless.views.ValidationError):
            return _extract_validation_error_message(exception)
        return rv

    _extract_error_messages, flask_restless.views.extract_error_messages = \
        flask_restless.views.extract_error_messages, extract_error_messages

app = flask.Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = flask_sqlalchemy.SQLAlchemy(app)

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode, unique=True)
    birth_date = db.Column(db.Date)

class Computer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode, unique=True)
    vendor = db.Column(db.Unicode)
    purchase_time = db.Column(db.DateTime)
    owner_id = db.Column(db.Integer, db.ForeignKey('person.id'))
    owner = db.relationship('Person', backref=db.backref('computers',
                                                         lazy='dynamic'))

db.create_all()

manager = flask_restless.APIManager(app, flask_sqlalchemy_db=db)

# Create API endpoints, which will be available at /api/<tablename> by
# default.
manager.create_api(Person, methods=['GET', 'POST', 'DELETE'])
manager.create_api(Computer, methods=['GET'])

if __name__ == '__main__':
    app.run()
