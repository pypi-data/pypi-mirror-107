import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "psconstructs",
    "version": "0.1.6",
    "description": "test cnxc constructs for cdk",
    "license": "Apache-2.0",
    "url": "https://github.com/cnxc-labs/psconstructs.git",
    "long_description_content_type": "text/markdown",
    "author": "Ken Papagno<kenneth.papagno@concentrix.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/cnxc-labs/psconstructs.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "ps_constructs",
        "ps_constructs._jsii"
    ],
    "package_data": {
        "ps_constructs._jsii": [
            "psconstructs@0.1.6.jsii.tgz"
        ],
        "ps_constructs": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "aws-cdk.aws-apigateway>=1.105.0, <2.0.0",
        "aws-cdk.aws-iam>=1.105.0, <2.0.0",
        "aws-cdk.aws-kms>=1.105.0, <2.0.0",
        "aws-cdk.aws-lambda>=1.105.0, <2.0.0",
        "aws-cdk.aws-logs>=1.105.0, <2.0.0",
        "aws-cdk.aws-s3>=1.105.0, <2.0.0",
        "aws-cdk.core>=1.105.0, <2.0.0",
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
