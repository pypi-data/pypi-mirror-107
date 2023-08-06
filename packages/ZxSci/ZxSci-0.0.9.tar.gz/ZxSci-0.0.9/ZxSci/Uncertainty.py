def CalUncer(data_list):
    data_num = len(data_list)
    data_sum=sum(data_list)
    data_Average=data_sum/data_num
    L2_sum=0
    for data in data_list:
        L2_sum+=(data-data_Average)**2
    Ua=(L2_sum/(data_num*data_num-1))**0.5
    E=Ua/data_Average
    print("+--------------------------------------+")
    print("|  平均值是:     \t"+str(data_Average))
    print("|  A类不确定度是: \t"+str(Ua))
    print("|  相对不确定度是: \t"+str(E*100)+"%")
    print("+--------------------------------------+")
