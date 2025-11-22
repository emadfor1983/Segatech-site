from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from .models import Inquiry, Project, db

admin_bp = Blueprint('admin', __name__, url_prefix='/admin/api')

@admin_bp.route('/inquiries')
@login_required
def get_inquiries_admin():
    inquiries = Inquiry.query.order_by(Inquiry.created_at.desc()).all()
    return jsonify([inquiry.to_dict() for inquiry in inquiries])

@admin_bp.route('/inquiries/<int:inquiry_id>', methods=['PUT'])
@login_required
def update_inquiry_status(inquiry_id):
    inquiry = Inquiry.query.get_or_404(inquiry_id)
    data = request.get_json()
    
    inquiry.status = data.get('status', inquiry.status)
    db.session.commit()
    
    return jsonify({'success': True, 'inquiry': inquiry.to_dict()})

@admin_bp.route('/projects', methods=['POST'])
@login_required
def create_project():
    data = request.get_json()
    
    project = Project(
        title=data['title'],
        description=data['description'],
        category=data['category'],
        technologies=data.get('technologies', '[]'),
        image_url=data.get('image_url', ''),
        client=data.get('client', ''),
        duration=data.get('duration', ''),
        status=data.get('status', 'completed'),
        year=data.get('year', datetime.now().year)
    )
    
    db.session.add(project)
    db.session.commit()
    
    return jsonify({'success': True, 'project_id': project.id})