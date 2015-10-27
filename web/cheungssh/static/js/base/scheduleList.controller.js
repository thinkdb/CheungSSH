angular.module('cheungSSH').controller('scheduleListCtr',['$scope', '$stateParams', '$state', '$sce','$timeout','animate','resource','Upload','uiGridConstants','utils',
        function ($scope, $stateParams, $state, $sce,$timeout,animate,resource,Upload,uiGridConstants,utils) {
            $scope.scheduleList = {
                enableColumnResizing:true,
                data:[],
                onRegisterApi:function(gridApi){
                },
                //显示table的th
                columnDefs: [
                    { name: "状态",field:'status' },
                    { name: "目标文件",field:'dfile' },
                    { name: "IP",field:'ip' },
                    { name: "源文件",field:'sfile' },
                    { name: "命令",field:'cmd' },
                    { name: "用户",field:'user' },
                    { name: "类型",field:'runtype' },
                    { name: "结果",field:'content' },
                    { name: "运行时间",field:'runtime' },
                    { name: "创建时间",field:'createtime' },
                    { name: "最后运行时间",field:'lasttime' },
                    { name: "操作",cellTemplate:'<div class="text-center"><button class="btn btn-sm btn-danger" style="height: 28px;" ng-click="grid.appScope.removeSchedule(row.entity)";">删&nbsp;&nbsp;除</button></div>'}
                ]
            };

            $scope.removeSchedule = function(entity){
                resource.JsonPRequest(globalUrl+"/cheungssh/delcrondlog/?fid="+entity.fid).then(function(data){
                    if(data.msgtype === "OK"){
                        $scope.scheduleList.data = utils.removeFromArrayByKeyValue($scope.scheduleList.data,'fid',entity.fid);
                    }else{
                        $alert("删除失败");
                    }
                })

            }

            $scope.toCommand = function(){
                $.each($scope.menus,function(key,item){
                    if(item.id == 1){
                        $timeout(function(){
                            $scope.menuClick(item);
                        })

                    }
                });
            };

            $scope.toUpload = function(){
                $.each($scope.menus,function(key,item){
                    if(item.id == 2){
                        item.collapse = true;
                        $timeout(function(){
                            $scope.menuClick(item.children[1]);
                            $scope.$parent.$digest();
                        })

                    }
                });
            };

            $scope.toDownload = function(){
                $.each($scope.menus,function(key,item){
                    if(item.id == 2){
                        item.collapse = true;
                        $timeout(function(){
                            $scope.menuClick(item.children[0]);
                            $scope.$parent.$digest();
                        })
                    }
                });
            };

            resource.JsonPRequest(globalUrl+"/cheungssh/showcrondlog/").then(function(data){
                $scope.scheduleList.data = data.content;
            });

        }]
);