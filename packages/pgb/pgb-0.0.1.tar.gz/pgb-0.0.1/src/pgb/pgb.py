#!/usr/bin/env python3

try:
    import sys
    from os import system, popen
except:
    raise
    sys.exit(1)

class ProgressBar(object):
    """print a progress bar with:

    1. processes count given

    2. do a loop in processes count and call "mark_as_done" method
    """

    def __init__(self, processes_count=0):
        super(ProgressBar, self).__init__()

        # init vars:
        try:
            self.processes_count = int(processes_count)
            self.step = 0
            self.percentage = 0
            self.term_step = 0
            self.term_lenght = lambda: int(popen('stty size', 'r').read().split()[1]) - 2
            self.left_term_lenght = lambda: self.term_lenght() - self.term_step
        except:
            raise
            sys.exit(1)

        # init bar:
        print()
        self.command = lambda: f'[{"#" * (self.term_lenght() - self.left_term_lenght())}{"." * self.left_term_lenght()}]'

    def mark_as_done(self):
        """mark the active process as done.
        """
        self.step += 1
        self.percentage = int((self.step * 100) / self.processes_count)
        self.term_step = int((self.percentage * self.term_lenght()) / 100)
        system(f'echo \033[A{self.command()}')

def main():
    from time import sleep
    try:
        bar = ProgressBar(processes_count=int(input("Please enter your processes count: ")))
    except:
        raise
        sys.exit(1)

    if str(input('Do you want to use "time.sleep(secends)" or not? (y, N): ')) == "y":
        try:
            print('using the "time" library ("sleep" function).')
            time = float(input("Please enter the time that you want to sleep at every loop (secends unit): "))
        except Exception:
            raise
            sys.exit(1)
        for i in range(bar.processes_count):
            bar.mark_as_done()
            sleep(time)
    else:
        print("choosed no.")
        print()
        for i in range(bar.processes_count):
            bar.mark_as_done()
        
if __name__ == '__main__':
    main()
