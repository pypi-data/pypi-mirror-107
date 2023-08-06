def AveDevCalTab(x_list,y_list):
    DEV=[]
    DEV.append(y_list)
    N=len(x_list)
    for jie in range(1,N):
        n=len(DEV[jie-1])
        dev=[]
        for i in range(n):
            if(i<jie):
                dev.append(0)
            else:
                ave_dev = (DEV[jie - 1][i] - DEV[jie - 1][i - 1]) / (x_list[i] - x_list[i - jie])
                dev.append(ave_dev)
        DEV.append(dev)
    print("均差计算表如下:")
    print("|{:^12}|{:^12}".format("X","Y"),end="|")
    for i in range(1,N):
        print("{:^12}|".format("N"+str(i)),end="")
    print("")
    for i in range(N):
        print("|",end="")
        print("{:^12.5f}".format(x_list[i]),end="|")
        for j in range(N):
            print("{:^12.5f}".format(DEV[j][i]),end="|")
        print("")

def NewtonChaZHi(x_list,y_list,x):
    DEV=[]
    DEV.append(y_list)
    N=len(x_list)
    for jie in range(1,N):
        n=len(DEV[jie-1])
        dev=[]
        for i in range(n):
            if(i<jie):
                dev.append(0)
            else:
                ave_dev = (DEV[jie - 1][i] - DEV[jie - 1][i - 1]) / (x_list[i] - x_list[i - jie])
                dev.append(ave_dev)
        DEV.append(dev)
    y=0
    for i in range(N):
        a=DEV[i][i]
        p=1
        for j in range(i):
            p*=(x-x_list[j])
        y+=a*p
    return y



