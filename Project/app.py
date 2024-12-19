# Imports
from flask import Flask, render_template, request, redirect
import time
import mysql
import mysql.connector
import mysql.connector as sql_db
from mysql import connector
from mysql.connector import Error
from flaskext.mysql import MySQL
import main

# Databse connection
app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = "knaapj"
app.config['MYSQL_DATABASE_PASSWORD'] = "VMGp#KPmbhWQAl"
app.config['MYSQL_DATABASE_DB'] = "zknaapj"
app.config['MYSQL_DATABASE_HOST'] = "oege.ie.hva.nl"
mysql = MySQL()
mysql.init_app(app)
con = mysql.connect()
cursor = con.cursor()

# Variables
game = ""


# Index pagina
@app.route("/")
def index():
    return render_template('index.html')


# Rules pagina
@app.route("/rules")
def rules():
    return render_template('rules.html')


# Leaderboard pagina
@app.route("/leaderboard")
def leaderboard():
    cursor.execute('SELECT ROW_NUMBER() OVER (ORDER BY points DESC) AS `rank`, `username`, `points`, `country` '
                   'FROM zknaapj.player WHERE `game_type` = "Speed"')
    leaderboardS = cursor.fetchall()
    cursor.execute('SELECT ROW_NUMBER() OVER (ORDER BY points DESC) AS `rank`, `username`, `points`, `country` '
                   'FROM zknaapj.player WHERE `game_type` = "Memory"')
    leaderboardM = cursor.fetchall()
    return render_template('leaderboard.html', leaderboardS=leaderboardS, leaderboardM=leaderboardM)


# Login pagina
@app.route("/login", methods=['GET', 'POST'])
def login():
    global game

    # runt als form word gesubmit
    if request.method == 'POST':
        username = request.form['username']
        country = request.form['country']
        game = request.form['game']
        print("Game " + game)
        sql = "INSERT INTO `player` (`username`, `country`, `game_type`, `date_played`) VALUES (%s, %s, %s, CURRENT_TIMESTAMP)"
        values = (username, country, game)
        cursor.execute(sql, values)
        con.commit()
        return redirect("/loading") # Gaat naar Loading
    elif request.method == 'GET':
        return render_template('login.html')


# Load pagina
@app.route("/loading", methods=['GET'])
def loading():
    global game
    return render_template('whilePlay.html', game=game)


# Insert data voor de speed game
@app.route("/Speed")
def speedGame():
    data = main.speedGame()

    cursor.execute('SELECT `id` FROM `player` ORDER BY `id` DESC LIMIT 1')
    id = cursor.fetchone()
    id = str(''.join(map(str, id)))

    sql = 'UPDATE `player` SET `points` = %s, time_played = %s WHERE `id` = ' + id + ''
    values = (data[0], data[1])
    cursor.execute(sql, values)
    con.commit()
    return redirect("/gameover")


# Insert data voor de memory game
@app.route("/Memory")
def memoryGame():
    data = main.memoryGame()

    cursor.execute('SELECT `id` FROM `player` ORDER BY `id` DESC LIMIT 1')
    id = cursor.fetchone()
    id = str(''.join(map(str, id)))

    sql = 'UPDATE `player` SET `points` = %s, time_played = %s WHERE `id` = ' + id + ''
    values = (data[0], data[1])
    cursor.execute(sql, values)
    con.commit()
    return redirect("/gameover")


# Sensor test pagina
@app.route("/sensorTest")
def sensorTest():
    print("KAAS!")
    cursor.execute('SELECT DATE(`datum`) AS `date`, `button`, `ldr`, `rotar.`, `accel.` FROM `sensor` ORDER BY `datum` '
                   'DESC LIMIT 10')
    sensors = cursor.fetchall()
    return render_template('sensorTest.html', sensors=sensors)

# Loading scherm voor sensor test
@app.route("/loadingTest")
def loadingTest():
    return render_template('testingSensors.html')


# insert de data voor de test sensoren
@app.route("/testingSensors")
def testingSensors():
    data = main.testing()
    sql = "INSERT INTO `sensor` (`datum`, `button`, `ldr`, `rotar.`, `accel.`) VALUES (CURRENT_TIMESTAMP, %s, %s, %s, %s)"
    values = (data[0], data[1], data[2], data[3])
    cursor.execute(sql, values)
    con.commit()
    return redirect("/sensorTest")


# laat de stats pagina zien
@app.route("/stats")
def stats():
    cursor.execute('SELECT COUNT(`id`) FROM `player` WHERE `game_type` = "Speed"')
    playersS = cursor.fetchone()
    playersS = int(''.join(map(str, playersS)))
    cursor.execute('SELECT SUM(`time_played`) FROM `player` WHERE `game_type` = "Speed"')
    totalTimeS = cursor.fetchone()
    totalTimeS = int(''.join(map(str, totalTimeS)))  # seconds to minutes
    cursor.execute('SELECT AVG(`time_played`) FROM `player` WHERE `game_type` = "Speed"')
    averageTimeS = cursor.fetchone()
    averageTimeS = float(''.join(map(str, averageTimeS)))
    cursor.execute('SELECT MAX(`points`) FROM `player` WHERE `game_type` = "Speed"')
    highscoreS = cursor.fetchone()
    highscoreS = int(''.join(map(str, highscoreS)))
    cursor.execute('SELECT MAX(`time_played`) FROM `player` WHERE `game_type` = "Speed"')
    longestTimeS = cursor.fetchone()
    longestTimeS = int(''.join(map(str, longestTimeS)))
    cursor.execute('SELECT COUNT(`id`) FROM `player` WHERE `game_type` = "Memory"')
    playersM = cursor.fetchone()
    playersM = int(''.join(map(str, playersM)))
    cursor.execute('SELECT SUM(`time_played`) FROM `player` WHERE `game_type` = "Memory"')
    totalTimeM = cursor.fetchone()
    totalTimeM = int(''.join(map(str, totalTimeM)))
    cursor.execute('SELECT AVG(`time_played`) FROM `player` WHERE `game_type` = "Memory"')
    averageTimeM = cursor.fetchone()
    averageTimeM = float(''.join(map(str, averageTimeM)))
    cursor.execute('SELECT MAX(`points`) FROM `player` WHERE `game_type` = "Memory"')
    highscoreM = cursor.fetchone()
    highscoreM = int(''.join(map(str, highscoreM)))
    cursor.execute('SELECT MAX(`time_played`) FROM `player` WHERE `game_type` = "Memory"')
    longestTimeM = cursor.fetchone()
    longestTimeM = int(''.join(map(str, longestTimeM)))
    cursor.execute('SELECT AVG(`time_played`) FROM `player`')
    averageTime = cursor.fetchone()
    averageTime = float(''.join(map(str, averageTime)))
    cursor.execute('SELECT COUNT(`id`) FROM `player`')
    players = cursor.fetchone()
    players = int(''.join(map(str, players)))
    return render_template('stats.html', playersS=playersS, totalTimeS=totalTimeS, averageTimeS=averageTimeS,
                           highscoreS=highscoreS, longestTimeS=longestTimeS, playersM=playersM,
                           totalTimeM=totalTimeM, averageTimeM=averageTimeM, highscoreM=highscoreM,
                           longestTimeM=longestTimeM, averageTime=averageTime, players=players)


# Laat de gameover pagina zien
@app.route('/gameover')
def gameover():
    cursor.execute('SELECT `game_type` FROM `player` ORDER BY `id` DESC LIMIT 1')
    gameType = cursor.fetchone()
    gameType = str(''.join(map(str, gameType)))
    cursor.execute('SELECT ROW_NUMBER() OVER (ORDER BY `points` DESC) AS `rank`, `username`, `points`, `country` '
                   'FROM `player` WHERE `game_type` = "' + gameType + '"')
    topTen = cursor.fetchall()
    print(topTen)
    cursor.execute('SELECT `username` FROM `player` ORDER BY `id` DESC LIMIT 1')
    username = cursor.fetchone()
    username = str(''.join(map(str, username)))
    cursor.execute('SELECT `points` FROM `player` ORDER BY `id` DESC LIMIT 1')
    points = cursor.fetchone()
    points = str(''.join(map(str, points)))
    cursor.execute('SELECT (SUM(CASE WHEN points > ' + points + ' THEN 1 END) + 1) AS `rank` FROM player'
                                                                ' WHERE game_type = "' + gameType + '" ')
    rank = cursor.fetchone()
    rank = str(''.join(map(str, rank)))
    return render_template('gameover.html', topTen=topTen, username=username, points=points, rank=rank)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=5000)
