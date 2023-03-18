import mysql.connector

class dbDriver:
    conection = ""
    def __init__(self):
        host_aa='localhost'
        data_base = 'regain'
        user_aa ='root'
        password_aa = 'root_password'
        self.conection = mysql.connector.connect(user=user_aa, password=password_aa,
                                host=host_aa,database=data_base)


    def sql_run(self, sql_str):
        cursor = self.conection.cursor (dictionary=True)
        cursor.execute (sql_str)
        rows = cursor.fetchall ()

        return rows



    def db_close(self):
        self.conection.close()