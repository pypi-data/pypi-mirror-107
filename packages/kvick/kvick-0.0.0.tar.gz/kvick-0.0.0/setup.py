try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

install_requires = ["requests>=2.25.0"]

setup(
    name="kvick",
    version="0.0.0",
    description="Python bindings for the Kvick API",
    author="Kvick",
    author_email="support@kvick.ai",
    url="https://github.com/kvickapi/kvick-python",
    keywords=[
        "kvick",
        "api",
        "annotation",
        "labeling",
        "categorization",
    ],
    install_requires=install_requires,
    python_requires=">=3.6",
    classifiers=[
        # "Development Status :: 5 - Production/Stable",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
