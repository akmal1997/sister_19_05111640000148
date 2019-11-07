Cara Menjalankan:

1. Jalankan nameserver Pyro (pyro4-ns -n localhost -p 50001)
2. Buat direktori untuk fileserver dengan nama yang sesuai di nameserver. Dalam kasus ini, nama "SEMBRANI" dan "GUMARANG" akan dipakai. (mkdir sembrani gumarang)
3. Jalankan server dengan file server.py dengan input program yang sudah sesuai oleh nameserver. (python2 server.py sembrani)
4. Jalankan script bash assign_fs_id.sh untuk mengatur id setiap fileserver yang sudah dibuat. (bash assign_fs_id.sh)
5. Jalankan client.py untuk memulai fileserver dengan nama yang dapat diakses oleh client. (python3 client.py sembrani)