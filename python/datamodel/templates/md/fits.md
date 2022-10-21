{% extends "md/base.md" %}

{# A list of FITS hdus for the content block #}
{% block content %}
{% for hdu_id, hdu in data.items() %}
  - [{{ hdu_id | upper }}: {{ hdu.name }}](#{{hdu_id | lower}}-{{hdu.name | lower}})
{% endfor %}
{% endblock content %}

{# Example HDU rendering for the example block #}
{% block example %}
{% for hdu_id, hdu in data.items() %}

### {{ hdu_id | upper }}: {{ hdu.name }}
{{ hdu.description }}

#### HDU Type: {{ 'IMAGE' if hdu.is_image else 'BINARY TABLE' }}
#### HDU Size:  {{ hdu.size }}

{% if hdu.header %}
##### Header Table Caption for {{ hdu_id | upper }}
Key | Value | Comment | |
| --- | --- | --- | --- |
{% for header in hdu.header %}
| {{ header.key }} | {{ header.value }} | {{ header.comment }} |
{% endfor %}
{% endif %}

{% if not hdu.is_image %}
{# BINARY TABLE HDUS #}
##### Binary Table Caption for {{ hdu_id | upper }}
Name | Type | Unit | Description |
| --- | --- | --- | --- |
{% for key, column in hdu.columns.items() %}
 | {{ column.name }} | {{ column.type }} | {{ column.unit }} | {{ column.description }} |
{% endfor %}

{% endif %}

{% endfor %}
{% endblock example %}