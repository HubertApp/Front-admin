from wtforms import Form, StringField, SelectField, validators, SubmitField, TextAreaField

class APIForm(Form):
    title = StringField('Titre', [validators.InputRequired(), validators.Length(max=100)], render_kw={"placeholder": "Titre de l'API..."})
    description = TextAreaField('Description', [validators.optional()])
    type = SelectField('Type de données', choices=[('gtfs', 'GTFS'), ('netex', 'NetEX'), ('geojson', 'GeoJSON'), ('gtfsrt', 'GTFS-RT')], validators=[validators.InputRequired()])
    endpoint_url = StringField('URL', [validators.InputRequired(), validators.URL(), validators.Length(max=200)], render_kw={"placeholder": "https://api.exemple.com/endpoint..."})
    api_key = StringField('Clé API', [validators.Optional(), validators.Length(max=100)], render_kw={"placeholder": "Clé API si nécessaire..."})


class CreateAPIForm(APIForm):
    submit = SubmitField('Ajouter l\'API')

class ModifyAPIForm(APIForm):
    submit = SubmitField('Enregistrer les modifications')
    
    