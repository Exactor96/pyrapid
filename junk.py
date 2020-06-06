class A:
    class B:
        def __init__(self):
            self.q1 = []
            self.q2 = []
            self.q3 = []

        def add_to_q1(self, obj):
            self.q1.append(obj)

        def add_to_q2(self, obj):
            self.q2.append(obj)

        def print_all_q(self):
            print(f'q1: {self.q1}')
            print(f'q2: {self.q2}')
            print(f'q3: {self.q3}')

    def __init__(self):
        self.B = self.B()

    def run(self):
        for i in range(10):
            if i % 2 == 0:
                self.B.add_to_q1(i)
            else:
                self.B.add_to_q2(i)

        self.B.print_all_q()

a = A()

a.run()