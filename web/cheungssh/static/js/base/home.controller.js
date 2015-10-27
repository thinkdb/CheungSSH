angular.module('cheungSSH').controller('homeCtr', ['$scope', '$rootScope', '$state', 'i18nService', '$interval', 'resource', 'allServers', function ($scope, $rootScope, $state, i18nService, $interval, resource, allServers) {
    $rootScope.homeScope = $scope;
    $scope.serverInfoList = allServers;
    $.each($scope.serverInfoList, function (key, server) {
        resource.JsonPRequest(globalUrl + '/cheungssh/sshcheck/?id=' + server.id).then(function (resp) {
            server.status = resp.status;
            server.content = resp.content;
        })
    });

    $interval(function () {
        $.each($scope.serverInfoList, function (key, server) {
            if (server.type == 'modify')
                resource.JsonPRequest(globalUrl + '/cheungssh/sshcheck/?id=' + server.id).then(function (resp) {
                    server.status = resp.status;
                    server.content = resp.content;
                })
        });
    }, 60 * 1000)
    $scope.menus = [
        {id: 5, name: '服务器配置', active: true},
        {id: 1, name: '命令'},
        {
            id: 2, name: '文件传输', children: [
            {id: 3, name: '下载'},
            {id: 4, name: '上传'}
        ]
        },
/*
        {
            id: 6, name: 'API', children: [
            {id: 7, name: '监控调用'},
            {id: 8, name: '资产调用'}
        ]
        },
        {
            id: 9, name: '自动安装部署', children: [
            {id: 10, name: 'Apache'},
            {id: 11, name: 'Tomcat'}
        ]},
*/
        {id: 12, name: '计划任务'},
        /*{id: 13, name: '报表绘图'},*/
        {id: 14, name: '秘钥文件管理'},
        {id: 15, name: '脚本'}/*,
        {
            id: 16, name: '审计', children: [
            {id: 17, name: '命令记录'},
            {id: 18, name: '访问记录'}
        ]}*/
    ];

    $scope.navs = [
        {
            id: 1, name: '命令'
        }
    ]

    $scope.menuClick = function (item) {
        if ($scope.serverInfoList.length == 0) {
            item.id != 5 && $alert("请先配置服务器后才能使用该功能");
            return;
        }
        $.each($scope.menus, function (key, item) {
            item.active = false;
            if (item.children)
                $.each(item.children, function (key, item) {
                    item.active = false;
                })
        });

        item.active = true;

        if (item.id === 1) {
            $scope.path = "index.html";
            $state.go('home.command', {path: item.id});
            return;
        }

        if (item.id === 2) {
            $state.go('home.transferLog', {path: item.id});
        }

        if (item.id == 3) {
            $state.go("home.download", {path: item.id});
            return;
        }

        if (item.id == 4) {
            $state.go("home.fileUpload", {path: item.id});
            return;
        }

        if (item.id === 5) {
            $state.go('home.serverList');
        }

        if (item.id === 12) {
            $state.go('home.scheduleList');
        }

        if (item.id === 14) {
            $state.go('home.keyfileMgr');
            return;
        }

        if (item.id === 15) {
            $state.go('home.script');
            return;
        }

        /*if (item.id === 17) {
            $state.go('home.cmdHistory');
            return;
        }

        if (item.id === 18) {
            $state.go('home.visitHistory');
            return;
        }*/

        if (item.children) {
            item.collapse = !item.collapse;
        }

    }

    $scope.$on('createSchedule', function (event, type, data, scheduleData) {
        resource.JsonPRequest(globalUrl + "/cheungssh/crontab/?type=" + type + "&value=" +
            JSON.stringify(data) + "&runtime=" + scheduleData).then(function (data) {
            if (data.msgtype.toLowerCase() != 'ok') {
                $alert(data.content);
            }
        }, function () {
            $alert("创建失败");
        });

    });

    $scope.donate = function () {
        $modal({
            callback: function (element, msg) {
            },
            cancelCallback: function () {
            },
            scope: $scope,
            html: true,
            title: '捐助',
            content: '<div class="clearfix"><p>&nbsp;&nbsp;&nbsp;&nbsp;我们的开发团队历经一个国庆，对Web系统的开发持续了84个小时，不分昼夜持续开发本系统。如果您觉得CheungSSH真的对贵司或者您个人的运维管理工作有帮助，我们是非常欣慰的，总算做了一点公益事业。为了能让我们有更强大并且持续的创新动力，我们还是希望能得到您（贵司）的捐助，以下是我们的捐助信息：</p><img style="width:150px;height:150px;float:left;margin-left:25px;" src="../static/img/donate.png"><div style="margin: 50px 0 0 200px;"><h4>收款人：张其川</h4><h4>支付宝账号: kc-c@qq.com</h4></div></div>'
//            contentTemplate: '../static/template/modal/modal.donate.tpl.html'
        });
    }

    $scope.loginOut = function () {
        $modal({
            callback: function (element, msg) {
                resource.JsonPRequest(globalUrl + "/cheungssh/logout/").then(function (data) {
                    if (data.msgtype.toLowerCase() == 'ok') {
                        $state.go("login");
                    }
                }, function () {
                    $alert("注销失败");
                });


            },
            cancelCallback: function () {
            },
            title: '确认提示',
            template: 'modal/modal.confirm.tpl.html',
            scope: $scope,
            html: true,
            content: '确定要退出到登录页面？'
        });

    }

    $state.go("home.serverList");
}])