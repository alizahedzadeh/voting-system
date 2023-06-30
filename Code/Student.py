import stdiomask
from Database import Database


class Student:
    instances = []

    def __init__(self):
        self.first_name = ""
        self.last_name = ""
        self.nat_code = None
        self.password = None
        self.logged_in = False
        self.student_id = ""
        self.manager_id = ""
        self.poll_id = ""
        self.can_show = False
        self.instances.append(self)

    def login(self):

        if self.logged_in:
            print("You are already logged in later")

        else:
            user = input("Nationality Code :")
            password = stdiomask.getpass(prompt="Password :")

            Dbase = Database()

            res = Dbase.login("student", user, password)

            if res[0]:
                self.logged_in = True
                self.student_id = res[1][0]
                self.first_name = res[1][1]
                self.last_name = res[1][2]
                self.nat_code = res[1][3]
                self.password = res[1][4]

    def logout(self):
        if self.logged_in:
            self.logged_in = False
            print("You are logged out , Good Bye !")
        else:
            print("You are not logged in yet")

    def polls_for_students(self):

        if self.logged_in:
            Dbase = Database()
            result = Dbase.show_polls_students_and_parents(("students", None), "audience")

            if len(result) == 0:
                print("No polls were created for students")
                return False

            else:
                self.can_show = True
                for index in result:
                    print(index[0], "-")
                    print("Title :", index[1])
                    print("Context :", index[2])
                    print("Published Date :", index[3])
                    print("Audiences :", index[4])
                    print("Choices :", index[5], "--", index[6], "--", index[7], "--", index[8])
                    print("*************")
                return True

        else:
            print("You Must Logged in First")
            return False

    def answer_poll(self):
        if self.logged_in:
            if self.polls_for_students():

                Dbase = Database()


                _id = input("Which poll do you want to take?(Please Select Id)")

                answered_polls = Dbase.check_answered_poll("student", self.student_id)[0]

                if not (answered_polls is None) and (_id in answered_polls):
                    print("You answered to this Poll , Can't answer again Sorry !!")
                else:
                    result = Dbase.show_polls_students_and_parents(("students", _id), "id")

                    if result is None:
                        print("There is no poll with such an ID : ")

                    else:
                        # print(result)
                        for index in result:
                            print("Title :", index[1])
                            print("Context :", index[2])
                            print("Published Date :", index[3])
                            print("Audiences :", index[4])
                            print("Choices :")
                            print("1 -", index[5])
                            print("2 -", index[6])
                            print("3 -", index[7])
                            print("4 -", index[8])

                        self.manager_id = index[-1]
                        self.poll_id = index[0]

                        choice = input("Select your choice(1/2/3/4) :")
                        Dbase.update_poll_result(self.poll_id, choice)
                        Dbase.update_answered_poll("student", self.student_id, self.poll_id)
            else:
                print("No polls created yet")

        else:
            print("You Must Logged in First")
