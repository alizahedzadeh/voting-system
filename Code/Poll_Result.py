class Poll_Result:
    instances = []

    def __init__(self,choice_1_count = 0,choice_2_count = 0,choice_3_count = 0,choice_4_count = 0):
        self.choice_1_count = choice_1_count
        self.choice_1_count = choice_2_count
        self.choice_1_count = choice_3_count
        self.choice_1_count = choice_4_count
        self.instances.append(self)
