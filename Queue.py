class Queue:
    def __init__(self):
        self.q = []
        self.seen = {}
  
    def push(self, val):
        if not val in self.seen:
            self.seen[val] = True
            self.q.append(val)

    def pop(self):
        if len(self.q) != 0:
            self.q.pop(0)

    def __len__(self):
        return len(self.q)

    def empty(self):
        return self.__len__() == 0
