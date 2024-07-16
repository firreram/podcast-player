from flask import Flask, render_template, request, session, redirect, flash, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
from user_model import User
from flask_session import Session
import dao

app = Flask(__name__)
app.config['SECRET_KEY'] = 'kjkjBKNJBKdjljwi/&di7767wkdj67igglNkm'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = False
Session(app)

login_manager = LoginManager()
login_manager.login_view = 'index'
login_manager.login_message = 'Accedi per visualizzare questa pagina'
login_manager.login_message_category = 'warning'
login_manager.init_app(app)

@app.route('/')
def auto_redirect():
    return redirect(url_for('index'))

@app.route('/Home',  methods=['GET', 'POST'])
def index():
    series = dao.get_series()
    if request.method == 'POST':
        
        id = request.form.get('id')    #attributo name nel form
        password = request.form.get('password')

        user = dao.get_userbyid(id)

        if not user or not check_password_hash(user['password'], password):
            flash('Credenziali non valide, riprovare', 'danger')
            return redirect(url_for('index'))
        else:
            log = User(id=user['id'], username=user['username'], password=user['password'], is_creator=user['is_creator'], userimg=user['userimg'])
            login_user(log, True)

            return redirect(url_for('index'))
    else:
        return render_template('index.html', series=series)

@app.route('/Signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        id = request.form.get('id')
        username = request.form.get('username')
        password = request.form.get('password')
        
        is_creator = request.form.get('is_creator')
        if is_creator:
            is_creator = 1
        else: 
            is_creator = 0

        userimg = request.files.get('userimg')
        
        if userimg:
            filename = secure_filename(userimg.filename)
            userimg.save('static/' + filename)

        user_in_db = dao.get_userbyid(id)
        if user_in_db:
            flash('C\'è già un utente registrato con questo nome', 'danger')
            return redirect(url_for('signup'))
        else:
            new_user = {
                "id": id,
                "username": username,
                "password": generate_password_hash(password, method='sha256'),
                "is_creator": is_creator,
                "userimg": userimg.filename
            }

            success = dao.add_user(new_user)

        if success:
            flash('Utente creato correttamente', 'success')
            return redirect(url_for('index'))
        else:
            flash('Errore nella creazione utente: riprova!', 'danger')
            return redirect(url_for('signup'))
    else:
        return render_template('signup.html')

@app.route('/Logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@login_manager.user_loader
def load_user(user_id):
    db_user = dao.get_userbyid(user_id)
    user = User(id=db_user['id'], username=db_user['username'], password=db_user['password'], is_creator=db_user['is_creator'], userimg=db_user['userimg'])

    return user  

@app.route('/Profile')
def showprofile():
    user_id = current_user.id
    series=dao.get_followed_series(user_id)
    return render_template('profilepage.html', series=series)  

@app.route('/Serie/<int:id>', methods=['GET', 'POST'])
def showserie(id):
    episode_id = request.args.get('episode_id')
    serie = dao.get_serie(id)
    episodes = dao.get_episodes(id)
    current_date = date.today()
    
    if current_user.is_authenticated:   #se utente auth. ma non seleziona episodio
        user_id = current_user.id    
        followed = dao.check_follow(user_id, id)
        
        if episode_id:                   #se utente auth. e seleziona episodio
            if request.method == 'POST':       #aggiunta commento solo se autenticato e selezionato episodio (verifica front e back end)
                newcomment = request.form.to_dict()
                dao.add_comment(user_id, newcomment, episode_id, current_date)
                return redirect(url_for('showserie', id=id, episode_id=episode_id)) 
            else:
                current_episode = dao.get_episode(episode_id)
                comments = dao.get_comments(episode_id)
                return render_template('serie.html', serie=serie, episodes=episodes, current_episode=current_episode, comments=comments, followed=followed)
        else:
            return render_template('serie.html', serie=serie, episodes=episodes, followed=followed)

    if episode_id:                       #se utente  non auth. e seleziona episodio
        current_episode = dao.get_episode(episode_id)
        comments = dao.get_comments(episode_id)
        return render_template('serie.html', serie=serie, episodes=episodes, current_episode=current_episode, comments=comments)
        
    else:                                 #se utente non auth. e non seleziona episodio
        return render_template('serie.html', serie=serie, episodes=episodes)

@app.route('/Newserie', methods=['GET', 'POST'])
def new_serie():
    if request.method == 'POST':
        if current_user.is_authenticated:
            
            serie = request.form.to_dict()

            if serie['description'] == '':
                app.logger.error('NO description')
                flash('Serie non creata: descrizione mancante', 'danger')
                return redirect(url_for('index'))

            if serie['title'] == '':
                app.logger.error('NO title')
                flash('Serie non creata: titolo mancante', 'danger')
                return redirect(url_for('index'))

            serie_img = request.files['serie_img']

            if serie_img:
                filename = secure_filename(serie_img.filename)
                serie_img.save('static/' + filename)
                serie['serie_img'] = filename

            

            user = current_user.id
            print(serie, user)

            if dao.add_serie(serie, user):
                flash('Serie creata correttamente', 'success')
            else:
                flash('Serie non creata correttamente', 'danger')
        return redirect(url_for('index'))
    else:
        return render_template('newserie.html')

@app.route('/Newepisode/<int:id>', methods=['GET', 'POST'])
def new_episode(id):
    if request.method == 'POST':
        if current_user.is_authenticated:
            
            episode = request.form.to_dict()

            if episode['description'] == '':
                app.logger.error('NO description')
                flash('Episodio non creato: descrizione mancante', 'danger')
                return redirect(url_for('showserie', id=id))

            if episode['title'] == '':
                app.logger.error('NO title')
                flash('Episodio non creato: titolo mancante', 'danger')
                return redirect(url_for('showserie', id=id))

            episode_audio = request.files['episode_audio']

            if episode_audio:
                filename = secure_filename(episode_audio.filename) #controllo sicurezza file
                episode_audio.save('static/' + filename)
                episode['episode_audio'] = filename
                
            current_date = date.today()
            
            if dao.add_episode(episode, id, current_date):
                flash('Episodio creato correttamente', 'success')
            else:
                flash('Episodio non creato correttamente', 'danger')
        return redirect(url_for('showserie', id=id))
    else:
        return render_template('newepisode.html', id=id)

@app.route('/Serie/<int:id>/Follow')
def follow(id):
    user = current_user.id
    dao.add_follower(user, id)
    return redirect(url_for('showserie', id=id))

@app.route('/Serie/<int:id>/Unfollow')
def unfollow(id):
    user = current_user.id
    dao.remove_follower(user, id)
    return redirect(url_for('showserie', id=id))

@app.route('/Serie/<int:id>/<int:eid>/Editcomment/<int:cid>', methods=['GET', 'POST'])
def editcomment(cid, id, eid):
    episode_id = eid
    upd_comment = request.form.get('commenttext')

    if upd_comment=='':   #possibile implementazione dentro serie tramite verifica del param. cid
        app.logger.error('NO text')
        return redirect(url_for('showserie', id=id, episode_id=episode_id))

    dao.update_comment(cid, upd_comment)

    return redirect(url_for('showserie', id=id, episode_id=episode_id))

@app.route('/Serie/<int:id>/<int:eid>/Deletecomment/<int:cid>')
def deletecomment(cid, id, eid):
    episode_id = eid

    dao.delete_comment(cid)

    return redirect(url_for('showserie', id=id, episode_id=episode_id))

@app.route('/Serie/<int:id>/Editserie', methods=['GET', 'POST'])
def editserie(id):
    upd_serie_title = request.form.get('serie_title')
    upd_serie_desc = request.form.get('serie_description')
    if upd_serie_title=='':
        app.logger.error('NO stitle')
        return redirect(url_for('showserie', id=id))

    if upd_serie_desc=='':
        app.logger.error('NO sdesc')
        return redirect(url_for('showserie', id=id))

    dao.update_serie(id, upd_serie_title, upd_serie_desc)
    return redirect(url_for('showserie', id=id))

@app.route('/Serie/<int:id>/Deleteserie', methods=['GET', 'POST'])
def deleteserie(id):

    dao.delete_serie(id)

    return redirect(url_for('index'))

@app.route('/Serie/<int:id>/Editepisode/<int:eid>', methods=['GET', 'POST'])
def editepisode(id, eid):
    upd_episode_title = request.form.get('episode_title')
    upd_episode_desc = request.form.get('episode_description')
    if upd_episode_title=='':
        app.logger.error('NO etitle')
        return redirect(url_for('showserie', id=id))

    if upd_episode_desc=='':
        app.logger.error('NO edesc')
        return redirect(url_for('showserie', id=id))

    dao.update_episode(eid, upd_episode_title, upd_episode_desc)
    return redirect(url_for('showserie', id=id))   

@app.route('/Serie/<int:id>/Deleteepisode/<int:eid>')
def deleteepisode(id, eid):
    
    dao.delete_episode(eid)

    return redirect(url_for('showserie', id=id))

if __name__ == "__main__":
    app.run(debug = True, host='0.0.0.0')