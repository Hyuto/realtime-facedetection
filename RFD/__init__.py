from os import environ

# Set Environ for logging
environ['OPENCV_VIDEOIO_PRIORITY_MSMF'] = '0'
environ['TF_CPP_MIN_LOG_LEVEL'] = '3'