import subprocess

class PortMonitor(object):
    def __init__(self, flag):
        '''
        
        :param flag:  0 --> port open; 1 --> port block
        '''
        self.flag = flag

    def test_stat(self, line):
        '''
        
        :param line:  read line
        :return: list
        '''
        ret = subprocess.call('nc -w1 -z {0}'.format(line), shell=True)
        if ret.numerator == self.flag:
            return line

    def echo_stat(self,line):
        '''
        
        :param line:  read line
        :return: None
        '''
        if self.flag == 0:
            print(self.test_stat(line))
        else:
            print(self.test_stat(line))

class FuncQueue(PortMonitor):
    def __init__(self, flag, q):
        '''

        :param flag: 0 --> port open; 1 --> port block
        :param q: queue.Queue()
        '''
        super(FuncQueue, self).__init__(flag)
        self.q = q
        self.flag = flag

    def listqueue(self, line):
        '''

        :param line: ip port
        :return:
        '''
        if self.test_stat(line):
            self.q.put(self.test_stat(line))

    def sizequeue(self):
        return self.q.qsize()




