capstone-project-9900-h18b-aoligei

The file [Work-Diary](Work-Diary) contains the weekly work diary maintained by each member,
Python + Django framework,  AWS mysql by default,

(INPUT AT TERMINAL, FOR ALL 'RUN' COMMOND)
    RUN:Ssh-keygen
    RUN:Cat ~/.ssh/id_rsa.pub
    RUN:Sudo apt-get update
    RUN:Sudo apt install python3-pip


python3 manage.py runserver
 - If you not clone/have the env files, You may need to do the several commands firstly,
1. create a python virtual environment
   RUN:Sudo apt-get install python3-venv
   RUN:python3 -m venv <venvname>

2. activate the virtual environment

   RUN:source <venvname>/bin/activate

3. need to install packages

   RUN:pip3 install -r requirements.txt

4. Run the  project on website

    RUN:python3 manage.py runserver [port number]
    (default 8000)


(IF you want to create a createsuperuser
    RUN:python3 manage.py createsuperuser
you can ignore the email whhen creating super user)



Becides:

Close the  virtual environment
    RUN: deactivate

STOP run:
    RUN: CRTL + C


URL address of the website test (localhost)
    administration system: 127.0.0.1:8000/admin    or     localhost:8000/admin
    User/Consumer: 127.0.0.1:8000   or   localhost:8000


Admin test account
    account name: admin72
    password: 99009900

