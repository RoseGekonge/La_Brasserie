from module import app
from module import db
from module.admin import admin1

app = app
#Checks if the run.py file has executed directly and not imported. Comment it out when deploying.
#-------------------------------#
if __name__ == "__main__":
    app.run(debug=True)
