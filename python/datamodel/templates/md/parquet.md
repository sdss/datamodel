{% extends "md/base.md" %}

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
- Description: {{ cdata.description }}
- Unit: {{ cdata.unit }}
- Data Type: {{ cdata.dtype }}

{% endfor %}
