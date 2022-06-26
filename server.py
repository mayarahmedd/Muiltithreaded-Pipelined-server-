from socket import *
import threading




class ClientThread(threading.Thread):
    def __init__(self, connect, address):
        threading.Thread.__init__(self)
        self.connection_socket = connect
        self.addr = address
        self.lockthread=threading.Lock()
        


      
    def run(self):
        
        lock = 0
        flag = 0
        try:
                
            
                if lock == 0:
                    message=b""
                    while True:
                        
        
                        messa = self.connection_socket.recv(1024)
                     
                        message+=messa
                        if len(messa)<1024:
                            break
                    if len(message)==0:
                        flag = 1
                    
                    if flag==0:   

                        self.lockthread.acquire()    
                        client_threadd = ClientThread(connectionSocket, addr,)
                        client_threadd.start()

                        

        
                        if message.find(b"GET") == -1:
                            method = "POST"
                        else:
                            method = "GET"


                        if method == "GET":
                        

                            filename = message.split()[1]             
                            if b".png" in filename:
                            
                                outdata = open(filename[1:],"rb").read()
                                x="\r\n"
                                x=x.encode()
                                outdata=outdata+x
                            
                             
                            
                            else:
                                f = open(filename[1:])
                                outdata = f.read()
                                outdata=outdata+"\r\n"
                                outdata=outdata.encode()
                                
                               

                            first_header = "HTTP/1.1 200 OK\r\n"
                                
                            header_information = {
                                    "Content-Length": len(outdata),
                                    "Keep-Alive": "timeout=%d,max=%d" % (50/ (threading.active_count() - 1), 50),
                                    "Connection": "Keep-Alive",
                                    "Content-Type": "text/html"
                                }
                            following_header = "\r\n".join("%s:%s" % (item, header_information[item]) for item in header_information)
                            print("first_header::", first_header)
                            print("following_header:", following_header)
                            headinitial=first_header+following_header+"\r\n\r\n"
                            headinitial=headinitial.encode()
                            
                            
                            head = headinitial + outdata
                            
                                # print(outputdata)
                                # time.sleep(20)

                            
                            lock=self.connection_socket.sendall(head)
                            

                            

                            if not lock:
                                    lock = 1
                            
                        elif method == "POST":
                                filename = message.split()[1]
                            
                                final = message


                                approve_info = {
                                    "HTTP/1.0 200 OK\r\n"
                                    "Content-Type": "text/html",
                                    "success": "true"
                                }
                                print("final:")
                                print(final)
                                if final:
                                    outputdataa = "\r\n".join("%s:%s" % (item, approve_info[item]) for item in approve_info)
                                    self.connection_socket.send(bytes(outputdataa.encode()))

                                filename = final.splitlines()
                                filename = filename[0]


                                
                                filename=filename.split(b"/")[1]
                                filename=filename.split(b" ")[0]

                                parsing_data=final.split(b"\r\n\r\n")[1]
                                parsing_data=parsing_data.rsplit(b"\r\n",1)[0]
                
                                filename=b"post"+filename
                                file=open(filename,'wb')
                                file.write(parsing_data)   
                                file.close()


        except IOError as e :
             if str(e) =="timed out":
                 print("Timeout")

                 self.connection_socket.close()                
             else:
                
                err = "HTTP/1.1 404 Not Found\r\n\r\n"
                self.connection_socket.sendall(bytes(err.encode()))
        if flag==0 & self.lockthread.acquire(True):
            self.lockthread.release() 
                

        


if __name__ == '__main__':
    serverSocket = socket(AF_INET, SOCK_STREAM)  # Prepare a sever socket
    serverPort = 6666
    serverHost = '127.0.0.1'
    serverSocket.bind((serverHost, serverPort))
    serverSocket.listen(5)
    threads = []
    while True:
        # Establish the connection
        connectionSocket, addr = serverSocket.accept()
        print('Ready to serve...')
        print("addr:\n", addr)
        timeoutt= 50 / (threading.active_count())
        connectionSocket.settimeout(timeoutt)
        # connectionSocket.settimeout(0.00000000000000000000001)
        client_thread = ClientThread(connectionSocket, addr,)
        
        # threading.Thread(daemon=True)
        client_thread.start()       
        # print("Length",threading.active_count()-1)      
        threads.append(client_thread)
    serverSocket.close()
