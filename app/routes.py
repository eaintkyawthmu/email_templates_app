from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from .models import TemplateManager
import logging

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/page/<int:page>')
def index(page=1, per_page=10):
    total_items = current_app.mongo.email_templates.templates.count_documents({})
    total_pages = TemplateManager.calculate_total_pages(total_items, per_page)
    templates = TemplateManager.get_all_templates(page, per_page)
    return render_template('index.html', templates=templates, page=page, total_pages=total_pages)

@main.route('/template/add', methods=['GET', 'POST'])
def add_template():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        tags = request.form.getlist('tags')
        if TemplateManager.add_template({'title': title, 'content': content, 'tags': tags}):
            flash('Template added successfully!')
        else:
            flash('Failed to add template.')
        return redirect(url_for('main.index'))
    return render_template('add_template.html')

@main.route('/template/edit/<template_id>', methods=['GET', 'POST'])
def edit_template(template_id):
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        tags = request.form.getlist('tags')
        if TemplateManager.update_template(template_id, {'title': title, 'content': content, 'tags': tags}):
            flash('Template updated successfully!')
        else:
            flash('Failed to update template.')
        return redirect(url_for('main.index'))
    else:
        template = TemplateManager.get_template_by_id(template_id)
        if template:
            return render_template('edit_template.html', template=template)
        else:
            flash('Template not found.')
            return redirect(url_for('main.index'))

@main.route('/template/delete/<template_id>')
def delete_template(template_id):
    if TemplateManager.delete_template(template_id):
        flash('Template deleted successfully!')
    else:
        flash('Failed to delete template.')
    return redirect(url_for('main.index'))

@main.route('/search', methods=['GET'])
def search_templates():
    query = request.args.get('search', '')
    page = request.args.get('page', 1, type=int)
    per_page = 10
    total_items = current_app.mongo.email_templates.templates.count_documents({"$text": {"$search": query}})
    total_pages = TemplateManager.calculate_total_pages(total_items, per_page)
    templates = TemplateManager.search_templates(query, page, per_page)
    return render_template('index.html', templates=templates, page=page, total_pages=total_pages)

@main.route('/tags/<tag>/page/<int:page>')
def filter_by_tag(tag, page=1, per_page=10):
    total_items = current_app.mongo.email_templates.templates.count_documents({"tags": tag})
    total_pages = TemplateManager.calculate_total_pages(total_items, per_page)
    templates = TemplateManager.get_templates_by_tag(tag, page, per_page)
    return render_template('index.html', templates=templates, page=page, total_pages=total_pages, tag=tag)

@main.route('/favicon.ico')
def favicon():
    try:
        return current_app.send_static_file('favicon.ico')
    except Exception as e:
        logging.error(f"Error serving favicon: {e}")
        abort(404)