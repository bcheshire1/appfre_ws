# Lancaster University Group 3 masters project "Autonomous Path Planning For Radioactive Environments"

For this workspace to run, a few extra packages need to be installed.

Firstly, udpate and upgrade apt
```
sudo apt update
sudo apt upgrade
```

Install colcon
```
sudo apt install python3-colcon-common-extensions
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

Install gazebo_ros_pkgs
```
sudo apt install ros-foxy-gazebo-ros-pkgs
```
Install python3-pip
```
sudo apt install python3-pip
```
install the xacro extension
```
pip install xacro
```

Then clone this repo (probably into your home directory)
```
git clone https://github.com/bcheshire1/appfre_ws.git
```
Navigate into the appfre_ws directory
```
cd appfre_ws
```
## Building the workspace
When building the workspace, you will need to remove the ```build```, ```log```, and ```install``` directories (simply open file explorer and delete them, or alternatively, run the command below). This will give colcon a clean build space to build from and will prevent any issues arising due to difference in PC names etc.

Do this by running this command from your workspace (```~/appfre_ws$ ```):
```
rm -r install && rm -r build && rm -r log
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
