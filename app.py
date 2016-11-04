from eve import Eve
from eve_sqlalchemy import SQL
from eve_sqlalchemy.validation import ValidatorSQL
from schema import User, Base

app = Eve(auth=None, data=SQL, validator=ValidatorSQL)
db = app.data.driver
Base.metadata.bind = db.engine
db.Model = Base
db.create_all()
if __name__ == '__main__':
    app.run(debug=True)