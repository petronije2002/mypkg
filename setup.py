from setuptools import setup
from glob import glob
import os

package_name = 'mypkg'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    
     
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),

        (os.path.join('share', package_name, 'config'),glob('config/*.yaml')),


        (os.path.join('share', package_name ,'launch'), glob('launch/*.launch.py')),

        
        (os.path.join('share', package_name ,'urdf'), glob('urdf/*.urdf')),
                (os.path.join('share', package_name ,'urdf'), glob('urdf/*.xacro')),

        (os.path.join('share', package_name ,'rviz'), glob('rviz/*.rviz')),
        (os.path.join('share', package_name ,'worlds'), glob('worlds/*.world')),

        #Here we define subfolders to transfer model correctly
        # (os.path.join('share', package_name ,'models'), glob('models/*.*')),
        (os.path.join('share', package_name ,'models/my_ground_plane'), glob('models/my_ground_plane/*.*')),
        (os.path.join('share', package_name ,'models/my_ground_plane/materials/scripts'), glob('models/my_ground_plane/materials/scripts/*.*')),
        (os.path.join('share', package_name ,'models/my_ground_plane/textures'), glob('models/my_ground_plane/textures/*.*'))






    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='pera',
    maintainer_email='pera@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [

                    'follower = mypkg.follower:main'

        ],
    },
)
