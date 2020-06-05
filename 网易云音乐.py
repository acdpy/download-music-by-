import requests
from bs4 import BeautifulSoup
import os
STATUS_OK,STATUS_ERROR,STATUS_EXITS=1,-1,0
class CloudMusic:
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0'
    }
    def Down(self, down_url, filePath, NowIndex, TotalCount, FileDir):
        if not os.path.isdir(FileDir):  os.makedirs(FileDir)
        if os.path.isfile(FileDir + "/" + filePath + ".mp3"):
            print(filePath+"，本地已存在")
            return STATUS_EXITS
        response = requests.get(down_url, headers=CloudMusic.header, allow_redirects=False)
        try:
            r = requests.get(response.headers['Location'], stream=True)
            size=int(r.headers['content-length'])
            print('\033[0;31m'+str(NowIndex) + "/" + str(TotalCount) + "  当前下载-" + filePath + "  文件大小:" + str(size) + "字节"+"\033[0m")
            CurTotal=0
            with open(FileDir + "/" + filePath + ".mp3", "wb") as f:
                for chunk in r.iter_content(chunk_size=512*1024):
                    if chunk:
                        f.write(chunk)
                        CurTotal += len(chunk)
                        print("\r" + filePath + "--下载进度:" + '%3s' % (str(CurTotal*100//size)) + "%", end='')
                print()
                r.close()
            return STATUS_OK
        except Exception as e:
            print(filePath + " 下载出错!" + " 错误信息" + str(e.args))
            if os.path.isfile(FileDir + "/" + filePath + ".mp3"):  os.remove(FileDir + "/" + filePath + ".mp3")
            return STATUS_ERROR

    def ParsingPlayList(self, url):
        response=requests.get(url=url, headers=CloudMusic.header)
        soup=BeautifulSoup(response.text, "html.parser")
        alist=soup.select("a")
        Songs=[]
        for music in alist:
            if music.has_attr("href"):
                if str(music.attrs["href"]).startswith("/song?id="):
                    id=str(music.attrs["href"]).replace("/song?id=", "")
                    try:
                        Songs.append({
                            "id": id,
                            "url": "http://music.163.com/song/media/outer/url?id=" + id + ".mp3",
                            "name": music.text
                        })
                    except:
                        pass
        return Songs

    def Start(self, MusicList, Dd):
        total=len(MusicList)
        CurIndex=OkCount=FalseCount=ExitCount=0
        print("歌单共计:" + str(len(MusicList)) + "首")
        for data in MusicList:
            CurIndex+=1
            status=self.Down(data["url"],data["name"].replace("/",""),CurIndex,total,Dd)
            if status==1:   OkCount+=1
            elif status==0: ExitCount+=1
            else:           FalseCount+=1
        print("下载成功"+str(OkCount)+"首"+"\n下载失败"+str(FalseCount)+"首"+"\n本地已存在"+str(ExitCount)+"首")

if __name__=="__main__":
    CrawlerClient= CloudMusic()
    # CrawlerClient.Start(CrawlerClient.ParsingPlayList("https://music.163.com/playlist?id=1992662269&userid=315893058"), "广场舞")
    # CrawlerClient.Start(CrawlerClient.ParsingPlayList("https://music.163.com/playlist?id=2584781662"),"治愈")
    CrawlerClient.Start(CrawlerClient.ParsingPlayList("https://music.163.com/playlist?id=2893603833&userid=315893058"),"mp3")

