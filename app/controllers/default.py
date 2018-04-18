from flask import render_template
from app import app, db
from flask import Flask, request, redirect, url_for, session, g, flash, \
     render_template

@app.route('/')
def index():
    return render_template('layout.html')

