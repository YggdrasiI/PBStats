from setuptools import find_packages, setup


setup(
    name="civpb_watchdog",
    version="2.0",
    author="Olaf S.",
    python_requires=">=3.7",
    packages=find_packages(),
    scripts=["bin/civpb-confirm-popup", "bin/civpb-kill"],
    entry_points="""
      [console_scripts]
      civpb-watchdog=civpb_watchdog:main
      """,
    install_requires=[
        "click",
        "click-config-file",
        "click_log",
        "scapy",
        "toml",
    ],
)
