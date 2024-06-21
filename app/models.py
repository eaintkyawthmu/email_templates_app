from bson.objectid import ObjectId
from flask import current_app
from .db import mongo_client

class TemplateManager:
    def __init__(self):
        self.db = mongo_client.email_templates

    def count_templates(self):
        return self.db.templates.count_documents({})

    @staticmethod
    def get_all_templates(page=1, per_page=10):
        """Retrieve templates with pagination."""
        try:
            skip_amount = (page - 1) * per_page
            templates = mongo_client.email_templates.templates.find().skip(skip_amount).limit(per_page)
            return list(templates)
        except Exception as e:
            current_app.logger.error("Failed to retrieve templates: %s", e)
            return []

    @staticmethod
    def get_template_by_id(template_id):
        """Retrieve a specific template by its ID."""
        try:
            return mongo_client.email_templates.templates.find_one({'_id': ObjectId(template_id)})
        except Exception as e:
            current_app.logger.error(f"Error retrieving template by ID {template_id}: {e}")
            return None

    @staticmethod
    def get_templates_by_tag(tag, page=1, per_page=10):
        """Retrieve templates by a specific tag with pagination."""
        try:
            skip_amount = (page - 1) * per_page
            templates = mongo_client.email_templates.templates.find({"tags": tag}).skip(skip_amount).limit(per_page)
            return list(templates)
        except Exception as e:
            current_app.logger.error(f"Error retrieving templates by tag {tag}: {e}")
            return []

    @staticmethod
    def add_template(data):
        """Add a new template to the database."""
        try:
            return mongo_client.email_templates.templates.insert_one(data).inserted_id
        except Exception as e:
            current_app.logger.error(f"Error adding new template: {e}")
            return None

    @staticmethod
    def update_template(template_id, data):
        """Update an existing template."""
        try:
            result = mongo_client.email_templates.templates.update_one({'_id': ObjectId(template_id)}, {'$set': data})
            return result.modified_count > 0  # Indicates a successful update
        except Exception as e:
            current_app.logger.error(f"Error updating template ID {template_id}: {e}")
            return False

    @staticmethod
    def delete_template(template_id):
        """Delete a template by its ID."""
        try:
            result = mongo_client.email_templates.templates.delete_one({'_id': ObjectId(template_id)})
            return result.deleted_count > 0  # Indicates a successful deletion
        except Exception as e:
            current_app.logger.error(f"Error deleting template ID {template_id}: {e}")
            return False

    @staticmethod
    def search_templates(query, page=1, per_page=10):
        """Search templates by text index with pagination."""
        try:
            skip_amount = (page - 1) * per_page
            templates = mongo_client.email_templates.templates.find({"$text": {"$search": query}}).skip(skip_amount).limit(per_page)
            return list(templates)
        except Exception as e:
            current_app.logger.error(f"Error searching templates: {e}")
            return []

    @staticmethod
    def calculate_total_pages(total_items, per_page):
        """Calculate the total number of pages needed to display all items."""
        return (total_items + per_page - 1) // per_page
