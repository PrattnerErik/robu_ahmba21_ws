#Exercise Title:    Remote Control for Burrgr
#Group:             ?
#Class:             ahmba21
#Date:              ?

import rclpy        # importiert ros2 framework
import os           # Betriebssystemspezifische Funktionen
import select       # zwischen mehrere Threads lesen
import sys          # Systembibliothek
import time         # time time time time time zb. time.sellp(1.0) -> 1 sek schlafen


from geometry_msgs.msg import Twist # Datentyp von ros2
from rclpy.qos import QoSProfile # Datentyp von ros2
from sensor_msgs.msg import LaserScan, Image
from rclpy.qos import QoSProfile

import termios
import tty

msg = """
Excercise:  ?
Group:      ?
Class:      ?
Date:       ?
"""

e = """
Communications Failed
"""

#Physikalische Grenzen des Roboters
MAX_LIN_VEL = 0.22          #m/s
MAX_ANG_VEL = 2.84          #rad/s

LIN_VEL_STEP_SIZE = 0.01    #m/s
ANG_VEL_STEP_SIZE = 0.1     #rad/s

def get_key():
    old_settings = termios.tcgetattr(sys.stdin)
    ts = time.time()
    key = ''
    try:
        tty.setraw(sys.stdin.fileno())
        while True:
            rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
            if rlist:
                key += os.read(sys.stdin.fileno(), 1).decode("utf-8")
            else:
                break
        return key
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)

def main():
    
    rclpy.init()

    qos = QoSProfile(depth=10)
    
    node = rclpy.create_node('remotectrl')
    pub = node.create_publisher(Twist, '/cmd_vel', qos)

    vel = Twist()

    try:
        while(1):
            key = get_key()
            if key != '':
                str = "String: " + key.replace(chr(0x1B), '^') + ", Code:"
                for c in key:
                    str += " %d" % (ord(c))
                print(str)
                
                if key == '\x03':
                    print("jojojoooooo tutell")
                    break

                if key == '\x1B[A':
                    vel.linear.x += LIN_VEL_STEP_SIZE
                    if vel.linear.x > MAX_LIN_VEL:
                        vel.linear.x = MAX_LIN_VEL
                    
                    print(f"Geschw >: %.3f", vel.linear.x)
                
                if key == '\x1B[B':
                    vel.linear.x -= LIN_VEL_STEP_SIZE
                    if vel.linear.x < -MAX_LIN_VEL:
                        vel.linear.x = -MAX_LIN_VEL
                    
                    print(f"Geschw <: %.3f", vel.linear.x)

                if key == '\x1B[D':
                    vel.angular.z += ANG_VEL_STEP_SIZE
                    if vel.angular.z > MAX_ANG_VEL:
                        vel.angular.z = MAX_ANG_VEL
                        
                    print(f"Ang >: %.3f", vel.angular.z)
                    
                if key == '\x1B[C':
                    vel.angular.z -= ANG_VEL_STEP_SIZE
                    if vel.angular.z < -MAX_ANG_VEL:
                        vel.angular.z = -MAX_ANG_VEL
                    
                    print(f"Ang <: %.3f", vel.angular.z)
                
                if key == '\x1B':
                    vel.angular.z = 0.0
                    vel.linear.x = 0.0

                    print(f"Geschw = 0 angl = 0")

                pub.publish(vel)
                




    except Exception as e:
        print(e)

    finally:
        vel.angular.z = 0.0
        vel.linear.x = 0.0
        pub.publish(vel)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()