'wav音乐播放器（目前仅支持wav文件的播放，╮(╯▽╰)╭）'
__author__ = "BluesYoung-web"

import os
import wave
import pyaudio 

def getDir():
    '''
    获取歌曲存放目录，如果未输入则使用默认值
    '''
    src=input("请输入歌曲目录（直接回车使用默认目录D:/music）") 
    src= src or 'D:/music'  
    showList(src)

def file_name(file_dir):
    '''
    遍历目录，返回文件名list
    '''
    sub_files=[]
    for root,dirs,files in os.walk(file_dir):
        sub_files=files
        return sub_files

def showList(root):
    '''
    根据传入的地址，显示目录内的歌曲清单
    root为目录地址
    '''
    lst=file_name(root)
    direct={}   #用于存放歌曲目录
    index=0     #歌曲索引号
    #筛选音频文件
    for item in lst:
        ext=os.path.splitext(item)[1]
        if ext == '.wav':
            direct[index]=item
            index += 1
    # 打印歌曲列表
    for k,v in direct.items():
        print(k,":",v)
    target=int(input("请输入歌名(对应序号，-1退出)："))
    if target == -1:
        return
    target= direct[target]

    fullUrl=getFullUrl(root,target)
    print('正在播放：',target)
    #调用播放函数
    play(fullUrl)

def getFullUrl(root,music_name):
    '''
    根据目录名和歌曲名拼接出歌曲的绝对地址
    '''
    return os.path.join(root,music_name)

def play(music_src):
    '''
    播放音乐的函数
    music_src为音乐的绝对地址，带扩展名
    '''
    f = wave.open(music_src,'rb')
    params = f.getparams()
    nchannels, sampwidth, framerate = params[:3]
    #instantiate PyAudio 
    p = pyaudio.PyAudio() 
    #define stream chunk  
    chunk = 1024 
    #打开声音输出流
    stream = p.open(format = p.get_format_from_width(sampwidth),
                    channels = nchannels,
                    rate = framerate, 
                    output = True) 
    
    #写声音输出流到声卡进行播放
    data = f.readframes(chunk) 
    while True:
        data = f.readframes(chunk)
        if data == b'': break
        stream.write(data)   
    f.close()
    #stop stream 
    stream.stop_stream() 
    stream.close() 
    #close PyAudio 
    p.terminate() 
    again=input("one more y/n?")
    if again == 'y':
        dirs=os.path.split(music_src)[0]
        showList(dirs)
    else:
        input("播放完毕，谢谢使用(*^▽^*)")

if __name__ == "__main__":
    getDir()
