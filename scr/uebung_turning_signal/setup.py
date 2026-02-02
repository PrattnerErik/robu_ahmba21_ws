from setuptools import find_packages, setup

package_name = 'uebung_turning_signal'

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
            'turning_client=uebung_turning_signal.turning_signal_client:main',
            'turning_service=uebung_turning_signal.turning_signal_service:main'
        ],
    },
)
