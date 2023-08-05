# -*- coding: utf-8 -*-

# pyramid-helpers -- Helpers to develop Pyramid applications
# By: Cyril Lacoux <clacoux@easter-eggs.com>
#     Valéry Febvre <vfebvre@easter-eggs.com>
#
# Copyright (C) 2011-2021 Cyril Lacoux, Easter-eggs
# https://gitlab.com/yack/pyramid-helpers
#
# This file is part of pyramid-helpers.
#
# pyramid-helpers is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# pyramid-helpers is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

""" Pyramid-Helpers common views """

import hashlib

from pyramid.httpexceptions import HTTPBadRequest
from pyramid.httpexceptions import HTTPForbidden
from pyramid.httpexceptions import HTTPFound
from pyramid.httpexceptions import HTTPInternalServerError
from pyramid.httpexceptions import HTTPNotFound
from pyramid.httpexceptions import HTTPUnauthorized
from pyramid.security import forget
from pyramid.security import remember
from pyramid.view import exception_view_config
from pyramid.view import view_config

from pyramid_helpers.api_doc import api_doc as api_doc_
from pyramid_helpers.auth import check_credentials
from pyramid_helpers.forms import validate
from pyramid_helpers.forms.auth import LoginForm
from pyramid_helpers.forms.validators import ValidatorsForm
from pyramid_helpers.i18n import N_
from pyramid_helpers.utils import get_settings


# HTTPExceptions' titles
N_('Bad Request')
N_('Forbidden')
N_('Not Found')

N_('Access was denied to this resource.')
N_('The resource could not be found.')


@view_config(route_name='api-doc', renderer='')
def api_doc(request):
    """ The API doc view """

    translate = request.translate

    renderer_values = dict(
        breadcrumb=[(translate('API documentation'), None)],
        subtitle=None,
        title=translate('API documentation'),
    )

    return api_doc_(request, renderer_values)


@exception_view_config(HTTPBadRequest, renderer='/errors.mako')
def http_400(request):
    """ HTTP 400 error view """

    translate = request.translate

    request.response.status_int = 400

    if request.matched_route.name.startswith('api.'):
        request.override_renderer = 'json'
        result = dict(
            url=request.url,
            method=request.method,
            params=request.params.mixed(),
            errors=request.exception.json if request.exception.body else {},
            apiVersion='1.0',
            result=False,
            message=request.exception.message or translate('Invalid or missing parameter(s)'),
        )
        return result

    # Prevent from rendering wrong template
    if hasattr(request, 'override_renderer'):
        del request.override_renderer

    return dict(
        title=translate(request.exception.title),
        subtitle=None,
    )


@exception_view_config(HTTPForbidden, renderer='/errors.mako')
@exception_view_config(HTTPUnauthorized, renderer='/errors.mako')
def http_403(request):
    """ HTTP 403 error view """

    translate = request.translate

    if request.authenticated_user is None:
        params = get_settings(request, 'auth', 'auth')
        if params.get('policies') == ['basic']:
            # Issuing a challenge
            response = HTTPUnauthorized()
            response.headers.update(forget(request))
            return response

        return HTTPFound(location=request.route_path('login', _query=dict(redirect=request.url)))

    request.response.status_int = 403

    if request.matched_route.name.startswith('api.'):
        request.override_renderer = 'json'
        result = dict(
            url=request.url,
            method=request.method,
            params=request.params.mixed(),
            apiVersion='1.0',
            result=False,
            message=request.exception.message or translate('Access denied'),
        )
        return result

    # Prevent from rendering wrong template
    if hasattr(request, 'override_renderer'):
        del request.override_renderer

    return dict(
        title=translate(request.exception.title),
        subtitle='',
    )


@exception_view_config(HTTPNotFound, renderer='/errors.mako')
def http_404(request):
    """ HTTP 404 error view """

    translate = request.translate

    request.response.status_int = 404

    if request.matched_route and request.matched_route.name.startswith('api.'):
        request.override_renderer = 'json'
        result = dict(
            url=request.url,
            method=request.method,
            params=request.params.mixed(),
            apiVersion='1.0',
            result=False,
            message=request.exception.message or translate('Not found'),
        )
        return result

    # Prevent from rendering wrong template
    if hasattr(request, 'override_renderer'):
        del request.override_renderer

    return dict(
        title=translate(request.exception.title),
        subtitle='',
    )


@view_config(route_name='index')
def index(request):
    """ Index view """
    return HTTPFound(location=request.route_path('articles.search'))


@view_config(route_name='login', renderer='/login.mako')
@validate('login_form', LoginForm)
def login(request):
    """ Login view """

    translate = request.translate
    form = request.forms['login_form']

    params = get_settings(request, 'auth', 'auth')
    if params.get('policies') == ['remote']:
        params = get_settings(request, 'auth', 'policy:remote')
        login_url = params.get('login_url')
        if login_url is None:
            raise HTTPInternalServerError(detail=translate('Authentication not available, please retry later.'))

        return HTTPFound(location=login_url)

    if request.method == 'POST':
        if not form.errors:
            username = form.result['username']
            password = form.result['password']
            redirect = form.result['redirect']

            if check_credentials(username, password, request):
                headers = remember(request, username)
                return HTTPFound(location=redirect, headers=headers)

            form.errors['username'] = translate('Bad user or password')
    else:
        redirect = request.GET.get('redirect')
        if redirect is None or redirect == request.current_route_url(_query=None):
            redirect = request.route_path('index')

        data = dict(redirect=redirect)
        form.set_data(data)

    return dict(
        title=translate('Authentication'),
    )


@view_config(route_name='logout', renderer='/logout.mako')
def logout(request):
    """ Logout view """

    session = request.session
    translate = request.translate

    # Clear session
    session.delete()

    if request.authentication_policy == 'remote':
        params = get_settings(request, 'auth', 'policy:remote')
        logout_url = params.get('logout_url')
        if logout_url is None:
            # Display logout page
            return dict(
                title=translate('Logged out'),
            )
    else:
        logout_url = request.route_path('index')

    headers = forget(request)
    return HTTPFound(location=logout_url, headers=headers)


@view_config(route_name='validators', renderer='/validators.mako')
@validate('validators_form', ValidatorsForm)
def validators(request):
    """ Validators view """

    translate = request.translate
    form = request.forms['validators_form']

    if request.method == 'POST':
        if not form.errors:
            qfile = form.result['upload_input']
            if qfile is not None:
                content = qfile.file.read()
                form.result['upload_input.name'] = qfile.filename
                form.result['upload_input.size'] = len(content)
                form.result['upload_input.md5sum'] = hashlib.md5(content).hexdigest()

    return dict(
        breadcrumb=[(translate('Validators'), None)],
        errors=form.errors,
        result=form.result,
    )
