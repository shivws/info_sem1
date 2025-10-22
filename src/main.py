from time import sleep


def main():
    print('Calculator!\n')
    while True:
        try: print(eval(input('Input some problem: ')))
        except KeyboardInterrupt: return
        except BaseException as e: print(f'{type(e).__name__}!')
        else: sleep(1)


if __name__ != '__main__': raise('You can\'t use it as library')
else: main()
