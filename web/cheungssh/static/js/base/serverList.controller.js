angular.module('cheungSSH').controller('serverListCtr', ['$scope', '$stateParams', '$state', '$sce', '$timeout', 'animate', 'resource', 'Upload', 'uiGridConstants', 'utils',
        function ($scope, $stateParams, $state, $sce, $timeout, animate, resource, Upload, uiGridConstants, utils) {
            var columnHead = {
                "ip": "IP",
                "hostname": "主机名",
                "username": "用户名",
                "sudo": "使用sudo",
                "sudopassword": "sudo密码",
                "su": "su切换root",
                "password": "密码",
                "supassword": "su的密码",
                "group": "组",
                "port": "端口",
                "loginmethod": "登录方式",
                "keyfile": "秘钥文件"
            };

            $scope.serverList = {
                enableColumnResizing: true,
                enableRowSelection: true,
                enableSelectAll: true,
                enableColumnMenus: true,
                enableSorting: true,
                selectionRowHeaderWidth: 35,
                enableCellEditOnFocus: true,
                data: $scope.serverInfoList,
                //点击展开时触发
                expandableRowCallBack: function (sc) {

                },
                onRegisterApi: function (gridApi) {

                    $scope.$parent.gridApi = gridApi;
                    gridApi.cellNav.on.navigate($scope, function (newRowCol, oldRowCol) {

                    });

                    $.extend(gridApi.edit.raise, {
                        beginCellEdit: function (rowEntity, colDef, triggerEvent) {

                        },
                        afterCellEdit: function (rowEntity, colDef, newValue, oldValue) {
                            if (colDef.field == 'su' && newValue == 'Y') {
                                rowEntity['sudo'] = 'N';
                                rowEntity['sudopassword'] = '';
                            }

                            if (colDef.field == 'sudo' && newValue == 'Y') {
                                rowEntity['su'] = 'N';
                                rowEntity['supassword'] = '';
                            }

                            if (colDef.field == 'loginmethod' && newValue == 'KEY') {
                                rowEntity['password'] = '';
                            }

                            if (colDef.field == 'keyfile' && newValue == '100') {
                                rowEntity[colDef.field] = oldValue;
                                return;
                            }

                            if (newValue != oldValue && rowEntity["type"] == "modify") {
                                var data = {};
                                for (var key in rowEntity) {
                                    if (key == colDef.field || key === "id") {
                                        data[key] = rowEntity[key];
                                    }
                                }
                                resource.JsonPRequest(globalUrl + "/cheungssh/configmodify/?type=modify&host=" + JSON.stringify(data))
                                    .then(function (data) {
                                        if (data.msgtype.toLowerCase() === "ok") {
                                            $alert("修改成功");
                                            resource.JsonPRequest(globalUrl+'/cheungssh/sshcheck/?id='+rowEntity.id).then(function(resp){
                                                rowEntity.status = resp.status;
                                                rowEntity.content = resp.content;
                                            })
                                        } else {
                                            $alert("修改失败");
                                        }
                                    });
                            } else if (rowEntity['type'] === "add") {
                                var isValidated = true;
                                if (rowEntity['loginmethod'] === 'PASSWORD' && !rowEntity['password'])
                                    isValidated = false;
                                if (rowEntity['su'] === 'Y' && !rowEntity['supassword'])
                                    isValidated = false;
                                if (rowEntity['sudo'] === 'Y' && !rowEntity['sudopassword'])
                                    isValidated = false;
                                $.each(['ip','username', 'group', 'port'], function (key, field) {
                                    if (!rowEntity[field]) {
                                        isValidated = false;
                                        return false;
                                    }
                                })
                                isValidated && resource.JsonPRequest(globalUrl + "/cheungssh/configmodify/?type=add&host=" + JSON.stringify(rowEntity))
                                    .then(function (data) {
                                        $alert("新增服务器成功");
                                        rowEntity.id = data.id;
                                        rowEntity.type = "modify";
                                        resource.JsonPRequest(globalUrl+'/cheungssh/sshcheck/?id='+rowEntity.id).then(function(resp){
                                            rowEntity.status = resp.status;
                                            rowEntity.content = resp.content;
                                        })
                                    });
                            }

                            $scope.gridApi.core.queueGridRefresh();
                        },
                        cancelCellEdit: function (rowEntity, colDef) {
                        }
                    });
                },
                //显示table的th
                columnDefs: [
                    { name: columnHead['ip'], field: 'ip', cellClass: function (grid, row, col, rowRenderIndex, colRenderIndex) {
                        var val = grid.getCellValue(row, col);
                        if (val === '' || typeof val === 'undefined') {
                            return 'validatorError';
                        }
                    }},
                    /* { name: columnHead['hostname'],field:'hostname',cellClass: function(grid, row, col, rowRenderIndex, colRenderIndex) {
                     var val = grid.getCellValue(row,col);
                     if (val === ''|| typeof val === 'undefined') {
                     return 'validatorError';
                     }
                     }},*/
                    { name: columnHead['port'], field: 'port', type: 'number', cellClass: function (grid, row, col, rowRenderIndex, colRenderIndex) {
                        var val = grid.getCellValue(row, col);
                        if (val === '' || typeof val === 'undefined') {
                            return 'validatorError';
                        }
                    }},
                    { name: columnHead['group'], field: 'group', cellClass: function (grid, row, col, rowRenderIndex, colRenderIndex) {
                        var val = grid.getCellValue(row, col);
                        if (val === '' || typeof val === 'undefined') {
                            return 'validatorError';
                        }
                    }},
                    { name: columnHead['username'], field: 'username', cellClass: function (grid, row, col, rowRenderIndex, colRenderIndex) {
                        var val = grid.getCellValue(row, col);
                        if (val === '' || typeof val === 'undefined') {
                            return 'validatorError';
                        }
                    }},
                    {name: columnHead['loginmethod'], field: 'loginmethod', editableCellTemplate: 'ui-grid/dropdownEditor',
                        cellFilter: 'loginMethodFilter', editDropdownValueLabel: 'text', editDropdownOptionsArray: [
                        { id: 'PASSWORD', text: '密码方式' },
                        { id: 'KEY', text: '秘钥文件' }
                    ] },

                    { name: columnHead['keyfile'], field: 'keyfile', editableCellTemplate: 'ui-grid/dropdownEditor',
                        cellFilter: 'KeyFileFilter', editDropdownValueLabel: 'text', editDropdownOptionsArray: $.map($scope.keyFileList, function (value, key) {
                        return {id: key, text: value};
                    }), cellEditableCondition: function ($scope) {
                        return $scope.grid.getCellValue($scope.row, $scope.grid.getColumn(columnHead['loginmethod'])) === 'KEY';
                    }},
                    { name: columnHead['password'], field: 'password', cellTemplate: '<div class="ui-grid-cell-contents">{{COL_FIELD CUSTOM_FILTERS?"******":"" }}</div>', cellClass: function (grid, row, col, rowRenderIndex, colRenderIndex) {
                        var val = grid.getCellValue(row, col);
                        var loginmethod = grid.getCellValue(row, grid.getColumn(columnHead['loginmethod']));
                        if (loginmethod == 'PASSWORD' && val === '' || typeof val === 'undefined') {
                            return 'validatorError';
                        }
                    }},
                    { name: columnHead['sudo'], field: 'sudo', editableCellTemplate: 'ui-grid/dropdownEditor',
                        cellFilter: 'YNFilter', editDropdownValueLabel: 'text', editDropdownOptionsArray: [
                        { id: 'Y', text: '是' },
                        { id: 'N', text: '否' }
                    ] },
                    { name: columnHead['sudopassword'], field: 'sudopassword', cellTemplate: '<div class="ui-grid-cell-contents">{{COL_FIELD CUSTOM_FILTERS?"******":"" }}</div>', cellClass: function (grid, row, col, rowRenderIndex, colRenderIndex) {
                        if (grid.getCellValue(row, grid.getColumn('使用sudo')) == 'N') {
                            row.entity[col.field] = "";
                            return '';
                        }
                        var val = grid.getCellValue(row, col);
                        if (val === '' || typeof val === 'undefined') {
                            return 'validatorError';
                        }
                    }, cellEditableCondition: function ($scope) {
                        return $scope.grid.getCellValue($scope.row, $scope.grid.getColumn('使用sudo')) == 'Y';
                    }},
                    { name: columnHead['su'], field: 'su', editableCellTemplate: 'ui-grid/dropdownEditor',
                        cellFilter: 'YNFilter', editDropdownValueLabel: 'text', editDropdownOptionsArray: [
                        { id: 'Y', text: '是' },
                        { id: 'N', text: '否' }
                    ] },
                    { name: columnHead['supassword'], field: 'supassword', cellTemplate: '<div class="ui-grid-cell-contents">{{COL_FIELD CUSTOM_FILTERS?"******":"" }}</div>', cellClass: function (grid, row, col, rowRenderIndex, colRenderIndex) {
                        if (grid.getCellValue(row, grid.getColumn(columnHead['su'])) == 'N') {
                            row.entity[col.field] = "";
                            return '';
                        }
                        var val = grid.getCellValue(row, col);
                        if (val === '' || typeof val === 'undefined') {
                            return 'validatorError';
                        }
                    }, cellEditableCondition: function ($scope) {
                        return $scope.grid.getCellValue($scope.row, $scope.grid.getColumn(columnHead['su'])) === 'Y';
                    }},
                    { name: '状态', field: 'status', allowCellFocus:false,enableCellEdit:false,cellTemplate:'<div class="ui-grid-cell-contents serverInit" ng-class="{\'OK\':\'serverConnected\',\'ERR\':\'serverDisconnected\'}[grid.getCellValue(row, col)]" data-content-Template="../static/template/popover/serverStatus.html" data-container="body" data-html="true" data-trigger="hover" data-placement="top" data-delay="200" data-hover-hold="true" bs-popover></div>'}
                ]
            };

            $scope.addServer = function () {
                if ($scope.serverList.data.length > 0 && $scope.serverList.data[$scope.serverList.data.length - 1].type === 'add') {
                    $alert("请填写完成当前服务器信息后，再添加下一个");
                    var addRow = $scope.serverList.data[$scope.serverList.data.length - 1];
                    $.each($scope.serverList.columnDefs, function (key, item) {
                        if (!addRow[item.field]) {
                            isValidated = false;
                            $scope.gridApi.cellNav.scrollToFocus(addRow, item);
                            return false;
                        }
                    });
                    return;
                }
                $scope.serverList.data.push({type: "add", id: "add", sudo: "N", su: "N", loginmethod: "PASSWORD",content:'未添加'});
                $timeout(function () {
                    $scope.gridApi.cellNav.scrollToFocus($scope.serverList.data[$scope.serverList.data.length - 1], $scope.serverList.columnDefs[0]);
                })
            };

            $scope.deleteServer = function () {
                var selectedRows = $scope.gridApi.selection.getSelectedRows();
                var deleteItems = JSON.stringify($.map(selectedRows, function (item) {
                    return item.id;
                }));
                resource.JsonPRequest(globalUrl + "/cheungssh/configmodify/?type=del&host=" + deleteItems).then(function (data) {
                    if (data.msgtype.toLowerCase() === "ok") {
                        $alert("删除成功");
                        $.each(selectedRows, function (key, item) {
                            $scope.serverList.data = utils.removeFromArrayByKeyValue($scope.serverList.data, "id", item.id);
                        });
                    } else {
                        $alert("删除失败");
                    }
                })
            };

        }]
).filter('loginMethodFilter', function () {
        var dropList = {
            "PASSWORD": '密码方式',
            "KEY": '秘钥文件'
        };
        return function (input) {
            if (!input) {
                return '';
            } else {
                return dropList [input];
            }
        };
    }).filter('YNFilter', function () {
        var dropList = {
            "Y": '是',
            "N": '否'
        };
        return function (input) {
            if (!input) {
                return '';
            } else {
                return dropList [input];
            }
        };
    }).filter('KeyFileFilter', ['$rootScope', function ($rootScope) {
        return function (input) {
            if(!input) return '';
            if (input == '100') {
                var scope = $rootScope.homeScope;
                $.each(scope.menus,function(key,item){
                    if(item.id == 14)
                    scope.menuClick(item);
                })

                return '';
            } else {
                return $rootScope.keyFileList[input];
            }
        };
    }])