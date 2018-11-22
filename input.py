class Input:
    def query(self, question, valid_answers, default):
        question += self._formatted_answers(valid_answers, default)
        user_answer = None
        while user_answer is None:
            user_input = input(question)
            if user_input == "":
                user_answer = default
            else:
                user_answer = self._lowercase_find(valid_answers, user_input)
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

    def _lowercase_find(self, valid_answers, answer):
        user_answer = None
        for valid_answer in valid_answers:
            if answer.lower() == valid_answer.lower():
                user_answer = valid_answer
                break
        return user_answer
                
