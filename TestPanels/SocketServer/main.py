from multiprocessing import Process
from maputil import row2dict
import dbutil, sys

def Server(name, seconds):
    sql = '''select a.project, a.projectname, a.msgtype, a.trancodexpath, a.serialnoxpath, b.listenport, b.servtype
                from t_projectdef a, t_serverdefine b where a.project = b.project'''
    rows = dbutil.select(sql)
    mp = row2dict(['project', 'projectname', 'msgtype', 'trancodexpath', 'serialnoxpath',
                   'listenport', 'servtype'], rows)
    for i in xrange(len(mp['project'])):
        print mp['project'][i]


if __name__ == "__main__":
    child_proc = Process(target=Server, args=('bob', 5))
    child_proc.start()
    print "in parent process after child process start"
    print "parent process abount to join child process"
    print "in parent process after child process join"