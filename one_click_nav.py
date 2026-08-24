#!/usr/bin/env python3
import subprocess
import time
import os
import signal
import sys

MAP_FILE = os.path.expanduser("~/turtlebot3_world_map.yaml")
NAV_SCRIPT = os.path.expanduser("~/auto_multi_goal_nav.py")

def start_process(cmd, env):
    return subprocess.Popen(cmd, shell=True, env=env, preexec_fn=os.setsid)

def main():
    os.system("killall gzserver gzclient 2>/dev/null")
    time.sleep(1)

    env = os.environ.copy()
    env['TURTLEBOT3_MODEL'] = 'burger'
    # 关键：添加 Gazebo ROS 插件路径
    env['GAZEBO_PLUGIN_PATH'] = '/opt/ros/humble/lib:' + env.get('GAZEBO_PLUGIN_PATH', '')
    # 不设置 GAZEBO_MODEL_PATH，使用系统默认
    for key in ['PYTHONPATH', 'LD_LIBRARY_PATH', 'ROS_DOMAIN_ID']:
        if key in os.environ:
            env[key] = os.environ[key]

    print("🚀 启动 Gazebo...")
    gazebo_proc = start_process("ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py", env)
    time.sleep(15)

    print("🧭 启动 Navigation2...")
    nav_cmd = f"ros2 launch turtlebot3_navigation2 navigation2.launch.py use_sim_time:=True map:={MAP_FILE}"
    nav_proc = start_process(nav_cmd, env)
    time.sleep(12)

    print("🤖 启动自动导航脚本...")
    nav_script_proc = start_process(f"python3 {NAV_SCRIPT}", env)

    print("✅ 一键启动完成！按 Ctrl+C 退出。")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🔄 关闭进程...")
        for p in [gazebo_proc, nav_proc, nav_script_proc]:
            try:
                os.killpg(os.getpgid(p.pid), signal.SIGTERM)
                p.wait()
            except Exception:
                pass
        print("已退出。")

if __name__ == '__main__':
    main()