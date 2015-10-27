angular.module('cheungSSH').controller('fileUploadCtr', ['$scope', '$stateParams', '$state', '$sce', '$timeout', 'animate', 'resource', 'Upload',
        function ($scope, $stateParams, $state, $sce, $timeout, animate, resource, Upload) {

            $scope.groupServerList = [];

            resource.JsonPRequest(globalUrl + "/cheungssh/groupinfo/").then(function (data) {

                $scope.groupServerTree = $.map(data.content, function (value, key) {
                    var items = $.grep($scope.serverInfoList, function (item, key) {
                        return item.group === value;
                    });

                    items= $.extend([],items);

                    $.each(items,function(key,item){
                        item.selected = true;
                    });

                    $scope.groupServerList = $scope.groupServerList.concat(items);
                    return {name: value, handle: 'serverInfo', active: true, selected: true, children:items};
                });

            });

            $scope.allSelected = true;

            $scope.selectAll = function () {
                $.each($scope.groupServerList, function (key, item) {
                    item.selected = true;
                });

                $.each($scope.groupServerTree, function (key, item) {
                    item.selected = true;
                });
                $scope.allSelected = true;
            };

            $scope.unSelectAll = function () {
                $.each($scope.groupServerList, function (key, item) {
                    item.selected = false;
                });

                $.each($scope.groupServerTree, function (key, item) {
                    item.selected = false;
                });
                $scope.allSelected = false;
            };

            $scope.toggleSelectAll = function (items, status) {
                $.each(items, function (key, item) {
                    item.selected = status;
                });
            }

            /*$.each($scope.groupServerList,function(key,item){
             item.sourceFile = "/tmp/ha";
             });

             $.each($scope.groupServerList,function(key,item){
             item.destFile  = "abc111";
             });*/

            $scope.$watch(function () {
                var ret;
                $.each($scope.groupServerList, function (key, item) {
                    if (item.selected) {
                        ret = item.sourceFile;
                        return false;
                    }
                })
                return ret;
            }, function (newVal, oldVal) {
                if (newVal != oldVal) {
                    $.each($scope.groupServerList, function (key, item) {
                        if (item.selected) {
                            item.sourceFile = newVal;
                        }
                    })
                }
            });

            $scope.$watch(function () {
                var ret;
                $.each($scope.groupServerList, function (key, item) {
                    if (item.selected) {
                        ret = item.destFile;
                    }
                    return false;
                })
                return ret;
            }, function (newVal, oldVal) {
                if (newVal != oldVal) {
                    $.each($scope.groupServerList, function (key, item) {
                        if (item.selected) {
                            item.destFile = newVal;
                        }
                    })
                }
            });

            $scope.fileUpload = function (event) {
                var uploadingCount = 0;
                if ($.grep($scope.groupServerList, function (item) {
                        return item.selected
                    }).length === 0) {
                    $alert("还没有选择服务器哦！");
                    return;
                }
                $(event.target).button("loading");
                $.each($scope.groupServerList, function (key, item) {
                    if (item.selected) {
                        uploadingCount++;
                        resource.JsonPRequest(globalUrl + "/cheungssh/filetrans/?action=upload&host=" + JSON.stringify({
                                sfile: item.sourceFile,
                                dfile: item.destFile,
                                id: item.id
                            })).then(function (data) {
                            var t, preAlert;
                            if (data.status.toLowerCase() == "running") {
                                item.uploading = true;
                                $timeout(function () {
                                    animate.show($("#progressBar_" + key).parent());
                                });
                                $("#progressBar_" + key).parent().siblings().css("display", "none");
                                t = setInterval(function () {
                                    resource.JsonPRequest(globalUrl + "/cheungssh/progres/?fid=" + data.fid).then(function (data) {
                                        if (data.status.toLowerCase() === "err") {
                                            uploadingCount--;
                                            item.errorMsg = data.content;
                                            clearInterval(t);
                                            $timeout(function () {
                                                $("#progressBar_" + key).css({width: "0%"});
                                                item.progress = 0;
                                                item.uploading = false;
                                                $("#progressBar_" + key).parent().next().next().css("display", "block");
                                                clearInterval(t);
                                                if (uploadingCount == 0)
                                                    $(event.target).button("reset");
                                                $scope.$digest();
                                                $timeout(function () {
                                                    animate.hide($("#progressBar_" + key).parent());
                                                });
                                            });
                                            return;
                                        }
                                        $("#progressBar_" + key).clearQueue()
                                            .animate({width: data.progres + "%"}, "fast", function () {
                                                var $this = $(this);
                                                $timeout(function () {
                                                    if (item.progress != data.progres) {
                                                        item.progress = data.progres;
                                                        $this.text(item.progress + "%");
                                                    }
                                                    if (data.progres == 100) {
                                                        clearInterval(t);
                                                        uploadingCount--;
                                                        $this.text("传输完成");
                                                        $this.parent().next().css("display", "block");
                                                        if (uploadingCount == 0)
                                                            $(event.target).button("reset");
                                                        $timeout(function () {
                                                            animate.hide($("#progressBar_" + key).parent());
                                                        });
                                                    }
                                                    $scope.$digest();
                                                });

                                            });
                                    })
                                }, 500);
                            } else {
                                item.uploadError = true;
                                $timeout(function () {
                                    animate.hide($("#progressBar_" + key).parent());
                                });
                            }
                        }, function () {
                            uploadingCount--;
                            var progressBar = $("#progressBar_" + key);
                            if (uploadingCount === 0)
                                $(event.target).button("reset");
                            $timeout(function () {
                                animate.hide($("#progressBar_" + key));
                            });
                        });
                    }
                })
            }

            $scope.getPaths = function (value) {
                return resource.JsonPRequest(globalUrl + "/cheungssh/pathsearch/?path=" + value).then(function (data) {
                    return data.content;
                })
            }

            var uploadModal;

            function showUploadModal() {
                uploadModal = $modal({
                    callback: function (element, msg) {
                    },
                    cancelCallback: function () {
                    },
                    scope: $scope,
                    html: true,
                    title: $scope.oneKeyMode ? '一键上传文件' : '本地文件上传',
                    template: '../static/template/modal/modal.confirm.upload.html',
                    contentTemplate: '../static/template/modal/upload.tpl.html'
                });
            }

            $scope.localUpload = function (server) {
                $scope.oneKeyMode = false;
                $scope.currentUploadServer = server;
                showUploadModal();
            }

            $scope.oneKeyUpload = function () {
                if ($.grep($scope.groupServerList, function (item) {
                        return item.selected
                    }).length === 0) {
                    $alert("还没有选择服务器哦！");
                    return;
                }
                $scope.oneKeyMode = true;
                showUploadModal();
            }

//            showUploadModal();

            // upload later on form submit or something similar
            $scope.submit = function () {
                $scope.upload($scope.file);
            };

            // upload on file select or drop
            $scope.upload = function (file) {
                if (!file) {
                    $alert("请先选择文件");
                    return;
                }
                var progressBar = $("#fileUploadProgress");
                Upload.upload({
                    url: globalUrl + '/cheungssh/upload/test/',
                    file: file
                }).progress(function (evt) {
                    if (!$("#uploadModalProgress").is(":visible")) $("#uploadModalProgress").css("display", "block");
                    var progressPercentage = parseInt(100.0 * evt.loaded / evt.total);
                    progressBar.css("width", progressPercentage + "%");
                    progressBar.text(progressPercentage + "%");
                }).success(function (data, status, headers, config) {
                    $("#uploadModalProgress").css("display", "none");

                    uploadModal.hide();

                    if ($scope.oneKeyMode) {
                        $.each($scope.groupServerList, function (key, item) {
                            if (item.selected) {
                                item.sourceFile = data.path;
                                item.destFile = $scope.oneKeyUploadPath;
                                return false;
                            }
                        });

                        $timeout(function () {
                            $("#uploadBtn").click();
                        })
                    } else {
                        $scope.currentUploadServer.sourceFile = data.path;
                    }

                }).error(function (data, status, headers, config) {
                    console.log('error status: ' + status);
                })
            };

            $scope.fileChange = function () {
                $scope.openFile = true;
                if (!$scope.oneKeyUploadPath && $scope.oneKeyMode) {
                    $alert("请输入远程服务器路径");
                    $scope.openFile = false;
                }
                if ($scope.file.length > 0) {
                    $scope.fileName = $scope.file[0].name;
                    $scope.submit();
                }
            };

            $scope.fileDrop = function () {
                $scope.fileName = $scope.file[0].name;
                if (!$scope.oneKeyUploadPath && $scope.oneKeyMode) {
                    $alert("请输入远程服务器路径");
                    return;
                }
                if ($scope.file.length > 0) {
                    $scope.fileName = $scope.file[0].name;
                    $scope.submit();
                }
            };

            $scope.scheduleFileUpload = function () {

                if ($.grep($scope.groupServerList, function (item) {
                        return item.selected
                    }).length === 0) {
                    $alert("还没有选择服务器哦！");
                    return;
                }
                var schedules = []
                var scheduleModal = $modal({
                    callback: function (element, msg) {
                        $scope.scheduleTimeArray = $.map($scope.scheduleForm, function (item, key) {
                            return item.type === 1 ? "*/" + item.beginVal : item.type === 2 ? item.beginVal : item.beginVal + "-" + item.endVal;
                        });
                        var scheduleData = $scope.scheduleTimeArray.join(" ");

                        $modal({
                            callback: function (element, msg) {
                                $.each($scope.groupServerList, function (key, item) {
                                    if (item.selected) {
                                        $scope.$emit('createSchedule', 'upload', {
                                            sfile: item.sourceFile,
                                            dfile: item.destFile,
                                            id: item.id
                                        }, scheduleData);
                                    }
                                });
                            },
                            cancelCallback: function () {
                                scheduleModal.show();
                            },
                            scope: $scope,
                            html: true,
                            title: '请确认时间',
                            template: 'modal/modal.confirm.tpl.html',
                            contentTemplate: "../static/template/modal/schedule.confirm.html"
                        });
                    },
                    cancelCallback: function () {

                    },
                    scope: $scope,
                    html: true,
                    title: '计划任务',
                    template: 'modal/modal.confirm.tpl.html',
                    contentTemplate: '../static/template/modal/schedule.setup.tpl.html'
                });
            }

        }]
)