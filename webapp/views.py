from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from models import Actividade, Usuario
from django.http import HttpResponseRedirect
from django.contrib import auth
from django.core.context_processors import csrf
from django.template.loader import get_template
from django.shortcuts import render_to_response
from datetime import datetime
from datetime import timedelta
from django.views.decorators.csrf import csrf_exempt
from django.template import Context, Template
import urllib2
import htmllib

import urllib
import sys
from bs4 import BeautifulSoup

def login(request):
    c={}
    c.update(csrf(request))
    
    return render_to_response("indexlogin.html",c)

def auth_view(request):
    username = request.POST.get("username", '')
    password = request.POST.get("password", '')
    user = auth.authenticate(username=username, password=password)

    if user is not None:
        auth.login(request,user)
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/invalid/')

def loggedin(request):
    return render_to_response('loggedin.html', {'full_name':request.user.username})

def invalid_login(request):
    c={}
    c.update(csrf(request))
    return render_to_response('indexinvalid.html',c)

def logout(request):
    auth.logout(request)
    return render_to_response('logout.html')

def cogerNombre(request):
    nombre = request.split("<br>")[1].split('<atributo nombre="TITULO">')[1].split('</atributo>')[0]
    return nombre

def cogerPrecio(request):
    if request.split("<br>")[2] == ('<atributo nombre="GRATUITO">1</atributo>'):
        precio = request.split("<br>")[2].split('<atributo nombre="GRATUITO">')[1].split('</atributo>')[0]
        precio = "gratuito"
    elif request.split("<br>")[2] == ('<atributo nombre="GRATUITO">0</atributo>'):
        precio = request.split("<br>")
        es_gratuito = ""
        i = 0
        for num in precio:
            if num.find('<atributo nombre="PRECIO">') != -1:
                es_gratuito = request.split("<br>")[i].split('<atributo nombre="PRECIO">')[1].split('</atributo>')[0]
                precio = es_gratuito
                break
            i += 1
        if es_gratuito == "":
            precio = "null"
    else:
        precio = request.split("<br>")[2].split('<atributo nombre="PRECIO">')[1].split('</atributo>')[0]
       # precio = request.split('<![CDATA[')[1].split(']')[0]
    return precio

def equals(resource):
    try:
        Actividade.objects.get(nombre=resource)
        return True
    except Actividade.DoesNotExist:
        return False

def cogerFecha(resource):
    fecha = resource.split("<br>")
    i = 0
    for nombre in fecha:
        if nombre.find('<atributo nombre="FECHA-EVENTO">') != -1:
            break
        i += 1
    fecha = resource.split("<br>")[i].split('<atributo nombre="FECHA-EVENTO">')[1].split('</atributo>')[0]
    fecha = fecha.split(' ')[0]
    return fecha

def cogerInicio(resource):
    inicio = resource.split("<br>")
    i = 0
    for hora_inicio in inicio:
        if hora_inicio.find('<atributo nombre="HORA-EVENTO">') != -1:
            break
        i += 1
    inicio = resource.split("<br>")[i].split('<atributo nombre="HORA-EVENTO">')[1].split('</atributo>')[0]
    return inicio

def cogerTipo(resource):
    tipo = resource.split("<br>")
    i = 0
    for tp in tipo:
        if tp.find('<atributo nombre="TIPO">') != -1:
            tipo = resource.split("<br>")[i].split('<atributo nombre="TIPO">')[1].split('</atributo>')[0]
            tipo = tipo.split("/")[3]
            break
        i += 1
    if  tipo == "":
        tipo = "Actividad"
    return tipo

def cogerDuracion(resource):
    inicio = cogerInicio(resource)
    fin = "23:59"
    hora_maxima = datetime.strptime(fin, '%H:%M')
    hora_inicio = datetime.strptime(inicio, '%H:%M')
    duracion = hora_maxima - hora_inicio
    return duracion

def cogerEs_Largo(resource):
    hora_maxima = timedelta(hours=3)
    es_largo = False
    if resource >= hora_maxima:
        es_largo = True
    return es_largo

def cogerUrl(resource):
    url = resource.split("<br>")
    i = 0
    for urls in url:
        if urls.find('<atributo nombre="CONTENT-URL">') != -1:
            break
        i += 1
    url = resource.split("<br>")[i].split('<atributo nombre="CONTENT-URL">')[1].split('</atributo>')[0]
    return url

def ponerCss(nombre):
    try:
        print "LETRAS Y FONDO BONITAS"
        usuario = Usuario.objects.get(nombre = str(nombre))
        usuario_pag = "<h2>"+ usuario.evento + "</h2>"
        fondo = usuario.fondo
        letra = usuario.letra
    except Usuario.DoesNotExist:
        print "NO HAY LETRAS NI FONDO"
        fondo = ""
        letra = ""
    return fondo,letra

def boton(resource, request):
    if request.user.is_authenticated():
        boton = "<form action='/add' method='POST'>"
        boton += "<button name='Identificador' value='"+ str(resource) +"' id='Identificador'>Add</button>"
        boton += "</form>"
    else:
        boton = ""
    return boton

@csrf_exempt
def pag_Todas_Actividades(request):
    template = get_template('indextodas.html')
    if request.method == "POST":
        value = request.POST['filter method']
        if value == "fecha":
            eventos = Actividade.objects.order_by("-fecha")
        else:
            eventos = Actividade.objects.order_by(value)

        pag_eventos = ""
        for noticia in eventos:
            pag_eventos += noticia.nombre +" "+ noticia.precio +" "+ noticia.fecha +" "+\
            noticia.hora_inicio +" "+ noticia.duracion + boton(noticia.id,request)+ "<br><br>"
        response = "<form action='' method='POST'>\n" +\
                   "Filtro: <select name='filter method'" +\
                   "<option selected value='name'> Name </option>"+\
                   "<option value='nombre'> Nombre </option>" +\
                   "<option value='hora_inicio'> Hora </option>" +\
                   "<option value='fecha'> Fecha </option>" +\
                   "<option value='precio'> Precio </option>" +\
                   "</optgroup>" +\
                   "</select>" +\
                   "<br>\n" +\
                   "<input type='submit' value='enviar'>\n" +\
                   "</form>\n"
    else:
        eventos = Actividade.objects.all()
        pag_eventos = ""
        for noticia in eventos:
            pag_eventos += noticia.nombre +" "+ noticia.precio +" "+ noticia.fecha +" "+\
            noticia.hora_inicio +" "+ noticia.duracion + boton(noticia.id,request) + "<br><br>"
        response = "<form action='' method='POST'>\n" +\
                   "Filtro: <select name='filter method'" +\
                   "<option selected value='name'> Name </option>"+\
                   "<option value='nombre'> Nombre </option>" +\
                   "<option value='hora_inicio'> Hora </option>" +\
                   "<option value='fecha'> Fecha </option>" +\
                   "<option value='precio'> Precio </option>" +\
                   "</optgroup>" +\
                   "</select>" +\
                   "<br>\n" +\
                   "<input type='submit' value='enviar'>\n" +\
                   "</form>\n"
    fondo, letra = ponerCss(request.user.username)
    c = {"todas" : pag_eventos, "filtro" : response, 'fondo':fondo, 'letra' : letra}
    return HttpResponse(template.render(Context(c)))

def ayuda(request):
    return render_to_response('ayuda.html', {'full_name':request.user.username})

def cogerPaginaUsuario(resource):
    lt = "<ul>"
    for ls in resource:
        lt += '<li type="circle">' + ls.nombre +" "+ ls.precio +" "+ ls.fecha +" "+\
        ls.hora_inicio +" "+ ls.duracion + "</li>"
    return lt + "</ul>"

def init(request):
    pag = ""
    activities = ""
    xml_doc = urllib.urlopen("http://datos.madrid.es/egob/catalogo/206974-0-agenda-eventos-culturales-100.xml")
    xml_codigo = BeautifulSoup(xml_doc)
    template = get_template('index.html')
    if request.user.is_authenticated():
        logged = "Logged in as " + request.user.username +\
                 ". <a href='http://127.0.0.1:8000/admin/logout/'>Logout</a><br>"
    else:
	    logged = "<br><br>Not logged. <a href='http://127.0.0.1:8000/login'>Login</a><br>"
        
    for contenido in xml_codigo.findAll("contenido"):
        titulo = ""
        for noticia in contenido.findAll("atributo"):
            titulo += str(noticia) + "<br>"
        nombre = cogerNombre(titulo)
        precio = cogerPrecio(titulo)
        fecha = cogerFecha(titulo)
        hora_inicio = cogerInicio(titulo)
        tipo = cogerTipo(titulo)
        duracion = cogerDuracion(titulo)
        es_largo = cogerEs_Largo(duracion)
        url = cogerUrl(titulo)
       
        if equals(nombre) != True:
            Actividade(nombre = str(nombre), \
                       precio = str(precio),
                       fecha = str(fecha),
                       hora_inicio = str(hora_inicio),
                       tipo = str(tipo),
                       duracion = str(duracion),
                       es_larga = str(es_largo),
                       url = str(url)).save()

    act = Actividade.objects.order_by('-fecha')
    for acts in range(0,10):
        activities += "Actividad: " + act[acts].nombre + ", Precio: " + \
                    act[acts].precio + ", Fecha: " + act[acts].fecha + \
                    ", Hora inicio: " + act[acts].hora_inicio + \
                    ", Duracion: " + act[acts].duracion + \
                    ", Url:" + "<a href=" + act[acts].url + "> Mas info</a>" + "<br><br>"
    pag += str(logged) + "<br>" + activities 
    
    pag_dos = ""
    pagina_usuarios = Usuario.objects.all()
    for pagina in pagina_usuarios:
        pag_dos += str(pagina.nombre) + ": <ul> " + \
        '<li type="circle">Nombre de la pagina: ' + str(pagina.evento) + "</li>" +\
        '<li type="circle">Lista de actividades:<br>' + cogerPaginaUsuario(pagina.actividad.all()) +"</li>" +\
        "</ul>"

    fondo, letra = ponerCss(request.user.username)
    c = {"recurso" : pag, "usuarios" : pag_dos,'fondo':fondo, 'letra' : letra}
    return HttpResponse(template.render(Context(c)))
#######################################################################

def decodeToOpenUrl(url):
    u = htmllib.HTMLParser(None)
    u.save_bgn()
    u.feed(url)
    url = u.save_end()
    return url

   
def actividades(request,resource):
    response = ""
    try:
        template = get_template('indexactividad.html')
        actividad = Actividade.objects.get(id=resource)
        response += actividad.nombre +" "+ actividad.precio +" "+ actividad.fecha +" "+\
        actividad.hora_inicio +" "+ actividad.duracion + "<br><br>"
        titulo = actividad.nombre
        
        urlInfor = decodeToOpenUrl(actividad.url)
        info = urllib2.urlopen(urlInfor).read()
        inicio = info.find('<div class="parrafo">')

        if inicio == -1:
            boolean = False
            response = "<a href=" + str(actividad.url) + ">" + "informacion" + "</a> <br>"
        else:
            boolean = True            
            fin = info.find('</div>',inicio)
            parrafo = info[inicio:fin]
            parrafo = parrafo.split('<div class="parrafo">')[1]
            parrafo = unicode(parrafo,'utf-8')
            response += parrafo + "<br>"
            response += "<a href=" + str(actividad.url) + ">" + "Amplie informacion" + "</a> <br>"
          

        if boolean == True:
           fondo, letra = ponerCss(request.user.username)
           c = Context({'texto': response,'fondo':fondo, 'letra' : letra})
           render = template.render(c)
           return HttpResponse(render)
        else:
           fondo, letra = ponerCss(request.user.username)
           c = Context({'texto': response,'fondo':fondo, 'letra' : letra})
           render = template.render(c)
           return HttpResponse(render)

        html = urllib2.urlopen(decodeToOpenUrl(actividad.url)).read()
        print html
        start = html.find('<a class="punteado" href="')
        
        if urllib2.urlopen(decodeToOpenUrl(actividad.url)).read().find('<a class="punteado" href="') != -1:
            response += "<a href=" + actividad.url + ">" + "informacion no diponible" + "</a> <br>"
            fin = html.find('">',start)
            parrafo = html[urllib2.urlopen(decodeToOpenUrl(actividad.url)).read().find('<a class="punteado" href="'):fin]
            urlInfo = parrafo.split('href="')[1]
        else:
            urlInfo = actividad.url

        if not urlInfo.startswith("http://www.madrid.es"):
            urlInfo = "http://www.madrid.es" + urlInfo

        urlInfo = decodeToOpenUrl(urlInfo)
        info = urllib2.urlopen(urlInfo).read()
        inicio = info.find('<div class="parrafo">')
        if inicio == -1:
            response += "<a href=" + urlInfo + ">" + "informacion" + "</a> <br>"
            c = Context({'title': title,'text': response})
           
            render = template.render(c)
            return HttpResponse(render)     
        fin = info.find('</div>',inicio)
        parrafo = infor[inicio:fin]
        response += parrafo + "<br>"
        response += "<a href=" + actividad.url + ">" + "Amplie informacion" + "</a> <br>"

        fondo, letra = ponerCss(request.user.username)

        c = Context({'title': title,'text': response,'fondo':fondo, 'letra' : letra})
        render = template.render(c)
        return HttpResponse(render) 
    except Actividade.DoesNotExist:
        titulo = '<h1>Id de la actividad no encontrada</h1>'
        fondo, letra = ponerCss(request.user.username)
        c = Context({'fallo': titulo,'fondo':fondo, 'letra' : letra})
        render = template.render(c)
        return HttpResponse(render) 

############################################################################
@csrf_exempt
def pag_usuario(request,resource):
    actividades = ""
    template = get_template('indexusuario.html')
    if request.user.username == resource:
			form = "<h2>Cambio de nombre de pagina personal</h2>"
			form += "<form action='/diezmas' method='POST' id='userPage'>"
			form += "Nombre: <input type='text' name='nombre' value=''><br>"
			form += "Fondo:  <input type='text' name='fondo' value=''><br>"
			form += "Letra:  <input type='text' name='letra' value=''><br>"
			form += "<input type='submit' value='enviar'>"
			form += "</form><br>"
    else:
            form = ""

    if request.method == "GET":
        response = ""
        fondo = ""
        letra = ""
        usuario_pag = ""
        boton = ""

        try:
            usr = Usuario.objects.get(nombre = resource)
            act_usr = ""
            acts = usr.actividad.all()
            if acts.count() > 10:
                acts = acts[:10]
			
            id_act =""
            for act in acts:
                act_usr += act.nombre + "   " + act.fecha + "<br>"
                id_act = act.id
            usuario_pag = "<h2>"+ "Pagina de " + usr.nombre + "</h2>" + "<h2>"+ usr.evento + "</h2>" + "<h3>"+ act_usr + "</h3>"
            response += act_usr
            acts = usr.actividad.all()
            if  acts.count() >10:
                boton = "<br><br> <form action='/" + resource + "' method='POST'>"
                boton += "<button name='Identificador' value='"+ str(act.id) +"' id='Identificador'>Ver mas</button>"
                boton += "</form>"
        except:
            return HttpResponse("El usuario no se encuentra en la base de datos")
        
        try:
            usuario = Usuario.objects.get(nombre = str(request.user.username))
            usuario_pag = "<h2>"+ usuario.evento + "</h2>"
            fondo = usuario.fondo
            letra = usuario.letra
        except Usuario.DoesNotExist:
            fondo = ""
            letra = ""
        
        try:
            for eventos in usr.actividad.all():
                actividades += eventos.nombre + "<a href=" + eventos.url + ">" + "   Amplie informacion" + "</a> <br>"
        except Usuario.DoesNotExist:
            return "User Page Not Found"

        if request.user.is_authenticated():    
            logged = "<br>Logged in as " + request.user.username +\
                 ". <a href='http://127.0.0.1:8000/admin/logout/'>Logout</a><br>"
           
        else:
            logged = "<br>Not logged. <a href='http://127.0.0.1:8000/login'>Login</a><br>"

        response += boton

        c = {"recurso" : resource, "login" : logged, "response":response, "form" : form, "nombre_usr" : usuario_pag, "fondo" : fondo, "letra" : letra}
        return HttpResponse(template.render(Context(c)))
    else:
        response = ""
        fondo = ""
        letra = ""
        usuario_pag = ""
        boton = ""
        id_usr = ""
        
        try:
            usr = Usuario.objects.get(nombre = resource)
            todas_act = usr.actividad.all()
            id_act = request.POST.get("Identificador", '')

            print id_act

            i = 0
            for act in todas_act:
                print i
                print act.id
                print id_act
                if str(act.id) == str(id_act):
		            break
                i += 1
            i+=1
            print todas_act
            todas_act = todas_act[i:]
            print todas_act
            act = ""
            for actividad in todas_act:
                act += (actividad.nombre + "   " + actividad.fecha + "<br>")
            
        except Usuario.DoesNotExist:
            return "User Page Not Found"
        
        try:
            for eventos in todas_act:
                actividades += eventos.nombre + "<a href=" + eventos.url + ">" + "   Amplie informacion" + "</a> <br>"
        except Usuario.DoesNotExist:
            return "User Page Not Found"
        if request.user.is_authenticated():    
            logged = "<br>Logged in as " + request.user.username +\
                 ". <a href='http://127.0.0.1:8000/admin/logout/'>Logout</a><br>"
            response += actividades
        else:
            logged = "<br>Not logged. <a href='http://127.0.0.1:8000/login'>Login</a><br>"

        response += boton
        c = {"recurso" : resource, "login" : logged, "response":response, "fondo" : fondo, "letra" : letra}
        return HttpResponse(template.render(Context(c)))

@csrf_exempt
def cogerActividad(request):
    actividad = request.POST.get("Identificador", '')
    try:
        pagina = Usuario.objects.get(nombre = request.user)
    except Usuario.DoesNotExist:
        pagina = Usuario(nombre = str(request.user), evento = "Pagina de " + str(request.user))
        pagina.save()
    evento = Actividade.objects.get(id=actividad)
    pagina.actividad.add(evento)
    return HttpResponseRedirect("/todas")

def prueba(request):
    template = get_template('index.html')
    c = Context({'title': "Nacho", "info" : 'Practica final'})
    rend = template.render(c)
    return HttpResponse(rend)

def cogerRss(request,resource):

    try:
        titulo = Usuario.objects.get(nombre=resource)
    except:
        titulo = ""
    
    descripcion = "Actividades: "

    for evento in titulo.actividad.all():
        descripcion += str(evento.id) + ", " 
    
    item = ""
    for evento in titulo.actividad.all():
        item += '\t\t<item>\n'
        item += '\t\t\t<title>'+ str(evento.id) + '</title>\n'
        item += '\t\t\t<link>' + "actividad/" + str(evento.id) + '</link>\n'
        item += '\t\t\t<pubDate>' +"" + '</pubDate>\n'
        item += '\t\t\t<description>' + evento.nombre + '</description>\n'
        item += '\t\t</item>\n'

    response = '<?xml version="1.0" encoding="UTF-8"?>\n'
    response += '<rss version="2.0">\n'
    response += '\t<channel>\n'
    if titulo == "":
        return HttpResponseNotFound('<h1>Resource Not Found</h1>')
    response += '\t\t<title>'+ str(titulo) + '</title>\n'
    response += '\t\t<link>'+ "/" + resource + '</link>\n'
    response += '\t\t<description>' + descripcion + '</description>\n'
    response += '\t\t<pubDate>' + "FECHA DE WISEL" + '</pubDate>\n'
    response += item
    response += '\t</channel>\n</rss>'
    return HttpResponse(response, content_type='rss')

@csrf_exempt
def diezMas(request):
    nombre_pag_usr = request.POST.get("nombre", '')
    fondo_css = request.POST.get("fondo", '')
    letra_css = request.POST.get("letra", '')
    try:
        info_usuario = Usuario.objects.get(nombre = request.user)
        if nombre_pag_usr != "":
            info_usuario.evento = nombre_pag_usr
            if fondo_css != "":
                info_usuario.fondo = fondo_css
            if letra_css != "":
                info_usuario.letra = letra_css
            info_usuario.save()
    except Usuario.DoesNotExist:
        info_usuario = Usuario(nombre = request.user, evento = nombre_pag_usr, fondo = fondo_css, letra = letra_css)
        info_usuario.save()

    return HttpResponseRedirect("/" + str(request.user))
    
