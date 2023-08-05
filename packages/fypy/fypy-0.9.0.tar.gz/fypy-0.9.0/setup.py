#coding:utf-8
#python setup.py sdist bdist_wheel

#C:\Users\admin\AppData\Roaming\Python\Python38\Scripts\twine.exe upload dist/*

#python -m twine upload dist/*

from setuptools import setup,find_packages

with open('README.md', 'r', encoding='utf-8') as fp :
    description = fp.read()


setup(
    name='fypy', # 项目名
    version='0.9.0', # 如 0.0.1/0.0.1.dev1
    description='meteorological satellite of FENGYUN',
    long_description = description,
    url='', # 如果有github之类的相关链接
    author='libin', # 作者
    author_email='libin033@126.com', # 邮箱
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Atmospheric Science',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    # keywords='', # 关键词之间空格相隔一般
    # 需要安装的依赖
    install_requires = [
        'numpy >= 1.0.0',
        'h5py >= 2.0.0',
        'netCDF4 >= 1.0.0',
        'pillow >= 7.0.0',
    ],

    packages=find_packages(),
    data_file=[

    ],
    include_package_data = True, #
    entry_points={ #如果发布的库包括了命令行工具
      },

    python_requires='>=3.0',
)

