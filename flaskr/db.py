from flask import g, current_app


def get_db():
    if 'db' not in g:
        g.db = current_app.config["firebase"].database()
    return g.db
    # if 'db' not in g:
    #     # g.db = psycopg2.connect(user="blackBoxAdmin",
    #     #                         password="12345678",
    #     #                         host="127.0.0.1",
    #     #                         port="5432",
    #     #                         database="BlackBoxExplanation")
    #
    #     g.db = psycopg2.connect(user=current_app.config['USERNAME'],
    #                             password=current_app.config['PASSWORD'],
    #                             host=current_app.config['HOST'],
    #                             port=current_app.config['PORT'],
    #                             database=current_app.config['DATABASE'])


# def close_db(e=None):
#     # db = g.pop('db', None)
#     # if db is not None:
#     #     db.close()
#     pass
#
#
# def check_db():
#     # db = get_db()
#
#     # check if connection to the database is successful
#     # as we will initialize DB ourselves remotely.
#
#     # Print PostgreSQL Connection properties
#     # print(db.get_dsn_parameters())
#     # print("using firebase")
#     pass


# @click.command('init-db')
# @with_appcontext
# def check_db_command():
#     check_db()
#     click.echo('Connection checked')
#
#
# def init_app(app):
#     app.teardown_appcontext(close_db)
#     app.cli.add_command(check_db_command)
