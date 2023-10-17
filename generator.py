class NumberGenerator:
    def __init__(self, m, a, c, X0, n):
        self.m = m
        self.a = a
        self.c = c
        self.X0 = X0
        self.n = n

    def generate(self):
        X = self.X0
        result = []

        for i in range(self.n):
            X = (self.a * X + self.c) % self.m
            result.append(X)

        return result


class GeneratorPeriod:
    def __init__(self, m, a, c, X0, ):
        self.m = m
        self.a = a
        self.c = c
        self.X0 = X0

    def get_period(self):
        X = self.X0
        result = []
        X = (self.a * X + self.c) % self.m
        result.append(X)
        i = 1

        while True:
            X = (self.a * X + self.c) % self.m
            if len(set(result)) < i:
                break
            else:
                result.append(X)
            i += 1

        return len(set(result))

