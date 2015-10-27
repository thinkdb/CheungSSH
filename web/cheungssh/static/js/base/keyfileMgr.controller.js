angular.module('cheungSSH').controller('keyfileMgrCtr', ['$scope', '$stateParams', '$state', '$sce', '$timeout', 'animate', 'resource', 'Upload', 'uiGridConstants', 'utils',
        function ($scope, $stateParams, $state, $sce, $timeout, animate, resource, Upload, uiGridConstants, utils) {
            $scope.keyfileList = {
                enableColumnResizing: true,
                data: [],
                onRegisterApi: function (gridApi) {
                    $scope.gridApi = gridApi;
                },
                //显示table的th
                columnDefs: [
                    { name: "文件名称", field: 'filename' },
                    { name: "上传人", field: 'user' },
                    { name: "上传时间", field: 'time' },
                    { name: "操作", cellTemplate: '<div class="text-center"><button class="btn btn-sm btn-danger" style="height: 28px;" ng-click="grid.appScope.delKeyFile(row.entity)";">删&nbsp;&nbsp;除</button></div>'}
                ]
            };

            resource.JsonPRequest(globalUrl+"/cheungssh/keyadmin/").then(function (data) {
                $scope.keyfileList.data = data.content;
            });

            // upload on file select or drop
            $scope.upload = function () {
                if (!$scope.file) {
                    $alert("请先选择文件");
                    return;
                }
                var progressBar = $("#fileUploadProgress");
                Upload.upload({
                    url: globalUrl+'/cheungssh/upload/test/?upload_type=keyfile',
                    file: $scope.file
                }).progress(function (evt) {
                    var progressPercentage = parseInt(100.0 * evt.loaded / evt.total);
                    progressBar.css("width", progressPercentage + "%");
                    progressBar.text(progressPercentage + "%");
                }).success(function (data, status, headers, config) {
                    $scope.keyfileList.data.push(data);
                    $scope.fileName = "";
                    $scope.file = "";
                    $alert("秘钥文件上传完成");
                    $timeout(function(){
                        progressBar.css("width", "0%");
                        progressBar.text("");
                        $scope.gridApi.cellNav.scrollToFocus( $scope.keyfileList.data[$scope.keyfileList.data.length - 1], $scope.keyfileList.columnDefs[0]);
                    },1000);
                }).error(function (data, status, headers, config) {
                    console.log('error status: ' + status);
                })
            };

            $scope.fileChange = function () {
                if ($scope.file.length > 0) {
                    $scope.fileName = $scope.file[0].name;
                    $scope.upload();
                }

            }

            $scope.fileDrop = function () {
                $scope.fileName = $scope.file[0].name;
                $scope.upload();
            }

            $scope.delKeyFile = function (entity) {
                resource.JsonPRequest(globalUrl+"/cheungssh/delkey/?fid=" + entity.fid).then(function (data) {
                    if (data.msgtype === "OK") {
                        $scope.keyfileList.data = utils.removeFromArrayByKeyValue($scope.keyfileList.data, 'fid', entity.fid);
                    } else {
                        $alert("删除失败");
                    }
                })
            }
        }]
);