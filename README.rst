.. contents::

Installation
==============

Requirements:

 * CentOS7 or Fedora23

Installation can be done through running the included ansible script::

  ansible-playbook -i inventoryfile playbook.yml

`inventoryfile` is a text file containing your server address (refer ansible
documentation for more details)

Example `inventoryfile`::

  [server]
  primary-linode.kagesenshi.org

Default username & password:

* username: user
* password: pass

System Details
================

This project is built on top of a thin, experimental component based web 
application & dashboard framework, Pysiphae, on top of Pyramid.

Pysiphae attempts to simplify developer workflow for common/repetitive 
projects through taking care of common web application functionalities 
(authentication, theme, security) through introducing plugin based 
architecture, and code generators for boilerplates.

Ideally developer should only have to worry about their plugin rather than
the whole system.

This application is an example application built on pysiphae which includes:

* a gameoflife simulator
* and a url shortener application

for more info on pysiphae check out http://github.com/koslab/pysiphae

More documentation?
====================

Use the source Luke .. 
