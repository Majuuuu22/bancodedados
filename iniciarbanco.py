from flask import Flask, render_template, redirect, url_for, request, session, flash
import mysql.connector


app = Flask(__name__)

# Conexão com o banco de dados
db = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="123456",
    database="trabalho"
)

try:
    conn = mysql.connector.connect(**trabalho)
    cursor = conn.cursor()
    print("conexão estabelecida")

    SCHEMA = 'db/database.sql'

    with open(SCHEMA, 'r') as f:
        sql_scrip = f.read()

    for statement in sql_scrip.split(';'):
        if statement.strip():
            try:
                cursor.execute(statement)
            except mysql.connector.Error as e:
                print(f'erro')
    
    conn.commit()
    print('script executado')

except mysql.connector.Error as erro:
    print('erro do banco')

finally:
    if cursor is not None:
        cursor.close()
    if conn is not None:
        conn.close()