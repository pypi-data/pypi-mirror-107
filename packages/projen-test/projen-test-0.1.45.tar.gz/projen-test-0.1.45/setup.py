import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "projen-test",
    "version": "0.1.45",
    "description": "@seeebiii/projen-test",
    "license": "Apache-2.0",
    "url": "https://github.com/seeebiii/projen-test",
    "long_description_content_type": "text/markdown",
    "author": "Sebastian Hesse",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/seeebiii/projen-test"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "projen_test",
        "projen_test._jsii"
    ],
    "package_data": {
        "projen_test._jsii": [
            "projen-test@0.1.45.jsii.tgz"
        ],
        "projen_test": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "aws-cdk.aws-lambda>=1.97.0, <2.0.0",
        "aws-cdk.core>=1.97.0, <2.0.0",
        "constructs>=3.2.27, <4.0.0",
        "jsii>=1.29.0, <2.0.0",
        "publication>=0.0.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
