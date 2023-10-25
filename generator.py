import json
from tkinter import messagebox


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

    @classmethod
    def from_config_file(cls, filename, x0, n):
        default_values = {
            'm': 4095,
            'a': 1024,
            'c': 2,
            'X0': 8
        }
        try:
            with open(filename, 'r') as config_file:
                config_data = json.load(config_file)

                # Перевірка, чи значення є цілими числами
                if all(map(lambda x: isinstance(x, int) and x > 0,
                           [config_data['m'], config_data['a'], config_data['c'], config_data['X0']])):
                    return cls(config_data['m'], config_data['a'], config_data['c'], x0, n)
                else:
                    m = int(default_values['m'])
                    a = int(default_values['a'])
                    c = int(default_values['c'])
                    return cls(m, a, c, x0, n)
        except:
            m = int(default_values['m'])
            a = int(default_values['a'])
            c = int(default_values['c'])
            return cls(m, a, c, x0, n)


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

