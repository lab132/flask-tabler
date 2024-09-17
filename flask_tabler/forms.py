from dominate.tags import *
from dominate.util import raw
import sys

def render_SelectField(field_container, field, multiple=False):
    with field_container:
        div(str(field.label), _class="form-label")
        with select(_class="form-select", id=field.id, value="", name=field.name) as select_field:
            if multiple:
                select_field["multiple"] = "multiple"
            for choice in field.choices:
                if choice is not tuple:
                    choice = (choice, choice)
                with option(choice[1], value=choice[0]):
                    if(choice[0] in field.data):
                        attr(selected="")

def render_SelectMultipleField(field_container, field):
    render_SelectField(field_container, field, multiple=True)


def render_ModelSelectMultipleField(field_container, field):
    with field_container:
        div(str(field.label), _class="form-label")
        with select(_class="form-select", id=field.id, value="", name=field.name, multiple="multiple", type="text"):
            for choice in field.queryset:
                with option(str(choice), value=choice.id):
                    for field_data in field.data:
                        if field_data.id == choice.id:
                            attr(selected="")
        

def render_script_SelectField(field):
    return [ script(raw(f"""
        document.addEventListener("DOMContentLoaded", function () {{
            new TomSelect(\"#{field.id}\" , {{
            copyClassesToDropdown: false,
    		dropdownParent: 'body',
    		controlInput: '<input>',
    		render:{{
    			item: function(data,escape) {{
    				if( data.customProperties ){{
    					return '<div><span class="dropdown-item-indicator">' + data.customProperties + '</span>' + escape(data.text) + '</div>';
    				}}
    				return '<div>' + escape(data.text) + '</div>';
    			}},
    			option: function(data,escape){{
    				if( data.customProperties ){{
    					return '<div><span class="dropdown-item-indicator">' + data.customProperties + '</span>' + escape(data.text) + '</div>';
    				}}
    				return '<div>' + escape(data.text) + '</div>';
    			}}
    		}}
        }});
        }});
    """))]

render_script_SelectMultipleField = render_script_SelectField
render_script_ModelSelectMultipleField = render_script_SelectMultipleField



def render_form(render_form, title, action, method="POST", submit_text="Submit"):
    result_form = form(_class="card", action=action, method=method, enctype="multipart/form-data")
    with result_form:
        for error in render_form.errors:
            if error in render_form:
                continue
            with div(_class="alert alert-danger"):
                h4(error, _class="alert-title")
                div(render_form.errors[error], _class="text-secondary")
        with div(_class="card-header"):
            h3(title, _class="card-title")
        with div(_class="card-body") as body:
            for field in render_form:
                if field.type == "CSRFTokenField":
                    body.add(render_form.csrf_token())
                else:
                    with div(_class="mb-3") as field_container:
                        render_callback = getattr(sys.modules[__name__], f"render_{field.type}", None)
                        if callable(render_callback):
                            render_callback(field_container, field)
                        else:
                            div(str(field.label), _class="form-label")
                            input_field = input_(_class="form-control", type=field.type, name=field.name, id=field.id, value=field.data, placeholder=field.description)   
                            if render_form.errors and field.name in render_form.errors:
                                input_field["class"] += " is-invalid"
                                with div(_class="invalid-feedback"):
                                    div(render_form.errors[field.name])
        with div(_class="card-footer text-end"):
            button(submit_text, _class="btn btn-primary", type="submit", value=submit_text)

    return result_form

def render_form_scripts(render_form):
    rendered_scripts = []
    for field in render_form:
        render_callback = getattr(sys.modules[__name__], f"render_script_{field.type}", None)
        if callable(render_callback):
            result = render_callback(field)
            print(result)
            if type(result) is list:
                rendered_scripts.extend(result)
            else:
                rendered_scripts.append(result)
    return "\n".join([script.render() for script in rendered_scripts])

def render_table(objects, headers, action_cb=None):
    container = div(_class="card")
    with container:
        with div(_class="table-responsive"):
            with table(_class="table table-vcenter card-table table-striped"):
                with thead():
                    with tr():
                        for header in headers:
                            th(header)
                        if action_cb:
                            th(_class="w-1")
                with tbody():
                    for obj in objects:
                        with tr():
                            for header in headers:
                                td(str(obj[header]))
                            if action_cb:
                                with td() as action_col:
                                    action_cb(action_col, obj)


    return container
