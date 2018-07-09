 <button name="button_validate_internal_tranf" attrs="{'invisible': ['|','|',('sale_return','=',True),('picking_type_code', 'in', ['outgoing','incoming']),('state','not in', ['rm_audit_manager_approval'])]}" string="Aduit Manager Validate" groups="ds_workflows.audit_manager" 
                                type="object" class="oe_highlight"/>
								
								
								
								
 @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        result = super(product_product, self).fields_view_get(view_id, view_type, toolbar=toolbar, submenu=submenu)
        if view_type=="form":
            doc = etree.XML(result['arch'])
            for node in doc.iter(tag="field"):
                if 'readonly' in node.attrib.get("modifiers",''):
                    attrs = node.attrib.get("attrs",'')
                    if 'readonly' in attrs:
                        attrs_dict = safe_eval(node.get('attrs'))
                        r_list = attrs_dict.get('readonly',)
                        if type(r_list)==list:
                            r_list.insert(0,('state','=','confirmed'))
                            if len(r_list)>1:
                                r_list.insert(0,'|')
                        attrs_dict.update({'readonly':r_list})
                        node.set('attrs', str(attrs_dict))
                        setup_modifiers(node, result['fields'][node.get("name")])
                        continue
                    else:
                        continue
                node.set('attrs', "{'readonly':[('state','=','confirmed')]}")
                setup_modifiers(node, result['fields'][node.get("name")])
                
            result['arch'] = etree.tostring(doc)
        return result