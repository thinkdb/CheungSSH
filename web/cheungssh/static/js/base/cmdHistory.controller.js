angular.module('cheungSSH').controller('cmdHisCtr', ['$scope', '$stateParams', '$state', '$sce', '$timeout', 'animate', 'resource', 'Upload', 'uiGridConstants', 'utils',
        function ($scope, $stateParams, $state, $sce, $timeout, animate, resource, Upload, uiGridConstants, utils) {
            $scope.cmdHisList = {
                enableColumnResizing: true,
                data: [],
                onRegisterApi: function (gridApi) {
                    $scope.gridApi = gridApi;
                },
                //显示table的th
                columnDefs: [
                    {name: "IP位置", field: 'IP-Locat'},
                    {name: "IP", field: 'IP'},
                    {name: "命令", field: 'cmd'},
                    {name: "服务器", field: 'servers'},
                    {name: "用户", field: 'user'},
                    {name: "执行时间", field: 'excutetime'},
                ]
            };

            resource.JsonPRequest(globalUrl + "/cheungssh/cmdhistory/").then(function (data) {
                $.each(data.content, function (key, item) {
                    item.servers = item.servers.join(",");
                });
                $scope.cmdHisList.data = data.content;
            });
        }]
);