from setuptools import setup

package_name = 'gcode_interface'

setup(
    name=package_name,
    version='0.9.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=[
        'setuptools',
        'pyserial',
    ],
    zip_safe=True,
    maintainer='Daniel Alvarez',
    maintainer_email='danidask@gmail.com',
    description='Gcode Interface',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'gcode_interface = gcode_interface.gcode_interface:main',
        ],
    },
)
