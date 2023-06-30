from Database import Database
import stdiomask
from Poll import Poll
from Poll_Result import Poll_Result


class Manager:
    instances = []

    def __init__(self):
        self.first_name = ""
        self.last_name = ""
        self.nat_code = None
        self.password = None
        self.role = ""
        self.logged_in = False
        self.reg = False
        self.can_show = False
        self.manager_id = ""

    def register(self):

        if self.reg:
            print("You are already registered later")

        else:
            Dbase = Database()

            n_code = input("Nationality Code :")

            if Dbase.check_natcode(n_code):

                self.nat_code = n_code

                f_name = input("First Name :")
                self.first_name = f_name

                l_name = input("Last Name :")
                self.last_name = l_name

                password = stdiomask.getpass(prompt="Password :")
                self.password = password

                role = input("Your Role :")
                self.role = role

                self.instances.append(self)

                Dbase.insert_new_manager((self.first_name, self.last_name, self.nat_code, self.password, self.role))
                self.reg = True
            else:
                print("This nationality code is repetitive")

    def login(self):

        if self.logged_in:
            print("You are already logged in later")

        else:
            user = input("Nationality Code :")
            password = stdiomask.getpass(prompt="Password :")

            Dbase = Database()


            res = Dbase.login("manager",user, password)

            if res[0]:
                #print(res)
                self.logged_in = True
                self.reg = True
                self.manager_id = res[1][0]
                self.first_name = res[1][1]
                self.last_name = res[1][2]
                self.nat_code = res[1][3]
                self.password = res[1][4]
                self.role = res[1][5]


    def logout(self):
        if self.logged_in:
            self.logged_in = False
            print("You are logged out , Good Bye !")
        else:
            print("You are not logged in yet")

    def show_all_polls(self):
        if self.logged_in:
            Dbase = Database()
            data = Dbase.show_polls()
            #print(data)

            if len(data) == 0:
                print("No polls created yet")
                return False
            else:
                self.can_show = True
                for index in data:
                    print(index[0], "-")
                    print("Title :", index[1])
                    print("Context :", index[2])
                    print("Published Date :", index[3])
                    print("Audiences :", index[4])
                    print("Choices :", index[5], "--", index[6], "--", index[7], "--", index[8])
                    print("*************")
                return True

        else:
            print("You Must Logged in first")
            return False


    def create_poll(self):

        if self.logged_in:
            title = input("Poll title :")
            audience = input("Poll audience (parents or students) :")
            context = input("Poll context :")
            choice_1 = input("Choice 1 :")
            choice_2 = input("Choice 2 :")
            choice_3 = input("Choice 3 :")
            choice_4 = input("Choice 4 :")
            obj = Poll(title, audience, context, choice_1, choice_2, choice_3, choice_4)

            data = (obj.title, obj.context, obj.published_date,
                    obj.audience, obj.choice_1, obj.choice_2, obj.choice_3, obj.choice_4, self.manager_id)

            poll_result = Poll_Result()

            Dbase = Database()
            Dbase.insert_new_poll(data)

        else:
            print("You Must Login first")

    def show_polls_result(self):
        if self.logged_in:
            if self.show_all_polls():

                print("\n")
                Dbase = Database()

                key = input("Which poll report do you want to view?")
                result = Dbase.show_polls_results(key)

                if result is None:
                    print("There is no poll with such an ID")

                else:
                    for index in result:
                        print("***********")
                        print("Title :", index[0])
                        print("Context :", index[1])
                        print("Published_date :", index[2])
                        print("Audience :", index[3])

                        s = index[8] + index[9] + index[10] + index[11]
                        if s == 0:
                            print("Note : No one answered to this poll !!")
                            r = [0, 0, 0, 0]
                        else:
                            r = [(index[8] / s), (index[9] / s), (index[10] / s), (index[11] / s)]
                            r = list(map(lambda x: x * 100, r))


                        print("1 -", index[4], "--", "(Number :", index[8], ")", "(Percentage :", round(r[0],2), "%)")
                        print("2 -", index[5], "--", "(Number :", index[9], ")", "(Percentage :", round(r[1],2), "%)")
                        print("3 -", index[6], "--", "(Number :", index[10], ")", "(Percentage :", round(r[2],2), "%)")
                        print("4 -", index[7], "--", "(Number :", index[11], ")", "(Percentage :", round(r[3],2), "%)")
            else:
                print("No polls created yet")
        else:
            print("You Must Login first")
