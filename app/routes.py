from flask import Blueprint, render_template, request, redirect, url_for, flash , jsonify

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
        tags = request.form.getlist('tags')  # Retrieve multiple select values
        TemplateManager.add_template({'title': title, 'content': content, 'tags': tags})
        flash('Template added successfully!')
        return redirect(url_for('main.index'))
    return render_template('add_template.html')

@main.route('/template/details/<template_id>')
def template_details(template_id):
    template = TemplateManager.get_template_by_id(template_id)
    if template:
        return jsonify({
            'title': template['title'],
            'content': template['content']
        })
    else:
        return jsonify({'error': 'Template not found'}), 404

@main.route('/template/edit/<template_id>', methods=['GET', 'POST'])
def edit_template(template_id):
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        tags = request.form.getlist('tags')  # Assuming tags are also editable

        if TemplateManager.update_template(template_id, {'title': title, 'content': content, 'tags': tags}):
            flash('Template updated successfully!')
        else:
            flash('Failed to update template.')
        return redirect(url_for('main.index'))
    else:
        template = TemplateManager.get_template_by_id(template_id)
        if template is not None:
            return render_template('edit_template.html', template=template)
        else:
            flash('Template not found.')
            return redirect(url_for('main.index'))


@main.route('/template/delete/<template_id>')
def delete_template(template_id):
    TemplateManager.delete_template(template_id)
    flash('Template deleted successfully!')
    return redirect(url_for('main.index'))

@main.route('/tags/<tag>')
def filter_by_tag(tag):
    templates = TemplateManager.get_templates_by_tag(tag)
    if not templates:
        flash(f"No templates found for tag: {tag}")
    return render_template('index.html', templates=templates)

@main.route('/search', methods=['GET'])
def search_templates():
    query = request.args.get('search', '')
    if query:
        templates = TemplateManager.search_templates(query)
        if not templates:
            flash('No templates found matching your search criteria.')
    else:
        templates = TemplateManager.get_all_templates()
    
    return render_template('index.html', templates=templates)
