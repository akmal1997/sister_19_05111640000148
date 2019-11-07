import os
import base64
from collections import defaultdict
class FileServer(object):
    peer = []
    filestate = None

    def __init__(self):
        pass

    def report(self, client_id):
        print(str(client_id) + ' has been connected')

    def init_filestate(self):
        FileServer.filestate = defaultdict(str)
        for x in os.listdir("{}".format(FileServer.basedir)):
            FileServer.filestate[x[FileServer.id.__len__()+1:]] = 'unlock'
        print(FileServer.filestate)

    def get_filestate(self, filename):
        if filename in FileServer.filestate:
            return FileServer.filestate[filename]
        else:
            return 'unlock'

    def unlock_file(self, filename):
        FileServer.filestate[filename] = 'unlock'

    def set_identifier(self, id):
        FileServer.id = id
        FileServer.basedir = id
        FileServer.init_filestate(FileServer)

    def add_peer(self, peer_proxy):
        FileServer.peer.append(peer_proxy)
    
    def is_unlocked(self, filename):
        flag = True
        for peer_proxy in FileServer.peer:
            if not FileServer.is_unlocked_peer(FileServer, filename, peer_proxy):
                flag = False
                break

        return flag 

    def is_unlocked_peer(self, filename, peer_proxy):
        return (peer_proxy.get_filestate(filename) == 'unlock')

    def propagate(self, cmd, filename=None):
        flag = False
        for peer_proxy in FileServer.peer:
            if not FileServer.is_unlocked_peer(FileServer, filename, peer_proxy):
                flag = True
                break

        if flag:
            return FileServer.create_return_message(FileServer, '9999','File masih dipakai oleh pengguna lain')

        # FileServer.filestate[filename] = 'lock'
        ret = None

        if cmd == 'create':
            for peer_proxy in FileServer.peer:
                peer_proxy.create(filename, prop=False)
            ret = FileServer.create_return_message(FileServer, '100','OK')
        elif cmd == 'update':
            for peer_proxy in FileServer.peer:
                peer_proxy.update(filename, content = open(str(FileServer.basedir)+'/'+str(FileServer.basedir)+"-"+filename,'r+b').read(), prop=False)
            ret = FileServer.create_return_message(FileServer, '101','OK')
        elif cmd == 'delete':
            for peer_proxy in FileServer.peer:
                peer_proxy.delete(filename, prop=False)
            ret = FileServer.create_return_message(FileServer, '101','OK')
        else:
            pass

        FileServer.filestate[filename] = 'unlock'
        return ret

    def create_return_message(self,kode='000',message='kosong',data=None):
        return dict(kode=kode,message=message,data=data)

    def list(self):
        print("list ops")
        print("{}".format(FileServer.basedir))
        try:
            daftarfile = []
            prefix = "{}-".format(FileServer.id)
            for x in os.listdir("{}".format(FileServer.basedir)):
                print(x[0:FileServer.id.__len__()])
                if x[0:FileServer.id.__len__()+1] == prefix:
                    daftarfile.append(x[FileServer.id.__len__()+1:])
            return FileServer.create_return_message(FileServer, '200',daftarfile)
        except:
            return FileServer.create_return_message(FileServer, '500','Error')

    def create(self, name='filename000', prop=True):
        oldname = name
        name='{}-{}' . format(FileServer.id, name)
        print("create ops {}" . format(name))
        try:
            if os.path.exists("{}/{}".format(FileServer.basedir, name)):
                return self.create_return_message(FileServer, '102', 'OK','File tersedia')
            if not FileServer.is_unlocked(FileServer, oldname) and prop:
                return FileServer.create_return_message(FileServer, '9999','File masih dipakai oleh pengguna lain')
            if prop:
                FileServer.filestate[oldname] = 'lock'
            f = open("{}/{}".format(FileServer.basedir, name),'wb',buffering=0)
            f.close()
            print(FileServer.filestate)
            if prop:
                return FileServer.propagate(FileServer, 'create', oldname)
            else:
                return FileServer.create_return_message('100','OK')
        except:
            return FileServer.create_return_message(FileServer, '500','Error')
    
    def read(self,name='filename000', prop=True):
        oldname = name
        name='{}-{}' . format(FileServer.id, name)
        print("read ops {}" . format(name))
        try:
            if not FileServer.is_unlocked(FileServer, oldname) and prop:
                return FileServer.create_return_message(FileServer, '9999','File masih dipakai oleh pengguna lain')
            # if prop:
            FileServer.filestate[oldname] = 'lock'
            f = open("{}/{}".format(FileServer.basedir, name),'r+b')
            contents = f.read().decode()
            f.close()
            FileServer.filestate[oldname] = 'unlock'
            print(FileServer.filestate)
            # if prop:
            #     tmp = FileServer.propagate(FileServer, 'read', oldname)
            return FileServer.create_return_message(FileServer, '101','OK',contents)
        except Exception as e:
            return FileServer.create_return_message(FileServer, '500','Error', str(e))
            
    def update(self,name='filename000',content='', prop=True):
        oldname = name
        name='{}-{}' . format(FileServer.id, name)
        print("update ops {}" . format(name))

        if (str(type(content))=="<class 'dict'>"):
            content = content['data']
        try:
            if not FileServer.is_unlocked(FileServer, oldname) and prop:
                return FileServer.create_return_message(FileServer, '9999','File masih dipakai oleh pengguna lain')
            if prop:
                FileServer.filestate[oldname] = 'lock'
            f = open("{}/{}".format(FileServer.basedir, name),'w+b')
            f.write( base64.b64decode( content ) )
            f.close()
            print(FileServer.filestate)
            if prop:
                return FileServer.propagate(FileServer, 'update', oldname)
            else:
                return FileServer.create_return_message('101','OK')
        except Exception as e:
            return FileServer.create_return_message(FileServer, '500','Error',str(e))

    def delete(self,name='filename000', prop=True):
        oldname = name
        name='{}-{}' . format(FileServer.id, name)
        print("delete ops {}" . format(name))

        try:
            if not FileServer.is_unlocked(FileServer, oldname) and prop:
                return FileServer.create_return_message(FileServer, '9999','File masih dipakai oleh pengguna lain')
            if prop:
                FileServer.filestate[oldname] = 'lock'
            os.remove("{}/{}".format(FileServer.basedir, name))
            del FileServer.filestate[oldname]
            print(FileServer.filestate)
            if prop:
                return FileServer.propagate(FileServer, 'delete', oldname)
            else:
                FileServer.create_return_message('101','OK')
        except:
            return FileServer.create_return_message(FileServer, '500','Error')