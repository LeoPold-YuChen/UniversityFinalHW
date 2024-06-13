i=2



# detect image
def ob_ima(file):
    # if ifHasRuns():
    #     i=2 #predict從2開始。季的測試完要刪除其他的predict
    global i
    file.save("..\runs\detect\sir.jpg")    #把接收到的圖片名稱取名叫sir(yes sir!!)
    model = YOLO("..\runs\detect\130_4.pt") #setting model
    # model = YOLO(pt_path) #setting model
    model.predict("..\runs\detect\sir.jpg", save=True, imgsz=(640,640), conf=0.5) #predict
    predict_path=f"..\runs\detect\predict{i}\sir.jpg"
    i=i+1#可能要用到session了
    return predict_path
    #return file.save("output.jpg")



# def convert_avi_to_mp4(avi_file_path, output_name):
#     abc=os.popen("ffmpeg -i '{input}' -ac 2 -b:v 2000k -c:a aac -c:v libx264 -b:a 160k -vprofile high -bf 0 -strict experimental -f mp4 '{output}.mp4'".format(input = avi_file_path, output = output_name))
#     return abc


#detect mp4
def ob_mp4(file):
    global i
    file.save("..\runs\detect\sir.mp4")    
    model = YOLO("..\runs\detect\100_6.pt")
    model.track(source="..\runs\detect\sir.mp4", conf=0.3,save=True)
#    model.track(source="sir.mp4", conf=0.3,save=True,show=True) #及時顯示
    predict_path_mp4=f"..\runs\detect\predict{i}/sir.avi"
    i=i+1#可能要用到session了

    clip=moviepy.VideoFileClip(predict_path_mp4)
    clip.write_videofile("..\runs\detect\myvideo.mp4")

    return "..\myvideo.mp4"#convMp4#predict_path_mp4


    #convMp4=convert_avi_to_mp4(predict_path_mp4,"output")
    # # 讀取 avi 檔案
    # input_file = predict_path_mp4
    # # 建立輸出檔案
    # output_file = "output.mp4"
    # # 轉換檔案
    # ffmpeg.input(input_file).output(output_file).run()

    




    # model.predict("sir.mp4", save=True, imgsz=(640,640), conf=0.5) #predict
    # predict_path=f"runs\detect/predict{i}/sir.mp4"
    # i=i+1#可能要用到session了
    # return predict_path
    #return file.save("output.jpg")




###########正式開始!!!###########
import pymongo
client=pymongo.MongoClient("mongodb+srv://david4366938789:j6u.j6xm4@cluster0.rude3cw.mongodb.net/?retryWrites=true&w=majority")
db=client.member_system
import moviepy.editor as moviepy
#import ffmpeg
import cv2,os
from ultralytics import YOLO
from flask import Flask,render_template, request, send_file
from flask import *
app=Flask(__name__,static_url_path="/",static_folder=".\runs\detect")
app.secret_key="any"

@app.route("/")
def home():
    return render_template("Home.html")


@app.route("/introduce_dataset.html")
def intro():
    return render_template("/introduce_dataset.html")


@app.route("/ob_image.html")
def myImage():
    return render_template("ob_image.html")


@app.route("/ob_image2.html", methods=["GET", "POST"])
def myImage2():
    global i
    if request.method == 'POST':
        f = request.files['file']
        result = ob_ima(f)
        return send_file(result, mimetype='image/jpeg')
    return "pass"




# detect mp4
@app.route("/ob_mp4.html")
def myMp4():
    if "nickname" in session:
        return render_template("/ob_mp4.html")
    else:
        return redirect("/")
    #return render_template("/ob_mp4.html")


@app.route("/ob_mp42.html", methods=["GET", "POST"])
def myMp42():
    global i
    if request.method == 'POST':
        f = request.files['file']
        result = ob_mp4(f)
        return send_file("myvideo.mp4", mimetype="video/mp4")
        #return render_template("/ob_mp4_start.html")
        #return send_file(result, mimetype='video/mp4')
    return send_file("myvideo.mp4", mimetype="video/mp4")#"pass"





# detect realtime

# @app.route("/ob_realtime.html")
# def myRealtime():
#     return render_template("/ob_realtime.html")


@app.route("/signinup.html")
def signinup():
    return render_template("signinup.html")


@app.route("/member")
def member():
    if "nickname" in session:
        return render_template("member.html")
    else:
        return redirect("/")
    
@app.route("/error.html")
def error():
    message=request.args.get("msg","發生錯誤，請聯繫客服")
    return render_template("error.html",message=message)

@app.route("/signup.html",methods=["POST"])
def signup():
    #從前端接收資料
    nickname=request.form["nickname"]
    email=request.form["email"]
    password=request.form["password"]
    #根據接收到的資料跟資料庫互動
    collection=db.user
    #檢查會員集合中是否有相同email的文件資料
    result=collection.find_one({
        "email":email
    })
    if result !=None:
        return redirect("/error?msg=信箱已經被註冊")
    #把資料放進資料庫，完成註冊
    collection.insert_one({
        "nickname":nickname,
        "email":email,
        "password":password
    })
    return redirect("/")


@app.route("/signin",methods=["POST"])
def signin():
    #從前端取得使用者的輸入
    email=request.form["email"]
    password=request.form["password"]
    #和資料庫互動
    collection=db.user
    #檢查信箱密碼是否正確
    result=collection.find_one({
        "$and":[
            {"email":email},
            {"password":password}
        ]
    })
    #找不到資料會導向錯誤頁面
    if result==None:
        return redirect("/error?msg=帳號或密碼輸入錯誤")
    #登入成功，在session紀錄會員資訊，導向會員介面
    session["nickname"]=result["nickname"]
    return redirect("/member")


@app.route("/signout")
def signout():
    #移除session中的會員資訊
    del session["nickname"]
    return redirect("/")


if __name__ == '__main__':
    app.run( host='127.0.0.1', port=5000)  