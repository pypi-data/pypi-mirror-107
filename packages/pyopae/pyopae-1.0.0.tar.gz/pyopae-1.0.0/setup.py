import setuptools


ext_modules = setuptools.Extension("pyopae.fpga",
                                   sources=["pyopae/wrapper.c"],
                                   language="c",
                                   include_dirs=["."],
                                   library_dirs=["."],
                                   libraries=["dpdk", "numa", "fdt", "rt"]
                                  )

setuptools.setup(
    name="pyopae",
    version="1.0.0",
    author="Wei Huang",
    author_email="wei.huang@intel.com",
    description="OPAE python API",
    long_description="file: REAME.md",
    long_description_content_type="text/markdown",
    url="https://gitlab.devtools.intel.com/OPAE/pyopae",
    platforms="Linux",
    license="BSD3",
    keywords="DPDK OPAE API wrapper",
    packages=setuptools.find_packages(),
    ext_modules=[ext_modules],
    classifiers=["Programming Language :: C",
                 "License :: OSI Approved :: BSD License",
                 "Operating System :: POSIX :: Linux",
                ],
    python_requires='>=3.6',
)
