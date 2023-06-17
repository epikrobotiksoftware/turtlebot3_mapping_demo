#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseWithCovarianceStamped

class MyNode(Node):
    def __init__(self):
        super().__init__('slamtoolbox_pose_node')
        self.subscription = self.create_subscription(
            PoseWithCovarianceStamped,
            '/pose',
            self.pose_callback,
            10  
        )
        self.publisher = self.create_publisher(PoseWithCovarianceStamped, '/new_pose', 10)
    def pose_callback(self, msg):
        self.last_pose = msg
        
        self.publish_messages()
    
    def publish_messages(self):
        timer_period = 1.0  
        timer = self.create_timer(timer_period, self.publish_pose)
    def publish_pose(self):
        pose_msg = PoseWithCovarianceStamped()
        pose_msg.header.frame_id='map'
        now = self.get_clock().now()
        pose_msg.header.stamp=now.to_msg()
        pose_msg.pose = self.last_pose.pose
        self.publisher.publish(pose_msg)

def main(args=None):
    rclpy.init(args=args)
    node = MyNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()