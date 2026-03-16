{% extends "md/base.md" %}

{% block content %}
- Primary data frame.
{% endblock content %}

{% block example %}
{% if data.metadata %}
### Metadata

{% for mdata in data.metadata %}
- {{ mdata.key }}: {{ mdata.description }}
{% endfor %}

{% endif %}

### Columns

{% for cname, cdata in data.columns.items() %}

#### {{ cname }}

- Column Name: {{ cdata.name }}
- Description: {{ cdata.description if cdata.description else "N/A" }}
- Unit: {{ cdata.unit if cdata.unit else "N/A" }}
- Data Type: {{ cdata.dtype }}

{% endfor %}
{% endblock example %}
