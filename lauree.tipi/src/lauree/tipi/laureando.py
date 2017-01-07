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









from Products.CMFCore.utils import getToolByName

@grok.provider(IContextSourceBinder)
def lista_relatori(self):
	terms = []
	membership = getToolByName(self, 'portal_membership')
	for member in membership.listMembers():
		if member.has_role('Relatore'):
    			terms.append(member.getProperty('fullname'))
	voc = SimpleVocabulary.fromValues(terms)
	return voc





@grok.provider(IContextSourceBinder)
def lista_possibili_valutazioni(self):
	terms = []
	v, d = divmod((8*3*(self.laureando_avg)/(27*11)), 1)
	#v = round(8*3*(self.laureando_avg)/(27*11))
	if v > 8:
		v = 8
	while v >= 0:
    		terms.append(v)
		v = v - 1
	voc = SimpleVocabulary.fromValues(terms)
	return voc


@grok.provider(IContextSourceBinder)
def lista_possibili_nlodi(self):
	terms = []
	n = 0
	while n < 22:
    		terms.append(n)
		n = n + 1
	voc = SimpleVocabulary.fromValues(terms)
	return voc







from DateTime import DateTime


@grok.provider(IContextSourceBinder)
def years_voc(self):
	zope_DT = DateTime()
	python_dt = zope_DT.asdatetime()
	curr_year = python_dt.year
	last_year = int(curr_year) -3
	init_year = int(curr_year) - 10
	years = []
	y = init_year
	while y <= last_year:
		years.append(y)
		y = y + 1

	voc = SimpleVocabulary.fromValues(years)
	return voc
	

def validatore_matricola(value):
	if value:
		l = len(value)
		caratteri_iniziali = value[0:3]
		"""
		if caratteri_iniziali not in ["O46","O45"] or l != 9:
			raise Invalid(
				_(u"Il formato della matricola inserita risulta errato.")
			)
		"""
		if l != 9:
			raise Invalid(
				_(u"La matricola deve essere lunga 9 caratteri.")
			)
		if caratteri_iniziali not in ["O46","O45"]:
			raise Invalid(
				_(u"I primi tre caratteri della matricola inserita sono errati.")
			)
		
		
	return True
		


	

# Interface class; used to define content-type schema.

class Ilaureando(form.Schema, IImageScaleTraversable):
    """
    studente laureando
    """

    # If you want a schema-defined interface, delete the form.model
    # line below and delete the matching file in the models sub-directory.
    # If you want a model-based interface, edit
    # models/laureando.xml to define the content type
    # and add directives here as necessary.

    laureando_name = schema.TextLine(
        title=_(u'Nome'),
        description=_(u'Inserire nome dello studente.'),
        required=True)

    laureando_surname = schema.TextLine(
        title=_(u'Cognome'),
        description=_(u'Inserire cognome dello studente.'),
        required=True)

    laureando_matricola = schema.TextLine(
        title=_(u'Matricola'),
	constraint = validatore_matricola,
        required=True)

    #form.read_permission(laureando_avg='laureando.privilegi_segreteria')
    form.write_permission(laureando_avg='laureando.privilegi_segreteria')
    laureando_avg = schema.Float(
        title=_(u'Media'),
        required=True)

    #form.read_permission(laureando_nlodi='laureando.privilegi_segreteria')
    #form.write_permission(laureando_nlodi='laureando.privilegi_segreteria')
    laureando_nlodi = schema.Choice(
        title=_(u'N. lodi'),
        description=_(u'Inserisci il numero di lodi.'),
	source = lista_possibili_nlodi,
        required=False)

    #form.read_permission(laureando_anno_immatricolazione='laureando.privilegi_segreteria')
    #form.write_permission(laureando_anno_immatricolazione='laureando.privilegi_segreteria')
    laureando_anno_immatricolazione = schema.Choice(
        title=_(u'Anno immatricolazione'),
        description=_(u'Seleziona anno di immatricolazione.'),
	source = years_voc,
        required=False)

    laureando_relatore = schema.Choice(
        title=_(u'Relatore'),
        description=_(u'Seleziona il relatore.'),
	source = lista_relatori,
	required=True)

    laureando_project = schema.TextLine(
        title=_(u'Progetto'),
        description=_(u'Titolo della tesi.'),
        required=False)

    laureando_project_description = schema.Text(
        title=_(u'Descrizione progetto'),
        description=_(u'Dettagli aggiuntivi.'),
        required=False)

    laureando_project_file = NamedFile(
        title=_(u'Upload della tesi.'),
        required=False)

    #form.read_permission(laureando_valutazione='laureando.privilegi_commissione')
    form.write_permission(laureando_valutazione='laureando.privilegi_commissione')
    laureando_valutazione = schema.Choice(
        title=_(u'Valutazione progetto'),
        description=_(u'Valutazione del progetto (relatore).'),
	source = lista_possibili_valutazioni,
        required=False)

    #form.omitted('laureando_voto_di_laurea')
    #form.read_permission(laureando_voto_di_laurea='laureando.privilegi_presidente')
    form.write_permission(laureando_voto_di_laurea='laureando.privilegi_presidente')
    laureando_voto_di_laurea = schema.Int(
        title=_(u'Voto di laurea'),
        required=False)

    #form.read_permission(laureando_lode='laureando.privilegi_presidente')
    form.write_permission(laureando_lode='laureando.privilegi_presidente')
    laureando_lode = schema.Bool(
        title=_(u'Lode'),
        required=False)

    



# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

class laureando(dexterity.Item):
    grok.implements(Ilaureando)

    # Add your class methods and properties here
    #voto_di_base = 11*(self.laureando_avg)/3 + (self.laureando_nlodi)/3

    def isValid(self):
	if self.laureando_valutazione:
		return 1
	else:
		return 0

    def isComplete(self):
	
	if self.laureando_valutazione:
		#Voto = 11/3 * M + C + P + L + E
		
		#(C + P + L + E) <=11
		#Il voto della prova finale, V, è calcolato tramite C <= 8/27 M
		#(L + E) <= 2
		
		
		#max_voto_proposto = round(8*(self.laureando_avg)/27)

		zope_DT = DateTime()
		python_dt = zope_DT.asdatetime()
		curr_year = python_dt.year

		bonus_temporale = 0
		
		if self.laureando_nlodi:
			bonus_lodi = ((self.laureando_nlodi)/3)
		else:
			bonus_lodi = 0

		if self.laureando_anno_immatricolazione:
			if (curr_year - (self.laureando_anno_immatricolazione) -3) == 1:
				bonus_temporale = 1
			if (curr_year - (self.laureando_anno_immatricolazione) -3) == 0:
				bonus_temporale = 2

		if bonus_lodi > 2:
			bonus_lodi = 2
			
		if (bonus_temporale + bonus_lodi + self.laureando_valutazione) > 11:
			totale = (self.laureando_avg) + 11
		else:
			totale = (self.laureando_avg) + bonus_temporale + bonus_lodi + self.laureando_valutazione

		if round(totale) > 110:
			self.laureando_voto_di_laurea = int(110)
		else:
			self.laureando_voto_di_laurea = int(round(totale))

		if (3*(self.laureando_avg)/11) >= 28:
			self.laureando_lode = True
		else:
			self.laureando_lode = False

		return 1
	else:
		return 0

   


# View class
# The view will automatically use a similarly named template in
# laureando_templates.
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@sampleview" appended.
# You may make this the default view for content objects
# of this type by uncommenting the grok.name line below or by
# changing the view class name and template filename to View / view.pt.

class SampleView(grok.View):
    grok.context(Ilaureando)
    grok.require('zope2.View')

    # grok.name('view')
