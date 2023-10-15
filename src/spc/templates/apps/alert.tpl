<div id="alert" class="alert-info hidden-xs" style="text-align: center">
    {% if cid is defined %}
        {% if not cid == '' %}
            <em>NOTE: Using inputs from case id: {{ cid }}</em>
        {% else %}
            <em>NOTE: Using default inputs</em>
        {% endif %}
    {% endif %}
</div>
