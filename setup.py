from distutils.core import setup
setup(
    name="glyphpractice",
    packages=["glyphpractice"],
    version="0.0.1",
    description="Chinese Glyph pratice book generator",
    author="Yan-ren Tsai",
    author_email="elleryq@gmail.com",
    url="",
    download_url="",
    keywords=["glyph", "chinese"],
    scripts=['scripts/glyphpractice'],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "Environment :: Other Environment",
        "Intended Audience :: Education",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Linguistic",
        "Topic :: Other/Nonlisted Topic",
        "Natural Language :: Chinese (Traditional)",
    ],
    long_description="""\
Chinese Glyph pratice book generator
------------------------------------

According to the text to generate practice book, then
Childrens can practice chinese glyph.
"""
)
