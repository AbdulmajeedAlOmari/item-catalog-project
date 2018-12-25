# Item Catalog Project
Develop an application that provides a list of items within a variety of categories as well as provide a user registration and authentication system. Registered users will have the ability to post, edit and delete their own items.

_This project is required for Full-Stack Nanodegree program._

It was developed by:
> Abdulmajeed Alomari

## Installation
- Download and install [Vagrant](https://www.vagrantup.com/downloads.html).
- Download and install [VirtualBox](https://www.virtualbox.org/wiki/Downloads).
- Download [FSND Virtual Machine](https://github.com/udacity/fullstack-nanodegree-vm).

## Prerequisites
- You need to use Terminal on Mac or Linux systems. On windows, you I recommend using [Git Bash](https://git-scm.com/downloads).

## Usage
Once you get the above software installed and the needed data downloaded:
1. Navigate to your **FSND Virtual Machine** folder and run the following commands:
```
cd vagrant
vagrant up
vagrant ssh
cd /vagrant
git clone https://github.com/AbdulmajeedAlOmari/item-catalog-project.git
cd item-catalog-project
```
2. You need to setup the database using **database_setup.py** by running the following command: `python database_setup.py`
3. After that, run the **seeder.py** by running the following command: `python seeder.py`
4. Then, run the server by using the following command: `python app.py`
5. Go to your browser, and visit `http://localhost:5000`
6. Enjoy :)

## API Endpoint
- `/catalog/JSON`: retrieve a list of all the categories and their items.
- `/catalog/<string:category_name>/JSON`: retrieve a list of all the items in the specified category.
- `/catalog/<string:category>/<int:item_id>/JSON`: retrieve item's details.

## References
I used the following references to help me finish this project:
- [Date and Time in SQLAlchemy](https://stackoverflow.com/questions/13370317/sqlalchemy-default-datetime)
- [Bootstrap Documentation](https://getbootstrap.com/docs/4.2/getting-started/introduction/)
- [Making a Footer](https://matthewjamestaylor.com/bottom-footer)
