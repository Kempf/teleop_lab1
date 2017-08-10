#!/usr/bin/env python
import roslib; roslib.load_manifest('teleop_lab1')
import rospy

from geometry_msgs.msg import Twist

import sys, select, termios, tty

msg = """
ENGN4627 Lab 1 teleop
---------------------------
Moving around:
        i    
   j    k    l
        m
---------------------------


CTRL-C to quit
"""

moveBindings = {
		#'i':(1,0,0,0),
		'j':(0,0,0,1),
		'l':(0,0,0,-1),
		#'m':(-1,0,0,0),
	       }

speedBindings={
		'i':(0.05,0),
		'm':(-0.05,0),
	      }

def getKey():
	tty.setraw(sys.stdin.fileno())
	select.select([sys.stdin], [], [], 0)
	key = sys.stdin.read(1)
	termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
	return key


def vels(speed,turn):
	return "currently:\tspeed %s\tturn %s " % (speed,turn)

if __name__=="__main__":
    	settings = termios.tcgetattr(sys.stdin)
	
	pub = rospy.Publisher('cmd_vel_mux/input/teleop', Twist, queue_size = 1)
	rospy.init_node('teleop_twist_keyboard')

	speed = rospy.get_param("~speed", 0.0)
	turn = rospy.get_param("~turn", 1.0)
	x = 0
	y = 0
	z = 0
	th = 0
	status = 0

	try:
		print msg
		print vels(speed,turn)
		while(1):
			th = 0
			key = getKey()
			#x = 1
			if key in moveBindings.keys():
				#x = moveBindings[key][0]
				y = moveBindings[key][1]
				#z = moveBindings[key][2]
				z = 0
				th = moveBindings[key][3]
			elif key in speedBindings.keys():
				x = 1
				speed = speed + speedBindings[key][0]
				#turn = turn * speedBindings[key][1]				

				print vels(speed,turn)
				if (status == 14):
					print msg
				status = (status + 1) % 15
			else:
				x = 0
				y = 0
				z = 0
				th = 0
				if (key == '\x03'):
					break

			twist = Twist()
			twist.linear.x = x*speed; twist.linear.y = y*speed; twist.linear.z = z*speed;
			twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = th*turn
			pub.publish(twist)

	except:
		print "Error:", sys.exc_info()[0]

	finally:
		twist = Twist()
		twist.linear.x = 0; twist.linear.y = 0; twist.linear.z = 0
		twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = 0
		pub.publish(twist)

    		termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)


