from dependency_injector.wiring import inject, Provide
from flask import render_template, Blueprint
from app.containers import Container
from app.domain.entities import Dataset
from app.domain.services import DatasetService
from app.forms import SearchForm


bp = Blueprint("main", __name__)


@bp.route('/', methods=['GET', 'POST'], endpoint="index")
@inject
def index(dataset_service: DatasetService = Provide[Container.dataset_service]) -> str:
    form: SearchForm = SearchForm()
    results: list[Dataset] = []
    results_number: int = 0
    if form.validate_on_submit():
        results_number, results = dataset_service.search(form.query.data)
    return render_template('index.html', form=form, results=results, results_number=results_number)
