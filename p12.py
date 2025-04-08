import xlrd, xlwt
import csv
import os
import re
import time
import datetime
import pandas as pd
import pymysql

import pymysql

def insert_data_into_db(data, host, user, password, db):
    # ½¨Á¢Êý¾Ý¿âÁ¬½Ó
    conn = pymysql.connect(
        host=host,
        user=user,
        password=password,
        db=db,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    try:
        with conn.cursor() as cursor:
            # ´´½¨±í
            # sql_create_table = """
            # CREATE TABLE your_table (
            #     Name varchar(190) CHARACTER SET utf8mb4,
            #     State varchar(190) CHARACTER SET utf8mb4,
            #     Laiyuan varchar(190) CHARACTER SET utf8mb4,
            #     jine FLOAT,
            #     shouzhi varchar(190) CHARACTER SET utf8mb4,
            #     shangpin varchar(190) CHARACTER SET utf8mb4,
            #     Buytime DATE,
            #     item varchar(190) CHARACTER SET utf8mb4,
            #     PRIMARY KEY (Name, Buytime, item)
            # ) ENGINE=INNODB;

            # """
            # cursor.execute(sql_create_table)

            # ²åÈëÊý¾Ý
            for single_data in data:
                sql_insert = """
                INSERT INTO your_table (
                    Name, State, Laiyuan, jine, shouzhi, shangpin, Buytime, item,buttimea
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE buttimea=buttimea;
                """
                cursor.execute(sql_insert, (
                    single_data.Name,
                    single_data.State,
                    single_data.Laiyuan,
                    single_data.jine,
                    single_data.shouzhi,
                    single_data.shangpin,
                    single_data.Buytime,
                    single_data.item,
                    single_data.buttimea
                ))

            # Ìá½»ÊÂÎñ
            conn.commit()

    finally:
        # ¹Ø±ÕÁ¬½Ó
        conn.close()


def xlsx_to_csv(filesNanme):
    data_xls = pd.read_excel(filesNanme, index_col=0)
    data_xls.to_csv(filesNanme)
def Thedate():
    #connection = connect_to_database('localhost', 'root', 'zhangkaifaA', 'mydeal')

    print(os.getcwd())
    patchfile = '/root/文档/zhangdan'
    if os.path.exists('Class') != True:
        os.mkdir('Class')
    path ="C:\\Users\\Administrator\\Desktop\\3\\"
    asda=[]
    for root, dirs, files in os.walk(patchfile+"/dan"):
        for a in files:
            if "csv" in a and re.findall("[0-9]",a):
                asda.append(a)
        #print(asda)
    asda.sort(key=lambda fn:os.path.getmtime(patchfile+"/dan/" + fn))#按时间排序

    sCsvFileName =patchfile+ "/dan/"+asda[len(asda)-1]
    print(sCsvFileName)
    NAME_LINE   = 0
    STATE_LINE = 0
    LAIYUAN_LINE = 0
    JIN_LINE = 0
    SHOUZHI_LINE=0
    LINE=0
    SHANGPIN_NAME_LINE=0
    BUYTIME = 0
    
    with open(sCsvFileName,newline='',encoding='GBK') as csvfile:
        rows=csv.reader(csvfile)
        for iRow,row in enumerate(rows):
            liemax=len(row)
            for lie in range(liemax):
                #print(row[lie])
                Name         = re.findall('交易对方',str(row[lie]))
                State        = re.findall('交易状态',str(row[lie]))
                Laiyuan      = re.findall('类型',str(row[lie]))
                jine         = re.findall('金额（元',str(row[lie]))
                shouzhi      = re.findall('收/支',str(row[lie]))
                shangpin     = re.findall('商品名称',str(row[lie]))
                buytime      = re.findall('交易创建时间',str(row[lie]))
                if Name  :
                    NAME_LINE   = int(lie)
                if State :
                    STATE_LINE = int(lie)
                if Laiyuan :
                    LAIYUAN_LINE = int(lie)
                if jine :
                    JIN_LINE = int(lie)
                if shouzhi:
                    SHOUZHI_LINE=int(lie)
                if shangpin:
                    SHANGPIN_NAME_LINE = int(lie)
                if buytime:
                    BUYTIME= int(lie)

            if NAME_LINE !=0 and  STATE_LINE != 0 and LAIYUAN_LINE !=0 and JIN_LINE !=0 and SHOUZHI_LINE!=0 and SHANGPIN_NAME_LINE != 0:
                #print(NAME_LINE,STATE_LINE,LAIYUAN_LINE,SHOUZHI_LINE,SHANGPIN_NAME_LINE)
                LINE=iRow
                break
    #########构建提交文件##########

    tody = time.strftime("%Y-%m-%d", time.localtime())
    tody=(tody.replace("-",""))
    TheTatille=[]
    try:

        datef = open(patchfile + "/TheDate.txt",'r')
        dateday=datef.readline(200)
        datef.close()
        print(dateday)
        fs= open("postfile.csv",'w',encoding="GBK")
        csv_writer = csv.writer(fs)
        numcnt =0
        haha22=""
        with open(sCsvFileName,newline='',encoding='GBK') as csvfile:
            rows=csv.reader(csvfile)

            for iRow,row in enumerate(rows):
                if iRow <= LINE:
                    print(type(row))
                    TheTatille.append(row)
                if len(row)>=12 and re.findall('[0-9]',row[BUYTIME]):

                    #print(row[BUYTIME].replace("-","").replace(" ","").replace(":","")[:12],int(dateday))

                    if iRow == LINE+1:
                        with open("TheDate.txt",'w') as fc:
                            fc.write(row[BUYTIME].replace("-","").replace(" ","").replace(":","")[:12])
                            haha22 = "上次更新账单时间 :  " + row[BUYTIME].replace("-","").replace(" ","").replace(":","")[:12]

                    if int(row[BUYTIME].replace("-","").replace(" ","").replace(":","")[:12]) <= int(dateday):

                        break
                    else:
                        numcnt = numcnt+1

                csv_writer.writerow(row)
        fs.close()

        with open("TheDate.txt",'a+') as fa:
            fa.write("\n"+str(numcnt))



    except Exception as e:
        print(e)
        print("生成提交文件失败")
    #############################
    #查找规则
    fenlei=['淘宝','家家悦超市','王者荣耀','滴滴','济南超市','外卖','出去吃','衣服','鞋子','联通','待分类的','待定','房租','基金']
    RuleList=[
                [r'待定oxffffffff'],   #花呗
                [r'家家悦'],    #超市
                [r'App Store','iCloud','刀锋','租号'],    #游戏
                [r'滴滴','火车'],
                [r'平安','北洋','转账','超市'],
                [r'美团点评','美团订单','饿了','亲情卡'],
                [r'烧烤','零食','饭','肠','肉蟹','火锅','周三刀','重庆炸酱面','光明晶品源','美食','牛杂','鸡柳','板面','小面','丰香源','快餐','包子','便利店','杨国','肯德基','君子蓝','捞面','丰e足食'],
                [r'衣服','圆领','衣','外套','袖','宽松','裤子','衬衫'],
                [r'鞋'],
                [r'话费'],
                [r'AASDGSAGS',],
                [r'花呗','拼多多','淘宝','支付宝担保','阿里'],
                [r'房租','长付','物业费','房东','GEAO'],
                [r'收益发放','蚂蚁','余额宝']
             ]             


    class item:

        def __init__(self):
            self.Name = []     # 名称
            self.State = []     # 尺寸
            self.Laiyuan = []     # 列表
            self.jine = []     # 列表
            self.shouzhi = []     # 列表
            self.shangpin = []     # 列表
            self.Buytime=[]
            self.item=[]
            self.Data=[]
            self.buttimea=[]
    TheDate=[]
    crut = time.strftime("%Y-%m", time.localtime())
    for i in range(len(fenlei)):
        TheDate.append([])
    with open(sCsvFileName,newline='',encoding='GBK') as csvfile:
        rows=csv.reader(csvfile)
        for iRow,row in enumerate(rows):
            if len(row)>=12:
                Useflag = 0

                if re.findall('成功',row[STATE_LINE]) and ((re.findall('支出',row[SHOUZHI_LINE]) or re.findall('还款成功',row[STATE_LINE]) or re.findall('基金',row[NAME_LINE]))):
                    if row[BUYTIME].replace("-","")[0:6]==crut.replace("-",""):

                        for fenleiindex,onelist in enumerate(RuleList):


                            for one in onelist:
                                if Useflag==0:

                                    Ruslt = re.findall(one,(row[NAME_LINE]+row[SHANGPIN_NAME_LINE]+row[LAIYUAN_LINE]))
                                    if Ruslt :
                                        Useflag = 1

                                        if(fenleiindex ==13):
                                            pass

                                            #print(row[NAME_LINE],row[JIN_LINE],row[STATE_LINE])
                                        if re.findall('退款成功',row[STATE_LINE]):
                                            pass

                                        else:
                                            date=item()
                                            date.Name=row[NAME_LINE]
                                            date.State=row[STATE_LINE]
                                            date.Laiyuan=row[LAIYUAN_LINE]
                                            date.jine=float(row[JIN_LINE])
                                            date.shouzhi=row[SHOUZHI_LINE]
                                            date.shangpin=row[SHANGPIN_NAME_LINE]
                                            date.Buytime=row[BUYTIME].replace("-","")[0:8]
                                            date.buttimea = row[BUYTIME].replace("-","")
                                            date.item=fenleiindex
                                            date.Data = row
                                            #print(fenleiindex)
                                            TheDate[fenleiindex].append(date)
                                        break
                        if not Useflag:

                            date=item()
                            date.Name=row[NAME_LINE]
                            date.State=row[STATE_LINE]
                            date.Laiyuan=row[LAIYUAN_LINE]
                            date.jine=float(row[JIN_LINE])
                            date.shouzhi=row[SHOUZHI_LINE]
                            date.shangpin=row[SHANGPIN_NAME_LINE]
                            date.Buytime=row[BUYTIME].replace("-","")[0:8]
                            date.buttimea = row[BUYTIME].replace("-","")
                            date.item=10
                            date.Data = row
                            #print(fenleiindex)
                            TheDate[10].append(date)
    shujuku=[]

    for i in range(len(fenlei)):
        shujuku.append([])
    with open(sCsvFileName,newline='',encoding='GBK') as csvfile:
        rows=csv.reader(csvfile)
        for iRow,row in enumerate(rows):
            if len(row)>=12:
                Useflag = 0

                if re.findall('关闭',row[STATE_LINE])  or re.findall('成功',row[STATE_LINE]) and ((re.findall('支出',row[SHOUZHI_LINE]) or re.findall('还款成功',row[STATE_LINE]) or re.findall('基金',row[NAME_LINE]))):
                    if 1:

                        for fenleiindex,onelist in enumerate(RuleList):


                            for one in onelist:
                                if Useflag==0:

                                    Ruslt = re.findall(one,(row[NAME_LINE]+row[SHANGPIN_NAME_LINE]+row[LAIYUAN_LINE]))
                                    if Ruslt :
                                        Useflag = 1

                                        if(fenleiindex ==13):
                                            pass

                                            #print(row[NAME_LINE],row[JIN_LINE],row[STATE_LINE])
                                        if re.findall('退款成功',row[STATE_LINE]):
                                            pass

                                        else:
                                            date=item()
                                            date.Name=row[NAME_LINE]
                                            date.State=row[STATE_LINE]
                                            date.Laiyuan=row[LAIYUAN_LINE]
                                            date.jine=float(row[JIN_LINE])
                                            date.shouzhi=row[SHOUZHI_LINE]
                                            date.shangpin=row[SHANGPIN_NAME_LINE]
                                            date.Buytime=row[BUYTIME].replace("-","")[0:8]
                                            date.buttimea = row[BUYTIME].replace("-","")
                                            date.item=fenleiindex
                                            date.Data = row
                                            #print(fenleiindex)
                                            shujuku[fenleiindex].append(date)
                                        break
                        if not Useflag:

                            date=item()
                            date.Name=row[NAME_LINE]
                            date.State=row[STATE_LINE]
                            date.Laiyuan=row[LAIYUAN_LINE]
                            date.jine=float(row[JIN_LINE])
                            date.shouzhi=row[SHOUZHI_LINE]
                            date.shangpin=row[SHANGPIN_NAME_LINE]
                            date.Buytime=row[BUYTIME].replace("-","")[0:8]
                            date.buttimea = row[BUYTIME].replace("-","")
                            date.item=10
                            date.Data = row
                            #print(fenleiindex)
                            shujuku[10].append(date)
    for dataitem in shujuku:

        insert_data_into_db(dataitem,"localhost","root","zhangkaifaA","mydeal")

    TheDate2 =[]
    for i in range(len(fenlei)):
        TheDate2.append([])
    with open('postfile.csv',newline='',encoding='GBK') as csvfile:
        rows=csv.reader(csvfile)
        for iRow,row in enumerate(rows):
            if len(row)>=12:
                Useflag = 0

                if re.findall('成功',row[STATE_LINE]) and ((re.findall('支出',row[SHOUZHI_LINE]) or re.findall('还款成功',row[STATE_LINE]) or re.findall('基金',row[NAME_LINE]))):

                    if row[BUYTIME].replace("-","")[0:6]==crut.replace("-",""):

                        for fenleiindex,onelist in enumerate(RuleList):


                            for one in onelist:
                                if Useflag==0:

                                    Ruslt = re.findall(one,(row[NAME_LINE]+row[SHANGPIN_NAME_LINE]+row[LAIYUAN_LINE]))
                                    if Ruslt :
                                        Useflag = 1
                                        #print(fenleiindex)
                                        if(fenleiindex ==13):

                                            pass
                                            #print(row[NAME_LINE],row[JIN_LINE],row[STATE_LINE])
                                        if re.findall('退款成功',row[STATE_LINE]):
                                            pass

                                        else:
                                            date=item()
                                            date.Data=row
                                            date.item=fenleiindex
                                            if fenleiindex == 14:
                                                print(row[NAME_LINE])
                                            #print(fenleiindex)
                                            TheDate2[fenleiindex].append(date)
                                        break
                        if not Useflag:
                            date=item()
                            date.Data=row
                            date.item=10
                            #print(fenleiindex)
                            TheDate2[10].append(date)

    TheGroup=[]
    for i in range(3):
            TheGroup.append([])

    excel_write = xlwt.Workbook(encoding = 'utf-8')
    borders = xlwt.Borders()  # Create borders
    borders = xlwt.Borders()  # Create borders
    borders.left = xlwt.Borders.THIN  # 添加边框-虚线边框
    borders.right = xlwt.Borders.THIN  # 添加边框-虚线边框
    borders.top = xlwt.Borders.THIN  # 添加边框-虚线边框
    borders.bottom = xlwt.Borders.THIN  # 添加边框-虚线边框

    style = xlwt.XFStyle()
    al = xlwt.Alignment()
    al.horz = 0x02      # 设置水平居中
    #al.vert = 0x01      # 设置垂直居中
    style.alignment = al
    style.borders = borders
    excel_write_sheet = excel_write.add_sheet("sheet",cell_overwrite_ok=True)
    excel_write_sheet1 = excel_write.add_sheet("sheet1",cell_overwrite_ok=True)
    groups=[0,1,0,1,1,1,1,0,0,0,2,0,2,0]
    for bc,i in enumerate(TheDate):

            if bc != 13:

                TheGroup[groups[bc]].append(i)

    for b,i in enumerate(TheGroup):

        cnt =0
        for a in i:


            for h in a:


                cnt=cnt+1
                excel_write_sheet1.write(cnt+2, b*3+2,h.Buytime,style)
                excel_write_sheet1.write(cnt+2, b*3+3,h.Name,style)
                excel_write_sheet1.write(cnt+2, b*3+4,h.jine,style)
    Thespent=[]
    Theiten=[]
    thedaysum=0
    crut = time.strftime("%Y%m%d", time.localtime())
    for index,i in  enumerate(TheDate):
        if index != 13:
            #print(index)
            for  a in (i):
                if a.Buytime==crut:
                   print(crut,a.Buytime,a.Name,a.jine)
                   thedaysum=thedaysum+a.jine
                if a.Name not in Theiten:
                    Theiten.append(a.Name)
                    #print(a.Name)
                    Thespent.append(a)
                else:
                    print(a.Name,a.jine)
                    Thespent[Theiten.index(a.Name)].jine=Thespent[Theiten.index(a.Name)].jine+a.jine

    buff = [[],[],[]]
    for aa,h in enumerate(Thespent):
                buff[groups[h.item]].append(h)

    data = [[],[],[]]
    for i in buff:
        for a in i:

                data[groups[a.item]].append(int(a.Buytime))

    data1=[[],[],[]]

    for m,i in enumerate(data):
        data1[m]=sorted(i)
    alldata=[[],[],[]]
    for index,a in enumerate(data1):
        for rr,haha in enumerate(a):
            alldata[index].append(buff[index][data[index].index(haha)])
            data[index][data[index].index(haha)]=0xFFFFFFFF
    momsun=0
    fensum=[0,0,0]
    daesum=[]

    for hhh,d in enumerate(alldata):
        for aaa,i in enumerate(d):
            

            momsun = momsun +i.jine
            fensum[hhh]=fensum[hhh]+i.jine
            if i.jine>=1000:
                daesum.append(i)
            excel_write_sheet.write(aaa+2+1, hhh*4+2,i.Buytime,style)
            excel_write_sheet.write(aaa+2+1, hhh*4+3,i.Name,style)
            excel_write_sheet.write(aaa+2+1, hhh*4+4,i.jine,style)

    print("本月总消费:",str('%.2f' % momsun),"元，其中网购花费",str('%.2f' % fensum[0]),"元 ，吃喝花费",str('%.2f' % fensum[1]),"元，其他店家等花费",str('%.2f' % fensum[2]),"元")
    print("其中大额消费有",len(daesum),'笔','分别为')
    for i in daesum:
        momsun=momsun-i.jine
        print(i.Name,i.jine)
    print("去掉大额消费后的总消费为",str('%.2f' % momsun)
)

    lin1 = "本月总消费:                 "+str('%.2f' % momsun)+"        元，\n其中网购花费           "+str('%.2f' % fensum[0])+"         元 ， \n吃喝花费   "+str('%.2f' % fensum[1])+"           元，\n其他店家等花费       "+str('%.2f' % fensum[2])+"                   元\n"
    lin2 = "其中大额消费有"+str('%.2f' % len(daesum))+'笔'+'分别为\n'
    lin3 = ""
    for i in daesum:
         lin3 = lin3+i.Name+str(i.jine)+'\n'
    lin4 = "去掉大额消费后的总消费为                               "+str('%.2f' % momsun)

    eng=['a','B','C','D','E','F','G','H','I','J','K','L','M','N']
    leng=[]
    for i in range(len(alldata)):
        leng.append(len(alldata[i]))

    for i in range(len(alldata)):

        excel_write_sheet.write(max(leng)+2+2+1,i*4+4, xlwt.Formula('SUM('+eng[i*4+4]+'2'+':'+eng[i*4+4]+str(2+1+len(alldata[i]))+')'))    # 正常运行
    pattern = xlwt.Pattern()
    pattern.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = 44
    style = xlwt.XFStyle()
    style.pattern = pattern
    al = xlwt.Alignment()
    al.horz = 0x02      # 设置水平居中
    #al.vert = 0x01      # 设置垂直居中
    style.alignment = al
    style.borders = borders
    excel_write_sheet.write_merge(0,0,2,12,'总消费',style)
    aaa='sum('+eng[4]+str(max(leng)+2+2+1+1)+':'+eng[12]+str(max(leng)+2+2+1+1)+')'
    print()
    excel_write_sheet.write_merge(1,1,2,12,xlwt.Formula(aaa),style)


    pattern1 = xlwt.Pattern()
    pattern1.pattern = xlwt.Pattern.SOLID_PATTERN
    pattern1.pattern_fore_colour = 21
    style1 = xlwt.XFStyle()
    style1.pattern = pattern1
    al2 = xlwt.Alignment()
    
    al2.horz = 0x02      # 设置水平居中
    #al.vert = 0x01      # 设置垂直居中
    style1.alignment = al2
    style1.borders = borders
    excel_write_sheet.write_merge(2,2,2,4,'会员、网购',style1)
    excel_write_sheet.write_merge(2,2,6,8,'吃',style1)
    excel_write_sheet.write_merge(2,2,10,12,'其他商家',style1)
    namelist=[[],[],[]]
    for jj,i in enumerate(alldata):
        for a in i:

            namelist[jj].append(len(a.Name.replace(' ','')))

    for i in range(len(alldata)):

        if len(namelist[i]) > 0:
            excel_write_sheet.col(i*4+3).width = (max(namelist[i])) * 256 * 2           #设置单元格列宽

    excel_write.save(patchfile+"/dan/"+'TheDateInfo.xls')
    with open("/var/www/html/haha.txt","w") as f:
       print(thedaysum)
       f.write(str(round(float(thedaysum),3)))
   # print(TheDate2)
    for i in range(len(TheDate2)):
        if len(TheDate2[i]):
            f= open(patchfile+'//Class//'+fenlei[i]+'.csv','w',encoding="GBK")
            csv_writer = csv.writer(f)
            for ab in TheTatille:
                #print(ab)
                csv_writer.writerow(ab)
            for n in TheDate2[i]:
                #print(n.Data)
                csv_writer.writerow(n.Data)
        else:
            try:
                if os.path.exists(patchfile+'//Class//'+fenlei[i]+'.csv') == True:

                    os.remove(patchfile+'//Class//'+fenlei[i]+'.csv')
            except:
                print('删除失败')
    return lin1 +lin2 +lin3 +lin4

if __name__ == '__main__':
    Thedate()
