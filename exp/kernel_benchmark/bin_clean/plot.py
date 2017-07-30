import os
import sys
import json

from matplotlib import pyplot as plt


def plot_data(filepath, plotpath, keyword=None):

    kernel = filepath.split('/')[-2]

    plot_id = ""
    x = list()
    labels = list()
    avg = list()
    confidence = list()
    config = dict()

    keywords = filepath.split('/')
    session = keywords[-1].split('.csv')[0].split('_')[-1]
    print keywords, session

    with open(filepath, 'r') as f:
        i = 0
        for row in f:
            row_list = row.split(',')
            #print row

            if i == 0:
                plot_id = row_list[0]
                x = row_list[1:]
                #print x
            else:
                if (i-1) % 3 == 0:
                    labels.append(row_list[0].split('__')[-1])
                    avg.append(map(float, row_list[1:]))
                elif (i-1) % 3 == 2:
                    confidence.append(map(float, row_list[1:]))
            
            i += 1

    with open("plot_config.json", 'r') as cf:
        config = json.load(cf) 


    plt.close('all')

    print plot_id

    fig, ax = plt.subplots()
    ax.set_title(config[kernel][plot_id]['title'], fontsize=24)

    if config[kernel][plot_id]["plot_type"] == "log-log":
        ax.set_xscale('log')
        ax.set_yscale('log')

    elif config[kernel][plot_id]["plot_type"] == "log-line":
        ax.set_xscale('log')

    ax.set_xlim(config[kernel][plot_id]['xlim'])
    ax.set_ylim(config[kernel][plot_id]['ylim'])
    ax.set_xlabel(config[kernel][plot_id]['xlabel'], fontsize=20)
    ax.set_ylabel(config[kernel][plot_id]['ylabel'], fontsize=20)
    ax.tick_params(labelsize=20)
    ax.grid(True)

    for i in range(len(avg)):
        (_, caps, _) = ax.errorbar(x, avg[i], yerr=confidence[i], label=labels[i])
        for cap in caps:
            cap.set_linewidth(5)

    ax.legend(loc='upper left')

    #plt.show()

    fig.set_size_inches(14, 12)
    if keyword == None:
        plt.savefig(plot_path+kernel+'_'+plot_id+'.pdf', dpi=144)
        plt.savefig(plot_path+kernel+'_'+plot_id+'.png', dpi=144)
    else:
        plt.savefig(plot_path+keyword+'_'+kernel+'_'+plot_id+'.pdf', dpi=144)
        plt.savefig(plot_path+keyword+'_'+kernel+'_'+plot_id+'.png', dpi=144)
        


if __name__ == "__main__":

    dir_path = sys.argv[1]
    plot_path = sys.argv[2]
    if dir_path[-1] != '/':
        dir_path = dir_path + '/'
    if plot_path[-1] != '/':
        plot_path = plot_path + '/'

    filenames = os.listdir(dir_path)

    for filename in filenames:
        if dir_path.split('/')[1] != 'set1':
            keyword = filename[:7]
        else:
            keyword = None
        try:
            plot_data(dir_path+filename, plot_path, keyword)
        except:
            print "plot config not setup yet\n"
            pass
