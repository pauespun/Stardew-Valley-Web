<div align="center">

# Stardew Valley Web

<p align="center">A web application inspired by Stardew Valley, developed with Django and PostgreSQL. The project allows users to manage a farm, crops, inventory, and other elements related to the game experience through a web application.

This is an unofficial educational project. It is not affiliated with, endorsed by, or developed by ConcernedApe or Stardew Valley.</p>

[![License: UNLICENSED](https://img.shields.io/badge/License-UNLICENSED-blue.svg?style=flat-square)](https://opensource.org/licenses/UNLICENSED)

![Python 3.12](https://img.shields.io/badge/-Python%203.12-555?style=flat-square&logo=python) ![Django 5](https://img.shields.io/badge/-Django%205-555?style=flat-square&logo=django) ![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-555?style=flat-square&logo=postgresql) ![HTML5](https://img.shields.io/badge/-HTML5-555?style=flat-square&logo=html5) ![CSS3](https://img.shields.io/badge/-CSS3-555?style=flat-square&logo=css) ![JavaScript](https://img.shields.io/badge/-JavaScript-555?style=flat-square&logo=javascript)

</div>

---

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)

## Installation

```bash
python3 -m venv venv
source venv/bin/activate
pip install django psycopg2-binary python-decouple

```
You must create an .env file and specify your DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT


## Usage

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## Features

- User registration and authentication.
- Farm creation and management.
- Crop management.
- Fisheries management.
- Inventory management.
- Item and resource system.
- Data persistence using PostgreSQL.
- Web interface built with Django, HTML, and CSS.
---
