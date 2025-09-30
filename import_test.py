# Import test file - Testing various Python modules
# Standard Library Imports
print("Starting import test...")
import os
import sys
import json
import time
import datetime
import random
import math
import re
import logging
import argparse
import pathlib
import collections
import itertools
import functools

print("Standard libraries imported successfully.")

# Data Science and Machine Learning
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scipy
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

print("Data science libraries imported successfully.")

# Computer Vision and Image Processing
import cv2
import PIL
from PIL import Image, ImageDraw, ImageFont

print("Computer vision libraries imported successfully.")

# Deep Learning Frameworks
import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.transforms as transforms

print("Deep learning libraries imported successfully.")

# Web and API related
import requests
import urllib.request
import flask
from flask import Flask, request, jsonify

print("Web and deep learning libraries imported successfully.")

# File handling and data formats
import yaml
import csv
import xml.etree.ElementTree as ET
import sqlite3

# GUI and Visualization
import tkinter as tk
from tkinter import filedialog, messagebox
import plotly.graph_objects as go
import plotly.express as px

# Utility libraries
import tqdm
from tqdm import tqdm
import pickle
import zipfile
import shutil
import glob

print("All utility libraries imported successfully.")

print("All imports successful!")
print(f"Python version: {sys.version}")
print(f"Current working directory: {os.getcwd()}")
print(f"Available modules imported: {len([name for name in globals() if not name.startswith('_')])}")
