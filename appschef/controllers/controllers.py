# -*- coding: utf-8 -*-
# from odoo import http


# class Appschef(http.Controller):
#     @http.route('/appschef/appschef', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/appschef/appschef/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('appschef.listing', {
#             'root': '/appschef/appschef',
#             'objects': http.request.env['appschef.appschef'].search([]),
#         })

#     @http.route('/appschef/appschef/objects/<model("appschef.appschef"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('appschef.object', {
#             'object': obj
#         })

