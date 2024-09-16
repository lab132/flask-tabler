from dominate.tags import *


def render_form(render_form, title, action, method="POST", submit_text="Submit"):
    result_form = form(_class="card", action=action, method=method)
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
                    with div(_class="mb-3"):
                        div(str(field.label), _class="form-label")
                        input_field = input_(_class="form-control", type=field.type, name=field.name, id=field.id, value=field.data)
                        if render_form.errors and field.name in render_form.errors:
                            input_field["class"] += " is-invalid"
                            with div(_class="invalid-feedback"):
                                div(render_form.errors[field.name])
        with div(_class="card-footer text-end"):
            button(submit_text, _class="btn btn-primary", type="submit", value=submit_text)

    return result_form

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
                                td(obj[header])
                            if action_cb:
                                with td() as action_col:
                                    action_cb(action_col, obj)

    return container
