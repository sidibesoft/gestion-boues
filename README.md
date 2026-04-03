{% extends "base.html" %}
{% block title %}Communes — GBV{% endblock %}
{% block page_title %}Communes{% endblock %}
{% block content %}
<div class="d-flex justify-content-between align-items-center mb-3">
  <h5 class="mb-0"><i class="bi bi-geo-alt me-2 text-success"></i>Communes</h5>
  <a href="{{ url_for('communes.nouveau') }}" class="btn btn-primary btn-sm"><i class="bi bi-plus-lg me-1"></i>Nouveau</a>
</div>
<div class="card table-card">
  <div class="table-responsive">
    <table class="table table-hover mb-0">
      <thead><tr><th>ID</th><th>Libellé</th><th>Longitude</th><th>Latitude</th><th>Stations</th><th>Ménages</th><th>Actions</th></tr></thead>
      <tbody>
        {% for c in communes %}
        <tr>
          <td>{{ c.id }}</td><td class="fw-semibold">{{ c.libelle_c }}</td>
          <td>{{ c.longitude or '—' }}</td><td>{{ c.latitude or '—' }}</td>
          <td><span class="badge bg-primary">{{ c.stations.all()|length }}</span></td>
          <td><span class="badge bg-success">{{ c.menages.all()|length }}</span></td>
          <td>
            <a href="{{ url_for('communes.modifier', id=c.id) }}" class="btn btn-sm btn-outline-secondary me-1"><i class="bi bi-pencil"></i></a>
            <form method="post" action="{{ url_for('communes.supprimer', id=c.id) }}" class="d-inline" onsubmit="return confirm('Confirmer ?')">
              <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
              <button class="btn btn-sm btn-outline-danger"><i class="bi bi-trash"></i></button>
            </form>
          </td>
        </tr>
        {% else %}
        <tr><td colspan="7" class="text-center text-muted py-4">Aucune commune. <a href="{{ url_for('communes.nouveau') }}">Ajouter.</a></td></tr>
        {% endfor %}
      </tbody>
    </table>
  </div>
</div>
{% endblock %}
