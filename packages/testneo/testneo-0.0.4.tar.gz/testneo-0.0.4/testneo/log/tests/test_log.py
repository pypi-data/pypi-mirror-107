from multiprocessing import Process,Lock
import os,time
class work(Process):
    def __init__(self,lock):
        super().__init__()
        self.lock=lock

    def run(self):
        self.lock.acquire()
        print("%s is running"%os.getpid())
        time.sleep(2)
        print("%s is done"%os.getpid())
        self.lock.release()

if __name__=='__main__':
    lock=Lock()
    for i in range(3):
        p=work(lock)
        p.start()



# def work(lock):
#     lock.acquire()
#     print('%s is running'%os.getpid())
#     time.sleep(2)
#     print('%s is done'%os.getpid())
#     lock.release()
# if __name__ == '__main__':
#     lock=Lock()
#     for i in range(3):
#         p=Process(target=work,args=(lock,))
#         p.start()