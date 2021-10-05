from dependency_injector.wiring import inject, Provide
from flask import render_template, Blueprint, request, url_for
from app.containers import Container
from app.domain.services import DatasetService
from app.presentation.forms import SearchForm


bp = Blueprint("main", __name__)


@bp.route('/', methods=['GET'], endpoint='index')
@inject
def index(dataset_service: DatasetService = Provide[Container.dataset_service]) -> str:
    form = SearchForm()
    results = []
    results_number = 0
    total_pages = 0
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 20, type=int)
    query_text = request.args.get('query', None)

    if query_text:
        results, results_number, total_pages = dataset_service.search(query_text, page, page_size)

    first_url = url_for('main.index', query=query_text, page=1, page_size=page_size, _external=True)
    next_url = url_for('main.index', query=query_text, page=page + 1, page_size=page_size, _external=True)
    prev_url = url_for('main.index', query=query_text, page=page - 1, page_size=page_size, _external=True)
    last_url = url_for('main.index', query=query_text, page=total_pages, page_size=page_size, _external=True)

    return render_template('index.html',
                           form=form,
                           page=page,
                           results=results,
                           results_number=results_number,
                           total_pages=total_pages,
                           first_url=first_url if page > 1 else None,
                           next_url=next_url if page < total_pages else None,
                           prev_url=prev_url if page > 1 else None,
                           last_url=last_url
                           )
