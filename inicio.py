# importamos la libreria pymysql para conectar con la base de datos y flask un framework para poder interactuar con los html y crearla pagina web
import pymysql
from flask import Flask, g,render_template, request, url_for, redirect,flash, session
import  os
from werkzeug.utils import secure_filename
## se crea un app de flask para poder abrir la pagina web
app = Flask(__name__)
app.secret_key = "MySecretKey1234"
estatus=0
usuario = 0

class user:
    def __init__(self, id, username, password, id_funcion, funcion):
        self.id = id
        self.username = username
        self.password = password
        self.id_funcion = id_funcion
        self.funcion = funcion
    def __repr__(self):
        return '<User:{self.username}>'

users=[]


@app.before_request
def before_request():
    global estatus
    if "user_id" in session:
        conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
        cursor = conn.cursor()
        cursor.execute('''SELECT a.idusuario, a.usuario, a.password, a.nombre, b.idperfil_admo, b.descripcion from Usuario a, perfil_admo b WHERE a.idperfil_admo = b.idperfil_admo  and a.idusuario=%s''',(session["user_id"]))
        dato = cursor.fetchone()
        print(dato)
        users.clear()
        users.append(user(id=dato[0],username=dato[1],password=dato[2], id_funcion=dato[4], funcion=dato[5]))
        g.user=users[0]




@app.route("/")
def home2():
    return render_template("login.html")


## se define el home
@app.route("/home")
def home():
    return render_template("home.html")#, usuarios=usuarios, perfiles=perfiles)





@app.route("/login")
def login():
    global estatus
    estatus=1
    return render_template("login.html")






@app.route("/inicio" , methods=["POST"])
def inicio():
    session.pop("user_id",None)
    global estatus,usuario,perfil
    conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')

    if request.method == 'POST':
        nombre= request.form["txtusuario"]
        passw= request.form["txtpassword"]
        print(passw)
        print(nombre)
        cursor = conn.cursor()
        cursor.execute("SELECT idusuario, usuario,password FROM Usuario ")#WHERE usuarios = '%s' and Password = '$s' ",(nombre,passw))
        datos= cursor.fetchall()
        print(datos)
        conn.close()
        #nr =  mysqli_num_rows(datos)
        for dato in datos:
            if dato[1]==nombre and dato[2]==passw:

                print("Bienvenido: " )
                session["user_id"] = dato[0]
                estatus=1
                usuario = dato[0]

                return redirect(url_for('home'))
        print("No ingreso")
        return render_template("login.html")
@app.route("/logout")
def logout():
    global estatus,usuario

    estatus=0
    session.pop('user_id',None)
    return redirect(url_for('home2'))

@app.route("/registro")
def registro():
    conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM perfil_admo ")
    perfiles =  cursor.fetchall()
    print (perfiles)
    return render_template("registro.html", perfiles= perfiles)



@app.route("/registrar",methods=["POST"])
def registrar():
    if request.method == 'POST':
        usu= request.form["user"]
        passw= request.form["password"]
        nombre= request.form["nombre"]
        conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
        cursor = conn.cursor()
        cursor.execute('insert into Usuario (usuario,Password,Nombre, idperfil_admo) values (%s,%s,%s,2)', (usu,passw,nombre))
        conn.commit()

        cursor.execute('select idusuario,usuario,Password,Nombre from Usuario where idusuario= (select max(idusuario) from Usuario) ')
        datos = cursor.fetchall()
        print(datos)
        cursor.execute(
            'SELECT a.idusuario, a.usuario, a.password, a.nombre, a.idperfil_admo, b.idperfil_admo, b.descripcion from Usuario a, perfil_admo b WHERE a.idperfil_admo = b.idperfil_admo and a.idusuario = (select max(idusuario) from Usuario)',)
        datos1 = cursor.fetchall()
        cursor.execute('select idperfil_admo, descripcion from perfil_admo ')
        datos3 = cursor.fetchall()
        conn.close()
        return render_template("edi_usuario.html", puestos=datos, pue_habs=datos1,habs=datos3)

















@app.route("/usuario")
def usuario():
    conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Usuario ")
    perfiles= cursor.fetchall()
    return render_template("usuario.html",perfiles=perfiles)


@app.route("/ed_usuario/<string:id>")
def ed_usuario(id):
    conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
    cursor = conn.cursor()
    cursor.execute('select idusuario from Usuario where idusuario= %s', (id))
    datos = cursor.fetchall()
    cursor.execute(
        'SELECT a.idusuario, a.usuario, a.password, a.nombre, a.idperfil_admo, b.idperfil_admo, b.descripcion from Usuario a, perfil_admo b WHERE a.idperfil_admo = b.idperfil_admo and a.idusuario = %s',
        (id))
    datos1 = cursor.fetchall()
    cursor.execute('select idperfil_admo, descripcion from perfil_admo ')
    datos3 = cursor.fetchall()
    return render_template("edi_usuario.html", puestos=datos, pue_habs=datos1,habs=datos3)



@app.route('/agrega_perfil_usuario', methods=['POST'])
def agrega_perfil_usuario():
    if request.method == 'POST':
        aux_pto = request.form['pto']
        aux_hab = request.form['habil']
        conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
        cursor = conn.cursor()
        cursor.execute('update Usuario set idperfil_admo=%s where idusuario=%s',
                       ( aux_hab,aux_pto))
        conn.commit()

        cursor.execute('select idusuario from Usuario where idusuario= %s', (aux_pto))
        datos = cursor.fetchall()
        cursor.execute(
            'SELECT a.idusuario, a.usuario, a.password, a.nombre, a.idperfil_admo, b.idperfil_admo, b.descripcion from Usuario a, perfil_admo b WHERE a.idperfil_admo = b.idperfil_admo and a.idusuario = %s',
            (aux_pto))
        datos1 = cursor.fetchall()
        cursor.execute('select idperfil_admo, descripcion from perfil_admo ')
        datos3 = cursor.fetchall()
        return render_template("edi_usuario.html", puestos=datos, pue_habs=datos1,habs=datos3)

@app.route('/bo_usuario/<string:id>')
def bo_usuario(id):
    global usuario
    conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
    cursor = conn.cursor()
    if id==usuario:

        error = "no se puede eliminar ese elemento, ya que esta siendo utilizado"
        conn.close()
        return render_template("error.html", error=error,paginaant="/usuario")
    else:
        cursor.execute('delete from Usuario where idusuario = {0}'.format(id))
        conn.commit()
        conn.close()
        return redirect(url_for('usuario'))


@app.route('/modifica_usuario/<string:id>', methods=['POST'])
def modifica_usuario(id):
    if request.method == 'POST':
        aux_des = request.form['descripcion']
        aux_pass = request.form['password']
        aux_nom = request.form['nombre']
        conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
        cursor = conn.cursor()
        cursor.execute(
            'update Usuario set usuario=%s,password=%s,nombre=%s where idusuario=%s',
            (aux_des, aux_pass,aux_nom,id))
        conn.commit()
        conn.close()
        return redirect(url_for('usuario'))






@app.route("/perfil")
def perfil():
    conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM perfil_admo ")
    perfiles= cursor.fetchall()
    return render_template("perfi.html",perfiles=perfiles)


@app.route("/ed_perfil/<string:id>")
def ed_perfil(id):
    conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
    cursor = conn.cursor()
    cursor.execute('select idperfil_admo, descripcion'
                   ' from perfil_admo where idperfil_admo= %s', (id))
    datos = cursor.fetchall()
    cursor.execute(
        'select a.idperfil_admo,a.descripcion, b.idproceso,b.desc_proceso,d.idpermisos, d.descripcion,d.idpermisos,d.descripcion  from perfil_admo a, proceso b,perfil_admo_has_proceso c, permisos d  where a.idperfil_admo=c.idperfil_admo and b.idproceso=c.idproceso and c.idpermisos=d.idpermisos and a.idperfil_admo=%s',
        (id))
    datos1 = cursor.fetchall()
    cursor.execute('select idproceso, desc_proceso from proceso ')
    datos3 = cursor.fetchall()
    cursor.execute('select idpermisos, descripcion from permisos ')
    datos4 = cursor.fetchall()
    conn.close()
    return render_template("edi_perfil.html", puestos=datos, pue_habs=datos1,permisos=datos4,habs=datos3)


@app.route('/agrega_proceso_perfil', methods=['POST'])
def agrega_proceso_perfil():
    if request.method == 'POST':
        aux_pto = request.form['pto']
        aux_hab = request.form['habil']
        aux_exp = request.form['perm']
        conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
        cursor = conn.cursor()
        cursor.execute('insert into perfil_admo_has_proceso (idperfil_admo, idproceso,idpermisos) values (%s,%s,%s)',
                       (aux_pto, aux_hab, aux_exp))
        conn.commit()

        cursor.execute('select idperfil_admo, descripcion'
                   ' from perfil_admo where idperfil_admo= %s', (aux_pto))
        datos = cursor.fetchall()
        cursor.execute(
            'select a.idperfil_admo,a.descripcion, b.idproceso,b.desc_proceso,d.idpermisos, d.descripcion,d.idpermisos,d.descripcion  from perfil_admo a, proceso b,perfil_admo_has_proceso c, permisos d  where a.idperfil_admo=c.idperfil_admo and b.idproceso=c.idproceso and c.idpermisos=d.idpermisos and a.idperfil_admo=%s',
            (aux_pto))
        datos1 = cursor.fetchall()
        cursor.execute('select idproceso, desc_proceso from proceso ')
        datos3 = cursor.fetchall()
        cursor.execute('select idpermisos, descripcion from permisos ')
        datos4 = cursor.fetchall()
        conn.close()
        return render_template("edi_perfil.html", puestos=datos, pue_habs=datos1,permisos=datos4,habs=datos3)


@app.route("/bo_pro_pe/<string:id>/<string:idh>/<string:idp>")
def bo_pro_pre(id, idh,idp):
    conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
    cursor = conn.cursor()
    cursor.execute('delete from perfil_admo_has_proceso where idperfil_admo =%s and idpermisos=%s and idproceso = %s', (id, idp,idh))
    conn.commit()

    cursor.execute('select idperfil_admo, descripcion'
               ' from perfil_admo where idperfil_admo= %s', (id))
    datos = cursor.fetchall()
    cursor.execute(
        'select a.idperfil_admo,a.descripcion, b.idproceso,b.desc_proceso,d.idpermisos, d.descripcion,d.idpermisos,d.descripcion  from perfil_admo a, proceso b,perfil_admo_has_proceso c, permisos d  where a.idperfil_admo=c.idperfil_admo and b.idproceso=c.idproceso and c.idpermisos=d.idpermisos and a.idperfil_admo=%s',
        (id))
    datos1 = cursor.fetchall()
    cursor.execute('select idproceso, desc_proceso from proceso ')
    datos3 = cursor.fetchall()
    cursor.execute('select idpermisos, descripcion from permisos ')
    datos4 = cursor.fetchall()
    conn.close()
    return render_template("edi_perfil.html", puestos=datos, pue_habs=datos1,permisos=datos4,habs=datos3)

@app.route('/modifica_perfil/<string:id>', methods=['POST'])
def modifica_perfil(id):
    if request.method == 'POST':
        aux_des = request.form['descripcion']
        conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
        cursor = conn.cursor()
        cursor.execute(
            'update perfil_admo set descripcion=%s where idperfil_admo=%s',
            (aux_des, id))
        conn.commit()
        conn.close()
        return redirect(url_for('perfil'))



@app.route("/agrega_perfil" , methods=["POST"])
def agrega_perfil():
    conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')

    if request.method == 'POST':
        nombre= request.form["descripcion"]
        cursor = conn.cursor()
        cursor.execute("insert into perfil_admo (descripcion) values ( %s ) ",(nombre))
        conn.commit()

        cursor.execute('select idperfil_admo, descripcion from perfil_admo where idperfil_admo=(select max(idperfil_admo) from perfil_admo)')
        datos = cursor.fetchall()
        cursor.execute(
            'select a.idperfil_admo,a.descripcion, b.idproceso,b.desc_proceso,d.idpermisos, d.descripcion,d.idpermisos,d.descripcion  from perfil_admo a, proceso b,perfil_admo_has_proceso c, permisos d  where a.idperfil_admo=c.idperfil_admo and b.idproceso=c.idproceso and c.idpermisos=d.idpermisos and a.idperfil_admo=(select max(idperfil_admo) from perfil_admo)')
        datos1 = cursor.fetchall()
        cursor.execute('select idproceso, desc_proceso from proceso ')
        datos3 = cursor.fetchall()
        cursor.execute('select idpermisos, descripcion from permisos ')
        datos4 = cursor.fetchall()
        conn.close()
        return render_template("edi_perfil.html", puestos=datos, pue_habs=datos1,permisos=datos4,habs=datos3)
@app.route("/nvo_perfil" )
def nvo_perfil():
     return render_template("agr_perfil.html")


@app.route('/bo_perfil/<string:id>')
def bo_perfil(id):
    conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) from perfil_admo_has_proceso WHERE idperfil_admo = %s", (id))
    ph_pue=cursor.fetchone()
    cursor.execute("SELECT COUNT(*) from Usuario WHERE idperfil_admo= %s", (id))
    pi_pue=cursor.fetchone()
    if ph_pue[0] == 0 and pi_pue[0] == 0 :
        cursor.execute('delete from perfil_admo where idperfil_admo = {0}'.format(id))
        conn.commit()
        conn.close()
        return redirect(url_for('perfil'))
    else:
        error = "no se puede eliminar ese elemento, ya que tiene relacion con otras tablas, elimina las relaciones y vuelve a intentarlo"
        conn.close()
        return render_template("error.html", error=error,paginaant="/perfil")











###################################################### catalogo de candidato#############################################################################
## muestra la tabla con los candidatos y la opcion de editar, agregar o borrar
@app.route("/solicitante")
def candidato():
    conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
    cursor = conn.cursor()
    cursor.execute(' select CURP,RFC, Domicilio, E_mail,  Sexo, Edad from candidato order by CURP')
    datos = cursor.fetchall()
    conn.close()
    return render_template("candidato.html", candidatos=datos)

## abre el html para agregar un candidato
@app.route("/agregar_solicitante")
def agregar_candidato():
    conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
    cursor = conn.cursor()
    cursor.execute('select * from estadocivil order by Descripcion')
    datos = cursor.fetchall()
    conn.close()
    return render_template("agr_candidato.html", datos=datos)

## agrega el candidato a la base de datos
@app.route("/agrega_solicitante", methods=["POST"])
def agrega_candidato():
    if request.method == 'POST':
        aux_curp = request.form['curp']
        aux_nombre = request.form['nombre']
        aux_rfc = request.form['rfc']
        aux_telefono = request.form['telefono']
        aux_domicilio = request.form['domicilio']
        aux_nss = request.form['nss']
        print(aux_nss, "si")
        aux_edad = request.form['edad']
        aux_sexo = request.form['sexo']
        aux_estadociv = request.form['estadoc']
        aux_email = request.form['email']
        conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
        cursor = conn.cursor()
        cursor.execute('''insert into candidato(CURP,RFC, Nombre,Domicilio, Telefono,E_mail,
            Sexo,Edad,NSS,idEstadoCivil) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
                       (aux_curp, aux_rfc, aux_nombre, aux_domicilio,
                        aux_telefono, aux_email, aux_sexo, aux_edad, aux_nss, aux_estadociv))
        conn.commit()
        cursor.execute(
            ' select CURP,RFC, Nombre,Domicilio, Telefono,E_mail, Sexo,Edad,NSS,idEstadoCivil from candidato where CURP=%s',
            (aux_curp))
        datos = cursor.fetchall()
        cursor.execute(' select * from habilidad ')
        datos1 = cursor.fetchall()
        cursor.execute(' select * from idioma ')
        datos2 = cursor.fetchall()
        cursor.execute(' select * from nivelacademico ')
        datos4 = cursor.fetchall()
        cursor.execute('select a.CURP, b.idIdioma,b.Lenguaje,c.CURP, c.idIdioma, c.Nivel '
                       'from candidato a, idioma b,candidato_has_idioma c '
                       'where a.CURP=c.CURP and b.idIdioma=c.idIdioma and a.CURP=%s ', (aux_curp))
        datos5 = cursor.fetchall()
        cursor.execute('select a.CURP, b.idHabilidad,b.Descripcion,c.CURP, c.idHabilidad, c.Experiencia '
                       'from candidato a, habilidad b,candidato_has_habilidad c '
                       'where a.CURP=c.CURP and b.idHabilidad=c.idHabilidad and a.CURP=%s ', (aux_curp))
        datos6 = cursor.fetchall()
        cursor.execute('select * from estadocivil order by Descripcion')
        datos7 = cursor.fetchall()

        cursor.execute(
            'select a.CURP, b.idNivelAcademico,b.Descripcion,c.Institucion,c.CURP, c.idNivelAcademico,c.idCarrera ,d.Descripcion '
            'from candidato a, nivelacademico b,candidato_has_nivelacademico c, carrera d '
            ' where a.CURP=c.CURP and b.idNivelAcademico=c.idNivelacademico and c.idCarrera = d.idCarrera and a.CURP=%s ',
            (aux_curp))
        datos9 = cursor.fetchall()
        cursor.execute('select * from carrera order by Descripcion')
        datos10 = cursor.fetchall()
        conn.close()
        return render_template("edi_candidato.html", datos=datos, habs=datos1, idiomas=datos2,
                               niveles=datos4, idis=datos5, can_habs=datos6, estados=datos7,
                               nivelesC=datos9, carrerasN=datos10)

## abre el html para editar el candidato
@app.route("/ed_solicitante/<string:id>")
def ed_candidato(id):
    conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
    cursor = conn.cursor()
    cursor.execute(
        ' select CURP,RFC, Nombre,Domicilio, Telefono,E_mail, Sexo,Edad,NSS,Fotografia,idEstadoCivil from candidato where CURP=%s',
        (id))
    datos = cursor.fetchall()
    print(datos)
    cursor.execute(' select * from habilidad ')
    datos1 = cursor.fetchall()
    cursor.execute(' select * from idioma ')
    datos2 = cursor.fetchall()

    cursor.execute(' select * from nivelacademico ')
    datos4 = cursor.fetchall()
    cursor.execute('select a.CURP, b.idIdioma,b.Lenguaje,c.CURP, c.idIdioma, c.Nivel '
                   'from candidato a, idioma b,candidato_has_idioma c '
                   'where a.CURP=c.CURP and b.idIdioma=c.idIdioma and a.CURP=%s ', (id))
    datos5 = cursor.fetchall()
    cursor.execute('select a.CURP, b.idHabilidad,b.Descripcion,c.CURP, c.idHabilidad, c.Experiencia '
                   'from candidato a, habilidad b,candidato_has_habilidad c '
                   'where a.CURP=c.CURP and b.idHabilidad=c.idHabilidad and a.CURP=%s ', (id))
    datos6 = cursor.fetchall()
    cursor.execute('select * from estadocivil order by Descripcion')
    datos7 = cursor.fetchall()

    cursor.execute(
        'select a.CURP, b.idNivelAcademico,b.Descripcion,c.Institucion,c.CURP, c.idNivelAcademico,c.idCarrera ,d.Descripcion '
        'from candidato a, nivelacademico b,candidato_has_nivelacademico c, carrera d '
        ' where a.CURP=c.CURP and b.idNivelAcademico=c.idNivelacademico and c.idCarrera = d.idCarrera and a.CURP=%s ',
        (id))
    datos9 = cursor.fetchall()
    cursor.execute('select * from carrera order by Descripcion')
    datos10 = cursor.fetchall()
    conn.close()
    return render_template("edi_candidato.html", datos=datos, habs=datos1, idiomas=datos2,
                           niveles=datos4, idis=datos5, can_habs=datos6, estados=datos7,
                           nivelesC=datos9, carrerasN=datos10)

## cambia los datos de la base de datos por lo que ya estan modificados
@app.route("/modifica_solicitante/<string:id>", methods=["POST"])
def modifica_candidato(id):
    if request.method == 'POST':
        aux_curp = request.form['curp']
        print(aux_curp)
        aux_nombre = request.form['nombre']
        print(aux_nombre)
        aux_rfc = request.form['rfc']
        print(aux_rfc)
        aux_telefono = request.form['telefono']
        print(aux_telefono)
        aux_domicilio = request.form['domicilio']
        print(aux_domicilio)
        aux_nss = request.form['nss']
        print(aux_nss)
        aux_edad = request.form['edad']
        print(aux_edad)
        aux_estadociv = request.form['estadoc']
        print(aux_estadociv)
        aux_email = request.form['email']
        print(aux_email)
        aux_sexo = request.form['sexo']
        print(aux_sexo)



        conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
        cursor = conn.cursor()
        cursor.execute('UPDATE candidato SET Curp =%s, RFC =%s, Nombre =%s, Domicilio =%s, Telefono =%s, E_mail =%s, Sexo =%s, Edad =%s, NSS =%s, idEstadoCivil=%s WHERE Curp =%s' ,
        (aux_curp, aux_rfc, aux_nombre, aux_domicilio,
        aux_telefono, aux_email, aux_sexo, aux_edad, aux_nss, aux_estadociv,aux_curp))
        conn.commit()
        conn.close()
        return redirect(url_for('candidato'))

## agrega las habilidades asociadas del candidato
@app.route("/agrega_hab_solicitante/<string:id>/<string:idh>", methods=["POST"])
def agrega_hab_candidato(id, idh):
    if request.method == 'POST':
        aux_pto = request.form['can']
        aux_hab = request.form['habil']
        aux_exp = request.form['expe']
        conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
        cursor = conn.cursor()
        cursor.execute('insert into candidato_has_habilidad (CURP, idHabilidad,Experiencia) values (%s,%s,%s)',
                       (aux_pto, aux_hab, aux_exp))
        conn.commit()
        cursor.execute(
            ' select CURP,RFC, Nombre,Domicilio, Telefono,E_mail, Sexo,Edad,NSS,Fotografia,idEstadoCivil from candidato where CURP=%s',
            (id))
        datos = cursor.fetchall()
        cursor.execute(' select * from habilidad ')
        datos1 = cursor.fetchall()
        cursor.execute(' select * from idioma ')
        datos2 = cursor.fetchall()

        cursor.execute(' select * from nivelacademico ')
        datos4 = cursor.fetchall()
        cursor.execute('select a.CURP, b.idIdioma,b.Lenguaje,c.CURP, c.idIdioma, c.Nivel '
                       'from candidato a, idioma b,candidato_has_idioma c '
                       'where a.CURP=c.CURP and b.idIdioma=c.idIdioma and a.CURP=%s ', (id))
        datos5 = cursor.fetchall()
        cursor.execute('select a.CURP, b.idHabilidad,b.Descripcion,c.CURP, c.idHabilidad, c.Experiencia '
                       'from candidato a, habilidad b,candidato_has_habilidad c '
                       'where a.CURP=c.CURP and b.idHabilidad=c.idHabilidad and a.CURP=%s ', (id))
        datos6 = cursor.fetchall()
        cursor.execute('select * from estadocivil order by Descripcion')
        datos7 = cursor.fetchall()

        cursor.execute(
            'select a.CURP, b.idNivelAcademico,b.Descripcion,c.Institucion,c.CURP, c.idNivelAcademico,c.idCarrera ,d.Descripcion '
            'from candidato a, nivelacademico b,candidato_has_nivelacademico c, carrera d '
            ' where a.CURP=c.CURP and b.idNivelAcademico=c.idNivelacademico and c.idCarrera = d.idCarrera and a.CURP=%s ',
            (id))
        datos9 = cursor.fetchall()
        cursor.execute('select * from carrera order by Descripcion')
        datos10 = cursor.fetchall()
        conn.close()
        return render_template("edi_candidato.html", datos=datos, habs=datos1, idiomas=datos2,
                               niveles=datos4, idis=datos5, can_habs=datos6, estados=datos7,
                               nivelesC=datos9, carrerasN=datos10)
## borra las habilidades asociadas del candidato

@app.route("/bo_hab_sol/<string:id>/<string:idh>")
def bo_hab_can(id, idh):
    conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
    cursor = conn.cursor()
    cursor.execute('delete from candidato_has_habilidad where CURP =%s and idHabilidad=%s', (id, idh))
    conn.commit()
    cursor.execute(
        ' select CURP,RFC, Nombre,Domicilio, Telefono,E_mail, Sexo,Edad,NSS,Fotografia,idEstadoCivil from candidato where CURP=%s',
        (id))
    datos = cursor.fetchall()
    cursor.execute(' select * from habilidad ')
    datos1 = cursor.fetchall()
    cursor.execute(' select * from idioma ')
    datos2 = cursor.fetchall()

    cursor.execute(' select * from nivelacademico ')
    datos4 = cursor.fetchall()
    cursor.execute('select a.CURP, b.idIdioma,b.Lenguaje,c.CURP, c.idIdioma, c.Nivel '
                   'from candidato a, idioma b,candidato_has_idioma c '
                   'where a.CURP=c.CURP and b.idIdioma=c.idIdioma and a.CURP=%s ', (id))
    datos5 = cursor.fetchall()
    cursor.execute('select a.CURP, b.idHabilidad,b.Descripcion,c.CURP, c.idHabilidad, c.Experiencia '
                   'from candidato a, habilidad b,candidato_has_habilidad c '
                   'where a.CURP=c.CURP and b.idHabilidad=c.idHabilidad and a.CURP=%s ', (id))
    datos6 = cursor.fetchall()
    cursor.execute('select * from estadocivil order by Descripcion')
    datos7 = cursor.fetchall()

    cursor.execute(
        'select a.CURP, b.idNivelAcademico,b.Descripcion,c.Institucion,c.CURP, c.idNivelAcademico,c.idCarrera ,d.Descripcion '
        'from candidato a, nivelacademico b,candidato_has_nivelacademico c, carrera d '
        ' where a.CURP=c.CURP and b.idNivelAcademico=c.idNivelacademico and c.idCarrera = d.idCarrera and a.CURP=%s ',
        (id))
    datos9 = cursor.fetchall()
    cursor.execute('select * from carrera order by Descripcion')
    datos10 = cursor.fetchall()
    conn.close()
    return render_template("edi_candidato.html", datos=datos, habs=datos1, idiomas=datos2,
                           niveles=datos4, idis=datos5, can_habs=datos6, estados=datos7,
                           nivelesC=datos9, carrerasN=datos10)

## agrega los idiomas asociadas del candidato
@app.route("/agrega_idio_sol/<string:id>/<string:idi>", methods=["POST"])
def agrega_idio_candidato(id, idi):
    if request.method == 'POST':
        aux_pto = request.form['cani']
        aux_hab = request.form['idio']
        aux_exp = request.form['nive']
        conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
        cursor = conn.cursor()
        cursor.execute('insert into candidato_has_idioma (CURP, idIdioma,Nivel) values (%s,%s,%s)',
                       (aux_pto, aux_hab, aux_exp))
        conn.commit()
        cursor.execute(
            ' select CURP,RFC, Nombre,Domicilio, Telefono,E_mail, Sexo,Edad,NSS,Fotografia,idEstadoCivil from candidato where CURP=%s',
            (id))
        datos = cursor.fetchall()
        cursor.execute(' select * from habilidad ')
        datos1 = cursor.fetchall()
        cursor.execute(' select * from idioma ')
        datos2 = cursor.fetchall()

        cursor.execute(' select * from nivelacademico ')
        datos4 = cursor.fetchall()
        cursor.execute('select a.CURP, b.idIdioma,b.Lenguaje,c.CURP, c.idIdioma, c.Nivel '
                       'from candidato a, idioma b,candidato_has_idioma c '
                       'where a.CURP=c.CURP and b.idIdioma=c.idIdioma and a.CURP=%s ', (id))
        datos5 = cursor.fetchall()
        cursor.execute('select a.CURP, b.idHabilidad,b.Descripcion,c.CURP, c.idHabilidad, c.Experiencia '
                       'from candidato a, habilidad b,candidato_has_habilidad c '
                       'where a.CURP=c.CURP and b.idHabilidad=c.idHabilidad and a.CURP=%s ', (id))
        datos6 = cursor.fetchall()
        cursor.execute('select * from estadocivil order by Descripcion')
        datos7 = cursor.fetchall()

        cursor.execute(
            'select a.CURP, b.idNivelAcademico,b.Descripcion,c.Institucion,c.CURP, c.idNivelAcademico,c.idCarrera ,d.Descripcion '
            'from candidato a, nivelacademico b,candidato_has_nivelacademico c, carrera d '
            ' where a.CURP=c.CURP and b.idNivelAcademico=c.idNivelacademico and c.idCarrera = d.idCarrera and a.CURP=%s ',
            (id))
        datos9 = cursor.fetchall()
        cursor.execute('select * from carrera order by Descripcion')
        datos10 = cursor.fetchall()
        conn.close()
        return render_template("edi_candidato.html", datos=datos, habs=datos1, idiomas=datos2,
                               niveles=datos4, idis=datos5, can_habs=datos6, estados=datos7,
                               nivelesC=datos9, carrerasN=datos10)

## borra los idiomas asociados al candidato
@app.route("/bo_idi_sol/<string:id>/<string:idi>")
def bo_idio_can(id, idi):
    conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
    cursor = conn.cursor()
    cursor.execute('delete from candidato_has_idioma where CURP =%s and idIdioma=%s', (id, idi))
    conn.commit()
    cursor.execute(
        ' select CURP,RFC, Nombre,Domicilio, Telefono,E_mail, Sexo,Edad,NSS,Fotografia,idEstadoCivil from candidato where CURP=%s',
        (id))
    datos = cursor.fetchall()
    cursor.execute(' select * from habilidad ')
    datos1 = cursor.fetchall()
    cursor.execute(' select * from idioma ')
    datos2 = cursor.fetchall()

    cursor.execute(' select * from nivelacademico ')
    datos4 = cursor.fetchall()
    cursor.execute('select a.CURP, b.idIdioma,b.Lenguaje,c.CURP, c.idIdioma, c.Nivel '
                   'from candidato a, idioma b,candidato_has_idioma c '
                   'where a.CURP=c.CURP and b.idIdioma=c.idIdioma and a.CURP=%s ', (id))
    datos5 = cursor.fetchall()
    cursor.execute('select a.CURP, b.idHabilidad,b.Descripcion,c.CURP, c.idHabilidad, c.Experiencia '
                   'from candidato a, habilidad b,candidato_has_habilidad c '
                   'where a.CURP=c.CURP and b.idHabilidad=c.idHabilidad and a.CURP=%s ', (id))
    datos6 = cursor.fetchall()
    cursor.execute('select * from estadocivil order by Descripcion')
    datos7 = cursor.fetchall()

    cursor.execute(
        'select a.CURP, b.idNivelAcademico,b.Descripcion,c.Institucion,c.CURP, c.idNivelAcademico,c.idCarrera ,d.Descripcion '
        'from candidato a, nivelacademico b,candidato_has_nivelacademico c, carrera d '
        ' where a.CURP=c.CURP and b.idNivelAcademico=c.idNivelacademico and c.idCarrera = d.idCarrera and a.CURP=%s ',
        (id))
    datos9 = cursor.fetchall()
    cursor.execute('select * from carrera order by Descripcion')
    datos10 = cursor.fetchall()
    conn.close()
    return render_template("edi_candidato.html", datos=datos, habs=datos1, idiomas=datos2,
                           niveles=datos4, idis=datos5, can_habs=datos6, estados=datos7,
                           nivelesC=datos9, carrerasN=datos10)


## agrega los niveles academicos asociadas del candidato
@app.route("/agrega_nivel_sol/<string:id>/<string:idn>", methods=["POST"])
def agrega_nivel_candidato(id, idn):
    if request.method == 'POST':
        aux_pto = request.form['cannv']
        aux_hab = request.form['nv']
        aux_car = request.form['car']
        aux_ins = request.form['ins']
        conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
        cursor = conn.cursor()
        cursor.execute(
            'insert into candidato_has_nivelacademico (CURP, idNivelAcademico,idCarrera,institucion) values (%s,%s,%s,%s)',
            (aux_pto, aux_hab, aux_car, aux_ins))
        conn.commit()
        cursor.execute(
            ' select CURP,RFC, Nombre,Domicilio, Telefono,E_mail, Sexo,Edad,NSS,Fotografia,idEstadoCivil from candidato where CURP=%s',
            (id))
        datos = cursor.fetchall()
        cursor.execute(' select * from habilidad ')
        datos1 = cursor.fetchall()
        cursor.execute(' select * from idioma ')
        datos2 = cursor.fetchall()

        cursor.execute(' select * from nivelacademico ')
        datos4 = cursor.fetchall()
        cursor.execute('select a.CURP, b.idIdioma,b.Lenguaje,c.CURP, c.idIdioma, c.Nivel '
                       'from candidato a, idioma b,candidato_has_idioma c '
                       'where a.CURP=c.CURP and b.idIdioma=c.idIdioma and a.CURP=%s ', (id))
        datos5 = cursor.fetchall()
        cursor.execute('select a.CURP, b.idHabilidad,b.Descripcion,c.CURP, c.idHabilidad, c.Experiencia '
                       'from candidato a, habilidad b,candidato_has_habilidad c '
                       'where a.CURP=c.CURP and b.idHabilidad=c.idHabilidad and a.CURP=%s ', (id))
        datos6 = cursor.fetchall()
        cursor.execute('select * from estadocivil order by Descripcion')
        datos7 = cursor.fetchall()
        cursor.execute(
            'select a.CURP, b.idNivelAcademico,b.Descripcion,c.Institucion,c.CURP, c.idNivelAcademico,c.idCarrera ,d.Descripcion '
            'from candidato a, nivelacademico b,candidato_has_nivelacademico c, carrera d '
            ' where a.CURP=c.CURP and b.idNivelAcademico=c.idNivelacademico and c.idCarrera = d.idCarrera and a.CURP=%s ',
            (id))
        datos9 = cursor.fetchall()
        cursor.execute('select * from carrera order by Descripcion')
        datos10 = cursor.fetchall()
        conn.close()
        return render_template("edi_candidato.html", datos=datos, habs=datos1, idiomas=datos2,
                               niveles=datos4, idis=datos5, can_habs=datos6, estados=datos7,
                               nivelesC=datos9, carrerasN=datos10)
## borra los niveles academicos asociados al candidato
@app.route("/bo_nivel_sol/<string:id>/<string:idn>/<string:idc>")
def bo_nivel_can(id, idn, idc):
    conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
    cursor = conn.cursor()
    cursor.execute('delete from candidato_has_nivelacademico where CURP =%s and idNivelAcademico=%s and idCarrera=%s',
                   (id, idn, idc))
    conn.commit()
    cursor.execute(
        ' select CURP,RFC, Nombre,Domicilio, Telefono,E_mail, Sexo,Edad,NSS,Fotografia,idEstadoCivil from candidato where CURP=%s',
        (id))
    datos = cursor.fetchall()
    cursor.execute(' select * from habilidad ')
    datos1 = cursor.fetchall()
    cursor.execute(' select * from idioma ')
    datos2 = cursor.fetchall()

    cursor.execute(' select * from nivelacademico ')
    datos4 = cursor.fetchall()
    cursor.execute('select a.CURP, b.idIdioma,b.Lenguaje,c.CURP, c.idIdioma, c.Nivel '
                   'from candidato a, idioma b,candidato_has_idioma c '
                   'where a.CURP=c.CURP and b.idIdioma=c.idIdioma and a.CURP=%s ', (id))
    datos5 = cursor.fetchall()
    cursor.execute('select a.CURP, b.idHabilidad,b.Descripcion,c.CURP, c.idHabilidad, c.Experiencia '
                   'from candidato a, habilidad b,candidato_has_habilidad c '
                   'where a.CURP=c.CURP and b.idHabilidad=c.idHabilidad and a.CURP=%s ', (id))
    datos6 = cursor.fetchall()
    cursor.execute('select * from estadocivil order by Descripcion')
    datos7 = cursor.fetchall()

    cursor.execute(
        'select a.CURP, b.idNivelAcademico,b.Descripcion,c.Institucion,c.CURP, c.idNivelAcademico,c.idCarrera ,d.Descripcion '
        'from candidato a, nivelacademico b,candidato_has_nivelacademico c, carrera d '
        ' where a.CURP=c.CURP and b.idNivelAcademico=c.idNivelacademico and c.idCarrera = d.idCarrera and a.CURP=%s ',
        (id))
    datos9 = cursor.fetchall()
    cursor.execute('select * from carrera order by Descripcion')
    datos10 = cursor.fetchall()
    conn.close()
    return render_template("edi_candidato.html", datos=datos, habs=datos1, idiomas=datos2,
                           niveles=datos4, idis=datos5, can_habs=datos6, estados=datos7,
                           nivelesC=datos9, carrerasN=datos10)
## elimina al candidato de la base de datos
@app.route('/bo_solicitante/<string:id>')
def bo_candidato(id):
    conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) from candidato_has_idioma WHERE CURP = %s", (id))
    s_niv=cursor.fetchone()
    cursor.execute("SELECT COUNT(*) from candidato_has_habilidad WHERE CURP= %s", (id))
    c_niv=cursor.fetchone()
    cursor.execute("SELECT COUNT(*) from candidato_has_nivelacademico WHERE CURP= %s", (id))
    c_hab=cursor.fetchone()
    #print(s_niv)
    #print(c_niv)
    if s_niv[0] == 0 and c_niv[0] == 0 and c_hab[0] == 0:
        cursor.execute('delete from candidato_has_idioma where CURP = %s',(id))
        conn.commit()
        cursor.execute('delete from candidato_has_habilidad where CURP = %s',(id))
        conn.commit()
        cursor.execute('delete from candidato_has_nivelacademico where CURP =  %s',(id))
        conn.commit()
        cursor.execute('delete from candidato where CURP =  %s',(id))
        conn.commit()
        conn.close()
        return redirect(url_for('candidato'))
    else:
        error = "no se puede eliminar ese elemento, ya que tiene relacion con otras tablas, elimina las relaciones y vuelve a intentarlo"


        conn.close()
        return render_template("error.html", error=error,paginaant="/candidato")


###########################################################################################################################################################
##########################################################catalogo de nivel academico###################################################
## abre el html de agr_nivel
@app.route('/nvo_nivel')
def nvo_nivel():

    return render_template("agr_nivel.html")

## abre el html con una tabla donde estan todos los niveles academicos y la opcion de agregar, editar y borrar dichos niveles
@app.route('/nivelacademico')
def nivelacademico():
    conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
    cursor = conn.cursor()
    cursor.execute('select idNivelAcademico, descripcion from nivelacademico order by descripcion')
    datos = cursor.fetchall()
    return render_template("Nivel_Academico.html", niveles=datos)

## agrega un nivel academico a la base de datos
@app.route('/agrega_nivel', methods=['POST'])
def agrega_nivel():
    if request.method == 'POST':
        aux_descripcion = request.form['descripcion']
        conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
        cursor = conn.cursor()
        cursor.execute('insert into nivelacademico (Descripcion) values (%s)', (aux_descripcion))
        conn.commit()
    return redirect(url_for('nivelacademico'))

## abre el html para editar un nivel academico
@app.route('/ed_nivel/<string:id>')
def ed_nivel(id):
    conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
    cursor = conn.cursor()
    cursor.execute('select idNivelAcademico, descripcion from nivelacademico where idNivelAcademico = %s', (id))
    dato = cursor.fetchall()
    return render_template("edi_nivel.html", nivel=dato[0])

## cambia los datos de la base de datos por lo que ya estan modificados
@app.route('/modifica_nivel/<string:id>', methods=['POST'])
def modifica_nivel(id):
    if request.method == 'POST':
        descrip = request.form['descripcion']
        conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
        cursor = conn.cursor()
        cursor.execute('update nivelacademico set  descripcion=%s where idNivelAcademico= %s', (descrip, id))
        conn.commit()
        conn.close()
    return redirect(url_for('nivelacademico'))

## borra el nivel academico
@app.route('/bo_nivel/<string:id>')
def bo_nivel(id):
    conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) from solicitud WHERE idNivelAcademico = %s", (id))
    s_niv=cursor.fetchone()
    cursor.execute("SELECT COUNT(*) from candidato_has_nivelacademico WHERE idNivelAcademico = %s", (id))
    c_niv=cursor.fetchone()
    #print(s_niv)
    #print(c_niv)
    if s_niv[0] == 0 and c_niv[0] == 0:
        cursor.execute('delete  from nivelacademico where idNivelAcademico = %s', (id))
        conn.commit()
        conn.close()

        return redirect(url_for('nivelacademico'))
    else:
        error = "no se puede eliminar ese elemento, ya que tiene relacion con otras tablas, elimina las relaciones y vuelve a intentarlo"
        conn.close()
        return render_template("error.html", error=error,paginaant="/nivelacademico")

##########################################################################################################################################################


##########################################################catalogo de habilidad ############################################################
## abre el html de habilidad
@app.route("/nvo_habilidad")

def nvo_habilidad():
    return render_template("Habilidad.html")

## agrega una habilidad a la base de datos
@app.route("/agrega_habilidad", methods=["POST"])
def agrega_habilidad():
    if request.method == 'POST':
        aux_descripcion = request.form['Descripcion']

        conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
        cursor = conn.cursor()
        cursor.execute('insert into habilidad (Descripcion ) values (%s)', (aux_descripcion))
        conn.commit()
        conn.close()
    return redirect(url_for('sel_habilidades'))

## abre el html con una tabla donde estan todas las habilidades  y la opcion de agregar, editar y borrar
@app.route('/habilidad')
def sel_habilidades():
    conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
    cursor = conn.cursor()
    cursor.execute('select idHabilidad,Descripcion from habilidad order by descripcion')
    datos = cursor.fetchall()
    conn.close()
    return render_template("tabla.html", habilidades=datos)

## abre el html para editar una habilidad
@app.route('/ed_habilidad/<string:id>')
def ed_habilidad(id):
    conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
    cursor = conn.cursor()
    cursor.execute('select idHabilidad,Descripcion  from habilidad where idHabilidad = %s', (id))
    dato = cursor.fetchall()
    conn.close()
    return render_template("editar_habilidad.html", habilidad=dato)

## cambia los datos de la base de datos por lo que ya estan modificados
@app.route('/modifica_habilidad/<string:id>', methods=['POST'])
def modifica_habilidad(id):
    if request.method == 'POST':
        aux_descripcion = request.form['descripcion']

        conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
        cursor = conn.cursor()
        cursor.execute('update habilidad set Descripcion=%s where idHabilidad=%s',
                       (aux_descripcion, id))
        conn.commit()
        conn.close()
    return redirect(url_for('sel_habilidades'))

## borra la habilidad
@app.route('/borrar_habilidad/<string:id>')
def borrar_habilidad(id):
    conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) from puesto_has_habilidad WHERE idHabilidad = %s", (id))
    s_niv=cursor.fetchone()
    cursor.execute("SELECT COUNT(*) from candidato_has_habilidad WHERE idHabilidad= %s", (id))
    c_niv=cursor.fetchone()
    #print(s_niv)
    #print(c_niv)
    if s_niv[0] == 0 and c_niv[0] == 0:
        cursor.execute('delete from habilidad where idHabilidad = {0}'.format(id))
        conn.commit()
        conn.close()
        return redirect(url_for('sel_habilidades'))

    else:
        error = "no se puede eliminar ese elemento, ya que tiene relacion con otras tablas, elimina las relaciones y vuelve a intentarlo"
        conn.close()
        return render_template("error.html", error=error,paginaant="/habilidad")

##########################################################################################################################################################


########################################################## catalogo de carrera #############################################################
## abre el html de agr_carrera
@app.route('/nva_carrera')
def nva_carrera():
    return render_template("agr_carrera.html")

## abre el html con una tabla donde estan todos las carreras y la opcion de agregar, editar y borrar
@app.route('/carrera')
def carrera():
    conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
    cursor = conn.cursor()
    cursor.execute('select idCarrera, descripcion from carrera order by descripcion')
    datos = cursor.fetchall()
    conn.close()
    return render_template("Carrera.html", niveles=datos)

## agrega una carrera a la base de datos
@app.route('/agr_carrera', methods=['POST'])
def agrega_carrera():
    if request.method == 'POST':
        aux_descripcion = request.form['descripcion']
        conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
        cursor = conn.cursor()
        cursor.execute('insert into carrera (Descripcion) values (%s)', (aux_descripcion))
        conn.commit()
        conn.close()
    return redirect(url_for('carrera'))

## abre el html para editar una carrera
@app.route('/ed_carrera/<string:id>')
def ed_carrera(id):
    conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
    cursor = conn.cursor()
    cursor.execute('select idCarrera, descripcion from carrera where idCarrera = %s', (id))
    dato = cursor.fetchall()
    conn.close()
    return render_template("edi_carrera.html", nivel=dato[0])

## cambia los datos de la base de datos por lo que ya estan modificados
@app.route('/modifica_carrera/<string:id>', methods=['POST'])
def modifica_carrera(id):
    if request.method == 'POST':
        descrip = request.form['descripcion']
        conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
        cursor = conn.cursor()
        cursor.execute('update carrera set  descripcion=%s where idCarrera=%s', (descrip, id))
        conn.commit()
        conn.close()
    return redirect(url_for('carrera'))

## borra la carrera
@app.route('/bo_carrera/<string:id>')
def bo_carrera(id):
    conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) from solicitud WHERE idCarrera = %s", (id))
    s_niv=cursor.fetchone()
    cursor.execute("SELECT COUNT(*) from candidato_has_nivelacademico WHERE idCarrera = %s", (id))
    c_niv=cursor.fetchone()
    #print(s_niv)
    #print(c_niv)
    if s_niv[0] == 0 and c_niv[0] == 0:
        cursor.execute('delete from carrera where idCarrera = {0}'.format(id))
        conn.commit()
        conn.close()
        return redirect(url_for('carrera'))

    else:
        error = "no se puede eliminar ese elemento, ya que tiene relacion con otras tablas, elimina las relaciones y vuelve a intentarlo"
        conn.close()
        return render_template("error.html", error=error,paginaant="/carrera")

##########################################################################################################################################################


########################################################## catalogo de idioma ###################################################


## abre el html con una tabla donde estan todos los idiomas y la opcion de agregar, editar y borrar
@app.route("/idioma")
def idioma():
    conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
    cursor = conn.cursor()
    cursor.execute(
        'select * from idioma order by Lenguaje')
    datos = cursor.fetchall()
    conn.close()
    return render_template("idioma.html", datos=datos)

## abre el html de agr_idioma
@app.route("/nvo_idioma")
def nvo_idioma():
    return render_template("agr_idioma.html")
## abre el html para editar un idioma

@app.route('/ed_idioma/<string:id>')
def edi_idioma(id):
    conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
    cursor = conn.cursor()

    cursor.execute(
        'select Lenguaje from idioma WHERE ididioma = %s', (id))
    idiomas = cursor.fetchall()
    #print(idiomas)
    conn.close()
    return render_template('edi_idioma.html', idiomas=idiomas, dato=id)

## cambia los datos de la base de datos por lo que ya estan modificados
@app.route('/edita_idioma/<string:id>', methods=["post"])
def edita_idioma(id):
    if request.method == 'POST':
        aux_descripcion = request.form['lenguaje']

        conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')

        cursor = conn.cursor()

        cursor.execute("""  UPDATE idioma SET lenguaje = %s  WHERE ididioma = %s;  """,
                       (aux_descripcion, id))
        conn.commit()
        conn.close()
    return redirect(url_for("idioma"))

# borra el idioma
@app.route("/bo_idioma/<string:id>")
def bo_idioma(id):
    conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) from puesto_has_idioma WHERE idIdioma = %s", (id))
    s_niv=cursor.fetchone()
    cursor.execute("SELECT COUNT(*) from candidato_has_idioma WHERE idIdioma = %s", (id))
    c_niv=cursor.fetchone()
    #print(s_niv)
    #print(c_niv)
    if s_niv[0] == 0 and c_niv[0] == 0:
        cursor.execute(""" DELETE FROM idioma WHERE ididioma = %s;""", (id))
        conn.commit()
        conn.close()
        return redirect(url_for("idioma"))

    else:
        error = "no se puede eliminar ese elemento, ya que tiene relacion con otras tablas, elimina las relaciones y vuelve a intentarlo"
        conn.close()
        return render_template("error.html", error=error,paginaant="/idioma")

## agrega un idioma a la base de datos

@app.route("/agrega_idioma", methods=["POST"])
def agrega_idioma():
    if request.method == 'POST':
        nombre = request.form['lenguaje']
        conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO   idioma (Lenguaje) VALUES (%s);''', (nombre))
        conn.commit()
        conn.close()
    return redirect(url_for('idioma'))

##########################################################################################################################################################




##########################################################catalogo de puesto ###################################################
## abre el html con una tabla donde estan todos los puestos y la opcion de agregar, editar y borrar
@app.route('/puesto')
def puesto():
    conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
    cursor = conn.cursor()
    cursor.execute(
        'select idPuesto, Descripcion, SalarioAnual, Beneficios, Bonos, Aprobacion from puesto order by Descripcion')

    datos = cursor.fetchall()
    conn.close()
    return render_template("puesto.html", puestos=datos)

## abre el html de agr_puesto
@app.route("/agregar_puesto")
def agregar_puesto():
    return render_template("agr_puesto.html")
## agrega un puesto a la base de datos

@app.route('/agrega_puesto', methods=["POST"])
def agrega_puesto():
    if request.method == 'POST':
        aux_des = request.form['descripcion']
        aux_sal = request.form['salario']
        aux_ben = request.form['beneficios']
        aux_bon = request.form['bonos']
        aux_aut = request.form['autorizar']
        conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
        cursor = conn.cursor()
        cursor.execute(
            'insert into puesto (Descripcion, SalarioAnual, Beneficios, Bonos,  Aprobacion) values (%s,%s,%s,%s,%s)',
            (aux_des, aux_sal, aux_ben, aux_bon, aux_aut))
        conn.commit()
        cursor.execute(
            'select idPuesto, Descripcion, SalarioAnual, Beneficios, Bonos,Aprobacion from puesto where idPuesto=(select max(idPuesto) from puesto)')
        datos = cursor.fetchall()
        cursor.execute('select a.idPuesto, b.idHabilidad,b.Descripcion,c.idPuesto, c.idHabilidad, c.Experiencia '
                       ' from puesto a, habilidad b,puesto_has_habilidad c '
                       ' where a.idPuesto=c.idPuesto and b.idHabilidad=c.idHabilidad and c.idPuesto=(select max(idPuesto) from puesto)')
        datos1 = cursor.fetchall()
        cursor.execute('select a.idPuesto, b.idIdioma,b.Lenguaje,c.idPuesto, c.idIdioma, c.Nivel '
                       'from puesto a, idioma b,puesto_has_idioma c '
                       'where a.idPuesto=c.idPuesto and b.idIdioma=c.idIdioma and c.idPuesto=(select max(idPuesto) from puesto)')
        datos2 = cursor.fetchall()
        cursor.execute('select idhabilidad, Descripcion from habilidad order by Descripcion')
        datos3 = cursor.fetchall()
        cursor.execute('select idIdioma, Lenguaje from idioma order by Lenguaje')
        datos4 = cursor.fetchall()
        conn.close()
        return render_template("edi_puesto.html", puestos=datos, pue_habs=datos1, pue_idis=datos2, habs=datos3,
                               idiomas=datos4)

## cambia los datos de la base de datos por lo que ya estan modificados
@app.route('/modifica_puesto/<string:id>', methods=['POST'])
def modifica_puesto(id):
    if request.method == 'POST':
        aux_des = request.form['descripcion']

        aux_sal = request.form['salario']
        print(aux_sal)
        aux_ben = request.form['beneficios']
        aux_bon = request.form['bonos']
        aux_aut = request.form['autorizar']
        conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
        cursor = conn.cursor()
        cursor.execute(
            'update puesto set Descripcion=%s, SalarioAnual=%s,Beneficios=%s, Bonos=%s, Aprobacion=%s where idpuesto=%s',
            (aux_des, aux_sal, aux_ben, aux_bon, aux_aut, id))

        conn.commit()
        conn.close()
    return redirect(url_for('puesto'))

## abre el html para editar un puesto
@app.route('/ed_puesto/<string:id>')
def ed_puesto(id):
    conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
    cursor = conn.cursor()
    cursor.execute('select idPuesto, Descripcion, SalarioAnual, Beneficios, Bonos, Aprobacion '
                   'from puesto where idPuesto=%s', (id))
    datos = cursor.fetchall()
    cursor.execute(
        'select a.idPuesto, b.idHabilidad,b.Descripcion,c.idPuesto, c.idHabilidad,c.Experiencia  from puesto a, habilidad b,puesto_has_habilidad c  where a.idPuesto=c.idPuesto and b.idHabilidad=c.idHabilidad and c.idPuesto=%s',
        (id))
    datos1 = cursor.fetchall()
    cursor.execute(
        'select a.idPuesto, b.idIdioma,b.Lenguaje,c.idPuesto, c.idIdioma, c.Nivel from puesto a, idioma b,puesto_has_idioma c where a.idPuesto=c.idPuesto and b.idIdioma=c.idIdioma and c.idPuesto=%s',
        (id))

    datos2 = cursor.fetchall()
    cursor.execute('select idhabilidad, Descripcion from habilidad order by Descripcion')
    datos3 = cursor.fetchall()
    cursor.execute('select idIdioma, Lenguaje from idioma order by Lenguaje')
    datos4 = cursor.fetchall()
    conn.close()
    return render_template("edi_puesto.html", puestos=datos, pue_habs=datos1,
                           pue_idis=datos2, habs=datos3, idiomas=datos4)

## borra el nivel academico
@app.route('/bo_puesto/<string:id>')
def bo_puesto(id):
    conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) from puesto_has_habilidad WHERE idPuesto = %s", (id))
    ph_pue=cursor.fetchone()
    cursor.execute("SELECT COUNT(*) from puesto_has_idioma WHERE idPuesto= %s", (id))
    pi_pue=cursor.fetchone()
    cursor.execute("SELECT COUNT(*) from solicitud WHERE idPuesto= %s", (id))
    s_pue=cursor.fetchone()
    if ph_pue[0] == 0 and pi_pue[0] == 0 and s_pue[0] == 0:
        cursor.execute('delete from puesto_has_idioma where idPuesto = {0}'.format(id))
        conn.commit()
        cursor.execute('delete from puesto_has_habilidad where idPuesto = {0}'.format(id))
        conn.commit()
        cursor.execute('delete from puesto where idPuesto = {0}'.format(id))
        conn.commit()
        conn.close()
        return redirect(url_for('puesto'))
    else:
        error = "no se puede eliminar ese elemento, ya que tiene relacion con otras tablas, elimina las relaciones y vuelve a intentarlo"
        conn.close()
        return render_template("error.html", error=error,paginaant="/puesto")

## agrega una habilidad que este ligada al puesto
@app.route('/agrega_hab_pto', methods=['POST'])
def agrega_hab_pto():
    if request.method == 'POST':
        aux_pto = request.form['pto']
        aux_hab = request.form['habil']
        aux_exp = request.form['expe']
        conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
        cursor = conn.cursor()
        cursor.execute('insert into puesto_has_habilidad (idPuesto, idHabilidad,Experiencia) values (%s,%s,%s)',
                       (aux_pto, aux_hab, aux_exp))
        conn.commit()
        cursor.execute(
            'select idPuesto, Descripcion, SalarioAnual, Beneficios, Bonos,Aprobacion from puesto where idPuesto=%s',
            (aux_pto))
        datos = cursor.fetchall()
        cursor.execute(
            'select a.idPuesto, b.idHabilidad,b.Descripcion,c.idPuesto,c.idHabilidad, c.Experiencia from puesto a, habilidad b,puesto_has_habilidad c  where a.idPuesto=c.idPuesto and b.idHabilidad=c.idHabilidad and c.idPuesto=%s',
            (aux_pto))
        datos1 = cursor.fetchall()
        cursor.execute(
            'select a.idPuesto, b.idIdioma,b.Lenguaje,c.idPuesto, c.idIdioma,c.Nivel from puesto a, idioma b,puesto_has_idioma c where a.idPuesto=c.idPuesto and b.idIdioma=c.idIdioma and c.idPuesto=%s',
            (aux_pto))
        datos2 = cursor.fetchall()
        cursor.execute('select idhabilidad, Descripcion from habilidad order by  Descripcion')

        datos3 = cursor.fetchall()
        cursor.execute('select idIdioma, Lenguaje from idioma order by Lenguaje')
        datos4 = cursor.fetchall()
        conn.close()
        return render_template("edi_puesto.html", puestos=datos, pue_habs=datos1, pue_idis=datos2, habs=datos3,
                               idiomas=datos4)

## agrega in idioma que este ligado con el puesto
@app.route('/agrega_idio_pto', methods=['POST'])
def agrega_idio_pto():
    if request.method == 'POST':
        aux_pto = request.form['ptoi']
        aux_idi = request.form['idio']
        aux_niv = request.form['nive']
        conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO `puesto_has_idioma` (`idPuesto`, `idIdioma`, `Nivel`) values(%s,%s,%s)',
                       (aux_pto, aux_idi, aux_niv))
        conn.commit()
        cursor.execute(
            'select idPuesto, Descripcion, SalarioAnual, Beneficios, Bonos,Aprobacion from puesto where idPuesto=%s',
            (aux_pto))
        datos = cursor.fetchall()
        cursor.execute(
            'select a.idPuesto, b.idHabilidad,b.Descripcion,c.idPuesto,c.idHabilidad, c.Experiencia  from puesto a, habilidad b,puesto_has_habilidad c  where a.idPuesto=c.idPuesto and b.idHabilidad=c.idHabilidad and c.idPuesto=%s',
            (aux_pto))
        datos1 = cursor.fetchall()
        cursor.execute(
            'select a.idPuesto, b.idIdioma,b.Lenguaje,c.idPuesto, c.idIdioma,c.Nivel from puesto a, idioma b,puesto_has_idioma c where a.idPuesto=c.idPuesto and b.idIdioma=c.idIdioma and c.idPuesto=%s',
            (aux_pto))
        datos2 = cursor.fetchall()
        cursor.execute('select idhabilidad, Descripcion from habilidad order by Descripcion')
        datos3 = cursor.fetchall()
        cursor.execute('select idIdioma, Lenguaje from idioma order by Lenguaje')
        datos4 = cursor.fetchall()
        conn.close()
        return render_template("edi_puesto.html", puestos=datos, pue_habs=datos1, pue_idis=datos2, habs=datos3,
                               idiomas=datos4)
## borra una habilidad que haya estado ligada al puesto

@app.route('/bo_hab_pto/<string:idP>/<string:idH>')
def bo_hab_pto(idP, idH):
    conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
    cursor = conn.cursor()
    cursor.execute('delete from puesto_has_habilidad where idPuesto =%s and idHabilidad=%s', (idP, idH))
    conn.commit()
    cursor.execute(
        'select idPuesto, Descripcion, SalarioAnual, Beneficios, Bonos, Aprobacion from puesto where idPuesto=%s',
        (idP))
    datos = cursor.fetchall()
    cursor.execute(
        'select a.idPuesto, b.idHabilidad,b.Descripcion,c.idPuesto, c.idHabilidad,c.Experiencia  from puesto a, habilidad b,puesto_has_habilidad c  where a.idPuesto=c.idPuesto and b.idHabilidad=c.idHabilidad and c.idPuesto=%s',
        (idP))
    datos1 = cursor.fetchall()
    cursor.execute(
        'select a.idPuesto, b.idIdioma,b.Lenguaje,c.idPuesto, c.idIdioma, c.Nivel from puesto a, idioma b,puesto_has_idioma c where a.idPuesto=c.idPuesto and b.idIdioma=c.idIdioma and c.idPuesto=%s',
        (idP))
    datos2 = cursor.fetchall()
    cursor.execute('select idhabilidad, Descripcion from habilidad order by Descripcion')
    datos3 = cursor.fetchall()
    cursor.execute('select idIdioma, Lenguaje from idioma order by Lenguaje')
    datos4 = cursor.fetchall()
    conn.close()
    return render_template("edi_puesto.html", puestos=datos, pue_habs=datos1, pue_idis=datos2, habs=datos3,
                           idiomas=datos4)

## borra un idioma que haya estado ligado al puesto
@app.route('/bo_idi_pto/<string:idP>/<string:idI>')
def bo_idi_pto(idP, idI):
    conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
    cursor = conn.cursor()
    cursor.execute('delete from puesto_has_idioma where idPuesto =%s and idIdioma=%s', (idP, idI))
    conn.commit()
    cursor.execute('select idPuesto, Descripcion, SalarioAnual, Beneficios, Bonos, Aprobacion '
                   'from puesto where idPuesto=%s', (idP))
    datos = cursor.fetchall()
    cursor.execute(
        'select a.idPuesto, b.idHabilidad,b.Descripcion,c.idPuesto, c.idHabilidad, c.Experiencia  from puesto a, habilidad b,puesto_has_habilidad c where a.idPuesto=c.idPuesto and b.idHabilidad=c.idHabilidad and c.idPuesto=%s',
        (idP))
    datos1 = cursor.fetchall()
    cursor.execute(
        'select a.idPuesto, b.idIdioma,b.Lenguaje,c.idPuesto, c.idIdioma, c.Nivel from puesto a, idioma b,puesto_has_idioma c where a.idPuesto=c.idPuesto and b.idIdioma=c.idIdioma and c.idPuesto=%s',
        (idP))
    datos2 = cursor.fetchall()
    cursor.execute('select idhabilidad, Descripcion from habilidad order by Descripcion')
    datos3 = cursor.fetchall()
    cursor.execute('select idIdioma, Lenguaje from idioma order by Lenguaje')
    datos4 = cursor.fetchall()
    conn.close()
    return render_template("edi_puesto.html", puestos=datos, pue_habs=datos1, pue_idis=datos2, habs=datos3,
                           idiomas=datos4)
##########################################################################################################################################################

##########################################################catalogo de area ###################################################
## abre el html de agr_area
@app.route('/nvo_area')
def nvo_area():
    return render_template("agr_area.html")

## abre el html con una tabla donde estan todas las areas y la opcion de agregar, editar y borrar
@app.route('/area')
def area():
    conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
    cursor = conn.cursor()
    cursor.execute('select idArea, AreaNombre, AreaDescripcion from area order by AreaDescripcion')
    datos = cursor.fetchall()
    conn.close()
    return render_template("area.html", areas=datos)

## agrega un area a la base de datos
@app.route('/agrega_area', methods=['POST'])
def agrega_area():
    if request.method == 'POST':
        aux_Nombre = request.form['nombre']
        aux_Descripcion = request.form['descripcion']
        conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
        cursor = conn.cursor()
        cursor.execute('insert into area (AreaNombre,AreaDescripcion) values (%s,%s)', (aux_Nombre, aux_Descripcion))
        conn.commit()
        conn.close()
    return redirect(url_for('area'))
## abre el html para editar un area

@app.route('/edita_area/<string:id>')
def edita_area(id):
    conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
    cursor = conn.cursor()
    cursor.execute('select idArea, AreaNombre, AreaDescripcion from area where idArea = %s', (id))
    dato = cursor.fetchall()
    conn.close()
    return render_template("edi_area.html", area=dato[0])

## cambia los datos de la base de datos por lo que ya estan modificados
@app.route('/modifica_area/<string:id>', methods=['POST'])
def modifica_area(id):
    if request.method == 'POST':
        nombr = request.form['nombre']
        descrip = request.form['descripcion']
        conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
        cursor = conn.cursor()
        cursor.execute('update area set  AreaNombre=%s,AreaDescripcion=%s where idArea=%s', (nombr, descrip, id))
        conn.commit()
        conn.close()
    return redirect(url_for('area'))

## borra el area
@app.route('/borrar_area/<string:id>')
def borrar_area(id):
    conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) from solicitud WHERE idArea = %s", (id))
    s_area=cursor.fetchone()
    if s_area[0] == 0:
        cursor.execute('delete from area where idArea = {0}'.format(id))
        conn.commit()
        conn.close()
        return redirect(url_for("area"))

    else:
        error = "no se puede eliminar ese elemento, ya que tiene relacion con otras tablas, elimina las relaciones y vuelve a intentarlo"
        conn.close()
        return render_template("error.html", error=error,paginaant="/area")

##########################################################################################################################################################



##########################################################catalogo de medio de publicidad ###################################################
## abre el html para agregar un medio de publicidad
@app.route('/medio_publicidad')
def medio_publicidadl():
    return render_template("Medio de publicidad.html")

## abre el html con una tabla donde estan todos los medios de publicidad y la opcion de agregar, editar y borrar
@app.route('/medio_de_publicidad')
def tabla_medio():
    conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
    cursor = conn.cursor()
    cursor.execute('select idMedioPublicidad,Descripcion from mediopublicidad order by descripcion')
    datos = cursor.fetchall()
    conn.close()
    return render_template("tabla_publicidad.html", medios=datos)

## agrega un medio de publicidad a la base de datos
@app.route("/agrega_medio_publicidad", methods=["POST"])
def agrega_medio_publicidad():
    if request.method == 'POST':
        aux_descripcion = request.form['des_publicidad']
        conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
        cursor = conn.cursor()
        cursor.execute('insert into mediopublicidad (Descripcion) values (%s)', (aux_descripcion))
        conn.commit()
        conn.close()
    return tabla_medio()

## abre el html para editar un medio de publicidad
@app.route('/ed_medio/<string:id>')
def ed_medio(id):
    conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
    cursor = conn.cursor()
    cursor.execute('select idMedioPublicidad,Descripcion from mediopublicidad where idMedioPublicidad = %s', (id))
    dato = cursor.fetchall()
    conn.close()
    return render_template("editar_medio.html", medio=dato[0])

## cambia los datos de la base de datos por lo que ya estan modificados
@app.route('/modifica_medio/<string:id>', methods=['POST'])
def modifica_medio(id):
    if request.method == 'POST':
        aux_descripcion = request.form['des_publicidad']
        conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
        cursor = conn.cursor()
        cursor.execute('update mediopublicidad set Descripcion=%s where idMedioPublicidad=%s', (aux_descripcion, id))
        conn.commit()
        conn.close()
    return redirect(url_for("tabla_medio"))

## borra el medio de publicidad
@app.route('/borrar_medio/<string:id>')
def borrar_medio(id):
    conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) from anuncio WHERE idMedioPublicidad = %s", (id))
    a_mpublicidad=cursor.fetchone()
    if a_mpublicidad[0] == 0:
        cursor.execute('delete from mediopublicidad where idMedioPublicidad = {0}'.format(id))
        conn.commit()
        conn.close()
        return redirect(url_for("tabla_medio"))
    else:
        error = "no se puede eliminar ese elemento, ya que tiene relacion con otras tablas, elimina las relaciones y vuelve a intentarlo"
        conn.close()
        return render_template("error.html", error=error,paginaant="/medio_de_publicidad")
##########################################################################################################################################################


##########################################################catalogo de contacto ###################################################
## abre el html para agregar un contacto
@app.route('/nvo_contacto')
def nvo_contacto():
    return render_template("agr_contacto.html")

## abre el html con una tabla donde estan todos los contactos y la opcion de agregar, editar y borrar
@app.route('/contacto')
def contacto():
    conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
    cursor = conn.cursor()
    cursor.execute('select idcontacto, Nombre, Domicilio, Razon_Social,Telefono from contacto  order by Nombre')
    dato = cursor.fetchall()
    # print(dato)
    conn.close()
    return render_template("Contacto.html", niveles=dato)

## agrega un contacto a la base de datos
@app.route("/agrega_contacto", methods=["POST"])
def agrega_contacto():
    if request.method == 'POST':
        aux_nombre = request.form['Nombre']
        aux_domicilio = request.form['domicilio']
        aux_razon = request.form['razonsocial']
        aux_numero = request.form['Numero']
        conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
        cursor = conn.cursor()
        cursor.execute('insert into contacto (Nombre, Domicilio, Razon_Social,Telefono) values (%s,%s,%s,%s)',
                       (aux_nombre, aux_domicilio, aux_razon, aux_numero))
        conn.commit()
        conn.close()
    return redirect(url_for('contacto'))

## abre el html para editar un contacto
@app.route('/ed_contacto/<string:id>')
def ed_contacto(id):
    conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
    cursor = conn.cursor()
    cursor.execute('select idcontacto, Nombre, Domicilio, Razon_Social,Telefono from contacto where idContacto = %s',
                   (id))
    dato = cursor.fetchall()
    conn.close()
    return render_template("edi_contacto.html", niveles=dato, id=id)

## cambia los datos de la base de datos por lo que ya estan modificados
@app.route('/modifica_contacto/<string:id>', methods=['POST'])
def modifica_contacto(id):
    if request.method == 'POST':
        descrip = request.form['Nombre']
        print(descrip)
        domic = request.form['domicilio']
        print(domic)
        razsoc = request.form['razonsocial']
        print(razsoc)
        num = request.form['Numero']
        print(num)
        conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
        cursor = conn.cursor()
        cursor.execute('update contacto set  Nombre=%s,Domicilio=%s,Razon_Social=%s,Telefono=%s where idContacto=%s',
                       (descrip, domic, razsoc, num, id))
        conn.commit()
        conn.close()
    return redirect(url_for('contacto'))

## borra el contacto
@app.route('/bo_contacto/<string:id>')
def bo_contacto(id):
    conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) from anuncio WHERE idcontacto = %s", (id))
    a_contacto=cursor.fetchone()
    if a_contacto[0] == 0:
        cursor.execute('delete from contacto where idcontacto = {0}'.format(id))
        conn.commit()
        conn.close()
        return redirect(url_for("contacto"))
    else:
        error = "no se puede eliminar ese elemento, ya que tiene relacion con otras tablas, elimina las relaciones y vuelve a intentarlo"
        conn.close()
        return render_template("error.html", error=error,paginaant="/contacto")
##########################################################################################################################################################


##########################################################Datos de la empresa###################################################


## muesta los datos de esta empresa y la opcion de modificarlos

@app.route('/datos de empresa')
def datos():
    conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
    cursor = conn.cursor()
    cursor.execute(
        'select Nombre_de_empresa, Descripcion,Estructura_Juridica,Razonsocial,E_mail,Domicilio,Telefono,Encargado,CIF_empresa from datos_de_empresa')
    datos = cursor.fetchall()
    conn.close()
    return render_template("Datos.html", niveles=datos)



## cambia los datos de la base de datos por lo que ya estan modificados
@app.route('/modifica_datos/<string:id>', methods=['POST'])
def modifica_datos(id):
    if request.method == 'POST':
        nom = request.form['Nombre_de_empresa']
        des = request.form['Descripcion']
        est = request.form['Estructura_Juridica']
        raz = request.form['Razon_social']
        ema = request.form['Email']
        dom = request.form['Domicilio']
        tel = request.form['Telefono']
        enc = request.form['Encargado']

        conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
        cursor = conn.cursor()
        cursor.execute(
            'update datos_de_empresa set Nombre_de_empresa=%s, Descripcion=%s, Estructura_juridica=%s ,Razonsocial=%s, E_mail=%s, Domicilio=%s, Telefono=%s, Encargado=%s  where Nombre_de_empresa= %s ',
            (nom, des, est, raz, ema, dom, tel, enc, id))
        conn.commit()
        conn.close()
    return redirect(url_for('datos'))

## abre el html con los datos para modificar
@app.route('/ed_datos/<string:id>')
def edi_datos(id):
    conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
    cursor = conn.cursor()
    cursor.execute(
        'select Nombre_de_empresa from datos_de_empresa where Nombre_de_empresa = %s', (id))
    nom = cursor.fetchall()
    cursor.execute(
        'select Descripcion from datos_de_empresa ')
    des = cursor.fetchall()
    cursor.execute(
        'select Estructura_Juridica from datos_de_empresa ')
    est = cursor.fetchall()
    cursor.execute(
        'select Razonsocial from datos_de_empresa')
    raz = cursor.fetchall()
    cursor.execute(
        'select E_mail from datos_de_empresa')
    ema = cursor.fetchall()
    cursor.execute(
        'select Domicilio from datos_de_empresa')
    dom = cursor.fetchall()
    cursor.execute(
        'select Telefono from datos_de_empresa')
    tel = cursor.fetchall()
    cursor.execute(
        'select Encargado from datos_de_empresa')
    enc = cursor.fetchall()
    cursor.execute(
        'select CIF_empresa from datos_de_empresa')
    cif = cursor.fetchall()
    conn.close()
    return render_template('edita_empresa.html', nom=nom, des=des, est=est, raz=raz, ema=ema, dom=dom, tel=tel, enc=enc,
                           cif=cif, dato=id)
##########################################################################################################################################################

##---------------------------------------------terminan los catalogos y comienzan los procesos------------------------------------------------------------##
########################################################## solicitud ###################################################
## abre el html con una tabla donde estan todas las solicitudes y la opcion de agregar, editar y borrar
@app.route("/solicitud")
def solicitud():
    conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
    cursor = conn.cursor()
    cursor.execute('''select a.idSolicitud,a.FechaSolicitud,a.NumeroVacante,a.idArea,b.AreaDescripcion,a.idPuesto,c.Descripcion,a.idNivelAcademico,d.Descripcion,a.idCarrera,e.Descripcion,a.idEstatus_Solicitud,f.Descripcion
        from solicitud a, area b, puesto c, nivelacademico d , carrera e,  estatus_solicitud f
        where b.idArea=a.idArea and c.idPuesto=a.idPuesto and d.idNivelAcademico=a.idNivelAcademico and f.idEstatus_Solicitud=a.idEstatus_Solicitud and a.idCarrera=e.idCarrera order by a.idEstatus_Solicitud''')
    datos = cursor.fetchall()
    #print(datos)
    conn.close()
    return render_template('solicitud.html', datos=datos)

## abre el html para agregar una solicitud
@app.route("/nvo_solicitud")
def nvo_solicitud():
    conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
    cursor = conn.cursor()
    cursor.execute('select idArea, AreaDescripcion from area')
    datos = cursor.fetchall()

    cursor.execute('select idPuesto, Descripcion from puesto')
    datos1 = cursor.fetchall()
    cursor.execute('select idCarrera, Descripcion from carrera')
    datos2 = cursor.fetchall()
    cursor.execute('select idNivelAcademico, Descripcion from nivelacademico')
    datos3 = cursor.fetchall()
    conn.close()
    return render_template("agr_solicitud.html", areas=datos, puestos=datos1, carreras=datos2, niveles=datos3)

## agrega una solicitud a la base de datos
@app.route("/agr_solicitud", methods=["POST"])
def agrega_solicitud():
    if request.method == 'POST':

        aux_fecha = request.form['Fecha']
        aux_area = request.form['area']
        aux_puesto = request.form['puesto']
        aux_carrera = request.form['Carrera']
        aux_vacantes = request.form['vacantes']
        aux_nivel = request.form['nivel']
        conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
        cursor = conn.cursor()
        cursor.execute('select Aprobacion from puesto where idPuesto = %s;', (aux_puesto))
        auto = cursor.fetchone()
        #print(auto)
        if auto[0] == 0:
            cursor.execute(
                'insert into solicitud (FechaSolicitud,NumeroVacante,idArea,idPuesto,idNivelAcademico,idCarrera,idEstatus_Solicitud) values (%s,%s,%s,%s,%s,%s,1)',
                (aux_fecha, aux_vacantes, aux_area, aux_puesto, aux_nivel, aux_carrera))
            conn.commit()
        else:
            cursor.execute(
                'insert into solicitud (FechaSolicitud,NumeroVacante,idArea,idPuesto,idNivelAcademico,idCarrera,idEstatus_Solicitud) values (%s,%s,%s,%s,%s,%s,2)',
                (aux_fecha, aux_vacantes, aux_area, aux_puesto, aux_nivel, aux_carrera))
            conn.commit()
        conn.close()
    return redirect(url_for('solicitud'))

## abre el html para editar la solicitud
@app.route("/ed_solicitud/<string:id>")
def ed_solicitud(id):
    conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
    cursor = conn.cursor()
    cursor.execute('select *from solicitud where idSolicitud=%s', (id))
    datos4 = cursor.fetchall()

    cursor.execute('select idArea, AreaDescripcion from area')
    datos = cursor.fetchall()

    cursor.execute('select idPuesto, Descripcion from puesto')
    datos1 = cursor.fetchall()
    cursor.execute('select idCarrera, Descripcion from carrera')
    datos2 = cursor.fetchall()
    cursor.execute('select idNivelAcademico, Descripcion from nivelacademico')
    datos3 = cursor.fetchall()
    cursor.execute('select idEstatus_Solicitud, Descripcion from estatus_solicitud')
    datos5 = cursor.fetchall()
    conn.close()
    return render_template("edi_solicitud.html", areas=datos, puestos=datos1, carreras=datos2, niveles=datos3,
                           solicitud=datos4, estatuses=datos5)

## cambia los datos de la base de datos por lo que ya estan modificados
@app.route("/edita_solicitud/<string:id>", methods=["POST"])
def edita_solicitud(id):
    if request.method == 'POST':
        aux_fecha = request.form['Fecha']
        aux_area = request.form['area']
        aux_puesto = request.form['puesto']
        aux_carrera = request.form['Carrera']
        aux_vacantes = request.form['vacantes']
        aux_nivel = request.form['nivel']
        aux_estatus = request.form['estatus']

        conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
        cursor = conn.cursor()
        cursor.execute(
            '''update solicitud set FechaSolicitud=%s,NumeroVacante=%s,idArea=%s,idPuesto=%s,idNivelAcademico=%s,idCarrera=%s,idEstatus_Solicitud=%s where idSolicitud=%s ''',
            (aux_fecha, aux_vacantes, aux_area, aux_puesto, aux_nivel, aux_carrera, aux_estatus, id))
        conn.commit()
        conn.close()
    return redirect(url_for('solicitud'))

## borra la solicitud
@app.route("/bo_solicitud/<string:id>")
def borra_solicitud(id):
    conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
    cursor = conn.cursor()
    cursor.execute('delete from solicitud where idSolicitud=%s', (id))
    conn.commit()
    conn.close()
    return redirect(url_for("solicitud"))
##########################################################################################################################################################




@app.route("/faltante")
def faltante():
    return render_template("faltante.html")

################################################################ autorizacion ##############################################################################
## muestra las solicitudes y la opcion para autorizarla o cancelarla
@app.route("/Autorizacion")
def Autorizacion():
    conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
    cursor = conn.cursor()
    cursor.execute('''select a.idSolicitud,a.FechaSolicitud,a.NumeroVacante,a.idArea,b.AreaDescripcion,a.idPuesto,c.Descripcion,a.idNivelAcademico,d.Descripcion,a.idCarrera,e.Descripcion,a.idEstatus_Solicitud,f.Descripcion
        from solicitud a, area b, puesto c, nivelacademico d , carrera e,  estatus_solicitud f
        where b.idArea=a.idArea and c.idPuesto=a.idPuesto and d.idNivelAcademico=a.idNivelAcademico and f.idEstatus_Solicitud=a.idEstatus_Solicitud and a.idCarrera=e.idCarrera order by a.idEstatus_Solicitud''')
    datos = cursor.fetchall()
    conn.close()
    return render_template("autoriza.html", datos=datos)

## cambia la solicitud de pendiente a aprobada
@app.route("/auto_solicitud/<string:id>")
def auto_solicitud(id):
    conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
    cursor = conn.cursor()
    cursor.execute(''' update solicitud set idEstatus_solicitud=2 where idSolicitud=%s''', (id))
    conn.commit()
    conn.close()
    return redirect(url_for('Autorizacion'))

## cambie la solicitud de pendiente a cancelada
@app.route("/can_solicitud/<string:id>")
def can_solicitud(id):
    conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
    cursor = conn.cursor()
    cursor.execute(''' update solicitud set idEstatus_solicitud=6 where idSolicitud=%s''', (id))
    conn.commit()
    conn.close()
    return redirect(url_for('Autorizacion'))

########################################################### PUBLICACIÓN DE LA SOLICITUD#########################################################

## muestra solo las solicitudes aprobadas y las ya publicadas
@app.route('/a_publicar')
def a_publicar():
    conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
    cursor = conn.cursor()
    cursor.execute(
        ' select a.idSolicitud, a.FechaSolicitud, a.idArea, b.AreaNombre, a.idPuesto, c.Descripcion, a.NumeroVacante, a.idEstatus_Solicitud, d.Descripcion '
        ' from solicitud a, area b, puesto c, estatus_solicitud d '
        ' where b.idArea=a.idArea and c.idPuesto=a.idPuesto and d.idEstatus_Solicitud=a.idEstatus_Solicitud'
        ' and (a.idEstatus_Solicitud=2 or a.idEstatus_Solicitud=3) order by a.idEstatus_Solicitud')

    datos = cursor.fetchall()
    conn.close()
    return render_template("publicacion.html", solicitudes=datos)

## abre el html para crear la publcacion
@app.route('/crea_pub/<string:id>')
def crea_pub(id):
    conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
    cursor = conn.cursor()
    cursor.execute(
        ' select a.idSolicitud, a.FechaSolicitud, a.idArea, b.AreaNombre, a.idPuesto, c.Descripcion, a.NumeroVacante, a.idEstatus_Solicitud, d.Descripcion '
        ' from solicitud a, area b, puesto c, estatus_solicitud d '
        ' where b.idArea=a.idArea and c.idPuesto=a.idPuesto and d.idEstatus_Solicitud=a.idEstatus_Solicitud'
        ' and (a.idEstatus_Solicitud=2 or a.idEstatus_Solicitud=3) and idSolicitud=%s', (id))

    dato = cursor.fetchone()
    cursor.execute(
        ' SELECT a.idAnuncio, a.Num_Solicitantes, a.FechaPublicacion, a.FechaCierre, b.Nombre, c.Descripcion '
        ' from anuncio a, contacto b, mediopublicidad c '
        ' where b.idcontacto=a.idcontacto and c.idMedioPublicidad=a.idMedioPublicidad and a.idSolicitud=%s', (id))
    datos = cursor.fetchall()

    cursor.execute(' select idcontacto, nombre from contacto order by nombre ')
    datos1 = cursor.fetchall()
    cursor.execute(' select idMedioPublicidad, Descripcion from mediopublicidad order by Descripcion ')
    datos2 = cursor.fetchall()
    conn.close()
    return render_template("crea_publicacion.html", sol=dato, publicaciones=datos, contactos=datos1, medios=datos2)

## agrega dicha publicacion a la base de datos
@app.route('/agrega_publicacion', methods=['POST'])
def agrega_publicacion():
    if request.method == 'POST':
        aux_sol = request.form['n_solicitud']
        aux_fep = request.form['fecha_pub']
        aux_fec = request.form['fecha_cie']
        aux_solicitantes = request.form['n_solicitantes']
        aux_con = request.form['contacto']
        aux_med = request.form['medio']

        conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
        cursor = conn.cursor()

        # El Puesto requiere de Autorizacion
        cursor.execute(
            ' insert into anuncio (idSolicitud, Num_Solicitantes, FechaPublicacion, FechaCierre, idcontacto, idMedioPublicidad) '
            ' values (%s,%s,%s,%s,%s,%s)', (aux_sol, aux_solicitantes, aux_fep, aux_fec, aux_con, aux_med))
        conn.commit()
        cursor.execute(' update solicitud set idEstatus_Solicitud=3 where idSolicitud=%s', (aux_sol))
        conn.commit()
        cursor.execute(
            ' select a.idSolicitud, a.FechaSolicitud, a.idArea, b.AreaNombre, a.idPuesto, c.Descripcion, a.NumeroVacante, a.idEstatus_Solicitud, d.Descripcion '
            ' from solicitud a, area b, puesto c, estatus_solicitud d '
            ' where b.idArea=a.idArea and c.idPuesto=a.idPuesto and d.idEstatus_Solicitud=a.idEstatus_Solicitud'
            ' and (a.idEstatus_Solicitud=2 or a.idEstatus_Solicitud=3) and idSolicitud=%s', (aux_sol))

        dato = cursor.fetchone()
        cursor.execute(
            ' SELECT a.idAnuncio, a.Num_Solicitantes, a.FechaPublicacion, a.FechaCierre, b.Nombre, c.Descripcion '
            ' from anuncio a, contacto b, mediopublicidad c '
            ' where b.idcontacto=a.idcontacto and c.idMedioPublicidad=a.idMedioPublicidad and a.idSolicitud=%s',
            (aux_sol))
        datos = cursor.fetchall()

        cursor.execute(' select idcontacto, nombre from contacto order by nombre ')
        datos1 = cursor.fetchall()
        cursor.execute(' select idMedioPublicidad, Descripcion from mediopublicidad order by Descripcion ')
        datos2 = cursor.fetchall()
        conn.close()
        return render_template("crea_publicacion.html", sol=dato, publicaciones=datos, contactos=datos1, medios=datos2)

## borra la publicacion
@app.route('/bo_publicacion/<string:id>')
def bo_publicacion(id):
    conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
    cursor = conn.cursor()
    cursor.execute(' select idSolicitud from anuncio where idanuncio = {0}'.format(id))
    aux_sol = cursor.fetchone()
    cursor = conn.cursor()
    cursor.execute(' delete from anuncio where idanuncio = {0}'.format(id))
    conn.commit()
    cursor.execute(
        ' select a.idSolicitud, a.FechaSolicitud, a.idArea, b.AreaNombre, a.idPuesto, c.Descripcion, a.NumeroVacante, a.idEstatus_Solicitud, d.Descripcion '
        ' from solicitud a, area b, puesto c, estatus_solicitud d '
        ' where b.idArea=a.idArea and c.idPuesto=a.idPuesto and d.idEstatus_Solicitud=a.idEstatus_Solicitud'
        ' and (a.idEstatus_Solicitud=2 or a.idEstatus_Solicitud=3) and idSolicitud=%s', (aux_sol[0]))

    dato = cursor.fetchone()
    cursor.execute(
        ' SELECT a.idAnuncio, a.Num_Solicitantes, a.FechaPublicacion, a.FechaCierre, b.Nombre, c.Descripcion '
        ' from anuncio a, contacto b, mediopublicidad c '
        ' where b.idcontacto=a.idcontacto and c.idMedioPublicidad=a.idMedioPublicidad and a.idSolicitud=%s',
        (aux_sol[0]))
    datos = cursor.fetchall()

    cursor.execute(' select idcontacto, nombre from contacto order by nombre ')
    datos1 = cursor.fetchall()
    cursor.execute(' select idMedioPublicidad, Descripcion from mediopublicidad order by Descripcion ')
    datos2 = cursor.fetchall()
    conn.close()
    return render_template("crea_publicacion.html", sol=dato, publicaciones=datos, contactos=datos1, medios=datos2)
###########################################################################################################################################################

@app.route("/asignacion_can")
def asignacion_can():
    conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
    cursor = conn.cursor()
    cursor.execute('''select a.idSolicitud,a.FechaSolicitud,a.NumeroVacante,a.idArea,b.AreaDescripcion,a.idPuesto,c.Descripcion,a.idNivelAcademico,d.Descripcion,a.idCarrera,e.Descripcion,a.idEstatus_Solicitud,f.Descripcion
        from solicitud a, area b, puesto c, nivelacademico d , carrera e,  estatus_solicitud f
        where b.idArea=a.idArea and c.idPuesto=a.idPuesto and d.idNivelAcademico=a.idNivelAcademico and f.idEstatus_Solicitud=a.idEstatus_Solicitud and a.idCarrera=e.idCarrera and (a.idEstatus_solicitud = 3 or a.idEstatus_solicitud = 4) order by a.idEstatus_Solicitud ''')
    datos = cursor.fetchall()
    #print(datos)
    conn.close()
    return render_template('Calificacion_tecnica.html', datos=datos)

@app.route("/sel_candidato/<string:id>")
def sel_candidato(id):

    conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
    cursor = conn.cursor()

    cursor.execute('''select a.Curp, a.Nombre, c.idNivelAcademico, c.descripcion, d.descripcion from
        candidato a, candidato_has_nivelacademico b, nivelacademico c, carrera d
        where b.curp = a.curp and c.idNivelAcademico = b.idNivelAcademico and d.idCarrera = b.idCarrera and
     NOT EXISTS (SELECT NULL FROM resultadocandidato e WHERE e.Curp = a.Curp and e.idSolicitud=%s) ''',(id))
    datos = cursor.fetchall()

    cursor.execute('''select a.Curp, b.Nombre, c.idNivelAcademico, c.idCarrera, d.descripcion, e.descripcion
        from resultadocandidato a,candidato b, candidato_has_nivelacademico c, nivelacademico d, carrera e where b.curp = a.curp
        and c.curp = b.curp and d.idNivelAcademico = c.idNivelAcademico and e.idcarrera = c.idcarrera and a.idSolicitud=%s''', (id))
    datos2 = cursor.fetchall()

    cursor.execute('''select a.idSolicitud,a.FechaSolicitud,a.NumeroVacante,a.idArea,b.AreaDescripcion,a.idPuesto,c.Descripcion,a.idNivelAcademico,d.Descripcion,a.idCarrera,e.Descripcion,a.idEstatus_Solicitud,f.Descripcion
        from solicitud a, area b, puesto c, nivelacademico d , carrera e, estatus_solicitud f where b.idArea=a.idArea
        and c.idPuesto=a.idPuesto and d.idNivelAcademico=a.idNivelAcademico and f.idEstatus_Solicitud=a.idEstatus_Solicitud and a.idCarrera=e.idCarrera
        and (a.idEstatus_solicitud = 3 or a.idEstatus_solicitud = 4) and a.idSolicitud=%s order by a.idEstatus_Solicitud ''',(id))
    datos4 = cursor.fetchall()

    conn.close()
    return render_template("Evaluar.html", candidatos=datos,can_selec=datos2,idSolicitud=id,solicitud=datos4 )


@app.route("/ins_candidato/<string:ca>/<string:so>")
def ins_candidato(ca,so):
    conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
    cursor = conn.cursor()
    cursor.execute(' select Curp from resultadocandidato where idSolicitud=  %s;',(so))
    curps=cursor.fetchall()
    for curp in curps:
        if curp[0] == ca:
            cursor.execute('''select a.Curp, a.Nombre, c.idNivelAcademico, c.descripcion, d.descripcion from
            candidato a, candidato_has_nivelacademico b, nivelacademico c, carrera d
            where b.curp = a.curp and c.idNivelAcademico = b.idNivelAcademico and d.idCarrera = b.idCarrera and
            NOT EXISTS (SELECT NULL FROM resultadocandidato e WHERE e.Curp = a.Curp and e.idSolicitud=%s) ''',(so))
            datos = cursor.fetchall()
            cursor.execute('''select a.Curp, b.Nombre, c.idNivelAcademico, c.idCarrera, d.descripcion, e.descripcion
                from resultadocandidato a,candidato b, candidato_has_nivelacademico c, nivelacademico d, carrera e where b.curp = a.curp
                and c.curp = b.curp and d.idNivelAcademico = c.idNivelAcademico and e.idcarrera = c.idcarrera and a.idSolicitud=%s''', (so))
            datos2 = cursor.fetchall()
            cursor.execute('''select a.idSolicitud,a.FechaSolicitud,a.NumeroVacante,a.idArea,b.AreaDescripcion,a.idPuesto,c.Descripcion,a.idNivelAcademico,d.Descripcion,a.idCarrera,e.Descripcion,a.idEstatus_Solicitud,f.Descripcion
                from solicitud a, area b, puesto c, nivelacademico d , carrera e, estatus_solicitud f where b.idArea=a.idArea
                and c.idPuesto=a.idPuesto and d.idNivelAcademico=a.idNivelAcademico and f.idEstatus_Solicitud=a.idEstatus_Solicitud and a.idCarrera=e.idCarrera
                and (a.idEstatus_solicitud = 3 or a.idEstatus_solicitud = 4) and a.idSolicitud=%s order by a.idEstatus_Solicitud ''',(so))
            datos3 = cursor.fetchall()
            conn.close()
            return render_template("Evaluar.html", candidatos=datos,can_selec=datos2,idSolicitud=so,solicitud=datos3 )
    cursor.execute(' INSERT INTO resultadocandidato (idSolicitud, Curp,id_actitud) VALUES ( %s, %s,4);',(so,ca))
    conn.commit()
    cursor.execute('''select a.Curp, a.Nombre, c.idNivelAcademico, c.descripcion, d.descripcion from
        candidato a, candidato_has_nivelacademico b, nivelacademico c, carrera d
        where b.curp = a.curp and c.idNivelAcademico = b.idNivelAcademico and d.idCarrera = b.idCarrera and
        NOT EXISTS (SELECT NULL FROM resultadocandidato e WHERE e.Curp = a.Curp and e.idSolicitud=%s) ''',(so))
    datos = cursor.fetchall()
    cursor.execute('''select a.Curp, b.Nombre, c.idNivelAcademico, c.idCarrera, d.descripcion, e.descripcion
        from resultadocandidato a,candidato b, candidato_has_nivelacademico c, nivelacademico d, carrera e where b.curp = a.curp
        and c.curp = b.curp and d.idNivelAcademico = c.idNivelAcademico and e.idcarrera = c.idcarrera and a.idSolicitud=%s''', (so))
    datos2 = cursor.fetchall()
    cursor.execute('''select a.idSolicitud,a.FechaSolicitud,a.NumeroVacante,a.idArea,b.AreaDescripcion,a.idPuesto,c.Descripcion,a.idNivelAcademico,d.Descripcion,a.idCarrera,e.Descripcion,a.idEstatus_Solicitud,f.Descripcion
        from solicitud a, area b, puesto c, nivelacademico d , carrera e, estatus_solicitud f where b.idArea=a.idArea
        and c.idPuesto=a.idPuesto and d.idNivelAcademico=a.idNivelAcademico and f.idEstatus_Solicitud=a.idEstatus_Solicitud and a.idCarrera=e.idCarrera
        and (a.idEstatus_solicitud = 3 or a.idEstatus_solicitud = 4) and a.idSolicitud=%s order by a.idEstatus_Solicitud ''',(so))
    datos3 = cursor.fetchall()
    conn.close()
    return render_template("Evaluar.html", candidatos=datos,can_selec=datos2,idSolicitud=so,solicitud=datos3 )

@app.route("/bo_solicitante/<string:ca>/<string:so>")
def bo_solicitante(ca,so):
    conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
    cursor = conn.cursor()
    cursor.execute(' delete from resultadocandidato where idSolicitud = %s and CURP =%s', (so, ca))
    conn.commit()
    cursor.execute('''select a.Curp, a.Nombre, c.idNivelAcademico, c.descripcion, d.descripcion from
        candidato a, candidato_has_nivelacademico b, nivelacademico c, carrera d
        where b.curp = a.curp and c.idNivelAcademico = b.idNivelAcademico and d.idCarrera = b.idCarrera and
        NOT EXISTS (SELECT NULL FROM resultadocandidato e WHERE e.Curp = a.Curp and e.idSolicitud=%s) ''',(so))
    datos = cursor.fetchall()
    cursor.execute('''select a.Curp, b.Nombre, c.idNivelAcademico, c.idCarrera, d.descripcion, e.descripcion
        from resultadocandidato a,candidato b, candidato_has_nivelacademico c, nivelacademico d, carrera e where b.curp = a.curp
        and c.curp = b.curp and d.idNivelAcademico = c.idNivelAcademico and e.idcarrera = c.idcarrera and a.idSolicitud=%s''', (so))
    datos2 = cursor.fetchall()
    cursor.execute('''select a.idSolicitud,a.FechaSolicitud,a.NumeroVacante,a.idArea,b.AreaDescripcion,a.idPuesto,c.Descripcion,a.idNivelAcademico,d.Descripcion,a.idCarrera,e.Descripcion,a.idEstatus_Solicitud,f.Descripcion
        from solicitud a, area b, puesto c, nivelacademico d , carrera e, estatus_solicitud f where b.idArea=a.idArea
        and c.idPuesto=a.idPuesto and d.idNivelAcademico=a.idNivelAcademico and f.idEstatus_Solicitud=a.idEstatus_Solicitud and a.idCarrera=e.idCarrera
        and (a.idEstatus_solicitud = 3 or a.idEstatus_solicitud = 4) and a.idSolicitud=%s order by a.idEstatus_Solicitud ''',(so))
    datos3 = cursor.fetchall()
    conn.close()
    return render_template("Evaluar.html", candidatos=datos, can_selec=datos2, idSolicitud=so,solicitud=datos3)

@app.route("/muestra_solicitante/<string:id>/<string:soli>")
def muestra_candidato(id,soli):
    conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
    cursor = conn.cursor()
    cursor.execute(
        ' select CURP,RFC, Nombre,Domicilio, Telefono,E_mail, Sexo,Edad,NSS,Fotografia,idEstadoCivil from candidato where CURP=%s',
        (id))
    datos = cursor.fetchall()
    print(datos)
    cursor.execute(' select * from habilidad ')
    datos1 = cursor.fetchall()
    cursor.execute(' select * from idioma ')
    datos2 = cursor.fetchall()

    cursor.execute(' select * from nivelacademico ')
    datos4 = cursor.fetchall()
    cursor.execute('select a.CURP, b.idIdioma,b.Lenguaje,c.CURP, c.idIdioma, c.Nivel '
                   'from candidato a, idioma b,candidato_has_idioma c '
                   'where a.CURP=c.CURP and b.idIdioma=c.idIdioma and a.CURP=%s ', (id))
    datos5 = cursor.fetchall()
    cursor.execute('select a.CURP, b.idHabilidad,b.Descripcion,c.CURP, c.idHabilidad, c.Experiencia '
                   'from candidato a, habilidad b,candidato_has_habilidad c '
                   'where a.CURP=c.CURP and b.idHabilidad=c.idHabilidad and a.CURP=%s ', (id))
    datos6 = cursor.fetchall()
    cursor.execute('select * from estadocivil order by Descripcion')
    datos7 = cursor.fetchall()

    cursor.execute(
        'select a.CURP, b.idNivelAcademico,b.Descripcion,c.Institucion,c.CURP, c.idNivelAcademico,c.idCarrera ,d.Descripcion '
        'from candidato a, nivelacademico b,candidato_has_nivelacademico c, carrera d '
        ' where a.CURP=c.CURP and b.idNivelAcademico=c.idNivelacademico and c.idCarrera = d.idCarrera and a.CURP=%s ',
        (id))
    datos9 = cursor.fetchall()
    cursor.execute('select * from carrera order by Descripcion')
    datos10 = cursor.fetchall()
    conn.close()
    return render_template("muestra_can.html", datos=datos, habs=datos1, idiomas=datos2,
                           niveles=datos4, idis=datos5, can_habs=datos6, estados=datos7,
                           nivelesC=datos9, carrerasN=datos10,idSolicitud=soli)
@app.route("/termina_solicitud/<string:id>")
def termina_solicitud(id):
    conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
    cursor = conn.cursor()
    cursor.execute(''' update solicitud set idEstatus_solicitud=5 where idSolicitud=%s''', (id))
    conn.commit()
    conn.close()
    return redirect(url_for('asignacion_can'))

@app.route("/calificacion_psicologica")
def calificacionpsicologica():
    conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
    cursor = conn.cursor()
    cursor.execute('''select a.idSolicitud,a.FechaSolicitud,a.NumeroVacante,a.idArea,b.AreaDescripcion,a.idPuesto,c.Descripcion,
        a.idNivelAcademico,d.Descripcion,a.idCarrera,e.Descripcion,a.idEstatus_Solicitud,f.Descripcion
        from solicitud a, area b, puesto c, nivelacademico d , carrera e, estatus_solicitud f where b.idArea=a.idArea
        and c.idPuesto=a.idPuesto and d.idNivelAcademico=a.idNivelAcademico and f.idEstatus_Solicitud=a.idEstatus_Solicitud
        and a.idCarrera=e.idCarrera and (a.idEstatus_solicitud = 3 or a.idEstatus_solicitud = 4)
        and EXISTS (SELECT NULL from resultadocandidato g WHERE g.idSolicitud = a.idSolicitud) ''')
    datos = cursor.fetchall()
    #print(datos)
    conn.close()
    return render_template("califiacion_psico.html",datos=datos)




@app.route("/calif_psicologica/<string:id>")
def califpsicologica(id):
    conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
    cursor = conn.cursor()
    cursor.execute('''select a.Curp, a.Nombre, c.idNivelAcademico, c.descripcion, d.descripcion from
        candidato a, candidato_has_nivelacademico b, nivelacademico c, carrera d
        where b.curp = a.curp and c.idNivelAcademico = b.idNivelAcademico and d.idCarrera = b.idCarrera and
        NOT EXISTS (SELECT NULL FROM resultadocandidato e WHERE e.Curp = a.Curp and e.idSolicitud=%s) ''',(id))
    datos = cursor.fetchall()
    cursor.execute('''select a.Curp, b.Nombre, c.idNivelAcademico, c.idCarrera, d.descripcion, e.descripcion
        from resultadocandidato a,candidato b, candidato_has_nivelacademico c, nivelacademico d, carrera e where b.curp = a.curp
        and c.curp = b.curp and d.idNivelAcademico = c.idNivelAcademico and e.idcarrera = c.idcarrera and a.idSolicitud=%s''', (id))
    datos2 = cursor.fetchall()
    cursor.execute('''select a.idSolicitud,a.FechaSolicitud,a.NumeroVacante,a.idArea,b.AreaDescripcion,a.idPuesto,c.Descripcion,a.idNivelAcademico,d.Descripcion,a.idCarrera,e.Descripcion,a.idEstatus_Solicitud,f.Descripcion
        from solicitud a, area b, puesto c, nivelacademico d , carrera e, estatus_solicitud f where b.idArea=a.idArea
        and c.idPuesto=a.idPuesto and d.idNivelAcademico=a.idNivelAcademico and f.idEstatus_Solicitud=a.idEstatus_Solicitud and a.idCarrera=e.idCarrera
        and (a.idEstatus_solicitud = 3 or a.idEstatus_solicitud = 4) and a.idSolicitud=%s order by a.idEstatus_Solicitud ''',(id))
    datos3 = cursor.fetchall()
    conn.close()
    return render_template("calif_psico.html", candidatos=datos, can_selec=datos2, idSolicitud=id,solicitud=datos3)

@app.route("/calificacion_p/<string:ca>/<string:so>")
def calificacion_p(ca,so):
    conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
    cursor = conn.cursor()
    cursor.execute('''select a.Curp, a.Nombre, c.idNivelAcademico, c.descripcion, d.descripcion from
        candidato a, candidato_has_nivelacademico b, nivelacademico c, carrera d
        where b.curp = a.curp and c.idNivelAcademico = b.idNivelAcademico and d.idCarrera = b.idCarrera and
        NOT EXISTS (SELECT NULL FROM resultadocandidato e WHERE e.Curp = a.Curp and e.idSolicitud=%s) ''',(so))
    datos = cursor.fetchall()
    cursor.execute('''select a.Curp, b.Nombre, c.idNivelAcademico, c.idCarrera, d.descripcion, e.descripcion, a.apto,a.Personalidad,a.CoeficienteIntelectual
        from resultadocandidato a,candidato b, candidato_has_nivelacademico c, nivelacademico d, carrera e where b.curp = a.curp
        and b.curp=%s and d.idNivelAcademico = c.idNivelAcademico and e.idcarrera = c.idcarrera and a.idSolicitud=%s''', (ca,so))
    datos2 = cursor.fetchall()
    cursor.execute('''select a.idSolicitud,a.FechaSolicitud,a.NumeroVacante,a.idArea,b.AreaDescripcion,a.idPuesto,c.Descripcion,a.idNivelAcademico,d.Descripcion,a.idCarrera,e.Descripcion,a.idEstatus_Solicitud,f.Descripcion
        from solicitud a, area b, puesto c, nivelacademico d , carrera e, estatus_solicitud f where b.idArea=a.idArea
        and c.idPuesto=a.idPuesto and d.idNivelAcademico=a.idNivelAcademico and f.idEstatus_Solicitud=a.idEstatus_Solicitud and a.idCarrera=e.idCarrera
        and (a.idEstatus_solicitud = 3 or a.idEstatus_solicitud = 4) and a.idSolicitud=%s order by a.idEstatus_Solicitud ''',(so))
    datos3 = cursor.fetchall()
    conn.close()

    return render_template("Calificacion_p.html", candidatos=datos, can_selec=datos2, idSolicitud=so,solicitud=datos3)
@app.route("/califica_psico/<string:so>/<string:ca>", methods=["POST"])
def califica_psico(so,ca):
     if request.method == 'POST':
        aux_ci = request.form['ci']
        print(aux_ci)
        aux_person = request.form['analisis']
        print(aux_person)
        aux_apto = request.form['apto']
        print(aux_apto)
        print(ca)
        conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
        cursor = conn.cursor()
        cursor.execute('''UPDATE resultadocandidato SET Personalidad = %s, CoeficienteIntelectual = %s, apto = %s
            WHERE resultadocandidato.idSolicitud = %s AND resultadocandidato.Curp = %s;''', (aux_person,aux_ci,aux_apto,so,ca))
        conn.commit()
        conn.close()
        return redirect(url_for("calificacionpsicologica"))



@app.route("/calificacion_tecnica")
def calificaciontecnica():
    conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
    cursor = conn.cursor()
    cursor.execute('''select a.idSolicitud,a.FechaSolicitud,a.NumeroVacante,a.idArea,b.AreaDescripcion,a.idPuesto,c.Descripcion,
        a.idNivelAcademico,d.Descripcion,a.idCarrera,e.Descripcion,a.idEstatus_Solicitud,f.Descripcion
        from solicitud a, area b, puesto c, nivelacademico d , carrera e, estatus_solicitud f where b.idArea=a.idArea
        and c.idPuesto=a.idPuesto and d.idNivelAcademico=a.idNivelAcademico and f.idEstatus_Solicitud=a.idEstatus_Solicitud
        and a.idCarrera=e.idCarrera and (a.idEstatus_solicitud = 3 or a.idEstatus_solicitud = 4)
        and EXISTS (SELECT NULL from resultadocandidato g WHERE g.idSolicitud = a.idSolicitud) ''')
    datos = cursor.fetchall()
    #print(datos)
    conn.close()
    return render_template("califica_tecnica.html",datos=datos)



@app.route("/sel_calif_tecnica/<string:id>")
def sel_calif_tecnica(id):

    conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
    cursor = conn.cursor()

    cursor.execute('''select a.Curp, a.Nombre, c.idNivelAcademico, c.descripcion, d.descripcion from
        candidato a, candidato_has_nivelacademico b, nivelacademico c, carrera d
        where b.curp = a.curp and c.idNivelAcademico = b.idNivelAcademico and d.idCarrera = b.idCarrera and
     NOT EXISTS (SELECT NULL FROM resultadocandidato e WHERE e.Curp = a.Curp and e.idSolicitud=%s) ''',(id))
    datos = cursor.fetchall()

    cursor.execute('''select a.Curp, b.Nombre, c.idNivelAcademico, c.idCarrera, d.descripcion, e.descripcion
        from resultadocandidato a,candidato b, candidato_has_nivelacademico c, nivelacademico d, carrera e where b.curp = a.curp
        and c.curp = b.curp and d.idNivelAcademico = c.idNivelAcademico and e.idcarrera = c.idcarrera and a.idSolicitud=%s''', (id))
    datos2 = cursor.fetchall()

    cursor.execute('''select a.idSolicitud,a.FechaSolicitud,a.NumeroVacante,a.idArea,b.AreaDescripcion,a.idPuesto,c.Descripcion,a.idNivelAcademico,d.Descripcion,a.idCarrera,e.Descripcion,a.idEstatus_Solicitud,f.Descripcion
        from solicitud a, area b, puesto c, nivelacademico d , carrera e, estatus_solicitud f where b.idArea=a.idArea
        and c.idPuesto=a.idPuesto and d.idNivelAcademico=a.idNivelAcademico and f.idEstatus_Solicitud=a.idEstatus_Solicitud and a.idCarrera=e.idCarrera
        and (a.idEstatus_solicitud = 3 or a.idEstatus_solicitud = 4) and a.idSolicitud=%s order by a.idEstatus_Solicitud ''',(id))
    datos4 = cursor.fetchall()

    conn.close()
    return render_template("calif_tecnica.html", candidatos=datos,can_selec=datos2,idSolicitud=id,solicitud=datos4 )



@app.route("/calif_solicitante_tecnica/<string:id>/<string:soli>")
def calif_solicitante_tecnica(id,soli):
    conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
    cursor = conn.cursor()
    cursor.execute(
        ' select CURP,RFC, Nombre,Domicilio, Telefono,E_mail, Sexo,Edad,NSS,Fotografia,idEstadoCivil from candidato where CURP=%s',
        (id))
    datos = cursor.fetchall()
    print(datos)
    cursor.execute(' select * from habilidad ')
    datos1 = cursor.fetchall()
    cursor.execute(' select * from idioma ')
    datos2 = cursor.fetchall()

    cursor.execute(' select * from nivelacademico ')
    datos4 = cursor.fetchall()
    cursor.execute('select a.CURP, b.idIdioma,b.Lenguaje,c.CURP, c.idIdioma, c.Nivel '
                   'from candidato a, idioma b,candidato_has_idioma c '
                   'where a.CURP=c.CURP and b.idIdioma=c.idIdioma and a.CURP=%s ', (id))
    datos5 = cursor.fetchall()
    cursor.execute('select a.CURP, b.idHabilidad,b.Descripcion,c.CURP, c.idHabilidad, c.Experiencia '
                   'from candidato a, habilidad b,candidato_has_habilidad c '
                   'where a.CURP=c.CURP and b.idHabilidad=c.idHabilidad and a.CURP=%s ', (id))
    datos6 = cursor.fetchall()
    cursor.execute('select * from estadocivil order by Descripcion')
    datos7 = cursor.fetchall()

    cursor.execute(
        'select a.CURP, b.idNivelAcademico,b.Descripcion,c.Institucion,c.CURP, c.idNivelAcademico,c.idCarrera ,d.Descripcion '
        'from candidato a, nivelacademico b,candidato_has_nivelacademico c, carrera d '
        ' where a.CURP=c.CURP and b.idNivelAcademico=c.idNivelacademico and c.idCarrera = d.idCarrera and a.CURP=%s ',
        (id))
    datos9 = cursor.fetchall()
    cursor.execute('select * from carrera order by Descripcion')
    datos10 = cursor.fetchall()
    conn.close()
    return render_template("calif_tec.html", datos=datos, habs=datos1, idiomas=datos2,
                           niveles=datos4, idis=datos5, can_habs=datos6, estados=datos7,
                           nivelesC=datos9, carrerasN=datos10,idSolicitud=soli)


@app.route("/califica_tecnica_sol/<string:id>", methods=["POST"])
def califica_tecnica_sol(id):
     if request.method == 'POST':
        aux_habil = request.form['calificahabil']
        aux_idio = request.form['calificaidio']
        aux_nivel = request.form['calificanivel']
        conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
        cursor = conn.cursor()
        cursor.execute('''UPDATE resultadocandidato SET Personalidad = %s, CoeficienteIntelectual = %s, apto = %s
            WHERE resultadocandidato.idSolicitud = %s AND resultadocandidato.Curp = %s;''', (aux_person,aux_ci,aux_apto,so,ca))
        conn.commit()
        conn.close()
        return redirect(url_for("calificacionpsicologica"))


@app.route("/calificacion_medica")
def calificacion_medica():
    conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
    cursor = conn.cursor()
    cursor.execute('''select a.idSolicitud,a.FechaSolicitud,a.NumeroVacante,a.idArea,b.AreaDescripcion,a.idPuesto,c.Descripcion,a.idNivelAcademico,d.Descripcion,a.idCarrera,e.Descripcion,a.idEstatus_Solicitud,f.Descripcion
        from solicitud a, area b, puesto c, nivelacademico d , carrera e,  estatus_solicitud f
        where b.idArea=a.idArea and c.idPuesto=a.idPuesto and d.idNivelAcademico=a.idNivelAcademico and f.idEstatus_Solicitud=a.idEstatus_Solicitud and a.idCarrera=e.idCarrera and (a.idEstatus_solicitud = 3 or a.idEstatus_solicitud = 4) order by a.idEstatus_Solicitud ''')
    datos = cursor.fetchall()
    #print(datos)
    conn.close()
    return render_template('Calificacion_medica.html', datos=datos)


@app.route("/calif_medica/<string:id>")
def calif_medica(id):

    conn = pymysql.connect(host='NovaTech.mysql.pythonanywhere-services.com', user='NovaTech', passwd='tacosdechile', db='NovaTech$default')
    cursor = conn.cursor()

    cursor.execute('''select a.Curp, a.Nombre, c.idNivelAcademico, c.descripcion, d.descripcion from
        candidato a, candidato_has_nivelacademico b, nivelacademico c, carrera d
        where b.curp = a.curp and c.idNivelAcademico = b.idNivelAcademico and d.idCarrera = b.idCarrera and
     NOT EXISTS (SELECT NULL FROM resultadocandidato e WHERE e.Curp = a.Curp and e.idSolicitud=%s) ''',(id))
    datos = cursor.fetchall()

    cursor.execute('''select a.Curp, b.Nombre, c.idNivelAcademico, c.idCarrera, d.descripcion, e.descripcion
        from resultadocandidato a,candidato b, candidato_has_nivelacademico c, nivelacademico d, carrera e where b.curp = a.curp
        and c.curp = b.curp and d.idNivelAcademico = c.idNivelAcademico and e.idcarrera = c.idcarrera and a.idSolicitud=%s''', (id))
    datos2 = cursor.fetchall()

    cursor.execute('''select a.idSolicitud,a.FechaSolicitud,a.NumeroVacante,a.idArea,b.AreaDescripcion,a.idPuesto,c.Descripcion,a.idNivelAcademico,d.Descripcion,a.idCarrera,e.Descripcion,a.idEstatus_Solicitud,f.Descripcion
        from solicitud a, area b, puesto c, nivelacademico d , carrera e, estatus_solicitud f where b.idArea=a.idArea
        and c.idPuesto=a.idPuesto and d.idNivelAcademico=a.idNivelAcademico and f.idEstatus_Solicitud=a.idEstatus_Solicitud and a.idCarrera=e.idCarrera
        and (a.idEstatus_solicitud = 3 or a.idEstatus_solicitud = 4) and a.idSolicitud=%s order by a.idEstatus_Solicitud ''',(id))
    datos4 = cursor.fetchall()

    conn.close()
    return render_template("calif_medica.html", candidatos=datos,can_selec=datos2,idSolicitud=id,solicitud=datos4 )


# if __name__ == "__main__":
#     app.run(port=3000, debug=True)