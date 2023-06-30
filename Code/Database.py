import mysql.connector

class Database:

    def __init__(self):
        try:
            self.conn = mysql.connector.connect(host='localhost',
                                                database='vote_system',
                                                user='root',
                                                password='$5*12mnJkiOLaa190')
        except mysql.connector.Error as error:
            raise error

    def check_natcode(self, code):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM vote_system.manager where nat_code={Nat_Code}".format(Nat_Code=code))
        result = cursor.fetchall()
        cursor.close()

        if len(result) > 0:
            return False
        else:
            return True

    def show_polls(self):
        cursor = self.conn.cursor()

        cursor.execute("SELECT * FROM vote_system.poll;")

        results = cursor.fetchall()

        return results

    def insert_new_manager(self, data):
        cursor = self.conn.cursor()

        cursor.execute("select count(*) from manager")
        ID = cursor.fetchone()[0] + 1

        sql = "INSERT INTO manager (id, first_name,last_name,nat_code,password,role) VALUES (%s,%s,%s,%s,%s,%s)"
        val = (ID, data[0], data[1], data[2], data[3], data[4])
        cursor.execute(sql, val)
        self.conn.commit()

        print("You Registered Succesfully")
        cursor.close()

    def login(self, user, nat_code, password):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM {u} "
                       "where nat_code = {n} and password = '{p}' ;".format(u=user, n=nat_code, p=password))

        result = cursor.fetchone()

        if result is None:
            print("There is no user with this information")
            return False, 0

        else:
            print("User", result[1], result[2], "Logged in.")
            return True, result

    def insert_new_poll(self, data):
        cursor = self.conn.cursor()

        cursor.execute("select count(*) from poll")
        ID = cursor.fetchone()[0] + 1

        sql = "INSERT INTO poll (id, title,context,published_date,audience,choice_1,choice_2,choice_3,choice_4,Manager_ID) " \
              "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (ID, data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8])
        cursor.execute(sql, val)
        self.conn.commit()

        sql_2 = "insert into poll_result values({id},0,0,0,0,{id},{manager_id});".format(id=ID, manager_id=data[-1])
        cursor.execute(sql_2)
        self.conn.commit()

        print("New Poll Created")
        cursor.close()

    def show_polls_students_and_parents(self, data, Type):
        cursor = self.conn.cursor()
        user = data[0]
        _id = data[1]
        if Type == "audience":
            cursor.execute("SELECT * FROM poll where audience='{u}';".format(u=user))
            result = cursor.fetchall()
        elif Type == "id":
            cursor.execute("SELECT * FROM poll where ID='{ID}';".format(ID=_id))
            result = cursor.fetchall()

        return result

    def update_poll_result(self, poll_id, choice):
        choices = {"1": "choice_1_count",
                   "2": "choice_2_count",
                   "3": "choice_3_count",
                   "4": "choice_4_count"
                   }
        key = choices[choice]
        cursor = self.conn.cursor()

        cursor.execute("update poll_result set {column} = {column} + 1 where  Poll_ID = {p_id};"
                       .format(column=key, p_id=poll_id))
        self.conn.commit()
        print("Poll result updated")

    def show_polls_results(self, poll_id):

        cursor = self.conn.cursor()

        sql = "SELECT title,context,published_date," \
              "audience,choice_1,choice_2,choice_3," \
              "choice_4,choice_1_count,choice_2_count," \
              "choice_3_count,choice_4_count" \
              " FROM poll INNER JOIN poll_result ON poll.ID=poll_result.Poll_ID " \
              "and poll.ID = {ID};".format(ID=poll_id)

        cursor.execute(sql)
        result = cursor.fetchall()

        return result

    def check_answered_poll(self, user, user_id):

        cursor = self.conn.cursor()

        sql = "SELECT answered_poll FROM {User} where ID = {ID} ;".format(User=user, ID=user_id)
        cursor.execute(sql)

        result = cursor.fetchone()

        return result

    def update_answered_poll(self, user, user_id, poll_id):

        cursor = self.conn.cursor()
        cmd = "CONCAT"

        check_null = "select answered_poll from {User} where ID = {ID}".format(User=user, ID=user_id)
        cursor.execute(check_null)
        res = cursor.fetchone()

        if res[0] is None:
            cmd = "COALESCE"

        sql = "update {User} set answered_poll = {CMD}(answered_poll,{Poll_id}) where ID = {ID};".format(
            User=user, Poll_id=poll_id, ID=user_id, CMD=cmd
        )

        cursor.execute(sql)

        self.conn.commit()
