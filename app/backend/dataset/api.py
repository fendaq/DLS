#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'ar'

import json

from flask import Blueprint
from flask import request, Response
from app.backend.dataset.service import DatasetService

dataset = Blueprint(__name__, __name__)

from app.backend.core.datasets.dbwatcher import DatasetsWatcher

datasetWatcher = DatasetsWatcher()
datasetWatcher.refreshDatasetsInfo()

dataset_service = DatasetService("test")


@dataset.route('/all/metadata/list', methods=['GET'])
def list_data_sets_metadata():
    metadata_list = json.dumps(datasetWatcher.get_data_sets_metadata())
    return Response(metadata_list, mimetype='application/json')


@dataset.route('/<string:id>/metadata', methods=['GET'])
def data_set_metadata(id):
    metadata = json.dumps(datasetWatcher.get_data_set_metadata(id))
    return Response(metadata, mimetype='application/json')


@dataset.route('/<string:id>/metadata/hists', methods=['GET'])
def data_set_metadata_hists(id):
    metadata_hists = json.dumps(datasetWatcher.get_data_set_metadata_hists(id))
    return Response(metadata_hists, mimetype='application/json')


@dataset.route('/<string:id>/img/preview', methods=['GET'])
def data_set_img_preview(id):
    try:
        img_data = datasetWatcher.get_data_set_img_preview(id)
    except Exception as err:
        img_data = None
        print (err)
    return img_data


@dataset.route('/<string:id>/img/mean', methods=['GET'])
def data_set_img_mean(id):
    try:
        img_data = datasetWatcher.get_data_set_img_mean(id)
    except Exception as err:
        img_data = None
        print (err)
    return img_data


@dataset.route('/metadata/range', methods=['POST'])
def data_set_metadata_in_range():
    metadata = datasetWatcher.get_data_set_metadata_in_range(request.args['id'],
                                                             request.args['type'],
                                                             request.args['label'],
                                                             int(request.args['from']),
                                                             int(request.args['to']))
    return Response(json.dumps(metadata), mimetype='application/json')


@dataset.route('/<string:dsId>/<string:dsType>/img/<string:imgIndex>', methods=['GET'])
def get_img_from_data_set(dsId, dsType, imgIndex):
    try:
        img = datasetWatcher.get_img_from_data_set(dsId, dsType, imgIndex)
    except Exception as err:
        img = None
        print (err)
    return img


@dataset.route('/delete/<path:id>')
def delete(id):
    datasetWatcher.delete(id)
    datasetWatcher.refreshDatasetsInfo()
    return list_data_sets_metadata()


@dataset.route('/data/types/config', methods=['GET'])
def data_types_config():
    return Response(json.dumps(dataset_service.data_types_config()), mimetype='application/json')


@dataset.route('/csv/load/rows', methods=['POST'])
def load_from_csv():
    header = True if request.args['header'] == "True" else False
    csv_rows = dataset_service.load_from_csv(request.args['file-path'],
                                             header,
                                             request.args['separator'],
                                             int(request.args['rows-num']))
    return Response(json.dumps(csv_rows), mimetype='application/json')