# ---- YOUR APP STARTS HERE ----
# -- Import section --
import os
from flask import Flask
from flask import render_template
from flask import request, redirect
from flask import session
from model import *
from random import choice

# -- Initialization section --
app = Flask(__name__)
my_secret = os.environ['SECRET_KEY']
app.config['SECRET_KEY'] = my_secret

# -- Routes section --
@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/begin')
def begin():
    return render_template("begin.html")

@app.route('/enter-village', methods=['GET', 'POST'])
def enterVillage():
    if (request.method == 'GET'):
        return redirect('/notFound')
    else:
        # Set session values
        # Create villains and hero player
        session['venom'] = to_json(Item("Venom", "key", None))
        session['aga'] = to_json(Player("Aga",health=50,max_health=50,defense=2))
        session['hilitai'] = to_json(Player("Hilitai",health=90,max_health=90,strength=7,defense=8))
        session['sorceress'] = to_json(Player("Sorceress Lanie",health=250,max_health=250,strength=15,defense=15,inventory=[Item("Beef Stew", "heal", 50)]))
        session['hero'] = to_json(Player())
        session['enemies'] = ['aga', 'hilitai']
        session['visit'] = 0
        session['round'] = 0

        if (request.form['gender'].lower() == "male"):
            session['title'] = "Mr."
        elif (request.form['gender'].lower() == "female"):
            session['title'] = "Ms."
        else:
            session['title'] = "Hero"
        
        hero = from_json(session['hero'])
        if (request.form['purpose'] == "vacation"):
            hero.add_item(Item("Candy Bar", "heal", 30))
        elif (request.form['purpose'] == 'business'):
            suit = Item("Suit", 'armor', 10)
            hero.add_item(suit)
            hero.add_armor(suit)
        else:
            shovel = Item("Shovel", "weapon", 15)
            hero.add_item(shovel)
            hero.add_weapon(shovel)
        hero.name = request.form['hero-name']
        session['hero_name'] = hero.name
        session['hero'] = to_json(hero)
        return render_template("enter-village.html", purpose=request.form['purpose'])

@app.route('/branch-1a', methods=['GET', 'POST'])
def branch_1a():
    if (request.method == 'GET'):
        return redirect('/notFound')
    else:
        if (request.form['answer'] == 'clara'):
            return render_template('clara.html')
        else:
            return render_template('investigate.html')

@app.route('/branch-1b', methods=['GET', 'POST'])
def branch_1b():
    if (request.method == 'GET'):
        return redirect('/notFound')
    else:
        hero = from_json(session['hero'])
        if (request.form['heal_item'] == 'apple'):
            heal_item = Item("Apple", "heal", 25)
            heal_level = "Good"
        elif (request.form['heal_item'] == 'beef'):
            heal_item = Item("Beef Stew", "heal", 50)
            heal_level = "Great"
        else:
            heal_item = Item("Ham", "heal", 100)
            heal_level = "Excellent"
        hero.add_item(heal_item)
        session['hero'] = to_json(hero)
        return render_template('investigate.html', heal_level=heal_level)
         
@app.route('/branch-2', methods=['GET', 'POST'])
def branch_2():
    if (request.method == 'GET'):
        return redirect('/notFound')
    else:
        if (request.form['answer'] == 'historian'):
            return render_template('darla.html')
        elif (request.form['answer'] == 'healer'):
            return render_template('flora.html')
        else:
            return render_template('cave.html')

@app.route('/branch-3', methods=['GET', 'POST'])
def branch_3():
    if (request.method == 'GET'):
        return redirect('/notFound')
    else:
        session['visit'] += 1
        hero = from_json(session['hero'])
        if (request.form['weapon_item'] == 'stick'):
            weapon_item = Item("Wooden Stick", "weapon", 10)
            weapon_level = "Good"
        elif (request.form['weapon_item'] == 'axe'):
            weapon_item = Item("Steel Axe", "weapon", 20)
            weapon_level = "Great"
        else:
            weapon_item = Item("Diamond Sword", "weapon", 30)
            weapon_level = "Excellent"
        hero.add_item(weapon_item)
        hero.add_weapon(weapon_item)
        session['hero'] = to_json(hero)
        return render_template('investigate.html', weapon_level=weapon_level)

@app.route('/branch-4', methods=['GET', 'POST'])
def branch_4():
    if (request.method == 'GET'):
        return redirect('/notFound')
    else:
        session['visit'] += 1
        hero = from_json(session['hero'])
        if (request.form['armor_item'] == 'steel'):
            armor_item = Item("Steel Plate", "armor", 15)
            armor_level = "Good"
        elif (request.form['armor_item'] == 'diamond'):
            armor_item = Item("Diamond Plate", "armor", 20)
            armor_level = "Great"
        else:
            armor_item = Item("Graphene Plate", "armor", 25)
            armor_level = "Excellent"
        hero.add_item(armor_item)
        hero.add_armor(armor_item)
        session['hero'] = to_json(hero)
        return render_template('investigate.html', armor_level=armor_level)

@app.route('/fight', methods=['GET', 'POST'])
def fight():
    # begin fight
    hero = from_json(session['hero'])
    aga = from_json(session['aga'])
    hilitai = from_json(session['hilitai'])
    sorceress = from_json(session['sorceress'])
    heal_name = ""
    heal = hero.check_heal()
    attack = "<h2>Get ready for battle!</h2>"
    if (heal):
        heal_name = heal.name
    if (len(request.form) > 0):
        if (request.form['fight'] == 'aga'):
            hero.attack(aga)
            attack = "<p>{} attacked Aga</p><p>Aga Health: {}%</p><br />".format(session['hero_name'], aga.health)
            if (aga.health <= 0):
                attack += "<h3>You defeated Aga.</h3>"
                session['enemies'].remove('aga')
                session['round'] += 1
        elif (request.form['fight'] == 'hilitai'):
            hero.attack(hilitai)
            attack = "<p>{} attacked Hilitai</p><p>Hilitai Health: {}%</p><br />".format(session['hero_name'], hilitai.health)
            if (hilitai.health <= 0):
                attack += "<h3>You defeated Hilitai.</h3>"
                session['enemies'].remove('hilitai')
                session['round'] += 1
        elif (request.form['fight'] == 'sorceress'):
            hero.attack(sorceress)
            attack = "<p>{} attacked Sorceress Lanie</p><p>Sorceress Lanie Health: {}%<p><br />".format(session['hero_name'], sorceress.health)
            if (sorceress.health <= 0):
                session.clear()
                return render_template('win.html')
        elif (request.form['fight'] == 'heal'):
            hero.heal_player()
            attack = "<p>You healed.</p><p>{} Health: {}%</p><br />".format(session['hero_name'], hero.health)
        elif (request.form['fight'] == 'run'):
            return render_template('run.html')
        
        if (len(session['enemies']) == 0 and session['round'] == 2):
            attack += "<p>You collected the Venom from Hilitai</p>"
            attack += "<p><strong>Sorceress Lanie:</strong> \"What is all this rukus out here?<br />"
            attack += "AGA! HILITAI! What did you do to them?\"</p><br />"
            attack += "<h2>Get ready for battle.</h2>"
            hero.add_item(from_json(session['venom']))
            session['round'] += 1
        elif (len(session['enemies']) == 0 and sorceress.health > 0):
            if (sorceress.health < 50 and len(sorceress.inventory) > 0):
                sorceress.heal_player()
                attack += "<p>Sorceress Lanie healed.</p><p>Sorceress Lanie Health: {}%</p><br />".format(sorceress.health)
            else:
                sorceress.attack(hero)
                attack += "<p>Sorceress Lanie attacked {0}</p><p>{0} Health: {1}%</p><br />".format(session['hero_name'], hero.health)
        elif (len(session['enemies']) > 0):
            enemy_name = choice(session['enemies'])
            if (enemy_name == 'aga'):
                enemy = aga
            else:
                enemy = hilitai
            enemy.attack(hero)
            attack += "<p>{0} attacked {1}</p><p>{1} Health: {2}%</p><br />".format(enemy.name, session['hero_name'], hero.health)

        if (hero.health <= 0):
            session.clear()
            return render_template("fail.html") 
    session['hero'] = to_json(hero)
    session['aga'] = to_json(aga)
    session['hilitai'] = to_json(hilitai)
    session['sorceress'] = to_json(sorceress)
    return render_template(
        'fight.html', 
        aga_hp = aga.health, 
        hilitai_hp = hilitai.health, 
        sorceress_hp = sorceress.health, 
        heal=heal_name, 
        attack=attack
        )  

@app.route('/fail')
def fail():
    session.clear()
    return render_template('fail.html')

@app.route('/notFound')
def handle404():
    session.clear()
    return render_template('404.html')

if __name__ == '__main__':
  # Run the Flask app
  app.run(
	host='0.0.0.0',
	debug=True,
	port=8080
  )