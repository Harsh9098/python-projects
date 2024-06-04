# -*- coding: utf-8 -*-
# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models
from odoo.exceptions import ValidationError

class CommissionLevel(models.Model):
    _name = 'commission.level'
    _description = 'Commission Level'
    _rec_name = 'commssion_name'
    
    commssion_name = fields.Char('Sales Commission Level')
    commssion_code = fields.Char('Code')
    
    def create(self, vals):
        existing_level = self.env['commission.level'].search([('commssion_name', '=', vals.get('commssion_name'))])
        if existing_level:
            raise ValidationError("Commission level with this name already exists!")
        return super(CommissionLevel, self).create(vals)
    
class CommissionSetting(models.Model): 
    _name = 'commission.settings'
    _description = 'Commission Settings'
    
    commission_level_id = fields.Many2one('commission.level', 'Sales Commission Level')
    percentage = fields.Float('Percentage(%)')
    product_id = fields.Many2one('product.template', string='Product')
    sales_team_id = fields.Many2one('crm.team', string='Sales Team')
    product_category_id = fields.Many2one('product.category', string='Product Category')
    partner_id = fields.Many2one('res.partner', string='Users/Partner')
    sale_order_id = fields.Many2one('sale.order', string='Partner ')
    purchase_order_id = fields.Many2one('purchase.order', string='Partner')
    partner_coman_id = fields.Many2one('res.partner', string='Users/Partner ')
        
    @api.constrains('product_id', 'product_category_id', 'commission_level_id',
                    'sales_team_id', 'partner_id','sale_order_id')
    def _check_unique_per_product(self):
        for record in self:
            if record.product_id and record.commission_level_id:
                duplicate_product_settings = self.search([('product_id', '=', record.product_id.id),
                                                           ('commission_level_id', '=', record.commission_level_id.id),
                                                           ('id', '!=', record.id)])
                if duplicate_product_settings:
                    raise ValidationError("A product can have only one commission setting per level.")
            
            if record.product_category_id and record.commission_level_id:
                duplicate_category_settings = self.search([('product_category_id', '=', record.product_category_id.id),
                                                            ('commission_level_id', '=', record.commission_level_id.id),
                                                            ('id', '!=', record.id)])
                if duplicate_category_settings:
                    raise ValidationError("A product category can have only one commission setting per level.")
            
            if record.sales_team_id and record.commission_level_id:
                duplicate_sales_team_settings = self.search([('sales_team_id', '=', record.sales_team_id.id),
                                                             ('commission_level_id', '=', record.commission_level_id.id),
                                                             ('id', '!=', record.id)])
                if duplicate_sales_team_settings:
                    raise ValidationError("A sales team can have only one commission setting per level.")
            
            if record.partner_id and record.commission_level_id:
                duplicate_partner_settings = self.search([('partner_id', '=', record.partner_id.id),
                                                           ('commission_level_id', '=', record.commission_level_id.id),
                                                           ('id', '!=', record.id)])
                if duplicate_partner_settings:
                    raise ValidationError("A partner can have only one commission setting per level.")
            
            if record.sale_order_id and record.commission_level_id:
                duplicate_partner_settings = self.search([('sale_order_id', '=', record.sale_order_id.id),
                                                           ('commission_level_id', '=', record.commission_level_id.id),
                                                           ('id', '!=', record.id)])
                if duplicate_partner_settings:
                    raise ValidationError("A Sale oder can have only one commission setting per level.")
           
            if record.purchase_order_id and record.commission_level_id:
                    duplicate_partner_settings = self.search([('purchase_order_id', '=', record.purchase_order_id.id),
                                                            ('commission_level_id', '=', record.commission_level_id.id),
                                                            ('id', '!=', record.id)])
                    if duplicate_partner_settings:
                        raise ValidationError("A purchase oder can have only one commission setting per level.")
                
            