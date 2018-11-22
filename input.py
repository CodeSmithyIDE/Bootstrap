from typing import List


class Input:
    """Provides functions to get user input."""

    def query(self, question: str, valid_answers: List[str], default: str):
        """Prints the text provided and awaits a response from the user.

        The answer given by the user must match one of the answers in the
        valid_answers argument. The question will be repeated until this
        condition is met.

        The comparison between the answer given by the user and the
        items in valid_answers is case-insensitive. The return value of the
        function will use the case from the valid_answers argument, not what
        was typed by the user.

        The only exception is when the user provides an empty answer. In that
        case the default value specified by the default argument will be
        returned.

        Parameters
        ----------
        question : str
            The text to print to the console.
        valid_answers: List[str]
            The list of valid answers.
        default: str
            The default answer that will be returned if the user provides an
            empty answer.

        Returns
        -------
        str
            The answer chosen by the user. This will be one of the items in the
            valid_answers argument or the default value.
        """
        question += self._formatted_answers(valid_answers, default)
        user_answer = None
        while user_answer is None:
            user_input = input(question)
            if user_input == "":
                user_answer = default
                break
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
                
