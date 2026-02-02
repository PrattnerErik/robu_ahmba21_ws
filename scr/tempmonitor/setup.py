# create new package:
# ros2 pkg create {package_name} --build-type ament_python


from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'tempmonitor'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='robu',
    maintainer_email='praerz21htl-kaindorf.at',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'temp_sensor=tempmonitor.temp_sensor_node:main',
            'temp_monitor=tempmonitor.temp_monitor_node:main'
        ],
    },
)
