angular.module('cheungSSH').controller('scriptCtr', ['$scope', '$stateParams', '$state', '$sce', '$timeout', 'animate', 'resource', 'Upload', 'uiGridConstants', 'utils',
        function ($scope, $stateParams, $state, $sce, $timeout, animate, resource, Upload, uiGridConstants, utils) {
            $scope.scriptList = {
                enableColumnResizing: true,
                data: [],
                onRegisterApi: function (gridApi) {
                    $scope.gridApi = gridApi;
                },
                //显示table的th
                columnDefs: [
                    { name: "脚本名称", field: 'filename' },
                    { name: "上传人", field: 'username' },
                    { name: "上传时间", field: 'time' },
                    { name: "操作", cellTemplate: '<div class="text-center"><button class="btn btn-sm btn-primary" style="height: 28px;" ng-click="grid.appScope.editScriptFile(row.entity)";">执&nbsp;&nbsp;行</button>&nbsp;&nbsp;&nbsp;<button class="btn btn-sm btn-primary" style="height: 28px;" ng-click="grid.appScope.editScriptFile(row.entity)";">编&nbsp;&nbsp;辑</button>&nbsp;&nbsp;&nbsp;<button class="btn btn-sm btn-danger" style="height: 28px;" ng-click="grid.appScope.delScriptFile(row.entity)";">删&nbsp;&nbsp;除</button></div>'}
                ]
            };

            // upload on file select or drop
            $scope.upload = function () {
                if (!$scope.file) {
                    $alert("请先选择文件");
                    return;
                }
                var progressBar = $("#fileUploadProgress");
                if (!progressBar.is(":visible")) progressBar.css("display", "block");
                Upload.upload({
                    url: globalUrl + '/cheungssh/upload/test/?upload_type=script',
                    file: $scope.file
                }).progress(function (evt) {
                    var progressPercentage = parseInt(100.0 * evt.loaded / evt.total);
                    progressBar.css("width", progressPercentage + "%");
                    progressBar.text(progressPercentage + "%");
                }).success(function (data, status, headers, config) {
                    $scope.scriptList.data.push(data.content);
                    $alert("脚本文件上传完成");
                    $scope.file = [];
                    $scope.fileName = "";
                    $timeout(function () {
                        progressBar.css("width", "0%");
                        progressBar.text("");
                        progressBar.css("display", "none")
                        $scope.gridApi.cellNav.scrollToFocus($scope.scriptList.data[$scope.scriptList.data.length - 1], $scope.scriptList.columnDefs[0]);
                    }, 1000);
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
                resource.JsonPRequest(globalUrl + "/cheungssh/delkey/?fid=" + entity.fid).then(function (data) {
                    if (data.msgtype === "OK") {
                        $scope.scriptList.data = utils.removeFromArrayByKeyValue($scope.scriptList.data, 'fid', entity.fid);
                    } else {
                        $alert("删除失败");
                    }
                })
            };

            $scope.deleteScirpts = function () {

            }

            $scope.editScriptFile = function (item) {
                $scope.type = 'modify';
                $scope.scriptName = item.filename;
                resource.JsonPRequest(globalUrl + '/cheungssh/script/?edit_type=show&filename=' + item.filename).then(function (data) {
                    if (data.msgtype.toLowerCase() == 'ok') {
                        $scope.scriptContent = data.content;
                        $scope.editScript();
                    }
                })
            }

            $scope.addScriptFile = function () {
                $scope.type = 'add'
                $scope.editScript();
            }

            $scope.uploadScript = function () {
                $modal({callback: function (element, msg) {
                },
                    cancelCallback: function () {
                    },
                    scope: $scope,
                    html: true,
                    title: '上传脚本文件',
                    template: '../static/template/modal/modal.confirm.upload.html',
                    contentTemplate: '../static/template/modal/upload.tpl.html'
                });
            }

            var editScriptModal;

            $scope.editScript = function () {
                editScriptModal = $modal({callback: function (element, msg) {
                },
                    cancelCallback: function () {
                    },
                    scope: $scope,
                    html: true,
                    title: '上传脚本文件',
                    template: '../static/template/modal/modal.confirm.upload.html',
                    contentTemplate: '../static/template/modal/script.edit.html'
                });
            }

            $scope.saveScript = function () {
                editScriptModal.hide();
                resource.cors(globalUrl + "/cheungssh/script/?edit_type=add", {
                    filename: $scope.scriptName,
                    filecontent: $scope.scriptContent
                }).then(function (data) {
                    if (data.msgtype.toLowerCase() == 'ok') {
                        var exists = fasle;
                        $.each($scope.scriptList.data, function (key, item) {
                            if (item.filename === $scope.scriptName){
                                exists = true;
                                $scope.scriptList.data[key] = data.content;
                            }
                        });

                        if(!exists)$scope.scriptList.data.push(data.content);
                        $timeout(function () {
                            $scope.gridApi.cellNav.scrollToFocus($scope.scriptList.data[$scope.scriptList.data.length - 1], $scope.scriptList.columnDefs[0]);
                        });

                        $alert("脚本成功写入");
                    }
                }, function () {
                });

            }

            resource.JsonPRequest(globalUrl + "/cheungssh/script/?edit_type=list").then(function (data) {
                $scope.scriptList.data = data.content;
            });
        }]
);