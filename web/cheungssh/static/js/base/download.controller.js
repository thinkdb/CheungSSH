angular.module('cheungSSH').controller('downloadCtr',['$scope', '$stateParams', '$state', '$sce','$timeout','animate','resource','Upload',
        function ($scope, $stateParams, $state, $sce,$timeout,animate,resource,Upload) {

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

            $scope.selectAll=  function(){
                $.each($scope.groupServerList,function(key,item){
                    item.selected = true;
                });

                $.each($scope.groupServerTree,function(key,item){
                    item.selected = true;
                });
                $scope.allSelected = true;
            };

            $scope.unSelectAll=  function(){
                $.each($scope.groupServerList,function(key,item){
                    item.selected = false;
                });

                $.each($scope.groupServerTree,function(key,item){
                    item.selected = false;
                });
                $scope.allSelected = false;
            };

            $scope.toggleSelectAll = function(items,status){
                $.each(items,function(key,item){
                    item.selected = status;
                });
            }

          /*  $scope.destFile = "abc111";

            $.each($scope.groupServerList,function(key,item){
                item.sourceFile = "/tmp/ha";
            });*/

            $scope.getPaths = function(value){
                return resource.JsonPRequest(globalUrl+"/cheungssh/pathsearch/?path="+value).then(function(data){
                    return data.content;
                })
            };

            $scope.$watch(function(){
                var ret;
                $.each($scope.groupServerList,function(key,item){
                    if(item.selected){
                        ret = item.sourceFile;
                        return false;
                    }
                })
                return ret;
            },function(newVal,oldVal){
                if(newVal != oldVal ){
                    $.each($scope.groupServerList,function(key,item){
                        if(item.selected){
                            item.sourceFile = newVal;
                        }
                    })
                }
            });

            $scope.downloadToWeb =function(event){
                var downloadingCount = 0;
                if($.grep($scope.groupServerList,function(item){
                    return item.selected
                }).length === 0){
                    $alert("还没有选择服务器哦！");
                    return;
                }
                $(event.target).button("loading");
                $.each($scope.groupServerList,function(key,item){
                    if(item.selected){
                        item.downloadComplete = false;
                        downloadingCount++;
                        resource.JsonPRequest(globalUrl+"/cheungssh/filetrans/?action=download&host="+JSON.stringify({
                            sfile:item.sourceFile,
                            dfile:item.destFile,
                            id:item.id
                        })).then(function(data){
                            var t,preAlert;
                            if(data.status.toLowerCase() == "running"){
                                    item.uploading = true;
                                $timeout(function(){
                                    animate.show($("#progressBar_"+key).parent());
                                });
                                $("#progressBar_"+key).parent().siblings().css("display","none");
                                t = setInterval(function(){
                                    resource.JsonPRequest(globalUrl+"/cheungssh/progres/?fid=" + data.fid).then(function(data){
                                        if(data.status.toLowerCase() === "err"){
                                            downloadingCount--;
                                            item.errorMsg = data.content;
                                            clearInterval(t);
                                            $timeout(function () {
                                                $("#progressBar_"+key).css({width: "0%"});
                                                item.progress = 0;
                                                $("#progressBar_"+key).parent().next().next().css("display","block");
                                                clearInterval(t);
                                                if(downloadingCount == 0){
                                                    $(event.target).button("reset");
                                                    downloadCompleted();
                                                }

                                                $scope.$digest();
                                                $timeout(function(){
                                                    animate.hide($("#progressBar_"+key).parent());
                                                });
                                            });
                                            return;
                                        }
                                        $("#progressBar_"+key).clearQueue()
                                            .animate({width: data.progres + "%"}, "fast", function () {
                                                var $this = $(this);
                                                $timeout(function () {
                                                    item.progress = data.progres;
                                                    $this.text(item.progress+"%");
                                                    if (data.progres == 100) {
                                                        item.downloadComplete = true;
                                                        clearInterval(t);
                                                        downloadingCount--;
                                                        $this.text("传输完成");
                                                        $this.parent().next().css("display","block");
                                                        if(downloadingCount == 0){
                                                            downloadCompleted();
                                                            $(event.target).button("reset");
                                                        }

                                                        $timeout(function(){
                                                            animate.hide($("#progressBar_"+key).parent());
                                                        });
                                                    }
                                                    $scope.$digest();
                                                });

                                            });
                                    })
                                },500);
                            }else{
                                item.uploadError = true;
                                $timeout(function(){
                                    animate.hide($("#progressBar_"+key).parent());
                                });
                            }
                        },function(){
                            downloadingCount--;
                            var progressBar = $("#progressBar_"+key);
                            if(downloadingCount === 0){
                                downloadCompleted();
                                $(event.target).button("reset");
                            }
                            $timeout(function(){
                                animate.hide($("#progressBar_"+key));
                            });
                        });
                    }
                })
            };

            function downloadCompleted(){
                $scope.firstAccess = false;
                 $scope.downloadedServerList.data = $.grep($scope.groupServerList,function(item){
                        return item.downloadComplete;
                 });
                $scope.downloadToLocal();
            };

            $scope.downloadedServerList = {
                enableColumnResizing:true,
                enableRowSelection: true,
                enableSelectAll: true,
                enableColumnMenus: true,
                enableSorting:true,
                selectionRowHeaderWidth: 35,
                excessRows:10,
                //点击展开时触发
                expandableRowCallBack:function(sc){

                },
                onRegisterApi:function(gridApi){
                    $scope.gridApi = gridApi;
                    $.extend(gridApi.core.raise,{
                        renderingComplete:function(rowEntity,colDef,triggerEvent){
                            gridApi.core.refresh();
                        }
                    });
                },
                //显示table的th
                columnDefs: [
                    { name: '服务器地址',field:'ip' },
                    { name: '已下载文件',field:'sourceFile' }
                ]
            }

            $scope.downloadToLocal = function(){
                var modal = $modal({callback: function (element, msg) {
                    var files = $.map($scope.gridApi.selection.getSelectedRows(),function(item,key){
                            return item.sourceFile;
                    });
                    resource.JsonPRequest(globalUrl+"/cheungssh/download/?file="+JSON.stringify(files)+"&callback=123").then(function(data){
                        window.open(data.url);
                    });
                    },
                    cancelCallback:function(){

                    },
                    scope:$scope,
                    html: true,
                    title: '下载文件到本地',
                    template: '../static/template/modal/modal.confirm.download.html',
                    contentTemplate: '../static/template/modal/download.local.tpl.html'
                }).$promise.then(function(){
                        $timeout(function(){
                            $scope.gridApi.selection.selectAllRows();

                            var selectedServers = $.grep($scope.groupServerList,function(item){
                                return item.selected;
                            });

                            console.log(selectedServers);

                            if($scope.downloadedServerList.data.length == selectedServers.length.length){
                                modal.hide();

                                var files = $.map($scope.downloadedServerList.data,function(item,key){
                                    return item.sourceFile;
                                });

                                resource.JsonPRequest(globalUrl+"/cheungssh/download/?file="+JSON.stringify(files)+"&callback=123").then(function(data){
                                    window.open(data.url);
                                });
                            }
                        })
                    });
            }

            $scope.scheduleDownload = function () {

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
                        $.each($scope.groupServerList, function (key, item) {
                            if (item.selected) {
                                $scope.$emit('createSchedule', 'download', {
                                    sfile: item.sourceFile,
                                    dfile: item.destFile,
                                    id: item.id}, scheduleData);
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

            $scope.firstAccess = true;

        }]
)