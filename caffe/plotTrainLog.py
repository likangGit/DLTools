import threading
import time
def input_func(context):
    context['data'] = input("press q to quit\n")

context={'data':'a'}
if __name__ == "__main__":
    t = threading.Thread(target=input_func, args=(context,))
    t.start()
    while True:
        t.join(3)
        print("x:",context)
        if context['data'] == 'q':
            break
    print("quit")