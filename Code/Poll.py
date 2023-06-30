from datetime import datetime

class Poll:
    instances = []

    def __init__(self, title, audience, context, choice_1, choice_2, choice_3, choice_4):
        time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        self.title = title
        self.audience = audience
        self.context = context
        self.published_date = time
        self.choice_1 = choice_1
        self.choice_2 = choice_2
        self.choice_3 = choice_3
        self.choice_4 = choice_4
        self.instances.append(self)
