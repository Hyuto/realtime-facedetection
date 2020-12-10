from .. import cv2
from .. import path, mkdir

faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def TakePic(LIST_DIR:list, TO_DIR:str, SIZE:int, N_FRAME:int, model = faceCascade):
    """
    Take image and extract all frame that contain faces to generate dataset

    Args:
        LIST_DIR (str)  : List of image directory
        SIZE     (int)  : Image Size
        N_FRAME  (int)  : time for taking
        model           : faceCascade
    """
    mkdir(TO_DIR)
    count = 1
    while count < N_FRAME:
        for item in LIST_DIR:
            image = cv2.imread(item)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = model.detectMultiScale(gray, scaleFactor = 1.1, 
                                        minNeighbors = 5, minSize = (30, 30))
            for (x, y, w, h) in faces:
                img = gray[y:y+h, x:x+w]
                resize = cv2.resize(img, (SIZE, SIZE))
                if count <= N_FRAME:
                    cv2.imwrite(path.join(TO_DIR, f'{count} .jpg'), resize)
                    count += 1
                else:
                    break
            cv2.destroyAllWindows()

def TakeVid(name:str, DIR:str, SIZE:int, N_FRAME:int, model = faceCascade):
    """
    Take video and extract all frame that contain faces to generate dataset

    Args:
        name (str)    : Person name
        DIR (str)     : Directory
        SIZE (int)    : Image Size
        N_FRAME (int) : time for taking
        model         : faceCascade
    """
    cap = cv2.VideoCapture(0)
    count = 1
    while(cap.isOpened()):
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = model.detectMultiScale(gray, scaleFactor = 1.1, 
                                       minNeighbors = 5, minSize = (30, 30))

        if cv2.waitKey(1) and count > N_FRAME:
            break

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, f"Frame taken {count}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
            img = gray[y:y+h, x:x+w]
            resize = cv2.resize(img, (SIZE, SIZE))
            cv2.imwrite(path.join(DIR, f'{count} .jpg'), resize)
            if count <= N_FRAME:
                count += 1
            else:
                break
        
        cv2.imshow(name, frame)

    cap.release()
    cv2.destroyAllWindows()