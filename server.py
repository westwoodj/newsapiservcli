# import socket programming library 
import socket

# import thread module 
from _thread import *
import threading


#newsapi imports
import pandas as pd
from newsapi import NewsApiClient
import json

print_lock = threading.Lock()

API_KEY="1562ed02072f49a193518d143d65603d"

newsApi = NewsApiClient(api_key=API_KEY)

def runAPI(datastream):

    data = newsApi.get_everything(q=datastream.get('q'),sources="", language=datastream.get('language'), sort_by=datastream.get('sort_by'), page_size=datastream.get('page_size'))


    articles = data['articles']

    df = pd.DataFrame(articles)

    print(df)
    return df


def recv_basic(the_socket):
    total_data=[]
    while True:
        data = the_socket.recv(8192)
        if not data: break
        total_data.append(data)
    return ''.join(total_data)


# thread function
def threaded(c):
    while True:

        # data received from client

        data = c.recv(8192)
        data = json.loads(data)
        if not data:
            print('Bye')

            # lock released on exit 
            print_lock.release()
            break

        print(data)

        articles = runAPI(datastream=data)

        data = articles.to_json(orient="index")
        # send back reversed string to client 
        c.send(bytes(data, encoding="utf-8"))

        # connection closed
    c.close()


def Main():
    host = ""

    # reverse a port on your computer 
    # in our case it is 12345 but it 
    # can be anything 
    port = 12345
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("socket binded to port", port)

    # put the socket into listening mode 
    s.listen(5)
    print("socket is listening")

    # a forever loop until client wants to exit 
    while True:
        # establish connection with client
        c, addr = s.accept()

        # lock acquired by client 
        print_lock.acquire()
        print('Connected to :', addr[0], ':', addr[1])

        # Start a new thread and return its identifier 
        start_new_thread(threaded, (c,))
    s.close()


if __name__ == '__main__':
    Main() 