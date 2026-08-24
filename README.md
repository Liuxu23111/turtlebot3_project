# turtlebot3_project
基于ROS2和Gazebo的TurtleBot3仿真导航
  环境要求
- 操作系统：Ubuntu 22.04 LTS（可在 VMware 虚拟机中运行）
- ROS 版本：ROS 2 Humble
- 仿真器：Gazebo 11.10.2
- 可视化工具：RViz2

-  实现思路
整体架构
本项目基于 ROS2 的 Navigation2 (Nav2) 导航堆栈，在 Gazebo 仿真环境中实现 TurtleBot3 的自主导航。整体架构分为三层：

仿真层：Gazebo 提供物理仿真环境，加载 TurtleBot3 模型和世界地图。

导航层：Nav2 堆栈负责路径规划（全局规划器 + 局部规划器）和 AMCL 定位。

控制层：Python 脚本通过 nav2_simple_commander API 控制机器人执行多目标点巡航。

运行方法
1. 创建工作空间并克隆代码
bash
mkdir -p ~/turtlebot3_ws/src && cd ~/turtlebot3_ws/src
git clone -b humble https://github.com/ROBOTIS-GIT/turtlebot3_msgs.git
git clone -b humble https://github.com/ROBOTIS-GIT/turtlebot3.git
git clone -b humble https://github.com/ROBOTIS-GIT/turtlebot3_simulations.git
2. 编译工作空间
bash
cd ~/turtlebot3_ws
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash
3. 配置环境变量
将以下内容添加到 ~/.bashrc：

bash
source /opt/ros/humble/setup.bash
source ~/turtlebot3_ws/install/setup.bash
export TURTLEBOT3_MODEL=burger
4. 准备地图文件
将 maps/turtlebot3_world_map.yaml 和 turtlebot3_world_map.pgm 放入 ~/ 目录下。

5. 修改目标点坐标（可选）
编辑 scripts/auto_multi_goal_nav.py，修改 WAYPOINTS 列表中的坐标值：

python
WAYPOINTS = [
    (1.0, 0.5, 0.0, 1.0),   # 目标点1
    (2.5, 1.5, 0.0, 1.0),   # 目标点2
    (0.5, 2.0, 0.0, 1.0),   # 目标点3
]
每个目标点格式为 (x, y, z, w)，其中 (x, y) 为位置坐标，(z, w) 为四元数朝向。

6. 一键启动
bash
cd ~
python3 one_click_nav.py

已实现功能
一键启动仿真环境：one_click_nav.py 自动启动 Gazebo、Navigation2 和 RViz

自动建图与地图保存：支持 Cartographer SLAM 建图，地图保存为 .yaml + .pgm 格式

多目标点自动导航：机器人按预设顺序依次通过多个目标点

初始位姿自动设置：脚本自动从 /odom 读取机器人当前位置作为初始位姿

实时导航状态监控：打印剩余距离和当前目标点索引

进程自动清理：退出时自动终止 Gazebo、Nav2 等子进程
