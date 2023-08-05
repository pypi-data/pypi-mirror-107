<%inherit file="../site.mako" />
<%
labels = {
    'draft': 'warning',
    'published': 'success',
    'refused': 'danger',
}
%>\
<div class="panel panel-default">
    <div class="panel-heading">
        <h2>${translate('Article #{0}').format(article.id)}</h2>
        <small>${format_date(article.creation_date, format='long')} ${translate('by {0}').format(article.author.fullname)}</small>
% if has_permission('articles.modify'):
        <span class="label label-${labels[article.status]} pull-right">${translate(article.status.capitalize())}</label>
% endif
    </div>

    <div class="panel-body">
        <p>${article.text.replace('\n', '<br />') | n}</p>
    </div>
% if has_permission('articles.modify'):

    <div class="panel-footer text-right">
        <a class="btn btn-primary" href="${request.route_path('articles.modify', article=article.id)}" title="${translate('Edit article {0}').format(article.title)}">${translate('Edit')}</a>
    % if has_permission('articles.delete'):
        <a class="btn btn-default" href="${request.route_path('articles.delete', article=article.id)}" title="${translate('Delete article {0}').format(article.title)}">${translate('Delete')}</a>
    % endif
    </div>
% endif
</div>
