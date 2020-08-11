from app import app
import os


if __name__ == "__main__":
	dirpath = os.getcwd()
	print("current directory is : " + dirpath)
	foldername = os.path.basename(dirpath)
	print("Directory name is : " + foldername)
	scriptpath = os.path.realpath(__file__)
	print("Script path is : " + scriptpath)
	app.run(host='0.0.0.0')
