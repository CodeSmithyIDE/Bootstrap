class Input:
    def query(self, question, valid_answers, default):
        answers = []
        for valid_answer in valid_answers:
            answer = valid_answer
            if valid_answer == default:
                if default.isnumeric():
                    answer += "(*)"
                else:
                    answer = valid_answer.upper()
            answers.append(answer)
        separator = "/"
        question += " [" + separator.join(answers) + "] "
        user_answer = None
        while user_answer not in valid_answers:
            user_answer = input(question)
            if user_answer == "":
                user_answer = default
        return user_answer
