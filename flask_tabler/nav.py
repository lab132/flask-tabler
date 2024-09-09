from visitor import Visitor
from dominate.tags import *
from hashlib import sha1

class TablerRenderer(Visitor):
    def __init__(self, id=None):
        self._in_dropdown = False
        self.id = id

    def visit_Navbar(self, node):
        node_id = self.id or sha1(str(id(node)).encode()).hexdigest()

        root = header(_class='navbar navbar-expand-md navbar-overlap d-print-none')

        title_content = root.add(div(_class="container-xl"))

        collapse_button = title_content.add(button(_class='navbar-toggler', type='button'))

        collapse_button['data-bs-toggle'] = 'collapse'
        collapse_button['data-bs-target'] = '#navbar-menu'
        collapse_button['aria-controls'] = 'navbar-menu'
        collapse_button['aria-expanded'] = 'false'
        collapse_button['aria-label'] = 'Toggle navigation'

        collapse_button.add(span(_class='navbar-toggler-icon'))

        title = title_content.add(a(node.title, _class='navbar-brand navbar-brand-autodark d-none-navbar-horizontal pe-0 pe-md-3', href=node.get_url() if hasattr(node, "get_url") else "."))
        nav = title_content.add(div(_class='collapse navbar-collapse', id='navbar-menu'))

        nav_items = None

        with nav:
            with div(_class='d-flex flex-column flex-md-row flex-fill align-items-stretch align-items-md-center'):
                with div(_class='container-xl'):
                    nav_items = ul(_class='navbar-nav')
                            
        for item in node.items:
            nav_items.add(self.visit(item))


        return root

    def visit_Text(self, node):
        if self._in_dropdown:
            return div(node.text, _class='dropdown-item')
        return li(node.text, _class='nav-item')

    def visit_Link(self, node):
        item = li()
        item.add(a(node.text, href=node.get_url(), _class='nav-link'))

        return item

    def visit_Separator(self, node):
        if not self._in_dropdown:
            raise RuntimeError('Cannot render separator outside Subgroup.')
        return li(role='separator', _class='divider')

    def visit_Subgroup(self, node):
        if not self._in_dropdown:
            button = li(_class='nav-item dropdown')

            with button:
                with a(_class='nav-link dropdown-toggle', href='#') as link:
                    link['data-bs-toggle'] = 'dropdown'
                    link['data-bs-auto-close'] = 'outside'
                    link['role'] = 'button'
                    link['aria-expanded'] = 'false'
                    span(node.text, _class='nav-link-title')
            menu = button.add(div(_class='dropdown-menu'))
            menu['data-bs-popper'] = 'static'


            self._in_dropdown = True
            for item in node.items:
                menu.add(self.visit(item))
            self._in_dropdown = False

            return button
        else:
            # TODO this is supported in tabler, just needs implementation
            raise RuntimeError('Cannot render nested Subgroups')

    def visit_View(self, node):
        if self._in_dropdown:
            item = a(node.text, _class='dropdown-item', href=node.get_url(), title=node.text)
        else:
            item = li(_class=f'nav-item {"active" if node.active else ""}')
            item.add(a(node.text, _class='nav-link', href=node.get_url(), title=node.text))

        return item