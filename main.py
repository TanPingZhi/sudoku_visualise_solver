from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
import requests
from time import sleep
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

def find_empty_location(arr,l): 
    for row in range(9): 
        for col in range(9): 
            if(arr[row][col]==0): 
                l[0]=row 
                l[1]=col 
                return True
    return False
def used_in_row(arr,row,num): 
    for i in range(9): 
        if(arr[row][i] == num): 
            return True
    return False

def used_in_col(arr,col,num): 
    for i in range(9): 
        if(arr[i][col] == num): 
            return True
    return False
  
def used_in_box(arr,row,col,num): 
    for i in range(3): 
        for j in range(3): 
            if(arr[i+row][j+col] == num): 
                return True
    return False
def check_location_is_safe(arr,row,col,num): 
    return not used_in_row(arr,row,num) and not used_in_col(arr,col,num) \
and not used_in_box(arr,row - row%3,col - col%3,num) 
def solve_sudoku(arr):   
    l=[0,0] 
    if(not find_empty_location(arr,l)): 
        return True
    row=l[0] 
    col=l[1] 
    for num in range(1,10): 
        if(check_location_is_safe(arr,row,col,num)):
            inputElement = driver.find_elements_by_xpath(f"//input[@id = 'f{col}{row}']")
            arr[row][col]=num
            inputElement[0].send_keys(num)
            if(solve_sudoku(arr)): 
                return True
            arr[row][col] = 0
            inputElement[0].send_keys(Keys.BACKSPACE)
            
    return False 

solve_sudoku(board)
