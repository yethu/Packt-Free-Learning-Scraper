from orator import DatabaseManager, Model

import dbconfig

db = DatabaseManager(dbconfig.databases)
Model.set_connection_resolver(db)


class Book(Model):
    pass
