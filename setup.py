#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name="Minetest Crafting Recipe",
    description="Minetest recipe conflict detector",
    author="Pablo Virgo",
    author_email="mailbox@pablovirgo.com",
    version="0.1.1",
    packages=["mt_crafting_recipe"],
    scripts=["scripts/detect_conflicts.py"] 
)
