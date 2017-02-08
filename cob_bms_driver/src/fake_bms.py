#!/usr/bin/env python

import rospy
from std_msgs.msg import Bool
from std_msgs.msg import Float64
from cob_srvs.srv import SetFloat, SetFloatResponse
from std_srvs.srv import SetBool, SetBoolResponse

class FakeBMS(object):
    def __init__(self):
        self.srv_charging = rospy.Service('~set_charging', SetBool, self.charging_cb)
        self.srv_relative_remaining_capacity = rospy.Service('~set_relative_remaining_capacity', SetFloat, self.relative_remaining_capacity_cb)
        self.pub_voltage            = rospy.Publisher('/bms/voltage', Float64, queue_size = 1)
        self.pub_current            = rospy.Publisher('/bms/current', Float64, queue_size = 1)
        self.pub_remaining_capacity = rospy.Publisher('/bms/remaining_capacity', Float64, queue_size = 1)
        self.pub_charge_capacity    = rospy.Publisher('/bms/full_charge_capacity', Float64, queue_size = 1)
        self.pub_temparature        = rospy.Publisher('/bms/temperature', Float64, queue_size = 1)
        self.pub_charging_state     = rospy.Publisher('/bms/battery_charging', Bool, queue_size = 1)        
        
        self.voltage            = 0.0
        self.current            = 0.0
        self.remaining_capacity = 0.0
        self.charge_capacity    = 0.0
        self.temperature        = 0.0
        self.charging_state     = False

        rospy.Timer(rospy.Duration(0.1), self.timer_cb)
        rospy.loginfo('FakeBMS is running')

    def charging_cb(self, req):
        self.charging_state = req.data
        res_charging = SetBoolResponse(True, "Set charging to {}".format(req.data))
        return res_charging
        
    def relative_remaining_capacity_cb(self, req):
        self.remaining_capacity = req.data
        res_capacity = SetFloatResponse(True, "Set relative remaining capacity to {}".format(req.data))
        return res_capacity

    def timer_cb(self, event):
        self.pub_voltage.publish(self.voltage)
        self.pub_current.publish(self.current)
        self.pub_remaining_capacity.publish(self.remaining_capacity)
        self.pub_charge_capacity.publish(self.charge_capacity)
        self.pub_temparature.publish(self.temperature)
        self.pub_charging_state.publish(self.charging_state)
        
if __name__ == '__main__':
  rospy.init_node('fake_bms')
  FakeBMS()
  rospy.spin()
