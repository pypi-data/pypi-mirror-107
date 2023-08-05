import cv2
import numpy as np
import face_recognition
import os


def difffaces(image1,image2):
    # image1 = str
    # image2 = str
    image1.replace("'", "")
    image2.replace("'", "")
    img1 = face_recognition.load_image_file(image1)
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
    img2 = face_recognition.load_image_file(image2)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)

    faces1 = face_recognition.face_locations(img1)[0]
    faces2 = face_recognition.face_locations(img2)[0]

    encoded1 = face_recognition.face_encodings(img1)[0]
    encoded2 = face_recognition.face_encodings(img2)[0]

    abc = face_recognition.compare_faces([encoded1], encoded2)
    if abc == "[True]":
        print("Same faces found")
    else:
        print("Different faces found")

def trainwebcam(knownfacesdirectory,webcamindex,windowname):
    def findencodingd(images):
        encodelist = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodelist.append(encode)
        return encodelist
    images = []
    classnames = []
    path = knownfacesdirectory
    mylist = os.listdir(path)
    for classes in mylist:
        imagescur = cv2.imread(f'{path}/{classes}')
        images.append(imagescur)
        classnames.append(os.path.splitext(classes)[0])
    # print(classnames)
    encodelistknown = findencodingd(images)
    cap = cv2.VideoCapture(webcamindex)
    while True:
        success, img = cap.read()
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        faceucrframe = face_recognition.face_locations(imgS)
        encodescurframe = face_recognition.face_encodings(imgS, faceucrframe)

        for encodeface, faceloc in zip(encodescurframe, faceucrframe):
            matches = face_recognition.compare_faces(encodelistknown, encodeface)
            facedis = face_recognition.face_distance(encodelistknown, encodeface)
            print(facedis)
            matchindex = np.argmin(facedis)

            if matches[matchindex]:
                name = classnames[matchindex].upper()
                print(name)
                y1, x2, y2, x1 = faceloc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

            else:
                cv2.putText(img, 'Unknown Person', (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 4)
                print('Unknown Person!')

        cv2.imshow(windowname, img)
        cv2.waitKey(1)
