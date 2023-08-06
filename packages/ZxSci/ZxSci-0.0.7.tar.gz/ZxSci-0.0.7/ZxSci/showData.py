import matplotlib.pyplot as plt
def printData(x_list,y_list):
    print("+-------------------------------+")
    x_label=input("|  请输入x轴英文名称:\t")
    y_label=input("|  请输入y轴英文名称:\t")
    title=  input("|  标题的英文是:     \t")
    print("+-------------------------------+")
    plt.plot(x_list,y_list)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.grid()
    plt.show()
