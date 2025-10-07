def render_template(template_path, context):
    if isinstance(template_path, str):
        with open(template_path, 'r', encoding='utf-8') as f:
            tpl = f.read()
    else:
        tpl = template_path
    for k, v in context.items():
        tpl = tpl.replace('{' + k + '}', v)
    return tpl
