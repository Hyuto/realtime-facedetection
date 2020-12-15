import time
from . import cv2
from . import info, warning
from tensorflow import reshape, argmax

def Live(model, CONFIG:dict):
    """
    Live detector setup

    Args:
        model  : Keras model that already have been trained
        CONFIG : Configurations
    """
    info('Setting environments for live detection')
    labels_dict = {0: 'unknown'}
    color_dict = {0: (0,0,255)}
    for i, x in enumerate(CONFIG["PERSONS"]):
        labels_dict[i + 1] = x
        color_dict[i + 1] = (0, 255, 0)

    info('Loading OpenCV model..')
    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    info('Running live detection. Press "Q" to exit.')
    cap = cv2.VideoCapture(0)

    start = time.time()
    frame_count, frame_count_fixed = 0, 0
    while(cap.isOpened()):

        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, scaleFactor = 1.1, minNeighbors = 5, minSize = (30, 30))

        for x, y, w, h in faces:
            face_img = gray[y:y+w, x:x+w]
            resized = cv2.resize(face_img, (CONFIG['IMAGE_DATA']['SIZE'], CONFIG['IMAGE_DATA']['SIZE']))
            normalized = resized / 255.0
            reshaped = reshape(normalized, (1, CONFIG['IMAGE_DATA']['SIZE'], CONFIG['IMAGE_DATA']['SIZE'], 1))
            
            result = model.predict(reshaped)
            label = argmax(result, axis = 1).numpy()[0]

            cv2.rectangle(frame, (x, y), (x+w, y+h), color_dict[label], 2)
            cv2.rectangle(frame, (x, y-40), (x+w, y), color_dict[label], -1)
            cv2.putText(frame, f'{labels_dict[label]} {round(result[0][label] * 100, 2)}%', 
                        (x+3, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)
        
        # Performance
        if time.time() - start <= 1:
            frame_count += 1
        else:
            frame_count_fixed = frame_count
            frame_count = 0
            start = time.time()
        
        cv2.putText(frame, f'Performance', (3, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255), 2)
        cv2.putText(frame, f'FPS : {frame_count_fixed}', (3, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)

        cv2.imshow('LIVE', frame)
        if cv2.waitKey(4) & 0xFF == ord('q'):
            info('Shutingdown live detection..')
            break
            
    cv2.destroyAllWindows()
    cap.release()