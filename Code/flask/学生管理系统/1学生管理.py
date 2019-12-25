from flask import Flask,session,render_template
import pymysql
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand