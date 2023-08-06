from setuptools import setup
from setuptools import find_packages

# change this.
NAME = "MST-AUGer"
AUTHOR = "Hui Chong"
EMAIL = "huichong.me@gmail.com"
URL = "https://github.com/AdeBC/MST-AUGer"
LICENSE = "GPL 3.0"
DESCRIPTION = "Synthetic mixture-based data augmentation for microbial source tracking"

if __name__ == "__main__":
    setup(
        name=NAME,
        version="0.0.1",
        author=AUTHOR,
        author_email=EMAIL,
        url=URL,
        license=LICENSE,
        description=DESCRIPTION,
        packages=find_packages(),
        include_package_data=True,
        install_requires=open("./requirements.txt", "r").read().splitlines(),
        long_description=open("./README.md", "r").read(),
        long_description_content_type='text/markdown',
        # change package_name to your package name.
        entry_points={
            "console_scripts": [
                "aug=MST_AUGer:shell.aug"
            ]
        },
        package_data={
            # change package_name to your package name.
            "MST-AUGer": ["src/*.txt"]
        },
        zip_safe=True,
        classifiers=[
            "Programming Language :: Python :: 3",
            # change $license to your license.
            "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
            "Operating System :: OS Independent",
        ],
        python_requires=">=3.6"
    )
