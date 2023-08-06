from docutils import nodes

def link_attr_visit_external_reference_advice(func,
                                              attr_internal, suffix_internal,
                                              attr_external, suffix_external):
    def advice(self, node):
        def modify_attr(node, attr, suffix):
            for key, value in attr.items():
                node[key] = value
            if suffix:
                if isinstance(suffix, dict):
                    node.children.append(
                        getattr(nodes, suffix['node'])(**suffix)
                    )
                    # Because the update of a configuration is checked by using '!='
                    # (see _update_config in sphinx/environment/__init__.py),
                    # the use of Python classes causes misdetection of updates,
                    # at least at Sphinx v 4.0.2. Hence, we employ the above code.
                else:
                    node.children.append(nodes.Text(suffix))
        if ('refuri' in node):
            if node.get('internal'):
                modify_attr(node, attr_internal, suffix_internal)
            else:
                modify_attr(node, attr_external, suffix_external)
        return func(self, node)
    return advice

def link_attr_overrite_reference_visitor(app):
    format = app.builder.format

    if format in app.config.linkattr_custom_translator_dict:
        translator = app.config.linkattr_custom_translator_dict[format]
    else:
        import importlib
        WRITERS = {
            'text':    ('sphinx.writers.text',    'TextTranslator'),
            'html':    ('sphinx.writers.html',    'HTMLTranslator'),
            'latex':   ('sphinx.writers.latex',   'LaTeXTranslator'),
            'manpage': ('sphinx.writers.manpage', 'TexinfoTranslator'),
            'texinfo': ('sphinx.writers.texinfo', 'ManualPageTranslator'),
        }
        if format in WRITERS:
            translator = getattr(importlib.import_module(WRITERS[format][0]),
                                 WRITERS[format][1])
        else:
            raise ValueError("unknown format.")
    app.add_node(nodes.reference,
                 override=True,
                 **{format:
                    (link_attr_visit_external_reference_advice(
                     translator.visit_reference,
                     app.config.linkattr_attr_internal,
                     app.config.linkattr_suffix_internal,
                     app.config.linkattr_attr_external,
                     app.config.linkattr_suffix_external),
                     translator.depart_reference)})

def setup(app):
    app.add_config_value('linkattr_attr_external',
                         {'target': '_blank', 'rel': 'nofollow'}, 'env', dict)
    app.add_config_value('linkattr_suffix_external',
                         None, 'env', (type(None), str, nodes.Node))
    app.add_config_value('linkattr_attr_internal',
                         {}, 'env', dict)
    app.add_config_value('linkattr_suffix_internal',
                         None, 'env', (type(None), str, nodes.Node))
    app.add_config_value('linkattr_custom_translator_dict',
                         {}, 'env', dict)

    app.connect('builder-inited', link_attr_overrite_reference_visitor)
    
    return {'parallel_read_safe': True, 'parallel_write_safe': True}

