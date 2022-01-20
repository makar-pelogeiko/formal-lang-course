class ObserverOtput:
    def __init__(self):
        self.out_lst = []

    def show(self):
        for string in self.out_lst:
            print(string)

        temp_lst = self.out_lst
        self.out_lst = []

        return temp_lst

    def send_out(self, string: str):
        self.out_lst.append(string)
