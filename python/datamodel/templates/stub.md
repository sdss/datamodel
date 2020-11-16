    There are {{ hdus | length }} hdus: 
    {% for hdu in hdus %}
    <div id="hdu{{loop.index0}}">
        <h2>HDU{{loop.index0}}: {{hdu.name}}</h2>
        <p>[Summarize contents of this HDU]</p>
        <dl>
        <dt>HDU Type</dt><dd>{{'IMAGE' if hdu.is_image else 'BINARY TABLE'}}</dd>
        <dt>HDU Size</dt><dd>{{hdu.size|getHDUSize}}</dd>
        </dl>
        {% set hdr = hdu.header %}

        {# IMAGE HDUS #}
        <table>
            <caption>Header Table Caption for HDU{{loop.index0}}</caption>
            <thead id="head{{loop.index0}}">
                <tr><th>Key</th><th>Value</th><th>Type</th><th>Comment</th></tr>
            </thead>
             <tbody id="body{{loop.index0}}">
                {% for key, value in hdr.items() %}
                    {% if key|isKeyAColumn %}
                    <tr><td>{{key}}</td><td>{{value}}</td><td>{{type}}</td><td>{{hdr.comments[key]}}</td></tr>
                    {% endif %}
                {% endfor %}
             </tbody>
        </table>

        {# BINARY TABLE HDUS #}
        {% if not hdu.is_image %}
        <table>
            <caption>Binary Table Caption for HDU{{loop.index0}}</caption>
            <thead id="binhead{{loop.index0}}">
                <tr><th>Name</th><th>Type</th><th>Unit</th><th>Description</th></tr>
            </thead>
             <tbody id="binbody{{loop.index0}}">
                {% for row in hdu.columns %}
                    <tr><td>{{row.name|upper}}</td><td>{{row.format|getType}}</td><td>Not Implemented</td><td></td></tr>
                {% endfor %}
             </tbody>
        </table>
        {% endif %}
    </div>
    {% endfor %}
