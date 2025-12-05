import queue


#alla on erillinen input threadi, joka ajaa main-loopin kanssa samaan aikaan
#syy: ilman tätä aiempi main-loopissa ollut input() pausetti koko loopin sekä ajan kulun

player_input_queue = queue.Queue()

global running

def get_input(running_flag):
    while running_flag():
        try:
            thread_input = input("> ")
            if not running_flag():
                break
            player_input_queue.put(thread_input)
        except EOFError:
            break