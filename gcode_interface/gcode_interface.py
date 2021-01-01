import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Point
from .gcode_serial import Gcode


class GcodeInterface(Node):

    def __init__(self):
        super().__init__('gcode_interface')
        self.gcode_sub = self.create_subscription(Point, 'gcode_pose', self.listener_callback, 10)
        # self.publisher_ = self.create_publisher(String, 'topic', 10)
        # timer_period = 0.5  # seconds
        # self.timer = self.create_timer(timer_period, self.timer_callback)
        self.gcode = Gcode(port="/dev/ttyUSB0", baudrate=115200, logger=self.get_logger())

    def listener_callback(self, msg):
        x = int(msg.x)
        y = int(msg.y)
        z = int(msg.z)
        self.get_logger().debug(f"Moving to {x}, {y}, {z}, feedrate {self.gcode.feedrate}")
        self.gcode.move(x, y, z)

    # def timer_callback(self):
    #     msg = String()
    #     msg.data = 'Hello World'
    #     self.publisher_.publish(msg)
    #     # self.get_logger().info('Publishing: "%s"' % msg.data)

    def stop(self):
        # self.gcode_sub.unregister()
        self.gcode.stop()


def main(args=None):
    rclpy.init(args=args)
    node = GcodeInterface()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e)
    finally:
        node.stop()
        node.destroy_node()  # (optional - otherwise it will be done automatically by the garbage collector
        rclpy.shutdown()


if __name__ == '__main__':
    main()
