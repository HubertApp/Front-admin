from wtforms import Form, StringField, SelectField, validators, SubmitField, TextAreaField

class TransitNetworkForm(Form):
    title = StringField('Titre', [validators.InputRequired(), validators.Length(max=200)], render_kw={"placeholder": "Titre du réseau de transport..."})
    description = TextAreaField('Description', [validators.optional()])
    external_id = StringField('ID externe', [validators.InputRequired()])
    #type = SelectField('Type de données', choices=[('gtfs', 'GTFS'), ('netex', 'NetEX'), ('geojson', 'GeoJSON'), ('gtfsrt', 'GTFS-RT')], validators=[validators.InputRequired()])
    endpoint_url = StringField('URL', [validators.optional(), validators.URL(), validators.Length(max=200)], render_kw={"placeholder": "https://api.exemple.com/endpoint..."})
    #api_key = StringField('Clé API', [validators.Optional(), validators.Length(max=100)], render_kw={"placeholder": "Clé API si nécessaire..."})
    city_or_region = StringField("Ville ou Zone concernée", [validators.InputRequired()])
    country_code = StringField('Code du Pays', [validators.InputRequired()])


class CreateTransitNetworkForm(TransitNetworkForm):
    submit = SubmitField('Ajouter le réseau de transport')

class ModifyTransitNetworkForm(TransitNetworkForm):
    submit = SubmitField('Enregistrer les modifications')
    
    