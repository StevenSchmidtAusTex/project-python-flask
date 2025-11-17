from flask import Blueprint, request, jsonify
from ..services.user_service import create_role, assign_role_to_user

# ISSUE IV Add API endpoints for creating and assigning a role

# @user_routes.route("/roles", methods=["POST"])
# def create_role_route();

# @user_routes.route("/users/<int:user_id>/roles", methods=["POST"])
# def assign_role_route(user_id)
