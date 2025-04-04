from setuptools import find_packages, setup

package_name = 'robu'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='robu',
    maintainer_email='praerz21@htl-kaindorf.at',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'remotectrl=robu.ue06_remotectrl:main',
            'distance_pub = robu.ue07_distance: main_distance_pub',
            'distance_sub = robu.ue07_distance: main_distance_sub'
        ],
    },
)
