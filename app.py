from flask import Flask, render_template, url_for, request, redirect, flash, session, jsonify
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
import yaml
import nexmo
from datetime import datetime


con=mysql.connector.connect(
		host='localhost',
		port='3306',
		user='root',
		passwd='',
		database='upravnik'
	)

mycursor = con.cursor(dictionary=True)

app = Flask(__name__)

app.secret_key='tajni_kljuc'

client=nexmo.Client(key='20803094',secret='qW4W9S6odeI0KJ4A')

# .............LOGIN RUTA, POCETAK............. #

@app.route('/', methods=['GET', 'POST'])
def Home():
	return render_template("login.html")

@app.route('/login', methods=['GET', 'POST'])
def Login():
	if request.method=='GET':
		return render_template('login.html')
	elif request.method=='POST':
		forma=request.form
		upit="SELECT *, vrstaUloge(uloga) as vrsta_uloge FROM korisnici WHERE korisnicko_ime=%s"
		vrednost=(forma['korisnicko_ime'],)
		mycursor.execute(upit, vrednost)
		korisnik=mycursor.fetchone()
		if (korisnik is not None):
			if check_password_hash(korisnik['korisnicka_lozinka'], forma['korisnicka_lozinka']) or korisnik['korisnicka_lozinka']==forma['korisnicka_lozinka']:
				if korisnik['vrsta_uloge'] == 'upravnik':
					session['ulogovani_upravnik']=str(korisnik)
					return redirect(url_for('UpravnikPocetna'))
				elif korisnik['vrsta_uloge'] == 'stanar':
					session['ulogovani_stanar']=str(korisnik)
					return redirect(url_for('StanariPocetna'))
				elif korisnik['vrsta_uloge'] == 'admin':
					session['ulogovani_admin']=str(korisnik)
					return redirect(url_for('AdminStrana'))
			else:
				flash("Pogrešna lozinka!", 'danger')
				return redirect(request.referrer)
		else:
			flash("Korisnik sa navedenim korisičkim imenom ne postoji.", 'danger')
			return redirect(request.referrer)
def Ulogovani_upravnik():
	if 'ulogovani_upravnik' in session:
		return True
	else:
		return False

def Ulogovani_stanar():
	if 'ulogovani_stanar' in session:
		return True
	else:
		return False
def Ulogovani_admin():
	if 'ulogovani_admin' in session:
		return True
	else:
		return False

# .............LOGIN RUTA, KRAJ............. #


# .............LOGOU RUTA, POCETAK............. #

@app.route('/odjavi_upravnika')
def OdjaviUpravnika():
	session.pop('ulogovani_upravnik', None)
	session.clear()
	return redirect(url_for('Login'))
	
@app.route('/odjavi_stanara')
def OdjaviStanara():
	session.pop('ulogovani_stanar', None)
	session.clear()
	return redirect(url_for('Login'))
@app.route('/odjavi_admina')
def OdjaviAdmina():
	session.pop('ulogovani_admin', None)
	session.clear()
	return redirect(url_for('Login'))

# .............LOGOU RUTA, KRAJ............. #

# .............BROJ STANARA U SVAKOM TRENUTKU, POCETAK............. #
def BrojStanara():
	mycursor.execute("SELECT count(*) AS broj_stanara FROM korisnici")
	broj_stanara=mycursor.fetchone()
	return broj_stanara['broj_stanara']
def IznosStambenogFonda():
	mycursor.execute("SELECT SUM(iznos) AS ukupno_s_f FROM placeni_racuni_fond")
	trenutni_fond=mycursor.fetchone()
	return trenutni_fond['ukupno_s_f']
def BrojSlobodnihStanova():
	mycursor.execute("SELECT DISTINCT broj_stana FROM korisnici")
	svi_stanovi_trenutno=mycursor.fetchall()
	a=[]
	for svi_stanovi_trenutno in svi_stanovi_trenutno:
		a.append(int(svi_stanovi_trenutno['broj_stana']))
	final=[]
	for x in range(1,25):
		if x in a:
			continue
		else:
			final.append(x)
	broj=len(final)
	return broj
	
	



# .............BROJ STANARA U SVAKOM TRENUTKU, KRAJ............. #

# .............ADMIN............. #
@app.route('/admin_strana', methods=['GET','POST'])
def AdminStrana():
	if Ulogovani_admin():
		mycursor.execute("SELECT * FROM korisnici WHERE uloga=1")
		upravnik=mycursor.fetchone()
		if upravnik:
			return render_template('admin_strana_izbor.html')
		else:
			return render_template('admin_strana_unos.html')
	else:
		return redirect(url_for("Login"))
@app.route('/dodaj_upravnika', methods=['GET','POST'])
def DodajUpravnika():
	if Ulogovani_admin():
			forma = request.form
			upit = "SELECT id FROM uloga WHERE uloga='upravnik'"
			mycursor.execute(upit)
			uloga = mycursor.fetchone()
			upit = "INSERT INTO korisnici (ime,prezime,broj_telefona,korisnicko_ime,korisnicka_lozinka,uloga,broj_stana) VALUES (%s, %s, %s, %s, %s,%s,%s)"
			hash_lozinka = generate_password_hash(forma['korisnicka_lozinka'])
			vrednosti = (forma['ime'],forma['prezime'],forma['broj_telefona'], forma['korisnicko_ime'],hash_lozinka,uloga['id'],forma['broj_stana'])
			mycursor.execute(upit, vrednosti)
			con.commit()
			return redirect(url_for('AdminStrana'))
	else:
		return redirect(url_for("Login"))
@app.route('/obrisi_upravnika', methods=['GET','POST'])
def ObrisiUpravnika():
	if Ulogovani_admin():
		mycursor = con.cursor()
		upit="DELETE FROM korisnici WHERE uloga=%s"
		uloga=1
		vrednost=(uloga,)
		mycursor.execute(upit, vrednost)
		con.commit()
		return redirect(url_for('AdminStrana'))
	else:
		return redirect(url_for("Login"))
@app.route('/upravnik_izmena', methods=['GET','POST'])
def UpravnikIzmena():
	if Ulogovani_admin():
		if request.method=='GET':
			mycursor.execute("SELECT * FROM korisnici WHERE uloga=1")
			upravnik = mycursor.fetchone()
			print(upravnik)
			return render_template('admin_strana_izmena.html', upravnik=upravnik)
		elif request.method=='POST':
			upit="UPDATE korisnici SET ime=%s,prezime=%s,broj_telefona=%s,korisnicko_ime=%s,korisnicka_lozinka=%s,uloga=%s,broj_stana=%s WHERE uloga=1"
			forma = request.form
			upravnik_uloga=1
			mycursor.execute("SELECT korisnicka_lozinka FROM korisnici WHERE uloga=1")
			lozinka=mycursor.fetchone()
			vrednosti=(forma['ime'],forma['prezime'],forma['broj_telefona'],forma['korisnicko_ime'],lozinka['korisnicka_lozinka'],upravnik_uloga,forma['broj_stana'])
			mycursor.execute(upit, vrednosti)
			con.commit()
			flash("Uspesno ste izmenili podatke!", 'success')
			return redirect(url_for("UpravnikIzmena"))
	else:
		return redirect(url_for("Login"))
# .............ADMIN KRAJ............. #

# .............UPRAVNIK............. #

# .............pocetna............. #
@app.route('/upravnik_pocetna', methods=['GET','POST'])
def UpravnikPocetna():
	if Ulogovani_upravnik():
		if request.method == 'GET':
			broj_stanara=BrojStanara()
			trenutni_fond=IznosStambenogFonda()
			trenutni_fond=format(trenutni_fond,".2f")
			broj_slobodnih_stanova=BrojSlobodnihStanova()
			return render_template("upravnik_pocetna.html",broj_stanara=broj_stanara,trenutni_fond=trenutni_fond,broj_slobodnih_stanova=broj_slobodnih_stanova)
	else:
		return redirect(url_for("Login"))
@app.route('/upravnik_podaci', methods=['GET','POST'])
def UpravnikPodaci():
	if Ulogovani_upravnik():
		if request.method=='GET':
			upit="SELECT * FROM korisnici WHERE id=%s"
			upravnik_sesija = session['ulogovani_upravnik']
			res=yaml.safe_load(upravnik_sesija)
			upravnik_id=res['id']
			vrednost=(upravnik_id,)
			print(vrednost)
			mycursor.execute(upit,vrednost)
			upravnik = mycursor.fetchone()
			print(upravnik)
			return render_template('upravnik_podaci.html', upravnik=upravnik)
	else:
		return redirect(url_for("Login"))
@app.route('/upravnik_podaci_izmena', methods=['GET','POST'])
def UpravnikPodaciIzmena():
	if Ulogovani_upravnik():
		if request.method=='GET':
			upit="SELECT * FROM korisnici WHERE id=%s"
			upravnik_sesija = session['ulogovani_upravnik']
			res=yaml.safe_load(upravnik_sesija)
			upravnik_id=res['id']
			vrednost=(upravnik_id,)
			print(vrednost)
			mycursor.execute(upit,vrednost)
			upravnik = mycursor.fetchone()
			print(upravnik)
			return render_template('upravnik_podaci_izmena.html', upravnik=upravnik)
		elif request.method=='POST':
			upit="UPDATE korisnici SET ime=%s,prezime=%s,broj_telefona=%s,korisnicko_ime=%s,korisnicka_lozinka=%s,uloga=%s,broj_stana=%s WHERE id=%s"
			forma = request.form
			upravnik_sesija = session['ulogovani_upravnik']
			res=yaml.safe_load(upravnik_sesija)
			upravnik_id=res['id']
			upravnik_lozinka=res['korisnicka_lozinka']
			upravnik_uloga=res['uloga']
			vrednosti=(forma['ime'],forma['prezime'],forma['broj_telefona'],forma['korisnicko_ime'],upravnik_lozinka,upravnik_uloga,forma['broj_stana'],upravnik_id)
			mycursor.execute(upit, vrednosti)
			con.commit()
			return redirect(url_for("UpravnikPocetna"))
	else:
		return redirect(url_for("Login"))

# .............racuni............. #
@app.route('/upravnik_racuni')
def UpravnikRacuni():
	return render_template("upravnik_racuni.html")
@app.route('/upravnik_racuni_struja',methods=['GET','POST'])
def UpravnikRacuniStruja():
	if Ulogovani_upravnik():
		if request.method=='GET':
			mycursor.execute("SELECT * FROM racuni_struja")
			racuni_struja=mycursor.fetchall()
			return render_template("upravnik_racuni_struja.html", racuni_struja=racuni_struja)
		elif request.method=='POST':
			forma = request.form
			upit = "INSERT INTO racuni_struja (broj_racuna,mesec_vazenja,iznos,utroseno_kwh) VALUES (%s, %s, %s, %s)"
			vrednosti = (forma['broj_racuna'],forma['mesec_vazenja'],forma['iznos_rsd'],forma['utroseno_kwh'])
			mycursor.execute(upit, vrednosti)
			con.commit()
			return redirect(url_for('UpravnikRacuniStruja'))
	else:
		return redirect(url_for("Login"))
@app.route('/upravnik_racuni_struja_izmena/<string:broj_racuna>', methods=['GET', 'POST'])
def UpravnikRacuniStrujaIzmena(broj_racuna):
	if Ulogovani_upravnik():
		if request.method == 'GET':
			    upit= "SELECT * FROM racuni_struja WHERE broj_racuna = %s"
			    vrednost = (broj_racuna,)
			    mycursor.execute(upit, vrednost)
			    struja_racun = mycursor.fetchone()
			    mesec=struja_racun['mesec_vazenja']
			    return render_template("upravnik_racuni_struja_izmena.html", struja_racun=struja_racun,mesec=mesec)
		elif request.method == 'POST':
			    upit="UPDATE racuni_struja SET broj_racuna=%s,mesec_vazenja=%s,iznos=%s,utroseno_kwh=%s WHERE broj_racuna=%s"
			    forma = request.form
			    vrednost = (forma['broj_racuna'], forma['mesec_vazenja'],forma['iznos_rsd'],forma['utroseno_kwh'],broj_racuna)
			    mycursor.execute(upit, vrednost)
			    con.commit()
			    return redirect(url_for("UpravnikRacuniStruja"))
	else:
		return redirect(url_for('Login'))
@app.route('/upravnik_racuni_struja_brisanje/<string:broj_racuna>', methods = ['GET', 'POST'])
def UpravnikRacuniStrujaBrisanje(broj_racuna):
	if Ulogovani_upravnik():
		mycursor = con.cursor()
		upit= "DELETE FROM racuni_struja WHERE broj_racuna = %s"
		vrednost = (broj_racuna,)
		mycursor.execute(upit, vrednost)
		con.commit()
		return redirect(url_for("UpravnikRacuniStruja"))
	else:
		return redirect(url_for('Login'))
@app.route('/upravnik_racuni_voda', methods = ['GET', 'POST'])
def UpravnikRacuniVoda():
	if Ulogovani_upravnik():
		if request.method=='GET':
			mycursor.execute("SELECT * FROM racuni_voda")
			racuni_voda=mycursor.fetchall()
			return render_template("upravnik_racuni_voda.html", racuni_voda=racuni_voda)
		elif request.method=='POST':
			forma = request.form
			upit = "INSERT INTO racuni_voda (broj_racuna,mesec_vazenja,iznos,utroseno_m3) VALUES (%s, %s, %s, %s)"
			vrednosti = (forma['broj_racuna'],forma['mesec_vazenja'],forma['iznos_rsd'],forma['utroseno_m3'])
			mycursor.execute(upit, vrednosti)
			con.commit()
			return redirect(url_for('UpravnikRacuniVoda'))
	else:
		return redirect(url_for("Login"))
@app.route('/upravnik_racuni_voda_izmena/<string:broj_racuna>', methods=['GET', 'POST'])
def UpravnikRacuniVodaIzmena(broj_racuna):
	if Ulogovani_upravnik():
		if request.method == 'GET':
			    upit= "SELECT * FROM racuni_voda WHERE broj_racuna = %s"
			    vrednost = (broj_racuna,)
			    mycursor.execute(upit, vrednost)
			    voda_racun = mycursor.fetchone()
			    mesec=voda_racun['mesec_vazenja']
			    return render_template("upravnik_racuni_voda_izmena.html", voda_racun=voda_racun ,mesec=mesec)
		elif request.method == 'POST':
			    upit="UPDATE racuni_voda SET broj_racuna=%s,mesec_vazenja=%s,iznos=%s,utroseno_m3=%s WHERE broj_racuna=%s"
			    forma = request.form
			    vrednost = (forma['broj_racuna'], forma['mesec_vazenja'],forma['iznos_rsd'],forma['utroseno_m3'],broj_racuna)
			    mycursor.execute(upit, vrednost)
			    con.commit()
			    return redirect(url_for("UpravnikRacuniVoda"))
	else:
		return redirect(url_for('Login'))
@app.route('/upravnik_racuni_voda_brisanje/<string:broj_racuna>', methods = ['GET', 'POST'])
def UpravnikRacuniVodaBrisanje(broj_racuna):
	if Ulogovani_upravnik():
		mycursor = con.cursor()
		upit= "DELETE FROM racuni_voda WHERE broj_racuna = %s"
		vrednost = (broj_racuna,)
		mycursor.execute(upit, vrednost)
		con.commit()
		return redirect(url_for("UpravnikRacuniVoda"))
	else:
		return redirect(url_for('Login'))
	
@app.route('/upravnik_racuni_cistac', methods = ['GET', 'POST'])
def UpravnikRacuniCistac():
	if Ulogovani_upravnik():
		if request.method=='GET':
			mycursor.execute("SELECT * FROM racuni_cistac")
			racuni_cistac=mycursor.fetchall()
			return render_template("upravnik_racuni_cistac.html", racuni_cistac=racuni_cistac)
		elif request.method=='POST':
			forma = request.form
			upit = "INSERT INTO racuni_cistac (broj_racuna,mesec_vazenja,iznos) VALUES (%s, %s, %s)"
			vrednosti = (forma['broj_racuna'],forma['mesec_vazenja'],forma['iznos_rsd'])
			mycursor.execute(upit, vrednosti)
			con.commit()
			return redirect(url_for('UpravnikRacuniCistac'))
	else:
		return redirect(url_for("Login"))
@app.route('/upravnik_racuni_cistac_izmena/<string:broj_racuna>', methods=['GET', 'POST'])
def UpravnikRacuniCistacIzmena(broj_racuna):
	if Ulogovani_upravnik():
		if request.method == 'GET':
			    upit= "SELECT * FROM racuni_cistac WHERE broj_racuna = %s"
			    vrednost = (broj_racuna,)
			    mycursor.execute(upit, vrednost)
			    cistac_racun = mycursor.fetchone()
			    mesec=cistac_racun['mesec_vazenja']
			    return render_template("upravnik_racuni_cistac_izmena.html", cistac_racun=cistac_racun ,mesec=mesec)
		elif request.method == 'POST':
			    upit="UPDATE racuni_cistac SET broj_racuna=%s,mesec_vazenja=%s,iznos=%s WHERE broj_racuna=%s"
			    forma = request.form
			    vrednost = (forma['broj_racuna'], forma['mesec_vazenja'],forma['iznos_rsd'],broj_racuna)
			    mycursor.execute(upit, vrednost)
			    con.commit()
			    return redirect(url_for("UpravnikRacuniCistac"))
	else:
		return redirect(url_for('Login'))
@app.route('/upravnik_racuni_cistac_brisanje/<string:broj_racuna>', methods = ['GET', 'POST'])
def UpravnikRacuniCistacBrisanje(broj_racuna):
	if Ulogovani_upravnik():
		mycursor = con.cursor()
		upit= "DELETE FROM racuni_cistac WHERE broj_racuna = %s"
		vrednost = (broj_racuna,)
		mycursor.execute(upit, vrednost)
		con.commit()
		return redirect(url_for("UpravnikRacuniCistac"))
	else:
		return redirect(url_for('Login'))	

@app.route('/upravnik_racuni_fond', methods = ['GET', 'POST'])
def UpravnikRacuniFond():
	if Ulogovani_upravnik():
		if request.method=='GET':
			mycursor.execute("SELECT * FROM racuni_fond")
			racuni_fond=mycursor.fetchall()
			return render_template("upravnik_racuni_fond.html", racuni_fond=racuni_fond)
		elif request.method=='POST':
			forma = request.form
			upit = "INSERT INTO racuni_fond (broj_racuna,mesec_vazenja,iznos) VALUES (%s, %s, %s)"
			vrednosti = (forma['broj_racuna'],forma['mesec_vazenja'],forma['iznos_rsd'])
			mycursor.execute(upit, vrednosti)
			con.commit()
			return redirect(url_for('UpravnikRacuniFond'))
	else:
		return redirect(url_for("Login"))
@app.route('/upravnik_racuni_fond_izmena/<string:broj_racuna>', methods=['GET', 'POST'])
def UpravnikRacuniFondIzmena(broj_racuna):
	if Ulogovani_upravnik():
		if request.method == 'GET':
			    upit= "SELECT * FROM racuni_fond WHERE broj_racuna = %s"
			    vrednost = (broj_racuna,)
			    mycursor.execute(upit, vrednost)
			    fond_racun = mycursor.fetchone()
			    mesec=fond_racun['mesec_vazenja']
			    return render_template("upravnik_racuni_fond_izmena.html", fond_racun=fond_racun ,mesec=mesec)
		elif request.method == 'POST':
			    upit="UPDATE racuni_fond SET broj_racuna=%s,mesec_vazenja=%s,iznos=%s WHERE broj_racuna=%s"
			    forma = request.form
			    vrednost = (forma['broj_racuna'], forma['mesec_vazenja'],forma['iznos_rsd'],broj_racuna)
			    mycursor.execute(upit, vrednost)
			    con.commit()
			    return redirect(url_for("UpravnikRacuniFond"))
	else:
		return redirect(url_for('Login'))
@app.route('/upravnik_racuni_fond_brisanje/<string:broj_racuna>', methods = ['GET', 'POST'])
def UpravnikRacuniFondBrisanje(broj_racuna):
	if Ulogovani_upravnik():
		mycursor = con.cursor()
		upit= "DELETE FROM racuni_fond WHERE broj_racuna = %s"
		vrednost = (broj_racuna,)
		mycursor.execute(upit, vrednost)
		con.commit()
		return redirect(url_for("UpravnikRacuniFond"))
	else:
		return redirect(url_for('Login'))
@app.route('/upravnik_placeni_racuni_struja', methods = ['GET', 'POST'])
def UpravnikPlaceniRacuniStruja():
	if Ulogovani_upravnik():
		mycursor.execute("SELECT * FROM placeni_racuni_struja")
		placeni_racuni=mycursor.fetchall()
		return render_template("upravnik_placeni_racuni_struja.html", placeni_racuni=placeni_racuni)
	else:
		return redirect(url_for('Login'))
@app.route('/upravnik_placeni_racuni_voda', methods = ['GET', 'POST'])
def UpravnikPlaceniRacuniVoda():
	if Ulogovani_upravnik():
		mycursor.execute("SELECT * FROM placeni_racuni_voda")
		placeni_racuni=mycursor.fetchall()
		return render_template("upravnik_placeni_racuni_voda.html", placeni_racuni=placeni_racuni)
	else:
		return redirect(url_for('Login'))
@app.route('/upravnik_placeni_racuni_cistac', methods = ['GET', 'POST'])
def UpravnikPlaceniRacuniCistac():
	if Ulogovani_upravnik():
		mycursor.execute("SELECT * FROM placeni_racuni_cistac")
		placeni_racuni=mycursor.fetchall()
		return render_template("upravnik_placeni_racuni_cistac.html", placeni_racuni=placeni_racuni)
	else:
		return redirect(url_for('Login'))
@app.route('/upravnik_placeni_racuni_fond', methods = ['GET', 'POST'])
def UpravnikPlaceniRacuniFond():
	if Ulogovani_upravnik():
		mycursor.execute("SELECT * FROM placeni_racuni_fond")
		placeni_racuni=mycursor.fetchall()
		return render_template("upravnik_placeni_racuni_fond.html", placeni_racuni=placeni_racuni)
	else:
		return redirect(url_for('Login'))
# .............stanari............. #
@app.route('/upravnik_stanari/<string:broj_stana>', methods=['GET','POST'])
def UpravnikStanari(broj_stana):
	if Ulogovani_upravnik():
			if broj_stana and broj_stana!='-':
				upit="SELECT * FROM korisnici WHERE broj_stana=%s"
				vrednost=(broj_stana,)
				broj=broj_stana
				mycursor.execute(upit,vrednost)
				stanari = mycursor.fetchall()
				con.commit()
				if stanari:
					return render_template("upravnik_stanari.html", stanari=stanari, broj=broj)
				else:
					flash('Ovaj stan je trenutno prazan!', 'danger')
					return render_template("upravnik_stanari.html", broj=broj)
			else:
				return render_template("upravnik_stanari.html")
	else:
		return redirect(url_for("Login"))
@app.route('/upravnik_novi_stanar', methods=['GET','POST'])
def UpravnikNoviStanar():
	if Ulogovani_upravnik():
		if request.method=='GET':
			return render_template('upravnik_novi_stanar_forma.html')
		elif request.method=='POST':
			upit1 ="SELECT id FROM uloga WHERE uloga='stanar'"
			mycursor.execute(upit1)
			uloga=mycursor.fetchone()
			forma=request.form
			broj_stana=(forma['broj_stana'])
			upit = "INSERT INTO korisnici (ime,prezime,broj_telefona,korisnicko_ime,korisnicka_lozinka,uloga,broj_stana) VALUES (%s, %s, %s, %s, %s,%s,%s)"
			hash_lozinka=generate_password_hash(forma['korisnicka_lozinka'])
			vrednost=(forma['ime'],forma['prezime'],forma['broj_telefona'],forma['korisnicko_ime'],hash_lozinka,uloga['id'],broj_stana)
			mycursor.execute(upit,vrednost)
			con.commit()
			flash("Uspesno ste dodali novog stanara zgrade!",'success')
			return redirect(url_for('UpravnikNoviStanar'))
	else:
		return redirect(url_for('Login'))
@app.route('/upravnik_stanari_izmena/<string:id_stanara>', methods=['GET', 'POST'])
def UpravnikStanarIzmena(id_stanara):
	if Ulogovani_upravnik():
		if request.method == 'GET':
			    upit= "SELECT * FROM korisnici WHERE id = %s"
			    vrednost = (id_stanara,)
			    mycursor.execute(upit, vrednost)
			    stanari = mycursor.fetchone()
			    return render_template("upravnik_stanari_izmena.html", stanari=stanari)
		elif request.method == 'POST':
			    upit1="SELECT broj_stana,korisnicka_lozinka,uloga,broj_stana FROM korisnici WHERE id=%s"
			    vrednosti=(id_stanara,)
			    mycursor.execute(upit1,vrednosti)
			    izabrani_stanar=mycursor.fetchone()
			    korisnicka_lozinka=izabrani_stanar['korisnicka_lozinka']
			    uloga=izabrani_stanar['uloga']
			    broj_stana=izabrani_stanar['broj_stana']
			    print(korisnicka_lozinka,uloga,broj_stana)
			    upit="UPDATE korisnici SET ime=%s,prezime=%s,broj_telefona=%s,korisnicko_ime=%s,korisnicka_lozinka=%s,uloga=%s,broj_stana=%s WHERE id=%s"
			    forma = request.form
			    vrednost = (forma['ime'], forma['prezime'],forma['broj_telefona'],forma['korisnicko_ime'],korisnicka_lozinka,uloga,broj_stana,id_stanara)
			    mycursor.execute(upit, vrednost)
			    con.commit()
			    return redirect(url_for("UpravnikStanari",broj_stana=izabrani_stanar['broj_stana']))
	else:
		return redirect(url_for('Login'))

@app.route('/upravnik_stanari_brisanje/<string:id_stanara>', methods = ['GET', 'POST'])
def UpravnikStanarBrisanje(id_stanara):
	if Ulogovani_upravnik():
		mycursor = con.cursor()
		upit1="SELECT broj_stana FROM korisnici WHERE id=%s"
		vrednosti=(id_stanara,)
		mycursor.execute(upit1,vrednosti)
		broj=mycursor.fetchone()
		print(broj[0])

		upit= "DELETE FROM korisnici WHERE id = %s"
		vrednost = (id_stanara,)
		mycursor.execute(upit, vrednost)

		con.commit()
		return redirect(url_for("UpravnikStanari",broj_stana=broj[0]))
	else:
		return redirect(url_for('Login'))
# .............obavestenja............. #
@app.route('/upravnik_obavestenja', methods = ['GET', 'POST'])
def UpravnikObavestenja():
	return render_template("upravnik_obavestenja.html")

@app.route('/upravnik_obavestenja_nova', methods = ['GET', 'POST'])
def UpravnikObavestenjaNova():
	if Ulogovani_upravnik():
		if request.method=='GET':
			mycursor.execute("SELECT * FROM korisnici WHERE uloga!=1 ORDER BY ime ASC")
			korisnici=mycursor.fetchall()
			return render_template("upravnik_obavestenja_nova.html", korisnici=korisnici)
		elif request.method=='POST':
			forma=request.form
			upit1="SELECT * FROM korisnici WHERE id=%s"
			vrednost=(forma['primalac'],)
			mycursor.execute(upit1,vrednost)
			rezultat=mycursor.fetchone()
			primalac=rezultat['ime']+' '+rezultat['prezime']
			broj_primaoca=rezultat['broj_telefona']
			upravnik_sesija = session['ulogovani_upravnik']
			res=yaml.safe_load(upravnik_sesija)
			broj_posiljaoca=res['broj_telefona']
			posiljalac=res['ime']+' '+res['prezime']
			datum=datetime.now().date().strftime("%d/%m/%Y")
			print(datum)
			vreme=datetime.now().time().strftime("%H:%M:%S")
			print(vreme)
			upit = "INSERT INTO obavestenja (posiljalac,broj_posiljaoca,primalac,broj_primaoca,datum,vreme,sadrzaj) VALUES (%s, %s, %s, %s, %s,%s,%s)"
			vrednosti=(posiljalac,broj_posiljaoca,primalac,broj_primaoca,datum,vreme,forma['sadrzaj'])
			mycursor.execute(upit,vrednosti)
			to_client_number='381'+broj_primaoca[1:]
			client.send_message({'from':'Upravnik15','to':to_client_number,'text':'Postovani imate obavestenje u aplikaciji upravnik! Jovan Nejkovic'})
			con.commit()
			flash("Poruka je uspesno poslata!",'success')
			return redirect(url_for("UpravnikObavestenjaNova"))
	else:
		return redirect(url_for('Login'))

@app.route('/upravnik_obavestenja_inbox', methods = ['GET', 'POST'])
def UpravnikObavestenjaInbox():
	if Ulogovani_upravnik():
		if request.method=='GET':
			mycursor.execute("SELECT * FROM obavestenja WHERE primalac='Jovan Nejkovic'")
			obavestenja=mycursor.fetchall()
			return render_template("upravnik_obavestenja_inbox.html", obavestenja=obavestenja)
	
	else:
		return redirect(url_for('Login'))
@app.route('/upravnik_obavestenja_brisanje/<string:id_obavestenja>', methods = ['GET', 'POST'])
def UpravnikObavestenjaBrisanje(id_obavestenja):
	if Ulogovani_upravnik():
		mycursor = con.cursor()
		upit= "DELETE FROM obavestenja WHERE id_obavestenja = %s"
		vrednost = (id_obavestenja,)
		mycursor.execute(upit, vrednost)
		con.commit()
		return redirect(url_for("UpravnikObavestenjaInbox"))
	else:
		return redirect(url_for('Login'))
	
# .............UPRAVNIK KRAJ............. #


# .............STANARI............. #

# .............pocetna............. #
@app.route('/stanari_pocetna',methods = ['GET', 'POST'])
def StanariPocetna():
	if Ulogovani_stanar():
		broj_stanara=BrojStanara()
		trenutni_fond=IznosStambenogFonda()
		trenutni_fond=format(trenutni_fond,".2f")
		broj_slobodnih_stanova=BrojSlobodnihStanova()
		return render_template("stanari_pocetna.html",broj_stanara=broj_stanara,trenutni_fond=trenutni_fond,broj_slobodnih_stanova=broj_slobodnih_stanova)
	else:
		return redirect(url_for('Login'))
@app.route('/stanari_podaci',methods = ['GET', 'POST'])
def StanariPodaci():
	if Ulogovani_stanar():
		if request.method=='GET':
			upit="SELECT *,vrstaUloge(uloga) as ime_uloge FROM korisnici WHERE id=%s"
			stanari_sesija = session['ulogovani_stanar']
			res=yaml.safe_load(stanari_sesija)
			stanari_id=res['id']
			vrednost=(stanari_id,)
			print(vrednost)
			mycursor.execute(upit,vrednost)
			stanari = mycursor.fetchone()
			print(stanari)
			return render_template('stanari_podaci.html', stanari=stanari)
	else:
		return redirect(url_for("Login"))
@app.route('/stanari_podaci_izmena',methods = ['GET', 'POST'])
def StanariPodaciIzmena():
	if Ulogovani_upravnik():
		if request.method=='GET':
			upit="SELECT *,vrstaUloge(uloga) as ime_uloge FROM korisnici WHERE id=%s"
			stanari_sesija = session['ulogovani_stanar']
			res=yaml.safe_load(stanari_sesija)
			stanari_id=res['id']
			vrednost=(stanari_id,)
			print(vrednost)
			mycursor.execute(upit,vrednost)
			stanari = mycursor.fetchone()
			print(stanari)
			return render_template('stanari_podaci_izmena.html', stanari=stanari)
		elif request.method=='POST':
			upit="UPDATE korisnici SET ime=%s,prezime=%s,broj_telefona=%s,korisnicko_ime=%s,korisnicka_lozinka=%s,uloga=%s,broj_stana=%s WHERE id=%s"
			forma = request.form
			stanari_sesija = session['ulogovani_stanar']
			res=yaml.safe_load(stanari_sesija)
			stanari_id=res['id']
			stanari_lozinka=res['korisnicka_lozinka']
			stanari_uloga=res['uloga']
			vrednosti=(forma['ime'],forma['prezime'],forma['broj_telefona'],forma['korisnicko_ime'],stanari_lozinka,stanari_uloga,forma['broj_stana'],stanari_id)
			mycursor.execute(upit, vrednosti)
			con.commit()
			return redirect(url_for("StanariPocetna"))
	else:
		return redirect(url_for("Login"))
# .............racuni............. #
@app.route('/stanari_racuni',methods = ['GET', 'POST'])
def StanariRacuni():
	if Ulogovani_stanar():
		return render_template("stanari_racuni.html")
	else:
		return redirect(url_for('Login'))
@app.route('/stanari_racuni_struja',methods = ['GET', 'POST'])
def StanariRacuniStruja():
	if Ulogovani_stanar():
		ukupan_broj_stanara=BrojStanara()

		stanar_sesija = session['ulogovani_stanar']
		res=yaml.safe_load(stanar_sesija)
		broj_stana=res['broj_stana']

		selectuj_za_prikaz="SELECT * FROM racuni_struja WHERE broj_racuna NOT IN (SELECT broj_racuna FROM placeni_racuni_struja WHERE broj_stana=%s)"
		vrednost_stana=(broj_stana,)
		mycursor.execute(selectuj_za_prikaz,vrednost_stana)
		neplaceni_r_s=mycursor.fetchall()
		
		broj_stanara_upit=("SELECT COUNT(*) AS broj_stanara FROM korisnici WHERE broj_stana=%s")
		vrednosti=(broj_stana,)
		mycursor.execute(broj_stanara_upit,vrednosti)
		broj_stanara=mycursor.fetchone()
		pomocni_broj_stanara=broj_stanara['broj_stanara']

		racuni_za_struju=[]
		for neplaceni_r_s in neplaceni_r_s:
			neplaceni_r_s['iznos']=(float(neplaceni_r_s['iznos'])/int(ukupan_broj_stanara))*pomocni_broj_stanara
			neplaceni_r_s['iznos']=format(neplaceni_r_s['iznos'], ".2f")
			racuni_za_struju.append(neplaceni_r_s)

		return render_template("stanari_racuni_struja.html", racuni_za_struju=racuni_za_struju)
	else:
		return redirect(url_for('Login'))

@app.route('/stanari_racuni_struja_plati/<string:id_racuna>',methods = ['GET', 'POST'])
def StanariRacuniStrujaPlati(id_racuna):
	if Ulogovani_stanar():
		if request.method=='GET':
			ukupan_broj_stanara=BrojStanara()

			upit="SELECT * FROM racuni_struja WHERE id=%s"
			vrednost=(id_racuna,)
			mycursor.execute(upit,vrednost)
			racuni_struja_plati_glavni=mycursor.fetchone()
			
			stanar_sesija = session['ulogovani_stanar']
			res=yaml.safe_load(stanar_sesija)
			broj_stana=res['broj_stana']

			broj_stanara_upit=("SELECT COUNT(*) AS broj_stanara FROM korisnici WHERE broj_stana=%s")
			vrednost=(broj_stana,)
			mycursor.execute(broj_stanara_upit,vrednost)
			broj_stanara=mycursor.fetchone()
			pomocni_broj_stanara=broj_stanara['broj_stanara']

			racuni_struja_plati_glavni['iznos']=(float(racuni_struja_plati_glavni['iznos'])/int(ukupan_broj_stanara))*pomocni_broj_stanara
			racuni_struja_plati_glavni['iznos']=format(racuni_struja_plati_glavni['iznos'], ".2f")
			racuni_struja_plati=racuni_struja_plati_glavni
			
			mesec=racuni_struja_plati['mesec_vazenja']
			return render_template("stanari_racuni_struja_plati.html", racuni_struja_plati=racuni_struja_plati,mesec=mesec)		
	else:
		return redirect(url_for('Login'))
@app.route('/uplatnica_struja',methods=['GET','POST'])
def UplatnicaStruja():
	if Ulogovani_stanar():
		if request.method=='POST':
			mycursor.execute("SELECT broj_telefona FROM korisnici WHERE uloga=1")
			broj_telefona_up=mycursor.fetchone()
			br_tel_upravnika=broj_telefona_up['broj_telefona']
			print(br_tel_upravnika)
			forma=request.form
			stanar_sesija = session['ulogovani_stanar']
			res=yaml.safe_load(stanar_sesija)
			broj_tel_stanara=res['broj_telefona']
			datum=datetime.now().date().strftime("%d/%m/%Y")
			vreme=datetime.now().time().strftime("%H:%M:%S")
			broj_racuna=forma['broj_racuna']
			iznos=forma['iznos_rsd']
			broj_stana=res['broj_stana']
			korisnicko_ime=res['korisnicko_ime']
			mesec_vazenja=forma['mesec_vazenja']
			upit="INSERT INTO placeni_racuni_struja (datum,vreme,broj_racuna,iznos,mesec_vazenja,broj_stana,korisnicko_ime) VALUES (%s, %s, %s,%s,%s, %s, %s)"
			vrednosti=(datum,vreme,broj_racuna,iznos,mesec_vazenja,broj_stana,korisnicko_ime)
			mycursor.execute(upit,vrednosti)
			to_client_number='381'+broj_tel_stanara[1:]
			poruka='Uspesno ste platili racun za struju broj - '+broj_racuna+' u iznosu od '+iznos+' dinara.'
			client.send_message({'from':'Upravnik15','to':to_client_number,'text':poruka})
			to_client_number='381'+br_tel_upravnika[1:]
			poruka='Stanar sa korisnickim imenom - '+korisnicko_ime+' je platio racun za struju u iznosu od '+iznos+' dinara.'
			client.send_message({'from':'Upravnik15','to':to_client_number,'text':poruka})
			con.commit()
			return redirect(url_for("StanariRacuniStruja"))
	else:
		return redirect('Login')
@app.route('/stanari_placeni_racuni_struja', methods = ['GET', 'POST'])
def StanariPlaceniRacuniStruja():
	if Ulogovani_stanar():
		stanar_sesija = session['ulogovani_stanar']
		res=yaml.safe_load(stanar_sesija)
		broj_stana=res['broj_stana']
		upit="SELECT * FROM placeni_racuni_struja WHERE broj_stana=%s"
		vrednost=(broj_stana,)
		mycursor.execute(upit,vrednost)
		placeni_racuni=mycursor.fetchall()
		return render_template("stanari_placeni_racuni_struja.html", placeni_racuni=placeni_racuni)
	else:
		return redirect(url_for('Login'))


@app.route('/stanari_racuni_voda',methods = ['GET', 'POST'])
def StanariRacuniVoda():
	if Ulogovani_stanar():
		ukupan_broj_stanara=BrojStanara()

		stanar_sesija = session['ulogovani_stanar']
		res=yaml.safe_load(stanar_sesija)
		broj_stana=res['broj_stana']

		selectuj_za_prikaz="SELECT * FROM racuni_voda WHERE broj_racuna NOT IN (SELECT broj_racuna FROM placeni_racuni_voda WHERE broj_stana=%s)"
		vrednost_stana=(broj_stana,)
		mycursor.execute(selectuj_za_prikaz,vrednost_stana)
		neplaceni_r_v=mycursor.fetchall()
		
		broj_stanara_upit=("SELECT COUNT(*) AS broj_stanara FROM korisnici WHERE broj_stana=%s")
		vrednosti=(broj_stana,)
		mycursor.execute(broj_stanara_upit,vrednosti)
		broj_stanara=mycursor.fetchone()
		pomocni_broj_stanara=broj_stanara['broj_stanara']

		racuni_za_vodu=[]
		for neplaceni_r_v in neplaceni_r_v:
			neplaceni_r_v['iznos']=(float(neplaceni_r_v['iznos'])/int(ukupan_broj_stanara))*pomocni_broj_stanara
			neplaceni_r_v['iznos']=format(neplaceni_r_v['iznos'], ".2f")
			racuni_za_vodu.append(neplaceni_r_v)

		return render_template("stanari_racuni_voda.html", racuni_za_vodu=racuni_za_vodu)
	else:
		return redirect(url_for('Login'))
@app.route('/stanari_racuni_voda_plati/<string:id_racuna>',methods = ['GET', 'POST'])
def StanariRacuniVodaPlati(id_racuna):
	if Ulogovani_stanar():
		if request.method=='GET':
			ukupan_broj_stanara=BrojStanara()

			upit="SELECT * FROM racuni_voda WHERE id=%s"
			vrednost=(id_racuna,)
			mycursor.execute(upit,vrednost)
			racuni_voda_plati_glavni=mycursor.fetchone()
			
			stanar_sesija = session['ulogovani_stanar']
			res=yaml.safe_load(stanar_sesija)
			broj_stana=res['broj_stana']

			broj_stanara_upit=("SELECT COUNT(*) AS broj_stanara FROM korisnici WHERE broj_stana=%s")
			vrednost=(broj_stana,)
			mycursor.execute(broj_stanara_upit,vrednost)
			broj_stanara=mycursor.fetchone()
			pomocni_broj_stanara=broj_stanara['broj_stanara']

			racuni_voda_plati_glavni['iznos']=(float(racuni_voda_plati_glavni['iznos'])/int(ukupan_broj_stanara))*pomocni_broj_stanara
			racuni_voda_plati_glavni['iznos']=format(racuni_voda_plati_glavni['iznos'], ".2f")
			racuni_voda_plati=racuni_voda_plati_glavni
			
			mesec=racuni_voda_plati['mesec_vazenja']

			return render_template("stanari_racuni_voda_plati.html", racuni_voda_plati=racuni_voda_plati, mesec=mesec)		
	else:
		return redirect(url_for('Login'))

@app.route('/uplatnica_voda',methods=['GET','POST'])
def UplatnicaVoda():
	if Ulogovani_stanar():
		if request.method=='POST':
			mycursor.execute("SELECT broj_telefona FROM korisnici WHERE uloga=1")
			broj_telefona_up=mycursor.fetchone()
			br_tel_upravnika=broj_telefona_up['broj_telefona']

			forma=request.form
			stanar_sesija = session['ulogovani_stanar']
			res=yaml.safe_load(stanar_sesija)
			broj_tel_stanara=res['broj_telefona']
			datum=datetime.now().date().strftime("%d/%m/%Y")
			vreme=datetime.now().time().strftime("%H:%M:%S")
			broj_racuna=forma['broj_racuna']
			iznos=forma['iznos_rsd']
			broj_stana=res['broj_stana']
			korisnicko_ime=res['korisnicko_ime']
			mesec_vazenja=forma['mesec_vazenja']

			upit="INSERT INTO placeni_racuni_voda (datum,vreme,broj_racuna,iznos,mesec_vazenja,broj_stana,korisnicko_ime) VALUES (%s, %s, %s,%s,%s, %s, %s)"
			vrednosti=(datum,vreme,broj_racuna,iznos,mesec_vazenja,broj_stana,korisnicko_ime)
			mycursor.execute(upit,vrednosti)

			to_client_number='381'+broj_tel_stanara[1:]
			poruka='Uspesno ste platili racun za vodu broj - '+broj_racuna+' u iznosu od '+iznos+' dinara.'
			client.send_message({'from':'Upravnik15','to':to_client_number,'text':poruka})

			to_client_number='381'+br_tel_upravnika[1:]
			poruka='Stanar sa korisnickim imenom - '+korisnicko_ime+' je platio racun za vodu u iznosu od '+iznos+' dinara.'
			client.send_message({'from':'Upravnik15','to':to_client_number,'text':poruka})

			con.commit()
			return redirect(url_for("StanariRacuniVoda"))
	else:
		return redirect('Login')
@app.route('/stanari_placeni_racuni_voda', methods = ['GET', 'POST'])
def StanariPlaceniRacuniVoda():
	if Ulogovani_stanar():
		stanar_sesija = session['ulogovani_stanar']
		res=yaml.safe_load(stanar_sesija)
		broj_stana=res['broj_stana']
		upit="SELECT * FROM placeni_racuni_voda WHERE broj_stana=%s"
		vrednost=(broj_stana,)
		mycursor.execute(upit,vrednost)
		placeni_racuni=mycursor.fetchall()
		return render_template("stanari_placeni_racuni_voda.html", placeni_racuni=placeni_racuni)
	else:
		return redirect(url_for('Login'))
@app.route('/stanari_racuni_cistac',methods = ['GET', 'POST'])
def StanariRacuniCistac():
	if Ulogovani_stanar():
		ukupan_broj_stanara=BrojStanara()

		stanar_sesija = session['ulogovani_stanar']
		res=yaml.safe_load(stanar_sesija)
		broj_stana=res['broj_stana']

		selectuj_za_prikaz="SELECT * FROM racuni_cistac WHERE broj_racuna NOT IN (SELECT broj_racuna FROM placeni_racuni_cistac WHERE broj_stana=%s)"
		vrednost_stana=(broj_stana,)
		mycursor.execute(selectuj_za_prikaz,vrednost_stana)
		neplaceni_r_c=mycursor.fetchall()
		
		broj_stanara_upit=("SELECT COUNT(*) AS broj_stanara FROM korisnici WHERE broj_stana=%s")
		vrednosti=(broj_stana,)
		mycursor.execute(broj_stanara_upit,vrednosti)
		broj_stanara=mycursor.fetchone()
		pomocni_broj_stanara=broj_stanara['broj_stanara']

		racuni_za_cistaca=[]
		for neplaceni_r_c in neplaceni_r_c:
			neplaceni_r_c['iznos']=(float(neplaceni_r_c['iznos'])/int(ukupan_broj_stanara))*pomocni_broj_stanara
			neplaceni_r_c['iznos']=format(neplaceni_r_c['iznos'], ".2f")
			racuni_za_cistaca.append(neplaceni_r_c)

		return render_template("stanari_racuni_cistac.html", racuni_za_cistaca=racuni_za_cistaca)

	else:
		return redirect(url_for('Login'))
@app.route('/stanari_racuni_cistac_plati/<string:id_racuna>',methods = ['GET', 'POST'])
def StanariRacuniCistacPlati(id_racuna):
	if Ulogovani_stanar():
		if request.method=='GET':
			ukupan_broj_stanara=BrojStanara()

			upit="SELECT * FROM racuni_cistac WHERE id=%s"
			vrednost=(id_racuna,)
			mycursor.execute(upit,vrednost)
			racuni_cistac_plati_glavni=mycursor.fetchone()
			
			stanar_sesija = session['ulogovani_stanar']
			res=yaml.safe_load(stanar_sesija)
			broj_stana=res['broj_stana']

			broj_stanara_upit=("SELECT COUNT(*) AS broj_stanara FROM korisnici WHERE broj_stana=%s")
			vrednost=(broj_stana,)
			mycursor.execute(broj_stanara_upit,vrednost)
			broj_stanara=mycursor.fetchone()
			pomocni_broj_stanara=broj_stanara['broj_stanara']

			racuni_cistac_plati_glavni['iznos']=(float(racuni_cistac_plati_glavni['iznos'])/int(ukupan_broj_stanara))*pomocni_broj_stanara
			racuni_cistac_plati_glavni['iznos']=format(racuni_cistac_plati_glavni['iznos'], ".2f")
			racuni_cistac_plati=racuni_cistac_plati_glavni
			
			mesec=racuni_cistac_plati['mesec_vazenja']

			return render_template("stanari_racuni_cistac_plati.html", racuni_cistac_plati=racuni_cistac_plati, mesec=mesec)		
	else:
		return redirect(url_for('Login'))
@app.route('/uplatnica_cistac',methods=['GET','POST'])
def UplatnicaCistac():
	if Ulogovani_stanar():
		if request.method=='POST':
			mycursor.execute("SELECT broj_telefona FROM korisnici WHERE uloga=1")
			broj_telefona_up=mycursor.fetchone()
			br_tel_upravnika=broj_telefona_up['broj_telefona']

			forma=request.form
			stanar_sesija = session['ulogovani_stanar']
			res=yaml.safe_load(stanar_sesija)
			broj_tel_stanara=res['broj_telefona']
			datum=datetime.now().date().strftime("%d/%m/%Y")
			vreme=datetime.now().time().strftime("%H:%M:%S")
			broj_racuna=forma['broj_racuna']
			iznos=forma['iznos_rsd']
			broj_stana=res['broj_stana']
			korisnicko_ime=res['korisnicko_ime']
			mesec_vazenja=forma['mesec_vazenja']

			upit="INSERT INTO placeni_racuni_cistac (datum,vreme,broj_racuna,iznos,mesec_vazenja,broj_stana,korisnicko_ime) VALUES (%s, %s, %s,%s,%s, %s, %s)"
			vrednosti=(datum,vreme,broj_racuna,iznos,mesec_vazenja,broj_stana,korisnicko_ime)
			mycursor.execute(upit,vrednosti)

			to_client_number='381'+broj_tel_stanara[1:]
			poruka='Uspesno ste platili racun za ciscenje broj - '+broj_racuna+' u iznosu od '+iznos+' dinara.'
			client.send_message({'from':'Upravnik15','to':to_client_number,'text':poruka})

			to_client_number='381'+br_tel_upravnika[1:]
			poruka='Stanar sa korisnickim imenom - '+korisnicko_ime+' je platio racun za ciscenje u iznosu od '+iznos+' dinara.'
			client.send_message({'from':'Upravnik15','to':to_client_number,'text':poruka})

			con.commit()
			return redirect(url_for("StanariRacuniCistac"))
	else:
		return redirect('Login')
@app.route('/stanari_placeni_racuni_cistac', methods = ['GET', 'POST'])
def StanariPlaceniRacuniCistac():
	if Ulogovani_stanar():
		stanar_sesija = session['ulogovani_stanar']
		res=yaml.safe_load(stanar_sesija)
		broj_stana=res['broj_stana']
		upit="SELECT * FROM placeni_racuni_cistac WHERE broj_stana=%s"
		vrednost=(broj_stana,)
		mycursor.execute(upit,vrednost)
		placeni_racuni=mycursor.fetchall()
		return render_template("stanari_placeni_racuni_cistac.html", placeni_racuni=placeni_racuni)
	else:
		return redirect(url_for('Login'))
@app.route('/stanari_racuni_fond',methods = ['GET', 'POST'])
def StanariRacuniFond():
	if Ulogovani_stanar():
		ukupan_broj_stanara=BrojStanara()

		stanar_sesija = session['ulogovani_stanar']
		res=yaml.safe_load(stanar_sesija)
		broj_stana=res['broj_stana']

		selectuj_za_prikaz="SELECT * FROM racuni_fond WHERE broj_racuna NOT IN (SELECT broj_racuna FROM placeni_racuni_fond WHERE broj_stana=%s)"
		vrednost_stana=(broj_stana,)
		mycursor.execute(selectuj_za_prikaz,vrednost_stana)
		neplaceni_r_f=mycursor.fetchall()
		
		broj_stanara_upit=("SELECT COUNT(*) AS broj_stanara FROM korisnici WHERE broj_stana=%s")
		vrednosti=(broj_stana,)
		mycursor.execute(broj_stanara_upit,vrednosti)
		broj_stanara=mycursor.fetchone()
		pomocni_broj_stanara=broj_stanara['broj_stanara']

		racuni_za_fond=[]
		for neplaceni_r_f in neplaceni_r_f:
			neplaceni_r_f['iznos']=(float(neplaceni_r_f['iznos'])/int(ukupan_broj_stanara))*pomocni_broj_stanara
			neplaceni_r_f['iznos']=format(neplaceni_r_f['iznos'], ".2f")
			racuni_za_fond.append(neplaceni_r_f)

		return render_template("stanari_racuni_fond.html", racuni_za_fond=racuni_za_fond)
	else:
		return redirect(url_for('Login'))
@app.route('/stanari_racuni_fond_plati/<string:id_racuna>',methods = ['GET', 'POST'])
def StanariRacuniFondPlati(id_racuna):
	if Ulogovani_stanar():
		if request.method=='GET':
			ukupan_broj_stanara=BrojStanara()

			upit="SELECT * FROM racuni_fond WHERE id=%s"
			vrednost=(id_racuna,)
			mycursor.execute(upit,vrednost)
			racuni_fond_plati_glavni=mycursor.fetchone()
			
			stanar_sesija = session['ulogovani_stanar']
			res=yaml.safe_load(stanar_sesija)
			broj_stana=res['broj_stana']

			broj_stanara_upit=("SELECT COUNT(*) AS broj_stanara FROM korisnici WHERE broj_stana=%s")
			vrednost=(broj_stana,)
			mycursor.execute(broj_stanara_upit,vrednost)
			broj_stanara=mycursor.fetchone()
			pomocni_broj_stanara=broj_stanara['broj_stanara']

			racuni_fond_plati_glavni['iznos']=(float(racuni_fond_plati_glavni['iznos'])/int(ukupan_broj_stanara))*pomocni_broj_stanara
			racuni_fond_plati_glavni['iznos']=format(racuni_fond_plati_glavni['iznos'], ".2f")
			racuni_fond_plati=racuni_fond_plati_glavni
			
			mesec=racuni_fond_plati['mesec_vazenja']

			return render_template("stanari_racuni_fond_plati.html", racuni_fond_plati=racuni_fond_plati, mesec=mesec)		
	else:
		return redirect(url_for('Login'))
@app.route('/uplatnica_fond',methods=['GET','POST'])
def UplatnicaFond():
	if Ulogovani_stanar():
		if request.method=='POST':
			mycursor.execute("SELECT broj_telefona FROM korisnici WHERE uloga=1")
			broj_telefona_up=mycursor.fetchone()
			br_tel_upravnika=broj_telefona_up['broj_telefona']

			forma=request.form
			stanar_sesija = session['ulogovani_stanar']
			res=yaml.safe_load(stanar_sesija)
			broj_tel_stanara=res['broj_telefona']
			datum=datetime.now().date().strftime("%d/%m/%Y")
			vreme=datetime.now().time().strftime("%H:%M:%S")
			broj_racuna=forma['broj_racuna']
			iznos=forma['iznos_rsd']
			broj_stana=res['broj_stana']
			korisnicko_ime=res['korisnicko_ime']
			mesec_vazenja=forma['mesec_vazenja']

			upit="INSERT INTO placeni_racuni_fond (datum,vreme,broj_racuna,iznos,mesec_vazenja,broj_stana,korisnicko_ime) VALUES (%s, %s, %s,%s,%s, %s, %s)"
			vrednosti=(datum,vreme,broj_racuna,iznos,mesec_vazenja,broj_stana,korisnicko_ime)
			mycursor.execute(upit,vrednosti)

			to_client_number='381'+broj_tel_stanara[1:]
			poruka='Uspesno ste platili racun za stambeni fond broj - '+broj_racuna+' u iznosu od '+iznos+' dinara.'
			client.send_message({'from':'Upravnik15','to':to_client_number,'text':poruka})

			to_client_number='381'+br_tel_upravnika[1:]
			poruka='Stanar sa korisnickim imenom - '+korisnicko_ime+' je platio racun za stambeni fond u iznosu od '+iznos+' dinara.'
			client.send_message({'from':'Upravnik15','to':to_client_number,'text':poruka})

			con.commit()
			return redirect(url_for("StanariRacuniFond"))
	else:
		return redirect('Login')
@app.route('/stanari_placeni_racuni_fond', methods = ['GET', 'POST'])
def StanariPlaceniRacuniFond():
	if Ulogovani_stanar():
		stanar_sesija = session['ulogovani_stanar']
		res=yaml.safe_load(stanar_sesija)
		broj_stana=res['broj_stana']
		upit="SELECT * FROM placeni_racuni_fond WHERE broj_stana=%s"
		vrednost=(broj_stana,)
		mycursor.execute(upit,vrednost)
		placeni_racuni=mycursor.fetchall()
		return render_template("stanari_placeni_racuni_fond.html", placeni_racuni=placeni_racuni)
	else:
		return redirect(url_for('Login'))
# .............obavestenja............. #
@app.route('/stanari_obavestenja',methods = ['GET', 'POST'])
def StanariObavestenja():
	if Ulogovani_stanar():
		return render_template("stanari_obavestenja.html")
	else:
		return redirect(url_for('Login'))
@app.route('/stanari_obavestenja_nova',methods = ['GET', 'POST'])
def StanariObavestenjaNova():
	if Ulogovani_stanar():
		if request.method=='GET':
			stanar_sesija = session['ulogovani_stanar']
			res=yaml.safe_load(stanar_sesija)
			print(res['korisnicko_ime'])
			korisnicko_ime=res['korisnicko_ime']
			upit=("SELECT * FROM korisnici WHERE uloga!=3 AND korisnicko_ime!=%s ORDER BY ime ASC")
			vrednost=(korisnicko_ime,)
			mycursor.execute(upit,vrednost)
			korisnici=mycursor.fetchall()
			return render_template("stanari_obavestenja_nova.html", korisnici=korisnici)
		elif request.method=='POST':
			forma=request.form
			upit1="SELECT * FROM korisnici WHERE id=%s"
			vrednost=(forma['primalac'],)
			mycursor.execute(upit1,vrednost)
			rezultat=mycursor.fetchone()
			primalac=rezultat['ime']+' '+rezultat['prezime']
			broj_primaoca=rezultat['broj_telefona']
			stanar_sesija = session['ulogovani_stanar']
			res=yaml.safe_load(stanar_sesija)
			broj_posiljaoca=res['broj_telefona']
			posiljalac=res['ime']+' '+res['prezime']
			datum=datetime.now().date().strftime("%d/%m/%Y")
			print(datum)
			vreme=datetime.now().time().strftime("%H:%M:%S")
			print(vreme)
			upit = "INSERT INTO obavestenja (posiljalac,broj_posiljaoca,primalac,broj_primaoca,datum,vreme,sadrzaj) VALUES (%s, %s, %s, %s, %s,%s,%s)"
			vrednosti=(posiljalac,broj_posiljaoca,primalac,broj_primaoca,datum,vreme,forma['sadrzaj'])
			mycursor.execute(upit,vrednosti)
			to_client_number='381'+broj_primaoca[1:]
			poruka='Postovani imate obavestenje u aplikaciji upravnik!'+posiljalac
			client.send_message({'from':'Upravnik15','to':to_client_number,'text':poruka})
			con.commit()
			flash("Poruka je uspesno poslata!",'success')
			return redirect(url_for("StanariObavestenjaNova"))
	else:
		return redirect(url_for('Login'))

@app.route('/stanari_obavestenja_inbox',methods = ['GET', 'POST'])
def StanariObavestenjaInbox():
	if Ulogovani_stanar():
		if request.method=='GET':
			stanar_sesija = session['ulogovani_stanar']
			res=yaml.safe_load(stanar_sesija)
			primalac=res['ime']+' '+res['prezime']
			upit=("SELECT * FROM obavestenja WHERE primalac=%s")
			vrednost=(primalac,)
			mycursor.execute(upit,vrednost)
			obavestenja=mycursor.fetchall()
			return render_template("stanari_obavestenja_inbox.html", obavestenja=obavestenja)
		
	else:
		return redirect(url_for('Login'))

@app.route('/stanari_obavestenja_brisanje/<string:id_obavestenja>', methods = ['GET', 'POST'])
def StanariObavestenjaBrisanje(id_obavestenja):
	if Ulogovani_stanar():
		mycursor = con.cursor()
		upit= "DELETE FROM obavestenja WHERE id_obavestenja = %s"
		vrednost = (id_obavestenja,)
		mycursor.execute(upit, vrednost)
		con.commit()
		return redirect(url_for("StanariObavestenjaInbox"))
	else:
		return redirect(url_for('Login'))
# .............STANARI KRAJ............. #



app.run(debug=True)


