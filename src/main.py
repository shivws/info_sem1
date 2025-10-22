from time import sleep


def main():
    print('Calculator!\n')
    while True:
        try: print(eval(input('Input some problem: ')))
        except BaseException: print('Error')
        finally: sleep(1)


if __name__ != '__main__': raise('You can\'t use it as library')
else: main()
