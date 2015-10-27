angular.module('cheungSSH').controller('commandCtr', ['$scope', '$stateParams', '$state', '$sce', '$timeout', 'animate', 'resource', 'Upload', 'uiGridConstants', 'utils',
    function ($scope, $stateParams, $state, $sce, $timeout, animate, resource, Upload, uiGridConstants, utils) {

        $scope.groupServerList = [];

        resource.JsonPRequest(globalUrl + "/cheungssh/groupinfo/").then(function (data) {
            $scope.groupServerTree = $.map(data.content, function (value, key) {
                var items = $.grep($scope.serverInfoList, function (item, key) {
                    return item.group === value;
                });

                items= $.extend([],items);

                $.each(items,function(key,item){
                    item.selected = true;
                    item.status = 'UNSTART';
                });

                $scope.groupServerList = $scope.groupServerList.concat(items);

                return {name: value, handle: 'serverInfo', active: true, selected: true, children:items};
            });
            $timeout(function () {
                window.onresize = resetContentHeight;
                resetContentHeight();
            })
        });

        function resetContentHeight() {
            $("#commandContentPanel").css("height", (document.body.scrollHeight - parseInt($("#commandServersGroup").css("height"), 10) - 180) + "px");
            $scope.$broadcast("resetScrollBar");
            $scope.$broadcast("scrollToBottom");
        }

        $scope.resetHeight = function(){
            $timeout(function(){
                resetContentHeight();
            },600);
        }

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
        };

        $scope.chooseServers = function () {
            $modal({callback: function (element, msg) {
            },
                cancelCallback: function () {
                },
                scope: $scope,
                html: true,
                title: '选择服务器',
                contentTemplate: '../static/template/modal/modal.chooseservers.tpl.html'
            });
        };

        $scope.getPaths = function (value) {
            return resource.JsonPRequest(globalUrl+"/cheungssh/pathsearch/?path=" + value).then(function (data) {
                return data.content;
            })
        }

        $scope.tags = [];

        $scope.applyTag = function (tag) {
            $scope.commandPath = tag;
        }

        $scope.removeTag = function (tag) {
            var len = $scope.tags.length;
            var sit = $scope.tags.indexOf(tag);
            $scope.tags = $scope.tags.slice(0, sit).concat($scope.tags.slice(sit + 1, len));
        }

        $scope.inProgress = false;

        var progressBar = $("#commandProgress");

        if (window.WebSocket) {
            $scope.ws = $.extend(new WebSocket(WSUrl), {
                onopen: function (e) {
                    $scope.mess = "连接端口成功";
                },
                onclose: function (e) {
                    $scope.mess = "服务器已关闭";
                },

                onerror: function () {
                    $scope.mess = "连接端口失败";
                },
                onmessage: function (e) {
                    if (e.data == "Starting") {
                        return;
                    }
                    if (e.data == "Done") {

                    }
                    try {
                        var data = e.data;
                        var evalData = eval("(" + e.data + ")");
                    } catch (e) {
                        return;
                    }

                    if (evalData) {
                        if(evalData.msgtype ==1){
                            var server = evalData.content[0].servers[0];
                            progressBar.css("width",server.jindu+"%");
                            progressBar.text(server.jindu+"%");
                            $("#realTimeContent").append(server.info);
                            $.each($scope.groupServerList,function(key,item){
                                if(server.ip.indexOf(item.ip) != -1){
                                    server.infoHtml = $sce.trustAsHtml(server.info);
                                    $.extend(item,server);
                                }
                            });
                            $scope.$broadcast("resetScrollBar");
                            $scope.$broadcast("scrollToBottom");

                            $timeout(function(){
                                $scope.$digest();
                                $timeout(function(){
                                    if(server.jindu === 100){
                                        if($scope.tags.indexOf($scope.commandPath) == -1)
                                            $scope.tags.push($scope.commandPath);
                                        $scope.inCommandExecuting = false;
                                        $scope.inProgress = false;
                                        $scope.$digest();
                                        $timeout(function(){
                                            progressBar.css("width","0%");
                                            progressBar.text("0%");
                                            resetContentHeight();
                                        },300);
                                        return;
                                    }
                                })
                            });
                        }else if(evalData.msgtype == 'token'){
                            $scope.RID = evalData.id;
                        }
                    }
                }
            });

            function getKeys(obj) {
                var keys = [];
                for (var key in obj) {
                    if (key) {
                        keys.push(key)
                    }
                    return keys;
                }
                return [0];
            }


            function setSelectionRange(input, selectionStart, selectionEnd) {
                if (input.setSelectionRange) {
                    input.focus();
                    input.setSelectionRange(selectionStart, selectionEnd);
                }
                else if (input.createTextRange) {
                    var range = input.createTextRange();
                    range.collapse(true);
                    range.moveEnd('character', selectionEnd);
                    range.moveStart('character', selectionStart);
                    range.select();
                }
            }

            function setCaretToPos(input, pos) {
                setSelectionRange(input, pos, pos);
            }

            function trim(s) {
                return s.replace(/(^\s*)|(\s*$)/g, '');
            }
        }

        $scope.executeCommand = function(event){
            var selectedServers= $.grep($scope.groupServerList,function(item){
                return item.selected;
            });

            if(selectedServers.length == 0){
                $alert("请选择至少一个服务器");
                return;
            }

            $scope.inCommandExecuting = true;
            $scope.inProgress = true;
            $timeout(function(){
                resetContentHeight();
            })


            var data = JSON.stringify({
                selectserver: $.map(selectedServers,function(item){
                    return item.id
                }).join(","),
                cmd: $scope.commandPath
            })

            resource.JsonPRequest(globalUrl + "/cheungssh/excutecmd/?cmd="+data+"&rid="+$scope.RID).then(function(resp){
                $("#realTimeContent").append('<div style="height:500px;"></div>');
            })
        }

        $timeout(function(){
            $("#commandPath").keyup(function(event){
                var b = document.all ? window.event : event;
                return 13 == b.keyCode && $scope.commandPath && $("#commandSendBtn").click();
            })
        });

        $scope.showGroupServer = true;

        $scope.hasSelectedServer = function(group){
            var is = false;
            if(group.children&&group.children.length>0)
            $.each(group.children,function(key,item){
                if(item.selected)is = true;
            });
            return is;
        }

        $scope.clearContent = function(){
              $("#realTimeContent").html("");
        }

        $scope.scheduleCommand = function(){

            if($.grep($scope.groupServerList,function(item){
                return item.selected
            }).length === 0){
                $alert("还没有选择服务器哦！");
                return;
            }

            var scheduleModal = $modal({callback: function (element, msg) {
                $scope.scheduleTimeArray = $.map($scope.scheduleForm,function(item,key){
                    return item.type === 1?"*/"+item.beginVal:item.type === 2?item.beginVal:item.beginVal+"-"+item.endVal;
                });
                var scheduleData = $scope.scheduleTimeArray.join(" ");

                $modal({callback: function (element, msg) {
                    selectedServers = $.grep($scope.groupServerList, function (item) {
                        return item.selected;
                    });

                    $.each(selectedServers,function(key,item){
                        $scope.$emit('createSchedule', 'cmd', {
                            cmd:$scope.commandPath,
                            id:item.id
                        }, scheduleData);
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
    }])