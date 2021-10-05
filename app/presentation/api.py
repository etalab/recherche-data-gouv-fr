from dependency_injector.wiring import inject, Provide
from flask import Blueprint, request, url_for, jsonify, abort
from werkzeug.wrappers import Response
from app.containers import Container
from app.domain.services import DatasetService


bp = Blueprint('api', __name__, url_prefix='/api/1')


@bp.route("/datasets/", methods=["GET"], endpoint='dataset_search')
@inject
def datasets_search(dataset_service: DatasetService = Provide[Container.dataset_service]) -> Response:
    page = request.args.get('page', 1, type=int)
    query_text = request.args.get('q', None)

    if not query_text:
        abort(400)

    results, results_number, total_pages = dataset_service.search(query_text, page)
    next_url = url_for('api.dataset_search', q=query_text, page=page + 1, _external=True)
    prev_url = url_for('api.dataset_search', q=query_text, page=page - 1, _external=True)

    return jsonify({
        "data": results,
        "next_page": next_url if page < total_pages else None,
        "page": page,
        "previous_page": prev_url if page > 1 else None,
        "total_pages": total_pages,
        "total": results_number
    })


@bp.route("/datasets/<dataset_id>/", methods=["GET"])
@inject
def get_dataset(dataset_id: str, dataset_service: DatasetService = Provide[Container.dataset_service]) -> Response:
    result = dataset_service.find_one(dataset_id)
    if result:
        return jsonify(result)
    abort(404, 'dataset not found')
