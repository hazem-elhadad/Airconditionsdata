import requests
from bs4 import BeautifulSoup
import csv
import undetected_chromedriver as uc
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import re
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pandas as pd
from xlsxwriter import workbook
from selenium.webdriver.chrome.service import Service
