import setuptools

setuptools.setup(
    name="pre-histogram",
    version="0.0.1",
    author="DigiNova",
    author_email='info@diginova.com.tr',
    description="Histogram - Preprocesing Component for NOVAVISION",
    url='https://github.com/novavision-ai/pre-histogram',
    license='MIT',
    install_requires=['sdk', 'opencv-python-headless'],

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    packages=[
        'pre.histogram',
        'pre.histogram.executors',
        'pre.histogram.models'
    ],
    package_dir={'pre.histogram': 'src'},
    python_requires=">=3.6"
)