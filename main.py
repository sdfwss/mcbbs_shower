import requests,json,sys
from PyQt6.QtWidgets import (
    QApplication, QDialog
)
from ui import Ui_Dialog
class ShowUI(Ui_Dialog,QDialog):
    def __init__(self):
        super(ShowUI, self).__init__()
        self.setupUi(self)
        self.SearchButton.clicked.connect(self.search_clicked)
        self.show()
    def search_clicked(self,arg):
        uidStr=self.lineEdit.text()
        if uidStr.isdigit():
            uid=int(self.lineEdit.text())
        else:
            self.lineEdit.clear()
            return
        self.lineEdit.clear()
        try:
            get=requests.get("https://mcbbs.wiki/rest.php/mbwutils/v0/credit/"+str(uid),timeout=10)
        except requests.exceptions.ConnectTimeout as e:
            self.ShowLabel.setText("<h1 style=\"color:red\">连接超时</h1>\n"+e.strerror)
            return
        code=get.status_code
        if code!=200:
            self.ShowLabel.setText("<h1 style=\"color:red\">状态异常</h1>\n"+str(code)+"\n<small>(404错误可能是用户不存在)</small>")
            return
        text=get.text
        jsonDict=json.loads(text)
        credits=jsonDict["credits"]
        activities=jsonDict["activities"]
        self.ShowLabel.setText(
            "UID:%d\n"%jsonDict["uid"]
            +"名称:%s\n"%jsonDict["nickname"]
            +"积分:%d\n"%credits["credit"]
            +"人气:%d\n"%credits["popularity"]
            +"金粒:%d\n"%credits["nugget"]
            +"金锭:%d\n"%credits["ingot"]
            +"宝石:%d\n"%credits["gem"]
            +"下界之星:%d\n"%credits["star"]
            +"贡献:%d\n"%credits["contribute"]
            +"爱心:%d\n"%credits["heart"]
            +"发帖:%d\n"%activities["post"]
            +"主题:%d\n"%activities["thread"]
            +"精华:%d\n"%activities["digiest"]
        )
if __name__ == '__main__':
    app = QApplication(sys.argv)
    myHellWorld = ShowUI()
    sys.exit(app.exec())