import time

import psycopg2


# noinspection PyMethodMayBeStatic
class PostgreSqlChecker(object):
    def __init__(self):
        super(PostgreSqlChecker, self).__init__()
        self.connection = None

    def wait_for_database_ready(self):
        # Define our connection string
        conn_string = "host='localhost' dbname='postgres' user='postgres' password=''"
        conn_string += " port='%d'" % 5432

        # print the connection string we will use to connect
        print "Connecting to database\n	->%s" % (conn_string)

        # Check if postgresql started correctly
        retry_cnt = 0
        while True:
            time.sleep(1)
            try:
                # get a connection, if a connect cannot be made an exception will be raised here
                self.connection = psycopg2.connect(conn_string)
                break
            except psycopg2.OperationalError:
                retry_cnt += 1
                print "retrying to connect postgresql server"
                if retry_cnt > 20:
                    print "postgresql start failed"
                    raise "Can not start database!!!"

    def is_django_table_created(self):
        cur = self.connection.cursor()
        try:
            cur.execute("""SELECT * from auth_user""")
            rows = cur.fetchall()
            return True
        except:
            return False

