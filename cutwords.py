import torch
import torch.nn as nn
import os

class SLA(nn.Module):
    def __init__(self,dic_path=None,multi_dic_dir_path=None, mydict=[]):
        super().__init__()
        assert dic_path==None or multi_dic_dir_path==None
        self.mydict=mydict      #创建新字典
        if dic_path:
            h=open(dic_path,'r+',encoding='UTF-8')
            text=h.readlines()
            for i in range(0, len(text)):
                self.mydict.append(str(text[i][0:len(text[i])-2]))
        if multi_dic_dir_path:
            if os.path.exists(os.path.join(multi_dic_dir_path,'dic.txt')):
                h=open(os.path.join(multi_dic_dir_path,'dic.txt'),'r+',encoding='UTF-8')
                text=h.readlines()
                for i in range(0, len(text)):
                    self.mydict.append(str(text[i][0:len(text[i])-2]))
            else:
                path,file_names = self.read_files(multi_dic_dir_path)
                self.mixed_file(path,file_names)
                h=open(os.path.join(multi_dic_dir_path,'dic.txt'),'r+',encoding='UTF-8')
                text=h.readlines()
                for i in range(0, len(text)):
                    self.mydict.append(str(text[i][0:len(text[i])-2]))
        h.close()
        print(self.mydict)
    
    def forward(self, sentence):
        tokens = self.CutWords(sentence)
        return tokens
    
    def CutWords(self, sentence):
        result = []
        start = 0
        m=7
        while len(sentence)- start>=1:
            n =len(sentence)- start
            if n<m:
                m=n
            cutword = sentence[start:start+m]
            def CheckWords():
                nonlocal start
                nonlocal m
                if cutword in self.mydict:
                    result.append(cutword)
                    start = start + m
                    m=7
            CheckWords()
            if cutword not in self.mydict:
                if m==1:
                    result.append(cutword)
                    start = start + m
                    m = 7
                else:
                    m = m - 1
                    CheckWords()
        print(result)
        return result
    
    
    def read_files(self,multi_dic_dir_path):
        """该函数用于读取对应文件夹下各txt文件的名字"""
        # path = input("目标文件夹：") + '/'
        path = multi_dic_dir_path + '/'
        files = os.listdir(path)
        file_names=[]
        for file in files:
            if file.split('.')[-1] =='txt':#如果不是txt文件就跳过
                file_names.append(file)
        return  path,file_names

    def mixed_file(self,path,files):
        """该函数用于合并刚才读取的各文件
        输入：文件路径，read_files()返回的文件名
        输出：一个合并后的文件"""
        content = ''
        for file_name in files:
            with open( path+file_name , 'r' ,encoding='utf-8') as file:
                content = content + file.read()
                file.close()

        with open(path + 'dic.txt', 'a',encoding='utf-8') as file:
            file.write(content)
            content = ''
            file.close()
        


if __name__ == '__main__':
    CutWords = SLA(multi_dic_dir_path=r'C:\Users\渺渺夕\Desktop\SLA\multi_dic_dir')
    CutWords('我爸爸去吃饭')
