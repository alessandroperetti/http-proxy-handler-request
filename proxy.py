#****************  HTTP Proxy  ************************************
#*                                                                 *
#*              Version: 1.0                                       *
#*              Author: Alessandro Peretti                         *
#*                                                                 *
#*                                                                 *
#*                                                                 *
#*                                                                 *
#* The software is able to catch the request from the              *
#* browser where it is configured in and modified the              *
#* the request. Each request is written inside handlerequest.conf  *
#* and the user can change the content                             *
#                                                                  *
#**********************      USAGE     *****************************
#                                                                  *
#                     python proxy.py 9000                         *
#                                                                  *
#                                                                  *
#                                                                  *
#                                                                  *
#                                                                  *
#*******************************************************************

import os,sys,thread,socket


class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

#********* CONSTANT VARIABLES *********
BACKLOG = 50            # how many pending connections queue will hold
MAX_DATA_RECV = 999999  # max number of bytes we receive at once
DEBUG = True            # set to True to see the debug msgs
BLOCKED = []            # just an example. Remove with [""] for no blocking at all.


def main():

    # check the length of command running
    if (len(sys.argv)<2):
        print "\n"
        print colors.FAIL + "Please specify a port where the socket is listen to!" + colors.ENDC
        sys.exit(1) 
    else:
        if (int(sys.argv[1])<1024): # port from argument
            print "\n"
            print colors.FAIL + "Please specify another port. You're using a System port! " + colors.ENDC
            sys.exit(1)

    port = int (sys.argv[1])
    # host and port info.
    host = ''               # blank for localhost
    
    print colors.OKGREEN + "Proxy Server is Running" + colors.ENDC 

    try:
        # create a socket
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # associate the socket to host and port
        s.bind((host, port))

        # listenning
        s.listen(BACKLOG)
    
    except socket.error, (value, message):
        if s:
            s.close()
        print "Could not open socket:", message 
        sys.exit(1)

    # get the connection from client
    while 1:
        conn, client_addr = s.accept()

        # create a thread to handle request
        proxy(conn, client_addr)
        
    s.close()
#************** END MAIN PROGRAM ***************

def printout(type,request,address):
    if "Block" in type or "Blacklist" in type:
        colornum = 91
    elif "Request" in type:
        colornum = 92
    elif "Reset" in type:
        colornum = 93

    print "\033[",colornum,"m",address[0],"\t",type,"\t",request,"\033[0m"

#proxy function
def proxy(conn, client_addr):

    # get the request from browser
    request = conn.recv(MAX_DATA_RECV)

  #  print colors.OKGREEN+ request + colors.ENDC 
    

    # parse the first line
    first_line = request.split('\n')[0]

    # get url
    url = first_line.split(' ')[1]


    request = request_handler(request)

    print colors.OKGREEN + request + colors.ENDC

    for i in range(0,len(BLOCKED)):
        if BLOCKED[i] in url:
            printout("Blacklisted",first_line,client_addr)
            conn.close()
            sys.exit(1)
    
    # find the webserver and port
    http_pos = url.find("://")          # find pos of ://
    if (http_pos==-1):
        temp = url
    else:
        temp = url[(http_pos+3):]       # get the rest of url
    
    port_pos = temp.find(":")           # find the port pos (if any)

    # find end of web server
    webserver_pos = temp.find("/")
    if webserver_pos == -1:
        webserver_pos = len(temp)

    webserver = ""
    port = -1
    if (port_pos==-1 or webserver_pos < port_pos):      # default port
        port = 80
        webserver = temp[:webserver_pos]
    else:       # specific port
        port = int((temp[(port_pos+1):])[:webserver_pos-port_pos-1])
        webserver = temp[:port_pos]

    try:
        # create a socket to connect to the web server
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        s.connect((webserver, port))
        s.send(request)         # send request to webserver
        
        while 1:
            # receive data from web server
            data = s.recv(MAX_DATA_RECV)
            
            if (len(data) > 0):
                #*\n send to browser
                #print data
                conn.send(data)
            else:
                break
        s.close()
        conn.close()
    except socket.error, (value, message):
        if s:
            s.close()
        if conn:
            conn.close()
        printout("Peer Reset",first_line,client_addr)
        sys.exit(1)
   

#
# Manage and modify the request
#
def request_handler(request):
    wfile = open("handlerequest.conf","w")
    wfile.write(request)
    wfile.close()
    name = raw_input("Change file handlerequest.conf and press a key")
    #Reload the changed request and send it to destination webserver
    rfile = open("handlerequest.conf","r")
    request = rfile.read()
    rfile.close()
    return request

if __name__ == '__main__':
    main()


