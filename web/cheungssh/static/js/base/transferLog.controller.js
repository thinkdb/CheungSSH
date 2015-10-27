angular.module('cheungSSH').controller('transferLogCtr',['$scope', '$stateParams', '$state', '$sce','$timeout','animate','resource','Upload',
        function ($scope, $stateParams, $state, $sce,$timeout,animate,resource,Upload) {
            $scope.transferLogList = {
                enableColumnResizing:true,
                enableRowSelection: true,
                enableSelectAll: true,
                enableColumnMenus: true,
                enableSorting:true,
                selectionRowHeaderWidth: 35,
                enableCellEditOnFocus:true,
                paginationPageSize: 20,
                //点击展开时触发
                expandableRowCallBack:function(sc){

                },
                onRegisterApi:function(gridApi){
                },
                //显示table的th
                columnDefs: [
                    { name: "IP",field:'ip' },
                    { name: "用户",field:'user' },
                    { name: "源文件",field:'sfile' },
                    { name: "动作",field:'action' },
                    { name: "结果",field:'result' },
                    { name: "完成时间",field:'time' },
                    { name: "消息",field:'msg' },
                    { name: "目标文件",field:'dfile' },
                    { name: "文件大小",field:'size' }
                ]
            };
            resource.JsonPRequest(globalUrl+"/cheungssh/translog/").then(function(data){
                $scope.transferLogList.data = data.content;
            });
        }]
)