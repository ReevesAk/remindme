from tkinter import *
from PIL import ImageTk, Image
from matplotlib import pyplot as plt
from imageai.Classification import ImageClassification
from io import BytesIO
import threading
import cv2 as cv
import time
import os
import webbrowser
import requests
import json
import base64

window = Tk()


# endpoint = "http://159.203.163.52:17778/api/items"
# api_request = requests.get(endpoint)
# print(api_request.status_code)
#
# api = json.loads(api_request.content)


# def video_window():
#     video = Listbox(window)
#
#     camera = cv2.VideoCapture("/home/reeves/Videos/jwb_E_202010_14_r360P.mp4")
#
#     if camera.isOpened() == False:
#         Label(video, text='error opening video file')
#
#     while camera.isOpened():
#         ret, frame = camera.read()
#         if ret == True:
#             cv2.imshow('Frame', frame)
#
#             # Press Q on keyboard to  exit
#             if cv2.waitKey(25) & 0xFF == ord('q'):
#                 break
#         else:
#             break
#
#     camera.release()
#
#     # Closes all the frames
#     cv2.destroyAllWindows()


def image_window(img):
    image = Toplevel(window)

    image.geometry('400x400+500+500')
    image.title('Image')

    load_image = Image.open(BytesIO(img))
    render = ImageTk.PhotoImage(load_image)

    image_lab = Label(image, image=render)
    image_lab.image = render
    image_lab.pack(fill=BOTH, expand=YES)


def url_window(link):
    def url_redirect():
        webbrowser.open(link, new=1)

    url = Toplevel(window)

    url.geometry('200x200+220+80')
    url.title('Url Window')

    Button(url, text='visit site',
           command=url_redirect).pack()  # open the URL using default browser on button click.


def text_window(decoded_string):
    text = Toplevel(window)

    text.geometry('400x400+700+80')
    text.title("Text Window")

    Label(text, text=decoded_string).pack(expand=YES)


def drop_down_function():
    for index in api:
        for api_list in index['items']:
            if api_list['type'] == 'text' and 'link':
                string = api[0]['items'][2]['Content']
                base64_msg = base64.b64decode(string)
                bm = base64_msg.decode('utf-8')
                time.sleep(4)
                text_window(str(bm))
                string2 = api[0]['items'][3]['Content']
                base64_msg2 = base64.b64decode(string2)
                bm2 = base64_msg2.decode('utf-8')
                text_window(str(bm2))
                link = api[0]['items'][4]['Content']
                base64_link = base64.b64decode(link)
                bl = base64_link.decode('utf-8')
                time.sleep(4)
                url_window(bl)
                break
            elif api_list['type'] == 'image':
                time.sleep(2)
                image = api[0]['items'][0]['Content']
                base64_img = base64.b64decode(image)
                image_window(base64_img)
                image2 = api[0]['items'][1]['Content']
                base64_img2 = base64.b64decode(image2)
                image_window(base64_img2)
                break
            # elif api_list['type'] == 'link':
            #     time.sleep(5)
            #     link = api[0]['items'][4]['Content']
            #     base64_link = base64.b64decode(link)
            #     bl = base64_link.decode('utf-8')
            #     url_window(bl)
            #     continue
            else:
                break
        else:
            break


def drop_down_function2():
    for index in api:
        for api_list in index['items']:
            if api_list['type'] == 'text' and 'link':
                string = api[1]['items'][0]['Content']
                base64_msg = base64.b64decode(string)
                bm = base64_msg.decode('utf-8')
                time.sleep(2)
                text_window(str(bm))
                string2 = api[1]['items'][1]['Content']
                base64_msg2 = base64.b64decode(string2)
                bm2 = base64_msg2.decode('utf-8')
                time.sleep(3)
                text_window(str(bm2))
                link = api[1]['items'][3]['Content']
                base64_link = base64.b64decode(link)
                bm2 = base64_link.decode('utf-8')
                time.sleep(5)
                url_window(bm2)
                break
            elif api_list['type'] == 'image':
                img = api[1]['items'][2]['Content']
                b64_msg = base64.b64decode(img)
                time.sleep(4)
                image_window(b64_msg)
                break
            # elif api_list['type'] == 'link':
            #     link = api[1]['items'][3]['Content']
            #     base64_link = base64.b64decode(link)
            #     bm2 = base64_link.decode('utf-8')
            #     url_window(str(bm2))
            #     break
            else:
                break
        else:
            break


window.title("Kinter demo app")
window.geometry('300x200')

variable = StringVar(window)
variable.set("Menu")

drop_down_menu = Menu(window)
file = Menu(drop_down_menu, tearoff=0)
sub_menu = Menu(drop_down_menu, tearoff=0)


def thread1():
    popup_manager1 = threading.Thread(target=drop_down_function)
    popup_manager1.start()


def thread2():
    popup_manager2 = threading.Thread(target=drop_down_function2)
    popup_manager2.start()


def thread3():
    camera = threading.Thread(target=take_picture)
    camera.start()


def thread4():
    imagedetection = threading.Thread(target=detectobjectinimage)
    imagedetection.start()


def take_picture():
    capture = cv.VideoCapture(0)  # video capture source camera (Here webcam of laptop)

    if not capture.isOpened():
        raise IOError("Cannot open webcam")

    result = True

    while result:
        ret, frame = capture.read()  # return a single frame in variable `frame`
        frame = cv.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv.INTER_AREA)
        cv.imshow('img.jpg', frame)  # display the captured image
        picture = cv.imwrite('img.jpg', frame)
        result = False
    capture.release()
    cv.destroyAllWindows()

    # obj = cv.imread(picture)


def detection_window(detectedobj):
    obj = Toplevel(window)

    obj.geometry('400x400+700+80')
    obj.title("Image reading")

    Label(obj, text=detectedobj).pack(expand=YES)


def detectobjectinimage():
    path = os.getcwd()
    image_prediction = ImageClassification()
    image_prediction.setModelTypeAsResNet50()
    image_prediction.setModelPath(os.path.join(path, "resnet50_imagenet_tf.2.0.h5"))
    image_prediction.loadModel()

    predictions, percentage_probabilities = image_prediction.classifyImage(os.path.join
                                                                           (path,
                                                                            "/home/akwa/PycharmProjects/remindme/img.jpg"),
                                                                           result_count=10)

    for eachPrediction, eachProbability in zip(predictions, percentage_probabilities):
        print(eachPrediction, " : ", eachProbability)
        result = "Cup wasn't detected, hence, user hasn't drank water today"
        vampire = 'Raid come to our aid, we are dying!!!'
        if eachPrediction == "mosquito_net":
            detection_window(vampire)
        break


# file.add_command(label=api[0]['name'], command=thread1)
#
# file.add_command(label=api[1]['name'], command=thread2)

file.add_command(label="Take a picture", command=thread3)

file.add_command(label="Detect Objects", command=thread4)

file.add_separator()

file.add_command(label="Exit", command=window.quit)

drop_down_menu.add_cascade(label="Menu", menu=file)

window.config(menu=drop_down_menu)

window.mainloop()

# def print_hi(name):
#     # Use a breakpoint in the code line below to debug your script.
#     print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
#
#
# # Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     print_hi('PyCharm')
#
# # See PyCharm help at https://www.jetbrains.com/help/pycharm/
