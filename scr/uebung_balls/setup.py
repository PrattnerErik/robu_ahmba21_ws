from setuptools import find_packages, setup

package_name = 'uebung_balls'

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
    maintainer_email='praerz21htl-kaindorf.at',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'balls_service=uebung_balls.balls_service:main',
            'balls_client=uebung_balls.balls_client:main'
        ],
    },
)
