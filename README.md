# capstone-project-9900-h18b-aoligei
-

## The file [Work-Diary](Work-Diary) contains the weekly work diary maintained by each member,
## Python + Django framework,  AWS mysql by default, 

(It is recommended to open two terminals (it is recommended that both need to be executed in a virtual environment)

## I - If you not clone/have the env files, You may need to do the several commands firstly,
> ### 1. create a python virtual environment
> ```.env
> python3 -m venv <venvname>
> ```
> #####  if you don't have virtualenv, install the virtualenv firstly
> ```.env
> pip install -user virtualenv
> ```
> ##### (if in the Linux System and above command return error)
> ##### try using the command below
> ```.env
> sudo apt-get install python-virtualenv
> ```
> #### 2. activate the virtual environment
> ```.env
> source <venvname>/bin/activate
> ```
> ###  3. need to install packages 
> ```.env
> pip install -r requirements.txt
> ```
> ###  4. createsuperuser
> ```.env
> python3 manage.py createsuperuser 
> # you can ignore the email whhen creating super user
> ```



## II - If you have the env files (same to the github)， You can run the project follow commands below,

### 1. First, it needs to be executed in a virtual environment:
```.env
source venv/bin/activate 
```

### 2. Close the  virtual environment
```.env
deactivate
```


### 3. Run the  project on website
```.env
python3 manage.py runserver [port number]
(or, for example, ./manage.py runserver 9000 (default 8000) )
```

### 4. STOP run:
```.env
CRTL + C
```

#### URL address of the website test (localhost)
>```text
>1. administration system: 127.0.0.1:8000/admin
>2. User/Consumer: 127.0.0.1:8000
>```

#### Admin test account
>```text
>account name: admin72
>password: 99009900
>```
