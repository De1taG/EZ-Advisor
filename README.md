# EZ-Advisor
# Setting up the virual environment
After you pull this branch to your local repository, you will have a couple of steps to complete.

## Install locally
You will need to allow cmd to run python commands (pip, py)
* Clone the branch normally and cd to the directory(cd within CMD):
    > :)
* From the Command Prompt, set up virtualenv:
    > py -m venv EZ-env
* Activate virtualenv:
    > source EZ-env/Scripts/activate
* Install requirements:
    > pip install -r requirements.txt
* Set the FLASK_APP to backend.py
    > set FLASK_APP=PythonCode/backend.py

To run, just type:
> flask run


