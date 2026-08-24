#!/usr/bin/env python3
import rclpy
import time
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult

# ------------------- 配置区域 --------------------
# 初始位姿（地图坐标系）—— 请根据实际情况修改
INITIAL_POSE = (0.0, 0.0, 0.0, 1.0)  # (x, y, z, w)

# 目标点列表 —— 设置为靠近初始位姿的短距离点（单位：米）
# 可根据需要修改坐标，但确保点位于自由空间（白色区域）
WAYPOINTS = [
    (1.0, 0.5, 0.0, 1.0),   # 目标点1：右前方
    (0.5, 1.0, 0.0, 1.0),   # 目标点2：左前方
    (1.5, 1.5, 0.0, 1.0),   # 目标点3：更远的右前方
]
# ------------------------------------------------

def create_pose_msg(navigator, x, y, z=0.0, w=1.0):
    pose = PoseStamped()
    pose.header.frame_id = 'map'
    pose.header.stamp = navigator.get_clock().now().to_msg()
    pose.pose.position.x = x
    pose.pose.position.y = y
    pose.pose.orientation.z = z
    pose.pose.orientation.w = w
    return pose

def main():
    rclpy.init()
    navigator = BasicNavigator()

    # 1. 设置初始位姿（使用固定坐标）
    print("📍 设置初始位姿: ({}, {})".format(INITIAL_POSE[0], INITIAL_POSE[1]))
    initial_pose = create_pose_msg(navigator, *INITIAL_POSE)
    navigator.setInitialPose(initial_pose)

    # 2. 等待导航激活
    print("⏳ 等待 Navigation2 激活...")
    navigator.waitUntilNav2Active()

    # 3. 构建目标点列表
    print("🗺️ 构建目标点列表...")
    goal_poses = []
    for i, (x, y, z, w) in enumerate(WAYPOINTS):
        pose = create_pose_msg(navigator, x, y, z, w)
        goal_poses.append(pose)
        print(f"   目标点 {i+1}: ({x}, {y})")

    # 4. 开始巡航
    print("🚀 开始依次通过目标点...")
    navigator.goThroughPoses(goal_poses)

    # 5. 监控导航状态（使用 current_goal）
    while not navigator.isTaskComplete():
        feedback = navigator.getFeedback()
        if feedback:
            try:
                current = feedback.current_goal
                if current is not None:
                    print(f'📍 当前目标点索引: {current+1}')
            except AttributeError:
                pass
            print(f'   剩余距离: {feedback.distance_remaining:.2f} 米')
        time.sleep(0.5)

    # 6. 检查结果
    result = navigator.getResult()
    print("\n" + "="*40)
    if result == TaskResult.SUCCEEDED:
        print("✅ 所有目标点已到达！")
    elif result == TaskResult.CANCELED:
        print("⛔ 任务被取消")
    elif result == TaskResult.FAILED:
        print("❌ 任务失败！")
    print("="*40)

    rclpy.shutdown()

if __name__ == '__main__':
    main()