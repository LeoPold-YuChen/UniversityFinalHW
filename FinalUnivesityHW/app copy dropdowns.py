i=2
#choosePt=False#True表示用原本的，False則代表用邊線圖的
#pt_path="runs\detect/100_6.pt"
def ob_ima(file):
    # if ifHasRuns():
    #     i=2 #predict從2開始。季的測試完要刪除其他的predict
    global i
#    global choosePt
#    global pt_path
    # if choosePt:
    #     pt_path="runs\detect/100_6.pt"
    # else:
    #     pt_path="runs\detect/130_4.pt"
    file.save("sir.jpg")    #把接收到的圖片名稱取名叫sir(yes sir!!)
    model = YOLO("runs\detect/100_6.pt") #setting model
    # model = YOLO(pt_path) #setting model
    model.predict("sir.jpg", save=True, imgsz=(640,640), conf=0.5) #predict
    predict_path=f"runs\detect/predict{i}/sir.jpg"
    i=i+1#可能要用到session了
    return predict_path
    #return file.save("output.jpg")


def ifHasRuns():
    if not hasattr(ifHasRuns,"has"):
        ifHasRuns.has=True
        return True
    else:
        return False



from ultralytics import YOLO
from flask import Flask,render_template, request, send_file
app=Flask(__name__,static_url_path="/",static_folder="runs\\detect")

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


@app.route("/ob_mp4.html")
def myMp4():
    return render_template("/ob_mp4.html")



@app.route("/ob_realtime.html")
def myRealtime():
    return render_template("/ob_realtime.html")



# @app.route("/ptChoose100")
# def Choose100():
#     global choosePt
#     choosePt=True
#     return "pass"

# @app.route("/ptChoose130")
# def Choose100():
#     global choosePt
#     choosePt=False
#     return "pass"


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)  