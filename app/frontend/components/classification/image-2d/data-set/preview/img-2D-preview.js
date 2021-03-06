/**
 * Created by ar on 11.09.16.
 */

'use strict';

angular.module('image2dPreview', ['ngMaterial', 'image2dPaging', 'cl.paging'])
.component('image2dPreview', {
    templateUrl: '/frontend/components/classification/image-2d/data-set/preview/img-2D-preview.html',
    bindings: {
        databaseId:     '@',
        datasetType:    '@',
        listClasses:    '<'
    },
    controller: function ($scope, $http, datasetService) {
        var self = this;
        self.listClasses = [];
        self.$onInit = function () {
            self.listClasses = [];
            datasetService.getDataSetMetadataHists(self.databaseId).then(
                function successCallback(response) {
                    var tdataHist   = response.data.hist.histTrain;
                    var numAll      = response.data.info.numTrain;
                    if(self.datasetType=='val') {
                        tdataHist = response.data.hist.histVal;
                        numAll      = response.data.info.numVal;
                    }
                    var tret=[];
                    for(var ii=0; ii<tdataHist.length; ii++) {
                        var tkey = tdataHist[ii][0];
                        var tnum = tdataHist[ii][1];
                        tret.push({
                            type:   'class',
                            label:  tkey,
                            idx:    ii,
                            num:    tnum
                        });
                    }
                    // all data:
                    tret.push({
                        type:   'all',
                        label:  '*all',
                        idx:    tdataHist.length,
                        num:    numAll
                    });
                    self.listClasses = tret;
                    // console.log(self.listClasses);
                }, function errorCallback(response) {
                    console.log(response);
                }
            );
        };
    }
});