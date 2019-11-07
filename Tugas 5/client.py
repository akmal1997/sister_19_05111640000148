import Pyro4
import base64
import json
import sys
import re

namainstance = sys.argv[1] or "sembrani"

def get_fileserver_object(host='localhost', port=50001):
    uri = "PYRONAME:{}@{}:{}" . format(namainstance, host, str(port))
    fserver = Pyro4.Proxy(uri)
    return fserver

def parseCommand(cmd):
    if cmd == None or cmd == '':
        return None
    parse = re.sub(r'\n', '', cmd)
    parse = parse.split(' ')
    if parse[0] == 'LIST':
        return ['LIST', None]
    elif parse.__len__() != 2:
        return ['Error', 'Filename doesn\'t exist / incorrect parameter']
    elif parse[0] == 'SEND' or parse[0] == 'DEL' or parse[0] == 'READ' or parse[0] == 'EDIT':
        return parse
    else:
        return ['Error', 'Incorrect command']

if __name__=='__main__':
    proxy = get_fileserver_object()
    proxy.report(namainstance)
    try:
        while True:
            response = ''
            print("Available command:\n\
                    SEND [filename]\t=> Send file \"filename\" to server\n\
                    DEL [filename]\t=> Delete file \"filename\" from server\n\
                    READ [filename]\t=> Read file \"filename\" from server\n\
                    EDIT [filename]\t=> Edit file \"filename\" from server\n\
                    LIST\t\t=> List files in server\n")

            cmd = input(">> ")
            cmd = parseCommand(cmd)
            print(cmd)
            if cmd[0] == 'SEND':
                response += str(proxy.create(cmd[1]))
                response += str(proxy.update(cmd[1], content = open(cmd[1],'r+b').read()))
            elif cmd[0] == 'EDIT':
                response += str(proxy.update(cmd[1], content = open(cmd[1],'r+b').read()))
            elif cmd[0] == 'READ':
                response += str(proxy.read(cmd[1]))
            elif cmd[0] == 'DEL':
                response += str(proxy.delete(cmd[1]))
            elif cmd[0] == 'LIST':
                response += str(proxy.list())
            else:
                print(cmd[0]+cmd[1])
                continue

            print(response)
    except KeyboardInterrupt:
        sys.exit("Client Closed.")
