# Description
This was a pet project I developed while working concurrently as part of a student activist group confronting sexual and racial harassment of students by faculty members. It was born primarily of frustration and a desire to do something. Ultimately the project was not deployed and the activism was successful. It is here on my github in the case that someone else would like to use it.

### Example Deployment
An example of this project can be found at https://reporting-example.herokuapp.com/report. After submitting example reports you can view the encrypted result by opening the web console.

### Contributors
I would like to thank Matthew Gray for his contributions to this project including html/css frameworks, and javascript hacking. I would also like to thank Gianna Passalacqua for assembling this list of resources I used as an example in this project. Thank you to both of them for their emotional support during this project.

# Setup
This section will tell you how to setup a reporting server of your own. This code is intended to be adapted into an existing webpage. The files which are most important to the purpose of reporting are `templates\report.html`, `static\javascript\submit.js`, `Server.py`(the `\report` endpoint), and the openpgp files. The other files serve as a framework for designing a webpage and as an example.
## Ingredients
You will need to fill in variables which represent the accounts, passwords, and keys from these steps at the top of `Server.py`.
### Protonmail
You will need a protonmail account for receiving and de-encrypting reports. This account will provide the public key we use to encrypt reports. Once you create your account download your public key only using the instructions at https://protonmail.com/support/knowledge-base/download-public-private-key/ and then copy the full text to `Server.py`.

### Intermediary Email Address
You will need a throw-away email address which the server will use to send emails to the protonmail account. We have found gmail accounts to be good for this purpose. Create an account and then follow the instructions at http://support.google.com/mail/answer/185833?hl=en to create an app-password. Copy the email address and this password to `Server.py`.

#### Security Concerns
The web-app password is stored in plaintext on the server so it is not recommended to use this email for any other purpose other than sending the encrypted reports. If anyone gets access to this gmail account they should only have access to encrypted reports.
### Recaptcha
`www.google.com/recaptcha` to setup a recaptcha for the reporting service. You will need to copy the site and secret keys to `Server.py`. We currently use V3 to prevent bot activity and attacks. This code may need to be tuned for your uses(within the `/report` endpoint in `Server.py`). One potential improvement would be to fall back upon recaptcha v2 in the case the user's recaptcha score is too low. Additionally if you are concerned about google tracking activity on your site switching over to v2 completely may be a better choice.

## Hosting and Installation
You will need root privileges for these steps.
### Heroku
Copy the contents of the `heroku` directory to the project directory. This directory and the `self-hosting` directory are no longer necessary. Create a heroku web app and upload your project to the repository(instructions provided on your heroku app under deploy). http://heroku.com
### Self-Hosting
Copy the contents of the `self-hosting` directory to the project directory. This directory and the `heroku` directory are no longer necessary.
#### Dependencies
The first step is to install the following dependencies on an Ubuntu 18.04 machine.
- python3-pip
- python3-dev
- build-essential
- libssl-dev
- libffi-dev
- python3-setuptools
- python3-venv

`apt install python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools python3-venv`

Install certbot
- `add-apt-repository ppa:certbot/certbot`
- `apt install python-certbot-nginx`

#### Virtual Environment
Within the project directory, create another directory called `serverenv`.
Run the following commands:
- `python3 -m venv serverenv`
- `source serverenv/bin/activate`

You will now be within your python virtual environment
Install the following packages using `pip install -r requirements.txt` (not pip3)
- wheel
- gunicorn
- flask
- requests

Copy the source code into your project directory
Deactivate the virtual environment by running deactivate

#### Server Service
Follow the instructions for the configuration files found in `config_files/README.md`
##### Gunicorn
Copy the `report.service file` to `/etc/systemd/system/report.service`. To start the service run `systemctl start report` and to start the service on every machine start run `systemctl enable report`. The current state of the server and some log output can be accessed using the systemctl status command.

##### Nginx
- Install Nginx `apt update`, `apt install nginx`
- Copy the `report-ng.conf` file to `/etc/nginx/sites-available/report-ng.conf`.
- Replace the server_name with your domain name
- Link the file to sites-enabled using: `ln -s /etc/nginx/sites-available/report-ng.conf /etc/nginx/sites-enabled`
- Test for syntax errors: `nginx -t`. If error free then restart nginx `systemctl restart nginx`. If you encounter errors you may need to modify the firewall using `ufw allow 'Nginx Full'`

#### Install Certificates
Run the following command as root
`certbox --nginx -d domain_name -d www.domain_name`

Then press 2 to redirect all requests to HTTPS.

#### Sources for These Instructions
https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https
https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-18-04

## Testing
You may test the server on your local machine by running `./Server` this will startup a flask instance running on port 5000. This instance will use the self-signed certificates found in the certs folder to perform HTTPS encryption. This implementation is very limited and should not be used in production.
