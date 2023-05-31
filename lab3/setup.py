from setuptools import setup, find_packages


setup(
    name="denvilk-serializer",
    version="1.0.0",
    description="JSON and XLM serializer",
    author="Vladimir Velikovich",
    author_email="vvelikovich@gmail.com",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [ 
            'serializer = MySerializer.serializer:main' 
        ],
    },
)