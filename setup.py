from setuptools import setup, find_packages


def setup_package():
    setup(name='discuit_package',
          packages=find_packages(),
          )


# see setup.cfg
if __name__ == "__main__":
    setup_package()
