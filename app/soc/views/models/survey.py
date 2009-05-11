#!/usr/bin/python2.5
#
# Copyright 2008 the Melange authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Views for Surveys.
"""

__authors__ = [
  'JamesLevy" <jamesalexanderlevy@gmail.com>',
  ]


from django import forms

from soc.logic import cleaning
from soc.logic import dicts
from soc.logic.models.survey import logic as survey_logic
from soc.logic.models.user import logic as user_logic
from soc.views.helper import access
from soc.views.helper import decorators
from soc.views.helper import redirects
from soc.views.helper import widgets, surveys
from soc.views.models import base


class View(base.View):
  """View methods for the Survey model.
  """

  def __init__(self, params=None):
    """Defines the fields and methods required for the base View class
    to provide the user with list, public, create, edit and delete views.

    Params:
      params: a dict with params for this View
    """

    # Param for entity?
    rights = access.Checker(params)
    rights['any_access'] = ['allow']
    rights['show'] = ['checkIsDocumentReadable']
    rights['create'] = ['checkIsUser']
    rights['edit'] = ['checkIsDocumentWritable']
    rights['delete'] = ['checkIsDocumentWritable']
    rights['list'] = ['checkDocumentList']
    rights['pick'] = ['checkDocumentPick']

    new_params = {}
    new_params['logic'] = survey_logic
    new_params['rights'] = rights

    new_params['name'] = "Survey"
    new_params['pickable'] = True

    new_params['export_content_type'] = 'text/text'
    new_params['export_extension'] = '.html'
    new_params['export_function'] = lambda x: (x.content, x.link_id)
    new_params['delete_redirect'] = '/'
    new_params['list_key_order'] = [
        'link_id', 'scope_path', 'name', 'short_name', 'title',
        'content', 'prefix','read_access','write_access']

    new_params['no_create_raw'] = True
    new_params['no_create_with_scope'] = True
    new_params['no_create_with_key_fields'] = True
    new_params['no_list_raw'] = True
    new_params['sans_link_id_create'] = True
    new_params['sans_link_id_list'] = True

    new_params['create_dynafields'] = [
        {'name': 'link_id',
         'base': forms.fields.CharField,
         'label': 'Survey Link ID',
         },
        ]

    new_params['create_extra_dynaproperties'] = {


        'survey_content': forms.fields.CharField(widget=surveys.EditSurvey(),
                                             required=False),
        'scope_path': forms.fields.CharField(widget=forms.HiddenInput,
                                             required=True),
        'prefix': forms.fields.CharField(widget=widgets.ReadOnlyInput(),
                                        required=True),
        'clean_content': cleaning.clean_html_content('content'),
        'clean_link_id': cleaning.clean_link_id('link_id'),
        'clean_scope_path': cleaning.clean_scope_path('scope_path'),
        'clean': cleaning.validate_document_acl(self, True),
        }
    new_params['extra_dynaexclude'] = ['author', 'created', 'content', 'home_for',
                                       'modified_by', 'modified', 'take_survey', 'this_survey' ]

    new_params['edit_extra_dynaproperties'] = {
                                            
        'doc_key_name': forms.fields.CharField(widget=forms.HiddenInput),
        'created_by': forms.fields.CharField(
            widget=widgets.ReadOnlyInput(), required=False),
        'last_modified_by': forms.fields.CharField(
            widget=widgets.ReadOnlyInput(), required=False),
        'clean': cleaning.validate_document_acl(self),
        }

    params = dicts.merge(params, new_params)

    super(View, self).__init__(params=params)

  def list(self, request, access_type,
           page_name=None, params=None, filter=None, order=None, **kwargs):
    """See base.View.list.
    """

    return super(View, self).list(request, access_type, page_name=page_name,
                                  params=params, filter=kwargs)

                                      
  def _public(self, request, entity, context):
    """Performs any required processing to get an entity's public page.

    Should return True if the public page should be displayed.

    Args:
      request: the django request object
      entity: the entity to make public
      context: the context object
    """

    if len(request.POST) == 0: return True
    user = user_logic.getForCurrentAccount()
    this_survey = survey_logic.create_survey_record(user, entity, request.POST)
    return True

  def _editContext(self, request, context):
    """Performs any required processing on the context for edit pages.

    Args:
      request: the django request object
      context: the context dictionary that will be used
      
      Adds list of SurveyRecord results as supplement to view.
      
      See surveys.SurveyResults for details.
      
    """

    if not getattr(self, '_entity', None): return
    results = surveys.SurveyResults()

    context['supplemental'] = results.render(self._entity, self._params, filter={})
    super(View, self)._editContext(request, context)

  def _editPost(self, request, entity, fields):
    """See base.View._editPost().
    
    Processes POST request items to add new dynamic field names, 
    question types, and default prompt values to SurveyContent model.
    """


    user = user_logic.getForCurrentAccount()

    if not entity:
      fields['author'] = user
    else:
		fields['author'] = entity.author
		
		""" Check for new fields  
		"""
    survey_fields = {}
    schema = {}
    PROPERTY_TYPES = ('long_answer','short_answer','selection')
    for key, value in request.POST.items():
		if 'survey_' in key:
			field_name = key.replace('survey_', '')
			for type in PROPERTY_TYPES:
				if type + "__" in field_name: 
				   field_name = field_name.replace(type + "__", "")
				   schema[field_name] = type
				   if type == "selection":
				   	value = str(  value.split(',')  )
			survey_fields[field_name] = value

    this_survey = survey_logic.create_survey(survey_fields, schema, this_survey=getattr(entity,'this_survey', None) )
    if entity: entity.this_survey = this_survey 
    else: fields['this_survey'] = this_survey
    
    fields['modified_by'] = user
    from soc.cache import home
    # Flush the cache! TODO - Not Working
    if entity: home.flush(entity)

    super(View, self)._editPost(request, entity, fields)

  def _editGet(self, request, entity, form):
    """See base.View._editGet().
    """
    
    self._entity = entity
    form.fields['survey_content'] = forms.fields.CharField(widget=surveys.EditSurvey(this_survey=entity.this_survey), 
                                     required=False)
    form.fields['created_by'].initial = entity.author.name
    form.fields['last_modified_by'].initial = entity.modified_by.name
    form.fields['doc_key_name'].initial = entity.key().id_or_name()

    super(View, self)._editGet(request, entity, form)

  def getMenusForScope(self, entity, params):
    """Returns the featured menu items for one specifc entity.

    A link to the home page of the specified entity is also included.

    Args:
      entity: the entity for which the entry should be constructed
      params: a dict with params for this View.
    """


    filter = {
        'prefix' : params['url_name'],
        'scope_path': entity.key().id_or_name(),
        'is_featured': True,
        }


    entities = self._logic.getForFields(filter)

    submenus = []

    # add a link to all featured documents
    for entity in entities:
      #TODO only if a document is readable it might be added
      submenu = (redirects.getPublicRedirect(entity, self._params),
                 entity.short_name, 'show')
      submenus.append(submenu)

    return submenus


view = View()

admin = decorators.view(view.admin)
create = decorators.view(view.create)
edit = decorators.view(view.edit)
delete = decorators.view(view.delete)
list = decorators.view(view.list)
public = decorators.view(view.public)
export = decorators.view(view.export)
pick = decorators.view(view.pick)
