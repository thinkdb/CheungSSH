angular.module('cheungSSH').controller('visitHisCtr', ['$scope', '$stateParams', '$state', '$sce', '$timeout', 'animate', 'resource', 'Upload', 'uiGridConstants', 'utils',
        function ($scope, $stateParams, $state, $sce, $timeout, animate, resource, Upload, uiGridConstants, utils) {
            $scope.visitHisList = {
                enableColumnResizing: true,
                data: [],
                onRegisterApi: function (gridApi) {
                    $scope.gridApi = gridApi;
                },
                //显示table的th
                columnDefs: [
                    { name: "URL", field: 'URL' },
                    { name: "IP", field: 'IP' },
                    { name: "用户名", field: 'username' },
                    { name: "操作时间", field: 'accesstime'},
                    { name: "IP位置", field: 'IPLocat'}
                ]
            };

            resource.JsonPRequest(globalUrl + "/cheungssh/operationrecord/").then(function (data) {
                $scope.visitHisList.data = data.content;
            });
        }]
);