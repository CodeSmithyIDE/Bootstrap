class Input:
    def query(self, question, valid_answers):
        answer = None
        while answer not in valid_answers:
            answer = input(question + " ")
        return answer
        
