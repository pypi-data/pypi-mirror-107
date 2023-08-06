import matplotlib.pyplot as plt

def printData():
    print("+-------------------------------+")
    x_label=input("|  请输入x轴英文名称:\t")
    y_label=input("|  请输入y轴英文名称:\t")
    title=  input("|  标题的英文是:     \t")
    print("+-------------------------------+")
    x_list = eval(input("|  请输入x坐标的数据列表[]:"))
    y_list = eval(input("|  请输入y坐标的数据列表[]:"))
    plt.plot(x_list,y_list)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.grid()
    plt.show()

def printNpic():
    print("+-------------------------------+")
    pic_row=int(input("|  请输入行数:\t"))
    pic_col=int(input("|  请输入列数:\t"))
    print("+-------------------------------+")
    print("")
    print("+-------------------------------+")
    for index in range(pic_col*pic_row):
        print("+  第"+str(index+1)+"张图:")
        plt.subplot(pic_row,pic_col,index+1)
        x_list=eval(input("|  请输入x坐标的数据列表[]:"))
        y_list=eval(input("|  请输入y坐标的数据列表[]:"))
        x_label = input("|  请输入x轴英文名称:\t")
        y_label = input("|  请输入y轴英文名称:\t")
        title = input("|  标题的英文是:     \t")
        plt.plot(x_list, y_list)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(title)
        plt.grid()
    plt.show()
    print("+-------------------------------+")

printNpic()

