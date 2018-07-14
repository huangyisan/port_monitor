from monitor import PortMonitor, FuncQueue
from monitor_alert import sendTemplateSMS
from send_mail import sendmail
from config import sms_info
import threading
import queue

if __name__ == '__main__':
    q = queue.Queue()
    b = FuncQueue(flag=1,q=q)
    t_list = []
    fhandler = open('./mechine.conf', 'r')
    for line in fhandler:
        t = threading.Thread(target=b.listqueue, args=(line,))
        t.start()
        t_list.append(t)
    fhandler.close()
    for j in t_list:
        j.join()

    qlist = [q.get() for i in range(q.qsize())]

    # alert sms email
    stat_str = (' '.join(qlist))
    if len(qlist) > 0:

        # 邮件告警
        sendmail(' '.join(qlist))

        # 短信告警
        # stat_str = stat_str.replace('\n', '')
        # sendTemplateSMS(sms_info[0], (stat_str, 'server down'), '185595')
