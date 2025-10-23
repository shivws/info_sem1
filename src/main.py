from time import sleep


def main():
    while True:
        print("Hello worker!")
        sleep(1)


if __name__ != '__main__': raise('You can\'t use it as a library')
else: main()
