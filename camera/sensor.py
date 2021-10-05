import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

trig = 23
echo = 24 
buzzer=17
led_red=27
led_green=22
std_distance = 0

GPIO.setup(led_red, GPIO.OUT)
GPIO.setup(led_green, GPIO.OUT)
GPIO.setup(buzzer, GPIO.OUT)
GPIO.setup(trig, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)


def legal_parking():
    GPIO.output(led_red,False)
    GPIO.output(led_green,False)

    
    GPIO.output(led_green,True)
    time.sleep(1)
    GPIO.output(led_green,False)

def illegal_parking():
    import RPi.GPIO as GPIO
    import time

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    trig = 23
    echo = 24 
    buzzer=26
    led_red=27
    led_green=22
    std_distance = 0

    GPIO.setup(led_red, GPIO.OUT)
    GPIO.setup(led_green, GPIO.OUT)
    GPIO.setup(buzzer, GPIO.OUT)
    GPIO.setup(trig, GPIO.OUT)
    GPIO.setup(echo, GPIO.IN)
        
    GPIO.output(led_red,False)
    GPIO.output(led_green,False)
    
    
    p=GPIO.PWM(buzzer,500)
    p.start(50)
    GPIO.output(led_red,True)
    time.sleep(5)
    GPIO.output(led_red,False)
    p.stop()

def distance():
    
    distance = 1.1
    GPIO.output(trig, False) 
    time.sleep(0.5)
              
    GPIO.output(trig, True)
    time.sleep(0.00001)
    GPIO.output(trig, False)
              
    while GPIO.input(echo) == False: 
        pulse_start = time.time()
                  
    while GPIO.input(echo) == True: 
        pulse_end = time.time()
                  
    pulse_duration = pulse_end - pulse_start 
    distance = pulse_duration * 17000
    distance = round(distance, 2)
    return distance


def sensor(stop_count): #이 함수로 거리가 어떻든 무언가 멈쳐 있다는걸 확인 할 수 있음
    global std_distance
    
    if True:
        #print("Std_distance : ", std_distance)
        
        dis = distance()
        #print("Distance : ", dis, "cm")
        
        diff = std_distance - dis
        #print("diff : ", diff)
        
        
        if(diff < 8 and diff > -8 and dis < 2000):
            stop_count = stop_count + 1
            print("stop_count : ",stop_count)
            print("distance:", distance())
            
            if(stop_count == 10): #몇 초동안 멈춰있을 때 할껀지 정함
                return 1 , stop_count
            else:
                std_distace = distance
        else:
            std_distance = distance()
            stop_count = 0

        time.sleep(1)
        return 0 , stop_count