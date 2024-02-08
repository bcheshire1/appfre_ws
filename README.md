# Lancaster University Group 3 masters project "Autonomous Path Planning For Radioactive Environments"

For this workspace to run, a few extra packages need to be installed.

Firstly, udpate and upgrade apt
```
sudo apt update
sudo apt upgrade
```

Install ROS2 Humble using the provided documentation (ros-humble-desktop recommended):
```
https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debians.html
```

Install the Navigation2 Package
```
sudo apt install ros-humble-navigation2 ros-humble-nav2-bringup
```

Install the SLAM Toolbox by Steve Macenski:
```
sudo apt install ros-humble-slam-toolbox
```

Install Gazebo classic
```
curl -sSL http://get.gazebosim.org | sh
```

Then clone this repo (probably into your home directory)
```
git clone https://github.com/bcheshire1/appfre_ws.git
```
Navigate into the appfre_ws directory
```
cd appfre_ws
```
Build the workspace with colcon
```
colcon build --symlink-install
```

Test to see if the package has installed correctly by running this command
```
ros2 launch bunker_mini launch_nav2.launch.py world:=./src/bunker_mini/worlds/room.world
```

This runs a launch file that's located within the bunker_mini package. This launch file effectively runs a bunch of terminal commands, opening the relevant software to run the navigation2 stack
