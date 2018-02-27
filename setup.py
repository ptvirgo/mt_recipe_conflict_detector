#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

setup(
    name="mt_crafting_recipe",
    description="Minetest recipe conflict detector",
    author="Pablo Virgo",
    author_email="mailbox@pablovirgo.com",
    url="https://github.com/ptvirgo/mt_recipe_conflict_detector",
    version="0.1.1",
    packages=["mt_crafting_recipe"],
    scripts=["scripts/detect_conflicts.py"] 
)
