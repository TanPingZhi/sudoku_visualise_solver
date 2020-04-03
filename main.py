from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import re
import requests
from time import sleep
import sudoku_solver
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get("https://nine.websudoku.com/?")
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'c00')))

content = driver.page_source
soup = BeautifulSoup(content,"html.parser")
board = [[0 for i in range(9)] for j in range(9)]
for row in range(9):
    for col in range(9):
        raw_val = str(soup.find_all('td',attrs = {'id': f'c{col}{row}'})[0])
        if(re.search(r'value="([1-9])"',raw_val)):
            board[row][col] = int(re.search(r'value="([1-9])"',raw_val).group(1))
        else:
            board[row][col] = 0

sudoku_solver.solve_sudoku(board,driver)
