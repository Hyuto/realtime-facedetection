import cv2
from numpy import reshape, argmax

def Live(model, CONFIG):

    labels_dict = {0:'unknown'}
    color_dict = {0:(0,0,255)}
    for i, x in enumerate(CONFIG["PERSONS"]):
        labels_dict[i + 1] = x
        color_dict[i + 1] = (0,255,0)

    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)
    while(cap.isOpened()):

        ret, frame = cap.read()
        gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for x, y, w, h in faces:
            face_img = gray[y:y+w, x:x+w]
            resized = cv2.resize(face_img, (CONFIG['IMG_SIZE'], CONFIG['IMG_SIZE']))
            normalized = resized / 255.0
            reshaped = reshape(normalized, (1, CONFIG['IMG_SIZE'], CONFIG['IMG_SIZE'], 1))
            result = model.predict(reshaped)

            label = argmax(result, axis = 1)[0]
        
            cv2.rectangle(frame, (x, y), (x+w, y+h), color_dict[label], 2)
            cv2.rectangle(frame, (x, y-40), (x+w, y), color_dict[label], -1)
            cv2.putText(frame, f'{labels_dict[label]} {round(result[0][label], 2)}%', 
                        (x+3, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)
            
        cv2.imshow('LIVE', frame)
        if cv2.waitKey(4) & 0xFF == ord('q'):
            break
            
    cv2.destroyAllWindows()
    cap.release()