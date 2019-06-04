from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#LISTS AND DATA STRUCTURES TO BE USED
data_to_print = "Student Type, Roll No,   Name, Branch, SGPA, Result"

print("*************** Welcome To KNIT Result Leecher ***************")

year = ""
roll_no, sem = input("\nEnter Roll Number without last digits and sem (ex:176 5 or 1886 3): \n").split()
def checkRoll():
	global year
	if roll_no[:2] == '16':
		if sem == '3' or sem == '4':
			year = "REGULAR (2017-18) Semester 3-4"
		elif sem == '5' or sem == '6':
			year = "REGULAR (2018-19) Semester 5-6"
		elif sem == '7' or sem == '8':
			year = "REGULAR (2019-20) Semester 7-8"
	if roll_no[:2] == '17':
		if sem == '1' or sem == '2':
			year = "REGULAR (2017-18) Semester 1-2"
		elif sem == '3' or sem == '4':
			year = "REGULAR (2018-19) Semester 3-4"
		elif sem == '5' or sem == '6':
			year = "REGULAR (2019-20) Semester 5-6"
		elif sem == '7' or sem == '8':
			year = "REGULAR (2020-21) Semester 7-8"
	if roll_no[:3] == '188':
		if sem == '3' or sem == '4':
			year = "REGULAR (2018-19) Semester 3-4"
		elif sem == '5' or sem == '6':
			year = "REGULAR (2019-20) Semester 5-6"
		elif sem == '7' or sem == '8':
			year = "REGULAR (2020-21) Semester 7-8"
checkRoll()

# roll_no = input("\nEnter Roll Number without last digits :\n(For example enter 1886 if your class is of batch 2018 and IT Lateral Entry) :\n")
	
roll_no_int = 1

final_roll = int(input("Enter Last Roll Number of Class :\n"))

##OPENING URL
options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
driver.get("https://govexams.com/knit/searchresult.aspx")

result = []
roll_list = []

sum_marks = 0.0

while roll_no_int!=final_roll+1:			## ( LIMIT CAN BE PLACED HERE )
	roll_no_temp = roll_no
	##CHANGING ROLL NUMBER
	if roll_no_int<=9:
		roll_no_final = str(roll_no_temp) + '0' + str(roll_no_int)
	else:
		roll_no_final = str(roll_no_temp) + str(roll_no_int)

	print(roll_no_final + "'s Result being fetched")

	##GETTING RESULT
	try:
		data_box = driver.find_element_by_name("txtrollno")
		data_box.clear()
	except Exception as e:
		driver.close()
		options = webdriver.ChromeOptions()
		options.add_argument('--headless')
		driver = webdriver.Chrome(options=options)
		driver.get("https://govexams.com/knit/searchresult.aspx")
		data_box = driver.find_element_by_name("txtrollno")
		data_box.clear()

	# data_box.send_keys(roll_no_final, )
	data_box.send_keys(roll_no_final, Keys.ENTER)
	try:
		sem_select = Select(driver.find_element_by_id("ddlResult"))
		sem_select.select_by_visible_text(year)
		enter_button = driver.find_element_by_id("btnGo")
		enter_button.click()
		try:
			sgpa =driver.find_element_by_id("lbltotlmarksDisp")
			name = driver.find_element_by_id("lblname")
			branch = driver.find_element_by_id("lblbranch")
			result = driver.find_element_by_id("lblresults")
			Stype = driver.find_element_by_id("lblEntry")
			#print(roll_no_int,name.text, sgpa.text, end=" ")
			data_to_print += "\n"+Stype.text + "," +roll_no_final + "," +name.text+","+ branch.text+","+sgpa.text+","+result.text+","
		except Exception as e:
			sgpa = "0"
			print("could not load next page")
	except Exception as e:
		print("Could not fetch result!")		
	roll_no_int += 1

driver.close()


file_name = str(roll_no_temp) + "_" + "_"+ year + ".csv"
# data_to_print += "\nFor more work:, find me @ Github.com/RoyalEagle73\n"
with open(file_name, "w") as result:
	result.write(data_to_print)

print("Successfully generated file with name %s at script location.........."%(file_name))