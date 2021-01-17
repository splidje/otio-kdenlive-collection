from setuptools import setup


setup(
    name="otio-kdenlive-collection",
    versioning="distance",
    author="https://github.com/splidje",
    package_data={
        'otio_kdenlive_collection': [
            'plugin_manifest.json',
        ],
    },
    entry_points={
        'opentimelineio.plugins': 'kdenlive-collection = otio_kdenlive_collection'
    },
    install_requires=[
        "opentimelineio>=0.12.0",
    ],
)
