# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['access_control']

package_data = \
{'': ['*']}

install_requires = \
['subscribe>=0.1.0,<0.2.0']

setup_kwargs = {
    'name': 'access-control',
    'version': '0.1.0',
    'description': 'Library for access control lists',
    'long_description': '# Access Control\n\nWith `access-control` you can manage access control list to check\nwether a principal has access to a context with a certain permission.\n\n## Concepts\n\n### ACL (Access Control List)\n\nAn *ACL* is an ordered list of *ACE* (Access Control Entry). Every *Context* \nhas an *ACL*.\n\n### ACE (Access Control Entry)\n\nAn *ACE* consists of:\n- a *Permit*\n- a *Principal*\n- a *Permission*\n\n### Principal\n\nA *Principal* represents an entity, typically a user or group.\nThis means that a typical user can have multiple principals, like `everyone`,\n`userid:1234` and `group:admin`.\n\n### Permit\n\nThe *Permit* is either ALLOW or DENY. This means that you can specify in the\n*ACE* that a *Principal* has either to be denied of allowed access to the\n*Context*.\n\n### Context\n\nThe *Context* is a resource, like a page on a website, including the context of\nthat resource, like the folders in which the page is located.\nEvery context has an *ACL*.\n\n### Permission\n\nThe *Permission* is the action like `view`, `change name`, `create user` on the *Context*.\n\n### Matching\n\nTo get the *Permit* for a combination of *Context*, *Principal* and *Permission*,\nthe *ACL* of the context will be looked up (in the specified order). When there is\na match (based on *Principal* and *Permission*), the specified *Permit* (DENY\nor ALLOW) is returned. When there is no match, the first match with *ACL* of the \nparent (like folders) will be returned.\nWhen there is still no match, a DENY will be returned.\n\n## Example\n\n    >>> import access_control as ac\n    >>> from typing import Optional\n\n    Create some principals, next to the predefined ac.principal.everyone\n    and ac.principal.authenticated.\n\n    >>> user_1 = ac.principal.Principal(\'user:1\')\n    >>> group_admin = ac.principal.Principal(\'group:admin\')\n\n    Create some context. You can use predefined ObjectContext which can make a context \n    from any object.\n\n    >>> class Page():\n    ...     def __init__(self, name: str, parent: Optional["Page"]):\n    ...         self.name = name\n    ...         self.parent = parent\n\n    >>> root_page = Page(\'root\', None)\n    >>> contact_page = Page(\'contact\', root_page)\n\n    >>> context_contact_page = ac.context.ObjectContext(contact_page)\n    >>> context_root = ac.context.ObjectContext(root_page)\n\n    Create permissions. For the contact page you can define a view and an edit permission\n\n    >>> view_permission = ac.permission.Permission(\'view\')\n    >>> edit_permission = ac.permission.Permission(\'edit\')\n\n    Next we need to glue them together in acls.\n    The context has a `acl` attribute which has the acl of the context *and* the parents of \n    the context. A subscription_list of the `subscribe` package will be used to\n    get the acl of a certain context. You can subscribe one or more functions to \n    a subscription_list of the context. All acls will be combined in the order\n    of the subscription_list.\n\n    Only the admins can edit the page.\n\n    >>> @context_contact_page.acl_subscription_list.subscribe()\n    ... def get_acl(context):\n    ...     return [ac.acl.ACE(ac.permit.Permit.ALLOW, group_admin, edit_permission)]\n\n    And every can view everything.\n\n    >>> @context_root.acl_subscription_list.subscribe()\n    ... def get_acl(context):\n    ...     return [ac.acl.ACE(ac.permit.Permit.ALLOW, ac.principal.everyone, view_permission)]\n    \n    When a user want to access the page for edit, we can ask whether the user is allowed.\n    Therefor we need to know the principals of that user.\n\n    >>> unauthenticated_user_principals = [ac.principal.everyone]\n    >>> admin_user_princpals = {ac.principal.everyone, ac.principal.authenticated, user_1, group_admin}\n\n    Both users can access the root and contact page with view permission\n\n    >>> ac.context.get_permit(context_contact_page, admin_user_princpals, view_permission) == ac.permit.Permit.ALLOW\n    True\n    >>> ac.context.get_permit(context_root, admin_user_princpals, view_permission) == ac.permit.Permit.ALLOW\n    True\n    >>> ac.context.get_permit(context_contact_page, unauthenticated_user_principals, view_permission) == ac.permit.Permit.ALLOW\n    True\n    >>> ac.context.get_permit(context_root, unauthenticated_user_principals, view_permission) == ac.permit.Permit.ALLOW\n    True\n\n\n    The unauthenticated user has no edit permission to the contact page\n\n    >>> ac.context.get_permit(context_contact_page, unauthenticated_user_principals, edit_permission) == ac.permit.Permit.DENY\n    True\n\n    The admin user does have access\n\n    >>> ac.context.get_permit(context_contact_page, admin_user_princpals, edit_permission) == ac.permit.Permit.ALLOW\n    True\n\n\n\n',
    'author': 'Marc Rijken',
    'author_email': 'marc@rijken.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/mrijken/access_control',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
