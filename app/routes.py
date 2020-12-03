#!/usr/bin/env python3
# -*- coding: utf8 -*-
""" HTTP route definitions """

from flask import request, render_template #allows interations with any requests. #renders our templates!
from app import app
from app.database import create, read, update, delete, scan
from datetime import datetime
from app.forms.product import ProductForm



@app.route("/")
def index():
    serv_time = datetime.now().strftime("%F %H:%M:%S") # verify server time. Used for users to verify if server is running
    tout = {}
    tout["ok"] = True
    tout["version"] = "1.0.0"
    tout["server_time"] = serv_time
    return render_template("index.html", out=tout)

@app.route("/product_form", methods=["GET", "POST"])
def product_form():
    if request.method == "POST":
        p_Name = request.form.get("name")
        p_Price = request.form.get("price")
        p_Description = request.form.get("description")
        p_Category = request.form.get("category")
        p_Quantitiy = request.form.get("quantity")
        p_Tag = request.form.get("unique_tag")

        create(p_Name, p_Price, p_Description, p_Category, p_Quantitiy, p_Tag)
        
    form = ProductForm()

    return render_template("form_example.html", form=form)

@app.route("/products")
def get_all_products():
    out = scan() 
    out["ok"] = True
    out["message"] = "Success"
    # return out
    return render_template("products.html", products=out["body"])

#method to create a new product and add to db
#you can add multiple request methods as params if you need. Not recommended.
# @app.route("/products", methods=["POST"])
# def create_product():
#     product_data = request.json
#     new_id = create(
#         product_data.get("name"), #find the key "name" and set value
#         product_data.get("price"),
#         product_data.get("description"),
#         product_data.get("category"),
#         product_data.get("quantity"),
#         product_data.get("unique_tag")
#     )
#     #this is returned as a JSON first, then converted to a python dictionary
#     return {"ok": True, "message": "Success", "new_id": new_id}

@app.route("/products/<pid>", methods=["PUT"])
def update_product(pid):
    product_data = request.json
    out = update(int(pid), product_data)
    return {"ok": out, "message": "Updated"}

#the term is a 'View Route' because it returns HTML content
@app.route('/aboutme')
#param is the user content to be added to the string output view. '%' dynamic content 
def aboutme():
    return render_template("about_me.html")

#our error 404 html page
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404
