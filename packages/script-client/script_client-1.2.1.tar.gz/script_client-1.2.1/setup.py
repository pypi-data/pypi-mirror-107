from setuptools import setup, find_packages
import shutil


try:
    shutil.rmtree("build")
    shutil.rmtree("dist")
except:
    pass


setup(name='script_client',
      version='1.2.1',
      author='TDC',
      author_email='tiandachun@meicai.cn',
      description="script client",
      long_description='''script client''',
      install_requires=['JPype1>=0.7.4',
                        "loguru>=0.3.2",
                        "requests>=2.22.0",
                        "tornado>=6.1",
                        "APScheduler>=3.7.0",
                        "psutil>=5.8.0",
                        ],
      license="MIT",
      packages=find_packages(),
      include_package_data=True,
      data_files=[
          ('script_client/templates', ['script_client/templates/upload.html']),
          ('script_client/static/css',
           ['script_client/static/css/bootstrap.min.css', 'script_client/static/css/fileinput.min.css']),
          ('script_client/static/js', ['script_client/static/js/bootstrap.min.js', 'script_client/static/js/fileinput.min.js',
                                    'script_client/static/js/jquery-3.4.1.min.js'])
      ]
      )
