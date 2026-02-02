from setuptools import find_packages, setup
import os
from glob import glob

package_name = 'turn_signal'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*launch.[pxy][yma]*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='robu',
    maintainer_email='li@htl-kaindorf.at',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'turn_service=turn_signal.turn_signal_service:main',
            'turn_client=turn_signal.turn_signal_client:main'
        ],
    },
)
