{% extends "md/base.md" %}

{# A list of Par tables for the content block #}
{% block content %}
{% for table in data['tables'] %}
  - [{{table}}](#{{table}})
{% endfor %}
{% endblock content %}

{# Example par rendering for the example block #}
{% block example %}
{# any yanny par comments #}
{% if data.comments %}
### Comments
```
{{ data.comments }}
```
{% endif %}

{# any yanny par header keys #}
{% if data.header %}
### Header

Key | Value | Comment | |
| --- | --- | --- | --- |
{% for header in data.header %}
| {{ header.key }} | {{ header.value }} | {{ header.comment }} |
{% endfor %}

{% endif %}

{# any yanny par tables #}
### Tables

{% for table, tdata in data.tables.items() %}

#### {{ table }}
- Description: {{ tdata.description }}
- Number of Rows: {{ tdata.n_rows }}

#### Structure
Name | Type | Unit | Description | Is Array | Example |
| --- | --- | --- | --- | --- | --- |
{% for column in tdata.structure %}
 | {{ column.name }} | {{ column.type }} | {{ column.unit }} | {{ column.description }} | {{ column.is_array }} | {{ column.example}} |
{% endfor %}

{% endfor %}
{% endblock example %}