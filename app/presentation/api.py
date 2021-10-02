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

#
# @bp.route("/datasets/<dataset_remote_id>/", methods=["GET"])
# def get_dataset(dataset_remote_id: str) -> Response:
#
#     query_body: dict = {
#         "query": {
#             "term": {
#                 "remote_id": {
#                     "value": dataset_remote_id
#                 }
#             }
#         }
#     }
#     result: dict = es.search(index='datasets', body=query_body, explain=True)
#     if result['hits']['hits']:
#         return jsonify({
#             "id": result['hits']['hits'][0]['_source']['remote_id'],
#             "title": result['hits']['hits'][0]['_source']['title']
#         })
#     return jsonify({})
