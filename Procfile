{% extends "base.html" %}
{% from "_macros.html" import render_field %}
{% block title %}{{ titre }} — GBV{% endblock %}
{% block page_title %}{{ titre }}{% endblock %}
{% block content %}
<div class="row justify-content-center"><div class="col-lg-6">
  <div class="form-card">
    <h5 class="mb-4"><i class="bi bi-geo-alt me-2 text-success"></i>{{ titre }}</h5>
    <form method="post">
      {{ form.hidden_tag() }}
      {{ render_field(form.libelle_c, placeholder="Ex: Abidjan Plateau") }}
      <div class="row">
        <div class="col-6">{{ render_field(form.longitude, placeholder="-3.9969") }}</div>
        <div class="col-6">{{ render_field(form.latitude,  placeholder="5.3600") }}</div>
      </div>
      <hr>
      <div class="d-flex gap-2">
        {{ form.submit(class="btn btn-primary") }}
        <a href="{{ url_for('communes.index') }}" class="btn btn-outline-secondary">Annuler</a>
      </div>
    </form>
  </div>
</div></div>
{% endblock %}
