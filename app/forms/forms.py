from wtforms import Form, StringField, SelectField, validators, SubmitField, TextAreaField, FormField
from wtforms.fields.choices import SelectMultipleField
from wtforms.fields.list import FieldList

class ResourceForm(Form):
    title = StringField()
    format = StringField()
    endpointUrl = StringField()

class TransitNetworkForm(Form):
    title = StringField('Titre', [validators.InputRequired(), validators.Length(max=200)], render_kw={"placeholder": "Titre du réseau de transport..."})
    description = TextAreaField('Description', [validators.optional()])
    external_id = StringField('ID externe', [validators.InputRequired()])
    endpoint_url = StringField('URL', [validators.optional(), validators.URL(), validators.Length(max=200)], render_kw={"placeholder": "https://exemple.com/gtfs.zip..."})
    city_or_region = StringField("Ville ou Zone concernée", [validators.InputRequired()])
    resources = FieldList(FormField(ResourceForm))
    country_code = StringField('Code du Pays', [validators.InputRequired()])


class CreateTransitNetworkForm(TransitNetworkForm):
    submit = SubmitField('Ajouter le réseau de transport')

class ModifyTransitNetworkForm(TransitNetworkForm):
    submit = SubmitField('Enregistrer les modifications')
