from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import TemplateManager

main = Blueprint('main', __name__)

@main.route('/')
def index():
    templates = TemplateManager.get_all_templates()
    return render_template('index.html', templates=templates)

@main.route('/template/add', methods=['GET', 'POST'])
def add_template():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        TemplateManager.add_template({'title': title, 'content': content})
        flash('Template added successfully!')
        return redirect(url_for('main.index'))
    return render_template('add_template.html')

@main.route('/template/edit/<template_id>', methods=['GET', 'POST'])
def edit_template(template_id):
    template = TemplateManager.get_template_by_id(template_id)
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        TemplateManager.update_template(template_id, {'title': title, 'content': content})
        flash('Template updated successfully!')
        return redirect(url_for('main.index'))
    return render_template('edit_template.html', template=template)

@main.route('/template/delete/<template_id>')
def delete_template(template_id):
    TemplateManager.delete_template(template_id)
    flash('Template deleted successfully!')
    return redirect(url_for('main.index'))
