// Micro-ROS libraries
#include <micro_ros_arduino.h>
#include <stdio.h>
#include <rcl/rcl.h>
#include <rcl/error_handling.h>
#include <rclc/rclc.h>
#include <rclc/executor.h>

// WiFi library
#include <WiFi.h>

// ROS2 messages
#include <std_msgs/msg/Int32.h>
// Car control library
#include <ESP32Servo.h>

// Micro-ROS variables
rcl_subscription_t subscriber_wheel_angle;
rcl_subscription_t subscriber_speed;
std_msgs__msg__Int32 msg;
rclc_executor_t executor;
rclc_support_t support;
rcl_allocator_t allocator;
rcl_node_t node;
rcl_timer_t timer;

// Initializing DC motor and controlling servo
Servo dc_motor;
Servo control_servo;



// Micro-ROS functions for error handling, checks initialization
#define RCCHECK(fn) { rcl_ret_t temp_rc = fn; if((temp_rc != RCL_RET_OK)){printf("Failed status on line %d: %d. Aborting.\n",__LINE__,temp_rc); error_loop();}}
#define RCSOFTCHECK(fn) { rcl_ret_t temp_rc = fn; if((temp_rc != RCL_RET_OK)){}}

// If checks failed - ESP goes to this loop
void error_loop(){
  delay(5000);
}



// Callback function. Called every time when new data from publishers recieved 
void wheel_angle_subscription_callback(const void *msgin) {
  const std_msgs__msg__Int32 *msg = (const std_msgs__msg__Int32 *)msgin;
  Serial.print("Wheel Angle: ");
  Serial.println(msg->data);
  int angle = msg->data;
  // Tells value to DC motor. Value has to be between 45 and 135 degrees
  // 135 = LEFT
  // 45 = RIGHT
  if (angle < 45) {
    angle = 45;
  } else if (angle > 135) {
    angle = 135;
  } 

  control_servo.write(angle);
  delay(15);
}

void speed_subscription_callback(const void *msgin) {
  const std_msgs__msg__Int32 *msg = (const std_msgs__msg__Int32 *)msgin;
  Serial.print("Speed: ");
  Serial.println(msg->data);
  int speed = msg->data;


  // Tells speed value to DC motor
  dc_motor.writeMicroseconds(speed);
  delay(4);
}

// SETUP
void setup() {
  // Initalize serial monitor
  Serial.begin(115200);
  // Connecting to WIFi
  WiFi.begin("jetson_team1", "jetson_team1");
  Serial.println("Connecting to Wi-Fi");
  // If WiFi not connected print dots
  while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.print(".");
    }
  // If connected to WiFi prints IP address.
  Serial.println("WiFi connected!");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  // Setting Micro-ROS transport
  set_microros_wifi_transports("jetson_team1", "jetson_team1", "10.42.0.1", 8888);
  // Delay to wait for WiFi settings apply
  delay(2000);


  //SERVO AND MOTOR SETTINGS

  // Motor pin 5
  dc_motor.attach(5);
  // 1500, motor not working
  dc_motor.writeMicroseconds(1500);
  // Controlling servo pin 4
  control_servo.attach(4);
  // Deafualt position for control servo
  control_servo.write(90);


  // MICRO-ROS SETTINGS

  allocator = rcl_get_default_allocator();
  //create init_options
  RCCHECK(rclc_support_init(&support, 0, NULL, &allocator));
  Serial.println("Initilizing...");

  // create node
  RCCHECK(rclc_node_init_default(&node, "arduino_node", "", &support));
  Serial.println("Initializing node...");

  // create subscriber for speed
  RCCHECK(rclc_subscription_init_default(
  &subscriber_speed,
  &node,
  ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Int32), 
  "wheel_angle_control"));
  Serial.println("Wheel angle subscriber ready...");

  // Create subscriber for wheels' angle
  RCCHECK(rclc_subscription_init_default(
  &subscriber_wheel_angle,
  &node,
  ROSIDL_GET_MSG_TYPE_SUPPORT(std_msgs, msg, Int32), 
  "speed_control"));
  Serial.println("Speed subscriber ready...");


  // create executor
  RCCHECK(rclc_executor_init(&executor, &support.context, 2, &allocator));
  RCCHECK(rclc_executor_add_subscription(&executor, &subscriber_wheel_angle, &msg, &speed_subscription_callback, ON_NEW_DATA));
  RCCHECK(rclc_executor_add_subscription(&executor, &subscriber_speed, &msg, &wheel_angle_subscription_callback, ON_NEW_DATA));
  Serial.println("Executor ready");
}

void loop() {
  delay(100);
  rclc_executor_spin_some(&executor, RCL_MS_TO_NS(100));
}
