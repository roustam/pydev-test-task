# Test tasks

## Task1

Script "main.py" filters dictionary for same id operations and returns ones with latest timestamp.

**Requirements**: Python3 is required. 

## Task2
Script uploads image files to specified server onto '/uploads' address.

**Requirements**: Python3, installed modules from requirements.txt.

Install requirements with `pip -r requirements.txt` command.

Parameters for **Task 2** script:

--server is for setting server address i.e. 
main.py --server https://yourserveraddr.com/

--imgdir parameter configures full path for directory with images you are going to upload

When started without parameters, script uses default ones. 

       DEFAULT_DEST_URL = 'https://httpbin.org/post'
       DEFAULT_IMAGE_DIR_PATH = '/var/www/images'

Script adds "/images" to server address url automatically. 

**Example**

    python3 main.py --imgdir ~/Desktop/MyImages --server https://mywebserver.org/

**Logs**

After main.py script execution 'uploader.log' file is created within same directory. It contains events / errors that occur during script execution.
