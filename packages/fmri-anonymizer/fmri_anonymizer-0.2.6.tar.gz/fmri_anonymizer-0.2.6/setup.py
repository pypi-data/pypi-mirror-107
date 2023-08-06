from setuptools import setup, find_packages


def get_requirements():
    with open('requirements.txt') as requirementsFile:
        requirements = requirementsFile.read().splitlines()
    return requirements


def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(name="fmri_anonymizer",
      version='0.2.6',
      __version__='0.2.6',
      description="Anonymize your DICOM and NIFTI files with this tool easily.",
      long_description=readme(),
      long_description_content_type="text/markdown",
      url="https://caoslab.psy.cmu.edu:32443/hugoanda/fmri_anonymizer",
      author="Hugo Angulo",
      author_email="hugoanda@andrew.cmu.edu",
      license="MIT",
      classifiers=["License :: OSI Approved :: MIT License",
                   "Programming Language :: Python :: 3",
                   "Programming Language :: Python :: 3.7", ],
      packages=find_packages(),
      include_package_data=True,
      package_data={'': ['util/deid.dicom']},
      install_requires=["alive-progress==1.6.2", "bleach==3.3.0", "bump2version==1.0.1", "cached-property==1.5.2",
                        "certifi==2020.12.5", "chardet==3.0.4", "chrisapp==2.5.3", "ci-info==0.2.0", "click==8.0.0rc1",
                        "colorama==0.4.4", "crcmod==1.7", "cycler==0.10.0", "dataclasses==0.6", "decorator==5.0.7",
                        "deid==0.1.42", "dicom2nifti==2.2.12", "docutils==0.17.1", "etelemetry==0.2.2",
                        "filelock==3.0.12", "fsleyes-props==1.7.3", "fsleyes-widgets==0.12.1",
                        "fslpy==3.6.0", "future==0.18.2", "h5py==3.2.1", "idna==3.1", "importlib-metadata==4.0.1",
                        "isodate==0.6.0", "keyring==23.0.1", "kiwisolver==1.3.1",
                        "lxml==4.6.3", "MarkupSafe==1.1.1", "matplotlib==3.4.1", "networkx==2.5.1", "neurdflib==5.0.1",
                        "nibabel==3.2.1", "nipype==1.6.0", "numpy==1.20.2", "packaging==20.9", "parso==0.8.2",
                        "Pillow==8.2.0", "pkginfo==1.7.0", "prov==2.0.0", "pudb==2021.1", "pydeface==2.0.0",
                        "pydicom>=1.2.1", "pydot==1.4.2", "pydotplus==2.0.2", "Pygments==2.8.1", "pyigtl==0.1.0",
                        "PyOpenGL==3.1.5", "pyparsing==2.4.7", "python-dateutil==2.8.1", "python-utils==2.5.6",
                        "rdflib==5.0.0", "readme-renderer==29.0", "requests==2.25.1", "requests-toolbelt==0.9.1",
                        "rfc3986==1.4.0", "scipy==1.6.3", "SimpleITK==1.2.0", "simplejson==3.17.2", "six==1.15.0",
                        "tqdm==4.60.0", "traits==6.2.0", "ttictoc==0.5.6", "twine==3.4.1", "typing-extensions==3.7.4.3",
                        "urllib3==1.26.4", "urwid==2.1.2", "webencodings==0.5.1", "wxPython==4.1.1", "zipp==3.4.1", ],
      entry_points={"console_scripts": ["fmri_anonymizer=fmri_anonymizer.__main__:main", ]},
      python_requires='>=3.7', )
