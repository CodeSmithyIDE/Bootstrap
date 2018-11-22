class Input:
    def query(self, question, valid_answers, default):
        question += self._formatted_answers(valid_answers, default)
        user_answer = None
        while user_answer not in valid_answers:
            user_answer = input(question)
            if user_answer == "":
                user_answer = default
        return user_answer

    def _formatted_answers(self, valid_answers, default):
        formatted_answers = []
        for valid_answer in valid_answers:
            formatted_answer = valid_answer
            if valid_answer == default:
                if default.isnumeric():
                    formatted_answer += "(*)"
                else:
                    formatted_answer = valid_answer.upper()
            formatted_answers.append(formatted_answer)
        separator = "/"
        return " [" + separator.join(formatted_answers) + "] "
