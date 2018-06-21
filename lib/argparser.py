import argparse as ap



class InputArguments:
    def __init__(self):
        self.parser = ap.ArgumentParser()
        self.parser.add_argument('--host', type=str, help='broker host address')
        self.parser.add_argument('-p', type=int, help='broker port number')
        self.parser.add_argument('--sensor', type=bool, help='sensor name')
        self.parser.add_argument('-t', type=bool, help='publish cpu temperature')
        self.parser.add_argument('--res', type=bool, help='publish cpu resources')
        self.parser.add_argument('--refr', type=float, help='refresh rate')

    def prepare(self):
        return 0