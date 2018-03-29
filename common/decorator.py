# from functools import wraps
# from flask import jsonify
# from flask_login import login_required, current_user
#
#
# # @login_required
# def info_required(func):
#     @wraps(func)
#     def func_wrapper(*args, **kwargs):
#         if current_user is not None:
#             if current_user.role:
#                 if not current_user.name or not current_user.phone:
#                     return jsonify({
#                         'message': 'Name and phone number are required!'
#                     })
#                 else:
#                     return func(*args, **kwargs)
#             else:
#                 if not current_user.name or not current_user.job:
#                     return jsonify({
#                         'message': 'Name and job information are required!'
#                     })
#                 else:
#                     return func(*args, **kwargs)
#         else:
#             return jsonify({
#                 'message': 'Current user is None!'
#             })
#     return func_wrapper()
