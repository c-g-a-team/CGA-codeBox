import datetime
import os
import tkinter.messagebox
import cv2

from aip import AipOcr, AipImageClassify
from flask import Flask, render_template, request
from MyDB import MyDBHelper

db = MyDBHelper()


app = Flask(__name__)

#管理员登录方法
@app.route('/login')
def login():
    return render_template('login.html', error="false")

#管理员注册方法
@app.route('/register')
def register():
    return render_template('register.html')

#路段查询页面
@app.route('/index')
def index():
    return render_template('index.html')


# 首页
@app.route('/')
def shouye():
    return render_template('shouye.html')


# 车主登录页面
@app.route('/login01')
def login01():
    return render_template('login01.html')


# 交警功能选择页面
@app.route('/policefunction')
def policefunction():
    return render_template('policefunction.html')


# 车主功能选择页面
@app.route('/caruserfunction')
def caruserfunction():
    return render_template('caruserfunction.html')


# 注册界面
@app.route("/doregister")
def doregister():
    Name = request.args.get("Name")
    Password = request.args.get("Password")
    print(Name, Password)
    args = [Name, Password]
    db.add(args)
    return render_template("login.html", error1="false")

# 管理员通过用户名和密码登录 不匹配将显示登录失败
@app.route("/dologin")
def dologin():
    Name = request.args.get('Name')
    Password = request.args.get('Password')
    args = [Name, Password]
    result = db.login(args)
    if result == '登录成功':
        return render_template("policefunction.html")
    else:
        # tkinter.messagebox.showwarning("系统提示", "该用户未注册！请先注册后登陆")
        return render_template("login.html", error="true")

# 车主通过用户名和密码登录 不匹配将显示登录失败
@app.route("/dologin1")
def dologin1():
    carNum = request.args.get('carNum')
    engineNum = request.args.get('engineNum')
    args = [carNum, engineNum]
    result = db.login01(args)
    if result == '登录成功':
        return render_template("caruserfunction.html")
    else:
        return render_template("login01.html")

# 进入路段查询功能  按路段查询违章数据
@app.route('/infoshow')
def infoshow():
    result = db.showAllUser('学院路')
    if result != ():
        return render_template('infoshow.html', u=result)
    else:
        return render_template('infoshowNone.html')

# 实时监控功能
@app.route('/monitor')
def monitor():
    return render_template("monitor.html")

# 调用车辆检测功能 将视频流截取成图片 识别公交车与非公交车 并将识别的私家车违章信息记录到数据库
@app.route('/carcheck')  # 按钮调用"车辆检测.py"
def carcheck():
    # 要提取的视频路径
    video_path = os.path.join('./static/video.MOV')

    times = 0

    # 提取视频的频率，每15帧提取一个
    frameFrequency = 15

    # 输出图片存放路径
    outPutDirName = 'static/pic/'

    if not os.path.exists(outPutDirName):
        # 如果文件目录不存在则创建目录
        os.makedirs(outPutDirName)

    camera = cv2.VideoCapture(video_path)

    while True:
        times += 1
        res, image = camera.read()

        if not res:
            print('not res , not image')
            break

        if times % frameFrequency == 0:
            cv2.imwrite(outPutDirName + str(times) + '.jpg', image)
            print(outPutDirName + str(times) + '.jpg')

    print("图片提取结束，下面开始识别")

    camera.release()

    # -------------------------- 你的 车牌识别 APPID AK SK --------------------------
    APP_ID1 = 'xxxxxxxxxx'
    API_KEY1 = 'xxxxxxxxxxxxxxxxxxxxxxx'
    SECRET_KEY1 = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxx'

    client1 = AipOcr(APP_ID1, API_KEY1, SECRET_KEY1)
    # -------------------------------------------------------------------------------

    # -------------------------- 你的 车型识别 APPID AK SK --------------------------
    APP_ID2 = 'xxxxxxxxxx'
    API_KEY2 = 'xxxxxxxxxxxxxxxxxxxxxx'
    SECRET_KEY2 = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxx'

    client2 = AipImageClassify(APP_ID2, API_KEY2, SECRET_KEY2)

    # -------------------------------------------------------------------------------

    # 读取图片
    def get_file_content(filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()

    for pic_num in range(15, 1485, 15):

        image = get_file_content('./static/pic/' + str(pic_num) + '.jpg')

        # 将图片路径以字符串的形式存入变量path
        path = '../static/pic/' + str(pic_num) + '.jpg'

        result1 = client1.licensePlate(image)  # 调用车牌识别结果
        result2 = client2.carDetect(image)  # 调用车型识别结果

        # 将公交车和无法识别的图片排除
        if 'error_code' in result1.keys() or "非车类" == result2['result'][0]['name'] or "日产贵士" == result2['result'][0][
            'name'] or "路虎DC100" == result2['result'][0]['name']:
            print("无法识别")
        else:
            car_license = (result1['words_result']['number'])  # 车牌识别结果
            car_shape = (result2['result'][0]['name'])  # 车型识别结果
            now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 识别时间

            args = [car_license, car_shape, now_time, path]
            print(args)

            row = db.add1(args)
            print("影响的行数", row)

    return render_template('checkVideoDone.html')

# 对各个路段的违章记录进行统计 并按降序排序
@app.route('/arr')
def arrange():
    row1 = db.checkplace("海淀区--成府路")
    row2 = db.checkplace("海淀区--学院路")
    row3 = db.checkplace("海淀区--中关村")
    row4 = db.checkplace("海淀区--清华东路")
    row5 = db.checkplace("海淀区--颐和园路")
    row6 = db.checkplace("海淀区--学清路")
    db.placeaddsta("海淀区--成府路", row1)
    db.placeaddsta("海淀区--学院路", row2)
    db.placeaddsta("海淀区--中关村", row3)
    db.placeaddsta("海淀区--清华东路", row4)
    db.placeaddsta("海淀区--颐和园路", row5)
    db.placeaddsta("海淀区--学清路", row6)
    result = db.arrange()
    return render_template("roadStatistics.html", u6=result)

# 车主按照车牌查询
@app.route('/userinfoshow')
def userinfoshow():
    user_result = db.searchUser("京FL0278")
    return render_template('userinfoshow.html', u2=user_result)

# 车主的待审核记录页面
@app.route('/pending')
def pending():
    pending_result = db.searchPending()
    if pending_result == None:
        return render_template('pendingNone.html')
    else:
        return render_template('pending.html', u4=pending_result)

# 车主的已审核记录页面
@app.route('/solved')
def solved():
    solved_result = db.searchSolved()
    if solved_result == None:
        return render_template('solvedNone.html')
    else:
        return render_template('solved.html', u5=solved_result)

# 车主提交申请重新审核
@app.route('/apply')
def apply():
    db.updatecarnumber("京FL0278")
    return render_template('applyResponse.html')

# 交警管理员对提交的记录进行重新审核
@app.route('/policeexamine')
def policeexamine():
    examine_result = db.searchMoreUser()
    if examine_result == ():
        return render_template('examineNone.html')
    else:
        return render_template('policeexamine.html', u3=examine_result)

# 交警判定没有违章
@app.route('/approve')
def approve():
    db.updatecheckIf()
    return render_template('checkOK.html')

# 交警判定车主已违章
@app.route('/disapprove')
def disapprove():
    db.updatecheckIf()
    return render_template('checkOK.html')

# 车主缴费
@app.route('/pay')
def pay():
    return render_template('pay.html')


if __name__ == '__main__':
    app.run()
