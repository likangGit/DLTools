import parse_log as log_parser
import argparse
import random
import matplotlib.pyplot as plt
import matplotlib.cm as cmx
import matplotlib.colors as colors
import matplotlib.legend as lgd
import matplotlib.animation as animation
import os
import paramiko

dirname = os.path.dirname(__file__)
fig = plt.figure()
ax_loss = fig.add_subplot(111)
ax_eval = ax_loss.twinx()
line_loss, = ax_loss.plot([],[],lw=0.75,label='mbox loss')
line_eval, = ax_eval.plot([],[],'r', label='detectiron eval')
ax_loss.grid()

def init():
    ax_loss.set_title("mbox loss and detection eval VS iteration")
    ax_loss.set_ylabel("mbox loss")
    ax_loss.set_xlim(0,10)
    ax_loss.set_ylim(0,10)
    ax_eval.set_ylabel("detection eval")
    ax_eval.set_xlabel('iteration')
    ax_eval.set_ylim(0,1)


    line_loss, line_eval = update(0)

    lns = [line_loss, line_eval]
    labs = [l.get_label() for l in lns]
    ax_loss.legend(lns, labs, loc='upper left')
    return line_loss, line_eval

def update(num):
    logfile_path = args.logfile_path
    if '@' in args.logfile_path:
        localfile_path = os.path.join(dirname, str(os.getpid())+"_temp.log")
        getLogFilefromRemote(localfile_path)
        logfile_path = localfile_path
    train_dic_list, test_dic_list = log_parser.parse_log(logfile_path)
    if len(train_dic_list)<=0:
        return line_loss, line_eval
    #train_dic_list = train_dic_list[0:counter]
    if args.type == 0:
        x_axis_field = "NumIters"
        y_axis_field = "mbox_loss"
        y_eval_field = "detection_eval"
    train_data = [[i[x_axis_field] for i in train_dic_list],
                    [i[y_axis_field] for i in train_dic_list]]
    test_data = [[i[x_axis_field] for i in test_dic_list], [i[y_eval_field] for i in test_dic_list]]
    xmin, xmax = ax_loss.get_xlim()
    if train_data[0][-1] >= xmax:
        ax_loss.set_xlim(xmin,int(train_data[0][-1]*1.3))
        ax_loss.figure.canvas.draw()
    ymin, ymax = ax_loss.get_ylim()
    if train_data[1][0] >= ymax:
        ax_loss.set_ylim(ymin,train_data[1][0]+10)
        ax_loss.figure.canvas.draw()
    
    line_loss.set_data(train_data[0], train_data[1])
    line_eval.set_data(test_data[0], test_data[1])
    return line_loss, line_eval

def getLogFilefromRemote(localfile_path):
    username, _, substr= str(args.logfile_path).partition('@')
    remote, _, file_path =substr.partition(':')
    port = 22
    sf = paramiko.Transport((remote,port))
    sf.connect(username = username,password=args.password)
    sftp = paramiko.SFTPClient.from_transport(sf)
    try:
        sftp.get(file_path,localfile_path)
    except Exception as e:
        print('download exception:',e)
    sf.close()
parser = argparse.ArgumentParser(description="This is to plot train log in real time", formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("logfile_path", help="The log file path，\"path\" or \"username@ip:/path\"")
parser.add_argument("-i",'--interval', type=int, default=5, help="Refresh interval time(s)")
parser.add_argument("-t","--type", type=int,choices=[0,], default=0,help="""char type:
0:mbox loss and detection eval VS iteration
1:mbox loss and detection eval VS seconds(no implement)""")
parser.add_argument("-pw","--password", type=str, default='123', help="The password of remote")
args = parser.parse_args()
def main():
    print('开始监测')
    print("  开始配置", end='\t')
    ani = animation.FuncAnimation(fig, update, interval=args.interval*1000, init_func=init,
                                repeat=False)
    if ani is None:
        print("faild")
        exit(-1)
    print("ok\n  监测开始")
    plt.show()
    print("停止监测")
    print("  删除临时文件",end='\t')
    files = os.listdir(dirname)
    try:
        for file in files:
            if "_temp.log" in file:
                os.remove(os.path.join(dirname, file) )
    except Exception as e:
        print("faild\n", e)
        exit(-1)
   
    print("ok\n  监测停止")

if __name__ == "__main__":
    main()