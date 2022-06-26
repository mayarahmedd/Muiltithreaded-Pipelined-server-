import sys
from socket import *
import os.path
import time

"""
Command line argument: import sys sys.argv
sys.argv is a list,no need for split
"""
inputFile = sys.argv[1]
# inputFile = "input.txt"
if os.path.isfile(inputFile):

    fop = open(inputFile)
    lines = fop.readlines()
    data = fop.read()
    fop.close()
    
    cach_dict={}

    
    for line in lines:
        # print(cach_dict)
        line = line.split()
        server_host = line[2]

        if len(line) == 4:
            server_port = line[3]
            server_port = server_port.split("(")[1].split(")")[0]


        else:
            server_port = 80
        filename = line[1]
        method = ""

        if "POST" == line[0]:
            method = "POST"
        elif "GET" == line[0]:
            method = "GET"
        
        file=server_host+filename 
        # print ("initial file:")
        # print(file)

        host_port = "%s:%s" % (server_host, server_port)
        try:
            

            if method == "GET":

                httpHeader = "GET /%s HTTP/1.1\r\n" % (filename)
                httpHeader += "host: %s\r\n\r\n" % (server_host)
            else:
                httpHeader = "POST /%s HTTP/1.1\r\n" % (filename)
                httpHeader += "host: %s\r\n\r\n" % (server_host)

            if method == "GET":
                
            
                    
             if httpHeader in cach_dict.keys():
                    
                    print('Fetched successfully from cache.')
                    serverheader=cach_dict.get(httpHeader)[0]
                    messagee=cach_dict.get(httpHeader)[1]
                    print("header:\r\n")
                    print(httpHeader)
                    print("serverheader:\r\n")
                    print(serverheader)
                    if messagee !=" ":
                        print("message:\r\n")
                        print(messagee)

             else:
                ClientSocket = socket(AF_INET, SOCK_STREAM)
                ClientSocket.connect((server_host, int(server_port)))
                
            
                ClientSocket.sendall(httpHeader.encode())
                if(".png" in filename):
                    ResponseMessage = b""
                               
                                
                    while True:
                
                        messa = ClientSocket.recv(1024)
                        ResponseMessage+=messa
                        if len(messa)<1024:
                            break
                   
                    head=ResponseMessage.split(b"\r\n\r\n")[0]                    
                    print("head",head)


                    final = ResponseMessage

                    print('Not in cache. Fetching from server.')
                    # print("final:\n" + final)
                    
                    ClientSocket.close()
                   
                    head=final.split(b"\r\n\r\n")[0] 
                    if b"404 Not Found" not in head:
                        parsing_data=final.split(b"\r\n\r\n")[1]
                        parsing_data=parsing_data.rsplit(b"\r\n",1)[0]
                        cach_dict[httpHeader]=[head,parsing_data]
                        # print(parsing_data)

                        filename="get"+filename
                        print("filename:")
                        print(filename)

                        f1= open(filename, 'wb')
                        f1.write(parsing_data)
                        f1.close()
                    else :
                        parsing_data=" "
                        cach_dict[httpHeader]=[head,parsing_data]
                        # print(parsing_data)

                        filename="get"+filename
                        print("filename:")
                        print(filename)

                        f1= open(filename, 'w')
                        f1.write(parsing_data)
                        f1.close()

                else:

                        ResponseMessage = ""
                                
                                    
                        while True:
                            # time.sleep(5)
                            messa = ClientSocket.recv(1024).decode()
                            ResponseMessage+=messa
                            if len(messa)<1024:
                                break
                    
                        head=ResponseMessage.split("\r\n\r\n")[0]
                       
                        final = ""
                        final = ResponseMessage
                       
                        print('Not in cache. Fetching from server.')
                        print("final:\n" + final)
                        head=final.split("\r\n\r\n")[0]

                        if "404 Not Found" not in head:
                            parsing_data=final.split("\r\n\r\n")[1]
                            parsing_data=parsing_data.rsplit("\r\n",1)[0]
                            cach_dict[httpHeader]=[head,parsing_data]

                            filename="get"+filename
                            f1= open(filename, 'w')
                            f1.write(parsing_data)
                            f1.close()
                        else :
                            parsing_data=" "
                            cach_dict[httpHeader]=[head,parsing_data]
                            # print(parsing_data)

                            filename="get"+filename
                            print("filename:")
                            print(filename)

                            f1= open(filename, 'w')
                            f1.write(parsing_data)
                            f1.close()

                                      
            elif method == "POST":
                
                 if httpHeader in cach_dict.keys():
                    
                    print('Fetched successfully from cache.')
                   
                    responsee=cach_dict.get(httpHeader)[0]          
                    print("header:\r\n")
                    print(httpHeader)
                    print("response:\r\n")
                    print(responsee)
                    
                 else:
                     
                        ClientSocket = socket(AF_INET, SOCK_STREAM)
                        ClientSocket.connect((server_host, int(server_port)))
                        if(".png" in filename): 
                            dataa= open(filename,'rb').read()
                            httpHeader=httpHeader.encode()
                            x="\r\n".encode()
                            dataa = httpHeader + dataa + x
                            test = ClientSocket.sendall(dataa)
                            print('Not in cache. Fetching from server.')
                            message_approve = ClientSocket.recv(1024).decode()
                            print("approve:\n", message_approve)
                            ClientSocket.close()
                            cach_dict[httpHeader]=[message_approve]
                            
                        else:
                            f1 = open(filename)
                            dataa = f1.read()

                            dataa = httpHeader + dataa + "\r\n"
                             
                            test = ClientSocket.sendall(dataa.encode())
                            print('Not in cache. Fetching from server.')
                            message_approve = ClientSocket.recv(1024).decode()
                            print("approve:\n", message_approve)
                            ClientSocket.close()
                            cach_dict[httpHeader]=[message_approve]

                           
        except IOError:
                sys.exit(1)