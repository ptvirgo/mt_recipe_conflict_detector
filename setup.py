#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name="MinetestRecipe",
    description="Minetest recipe conflict detector",
    author="Pablo Virgo",
    author_email="mailbox@pablovirgo.com",
    version="0.1.0",
    packages=["recipe"],
    scripts=["scripts/detect_conflicts.py"] 
)
