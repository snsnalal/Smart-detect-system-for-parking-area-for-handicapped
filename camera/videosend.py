import cv2
import socket
import numpy
from threading import Thread
import time
import sensor


def receive(sock):
    while True:
        recvData = sock.recv(1024)
        print('상대방 :', recvData.decode())
        
        illegal = recvData.decode() #여기서 illegal은 string이다.
        if(illegal == "False"):
            print("합법 주차 입니다.")
            sensor.legal_parking()
            sensor.stop_count = 0
        elif(illegal == "True"):
            print("불법 주차 입니다.")
            sensor.illegal_parking()
            sensor.stop_count = 0
        else:
            print("방해행위가 감지 됐습니다.")
        
        
def capture_send(s):


    #frame = cv2.imread("test3.jpg")
    ## webcam 이미지 capture
    cam = cv2.VideoCapture(0)
    ## 이미지 속성 변경 3 = width, 4 = height
    cam.set(3, 640);
    cam.set(4, 480);
    ret, frame = cam.read()

    ## 0~100에서 90의 이미지 품질로 설정 (default = 95)
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    


    # 비디오의 한 프레임씩 읽는다.
    # 제대로 읽으면 ret = True, 실패면 ret = False, frame에는 읽은 프레임
    # cv2. imencode(ext, img [, params])
    ## encode_param의 형식으로 frame을 jpg로 이미지를 인코딩한다.
    result, frame = cv2.imencode('.jpg', frame, encode_param)
    # frame을 String 형태로 변환
    data = numpy.array(frame)
    stringData = data.tostring()
 
    #서버에 데이터 전송
    #(str(len(stringData))).encode().ljust(16)
    s.sendall((str(len(stringData))).encode().ljust(16) + stringData)
    #cam.release()


if __name__== "__main__":

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ## server ip, port
    s.connect(('113.198.234.39', 9999))

    receiver = Thread(target=receive, args=(s,))
    receiver.start()

    stop_count =0
    while True:
        case,stop_count= sensor.sensor(stop_count)
        if(case == 1): #여기 조건에 서버에서 클래스 받아와서 조건추가 해줄꺼임
            capture_send(s)
            

