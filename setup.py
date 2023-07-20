import setuptools

with open("README.md", "r") as fh:
        long_description = fh.read()

        setuptools.setup(
                name="yiddishycode",
                version="0.9",
                description="yiddish transliteration",
                long_description=long_description,
                long_description_content_type="text/markdown",
                classifiers=[
                            "Programming Language :: Python :: 3",
                        ],
                url="https://github.com/skulick/yiddishycode",
                author="Seth Kulick",
                author_email="skulick@ldc.upenn.edu",
                packages=setuptools.find_packages(),
                python_requires='>=3.7',
            )

        
