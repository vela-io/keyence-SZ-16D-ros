import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from .KeyenceSZ16D import KeyenceSZ16D
from .FakerLaserData import FakeLaser

class CloudPointsPublisher(Node):
    def __init__(self):
        super().__init__('cloud_points_publisher')
        self.publisher = self.create_publisher(LaserScan, 'cloud_points_topic', 10)   
        self.laser_callback()
    
    def laser_callback(self):

        laser_freq_in_ms = 66.0e-06
        num_points = 751

        laser = LaserScan()
        
        laser.header.frame_id = "frame_keyence_scan"

        angle_min_in_rad = -0.785398
        angle_max_in_rad = 0.92699
        angle_increment_in_rad = 0.00628 

        laser.angle_min = angle_min_in_rad
        laser.angle_max = angle_max_in_rad
        laser.angle_increment = angle_increment_in_rad

        laser.scan_time = 1.0 / laser_freq_in_ms
        laser.time_increment = 1.0 / laser_freq_in_ms / num_points
        
        range_min_in_m = 4.2
        range_max_in_m = 10.0

        laser.range_min = range_min_in_m
        laser.range_max = range_max_in_m

        laser_inputs = KeyenceSZ16D

        laser.ranges = laser_inputs.tick() 

        self.publisher.publish(laser)

        self.get_logger().info("Publishing: %s" % laser.ranges)

def main():

    rclpy.init()

    publisher = CloudPointsPublisher()

    rclpy.spin(publisher)

    publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()