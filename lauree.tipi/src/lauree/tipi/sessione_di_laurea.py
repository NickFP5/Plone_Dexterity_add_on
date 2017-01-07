from five import grok
from plone.directives import dexterity, form

from zope import schema
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm

from zope.interface import invariant, Invalid

from z3c.form import group, field

from plone.namedfile.interfaces import IImageScaleTraversable
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile

from plone.app.textfield import RichText

from z3c.relationfield.schema import RelationList, RelationChoice
from plone.formwidget.contenttree import ObjPathSourceBinder

from lauree.tipi import MessageFactory as _










from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView

from lauree.tipi.laureando import Ilaureando





import csv
from StringIO import StringIO





from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.uuid.utils import uuidToObject






from plone import api







# Interface class; used to define content-type schema.

class Isessione_di_laurea(form.Schema, IImageScaleTraversable):
    """
    Sessione di laurea
    """

    # If you want a schema-defined interface, delete the form.model
    # line below and delete the matching file in the models sub-directory.
    # If you want a model-based interface, edit
    # models/sessione_di_laurea.xml to define the content type
    # and add directives here as necessary.

    form.model("models/sessione_di_laurea.xml")


# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class sessione_di_laurea(dexterity.Container):
    grok.implements(Isessione_di_laurea)

    # Add your class methods and properties here



# View class
# The view will automatically use a similarly named template in
# sessione_di_laurea_templates.
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@sampleview" appended.
# You may make this the default view for content objects
# of this type by uncommenting the grok.name line below or by
# changing the view class name and template filename to View / view.pt.

class SampleView(BrowserView):
    #grok.context(Isessione_di_laurea)
    #grok.require('zope2.View')

    # grok.name('view')
    def laureandi(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')

        return catalog(object_provides=Ilaureando.__identifier__,
			path='/'.join(context.getPhysicalPath()))
	#result =[]
	#for laureando in context.laureandi:
		#result.append(dict(url=laureando.absolute_url(),
		     #nome=laureando.laureando_name,
		     #matricola=laureando.laureando_matricola,))

	#return result


    def n_candidati(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')

	count = 0

        laureandi = catalog(object_provides=Ilaureando.__identifier__,
			path='/'.join(context.getPhysicalPath()))

	for brain in laureandi:
		count = count + 1

	return count


    def somma_medie_candidati(self):
        context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')

	sum = 0

        laureandi = catalog(object_provides=Ilaureando.__identifier__,
			path='/'.join(context.getPhysicalPath()))

	for brain in laureandi:
		if brain.laureando_avg:
			sum = sum + brain.laureando_avg

	return sum

    def medie_candidati(self):
	sum = self.somma_medie_candidati()
	count = self.n_candidati()
	voto_medio = round(sum/count, 3)
	return voto_medio


class ImportFromCSVView(BrowserView):
    #template="sessione_di_laurea_templates/import_from_csv.pt"
    template = ViewPageTemplateFile('sessione_di_laurea_templates\import_from_csv.pt')

    def __call__(self):
	risposta = self.request.form.items()

	if risposta:
		context = aq_inner(self.context)

		in_fd = open('in_laureandi.csv','r')
		out_fd = open('out_laureandi.txt', 'a+')

		for k,v in risposta:
			if k == "file":
				#out_fd.write(v)

				csv_io = StringIO(in_fd)
				#csv_reader = csv.reader(in_fd, delimiter=';', quotechar='"')
				csv_reader = csv.reader(v, delimiter=';', quotechar='"')
	
		for row in csv_reader:
			matricola = row[0]
			nome = row[1]
			cognome = row[2]
			media = row[3]
			relatore = row[4]

			portal = api.portal.get()
			obj = api.content.create(
    				type='lauree.tipi.laureando',
    				title=matricola,
    				container=context)

			obj.laureando_name = nome
			obj.laureando_matricola = matricola
			obj.laureando_surname = cognome
			obj.laureando_avg = float(media)
			obj.laureando_relatore = relatore

			out_fd.write(matricola)
			out_fd.write(nome)
			out_fd.write(cognome)
			out_fd.write(media)
			out_fd.write(relatore)

		return self.template()

	else:
		return self.template()

		


class CSVView(BrowserView):

    def __call__(self):
	context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')

        brains = catalog(object_provides=Ilaureando.__identifier__,
			path='/'.join(context.getPhysicalPath()))

	

	







	out = StringIO()
	writer = csv.writer(out)

	out.write("Matricola")
	out.write(";")
	out.write("Nome")
	out.write(";")
	out.write("Cognome")
	out.write(";")
	out.write("Relatore")
	out.write(";")
	out.write("Media")
	out.write(";")
	out.write("Titolo_tesi")
	out.write(";")
	out.write("Valutazione_proposta")
	out.write(";")
	out.write("Voto_proposto")
	out.write(";")
	out.write("Proposta_lode")
	out.write(";")
	out.write("\r")	

        for brain in brains:
		out.write(brain.laureando_matricola)
		out.write(";")
		out.write(brain.laureando_name)
		out.write(";")
		out.write(brain.laureando_surname)
		out.write(";")
		out.write('"')
		out.write(brain.laureando_relatore)
		out.write('"')
		out.write(";")
		out.write(brain.laureando_avg)
		out.write(";")
		out.write('"')
		out.write(brain.laureando_project)
		out.write('"')
		out.write(";")
		out.write(brain.laureando_valutazione)
		out.write(";")
		out.write(brain.laureando_voto_di_laurea)
		out.write(";")
		if brain.laureando_lode: out.write("Si")
		else: out.write("No")
		out.write(";")
		out.write("\r")	
	#out_file.close()

	filename = "%s.csv" % context.ID

	self.request.response.setHeader('Content-Type', 'text/csv')
	self.request.response.setHeader('Content-Disposition', 'attachment; filename="%s"' % filename)

        return out.getvalue()




class ChangeStateToLaureatoView(BrowserView):

    template = ViewPageTemplateFile('sessione_di_laurea_templates\mass_approval.pt')

    def laureandi(self):

	context = aq_inner(self.context)
        catalog = getToolByName(context, 'portal_catalog')

        laureandi_list = catalog(object_provides=Ilaureando.__identifier__,
			path='/'.join(context.getPhysicalPath()))
	
	pubblicandi = []
	for laureando in laureandi_list:
		status = laureando.review_state
		if status == "published":
			pubblicandi.append(laureando)

	return pubblicandi

    def __call__(self):
	risposta = self.request.form.items()
	

	if risposta:
		out_file = open('risposta_http.txt','w')
        	for key, value in risposta:
			if value == "on":
				obj = uuidToObject(key)
				workflowTool = getToolByName(obj, "portal_workflow")
				workflowTool.doActionFor(obj, "move_to_laureato_state")  
			out_file.write(key)
			out_file.write(" ")
			out_file.write(value)
			out_file.write("\r")
		out_file.close()
		return self.template()

	else:
		return self.template()

	