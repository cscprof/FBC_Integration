Welcome to the Resources/Partner Blueprint

Most everything you need to know can be found within comments, but a general guide for how we suggest you go through the folder can be found here, as well as a to-do list to pick up where we left off

Suggested First-Time Traversal

views.py - this file holds several routes for the resource and partner directory, including not only the pages themselves but the code for many of the interactive admin buttons

__init__.py - there should be almost no need to ever edit this file, but it's worth a look if you want to make sure everything checks out under the hood

models.py - this is the second most important file in this list. Unlike the other groups, ours uses SQLAlchemy to access the database. This makes coding any database queries in views.py incredibly easy, but that means that an accurate form of the database must exist in views.py. You can import tables as you would any other module in python, but a mismatch between models.py and the real database schema will break the connection. The upside is that if it is correct you will have automatic error checking on your python SQL queries within a python IDE

AddResource.xlsx - this file contains a spreadsheet template to help you add resources to the database en mass. It is slightly outdated (see to-do list), but with one small adjustment it will be ready to use or send to other orginizations so they can add their resources.

categoryReplacement.py - this independent program can be used in conjunction with the AddResource spreadsheet to make your job easier. Currently, AddResource's resourceCategory column is a dropdown in human-readable format. Unfortunatly, it needs to be in integer format before being imported into the database. This program, given the CSV file as an input, will output the same document with Resource category translated to an integer.

Full process for adding resources via the AddResource.xlsx: