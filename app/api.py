from flask import Flask, request, jsonify
from .models.expert import Expert
from .models.service import Service
from .models.booking import Booking
from .models.message import Message
from .models import db
from datetime import datetime, timedelta
from .schemas import ExpertCreateSchema, ServiceCreateSchema, BookingCreateSchema, MessageCreateSchema
from pydantic import ValidationError

def register_routes(app):

    # Route for registering new experts
    @app.route('/api/experts/', methods=['POST'])
    def register_expert():
        data = request.get_json()
        try:
            validated_data = ExpertCreateSchema(**data)
        except ValidationError as err:
            return jsonify(err.errors()), 400

        expert = Expert(
            name=validated_data.name,
            email=validated_data.email,
            bio=validated_data.bio,
            profile_picture_url=validated_data.profile_picture_url
        )
        expert.set_password(validated_data.password)
        db.session.add(expert)
        db.session.commit()
        return jsonify({
            'id': str(expert.id),
            'name': expert.name,
            'email': expert.email
        }), 201
    

    # Route for registering a new service

    @app.route('/api/services/', methods=['POST'])
    # @token_required
    def create_service(current_expert):
        data = request.get_json()

        try:
            validated_data = ServiceCreateSchema(**data)
        except ValidationError as err:
            return jsonify(err.errors()), 400

        service = Service(
            expert_id=current_expert.id,
            service_type=validated_data.service_type,
            title=validated_data.title,
            description=validated_data.description,
            price=validated_data.price,
            duration=validated_data.duration
        )
        db.session.add(service)
        db.session.commit()
        return jsonify({
            'id': str(service.id),
            'service_type': service.service_type,
            'title': service.title
        }), 201

    # Route for booking a certain service 

    @app.route('/api/bookings/', methods=['POST'])
    def book_service():
        data = request.get_json()
        service = Service.query.get(data['service_id'])
        if not service:
            return jsonify({'error': 'Service not found'}), 404

        expiry_time = datetime.utcnow() + timedelta(days=2)
        booking = Booking(
            service_id=service.id,
            user_email=data['user_email'],
            expiry_time=expiry_time
        )
        db.session.add(booking)
        db.session.commit()
        return jsonify({
            'id': booking.id,
            'service_id': booking.service_id,
            'user_email': booking.user_email,
            'status': booking.status,
            'expiry_time': booking.expiry_time
        }), 201

    # Route for checking messages 
    @app.route('/api/bookings/<int:booking_id>/messages/', methods=['POST'])
    def send_priority_dm(booking_id):
        booking = Booking.query.get(booking_id)
        if not booking:
            return jsonify({'error': 'Booking not found'}), 404

        data = request.get_json()
        message = Message(
            booking_id=booking.id,
            message=data['message']
        )
        db.session.add(message)
        db.session.commit()
        return jsonify({
            'id': message.id,
            'booking_id': message.booking_id,
            'message': message.message,
            'sent_at': message.sent_at
        }), 201

    # Route for checking bookings done 

    @app.route('/api/bookings/', methods=['GET'])
    def get_bookings():
        expert_id = request.args.get('expert_id')
        service_type = request.args.get('service_type')
        status = request.args.get('status')

        query = db.session.query(Booking).join(Service).filter(Service.expert_id == expert_id)
        if service_type:
            query = query.filter(Service.service_type == service_type)
        if status:
            query = query.filter(Booking.status == status)

        bookings = query.all()

        return jsonify([{
            'id': booking.id,
            'service_id': booking.service_id,
            'user_email': booking.user_email,
            'status': booking.status,
            'expiry_time': booking.expiry_time
        } for booking in bookings]), 200
    
    # api for checking all the services
    @app.route('/api/experts-services/', methods=['GET'])
    def get_expert_services():
        experts = Expert.query.all()
        if not experts:
            return jsonify({'message': 'No experts found'}), 200

        expert_service_list = []

        for expert in experts:
            services = Service.query.filter_by(expert_id=expert.id).all()
            expert_info = {
                'expert_name': expert.name,
                'expert_bio': expert.bio,
                'profile_picture_url': expert.profile_picture_url,
                'services': []
            }

            for service in services:
                service_info = {
                    'service_id': service.id,
                    'service_type': service.service_type,
                    'title': service.title,
                    'description': service.description,
                    'price': service.price,
                    'duration': service.duration
                }
                expert_info['services'].append(service_info)

            expert_service_list.append(expert_info)

        return jsonify(expert_service_list), 200
    
    # Default Route

    @app.route("/")
    def home():
        return "Welcome to Checkmate.io !!"
    