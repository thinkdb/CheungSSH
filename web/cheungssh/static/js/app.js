angular.module('cheungSSH', [
    'ui.router',
    'ui.grid',
    'ui.grid.selection',
    'ui.grid.autoResize',
    'ui.grid.cellNav',
    'ui.grid.edit',
    'ui.grid.expandable',
    'ui.grid.exporter',
    'ui.grid.grouping',
    'ui.grid.pagination',
    'ui.grid.resizeColumns',
    'ui.grid.moveColumns',
    'ngAnimate',
    'ngMessages',
    'ngFileUpload',
    'mgcrea.ngStrap',
    'widget.scrollbar',
    'angular-loading-bar',
    'drag'
]).run(
    [          '$rootScope', '$modal', '$alert', '$templateCache', 'i18nService',
        function ($rootScope, $modal, $alert, $templateCache, i18nService) {
            i18nService.setCurrentLang("zh-cn");
            window.$alert = function (content, options) {
                var defaultVal = {
                    title: '提示：',
                    placement: 'alert-position',
                    animation: 'am-fade-and-slide-bottom',
                    container: '.alert-container',
                    duration: 1,
                    type: 'info',
                    show: true
                };
                options = $.extend(defaultVal, options);
                options.content = content;
                $alert(options);
            };
            window.$alertError = function (content, options) {
                var defaultVal = {
                    title: '提示：',
                    placement: 'alert-position',
                    animation: 'am-fade-and-slide-bottom',
                    container: '.alert-container',
                    type: 'info',
                    backdrop:true,
                    show: true,
                    dismissable:true
                };
                options = $.extend(defaultVal, options);
                options.content = content;
                $alert(options);
            };

            window.$confirm = function (content, callback, options) {
                var defaultVal = {
                    template: 'modal/modal.confirm.tpl.html',
                    animation: 'am-fade',
                    html: true,
                    placement: 'center',
                    title: "提示"
                };
                options = $.extend(defaultVal, options);
                options.content = content;
                options.callback = callback;
                $modal(options);
            };

            window.$modal = $modal;
        }
    ]
)
    .config(
    [          '$stateProvider', '$urlRouterProvider',
        function ($stateProvider, $urlRouterProvider) {
            $stateProvider
                .state("login", {
                    url: "/login",
                    views: {
                        'main': {
                            templateUrl: '../static/template/login.tpl.html'
                        },
                        'login@login': {
                            templateUrl: '../static/template/loginForm.tpl.html',
                            controller: ['$scope', '$state', 'resource', '$rootScope', function ($scope, $state, resource, $rootScope) {
                                $scope.logining = false;
                                $scope.login = function () {
                                    $scope.logining = true;
                                    resource.cors(globalUrl + "/cheungssh/login/", {
                                        username: $scope.username,
                                        password: $scope.password
                                    }).then(function (resp) {
                                        if (resp.auth === "yes") {
                                            $rootScope.sessionid = resp.sid;
                                            $state.go("home");
                                        } else if (resp.auth == "no") {
                                            $alert(resp.content ? resp.content : "登录失败");
                                        }
                                        $scope.logining = false;
                                    }, function () {
                                        $scope.logining = false;
                                    });
                                };

                                document.onkeyup = function (e) {
                                    if (e.keyCode == 13) $scope.login();
                                };
                            }]
                        }
                    }
                }).state("login.register", {
                    url: "/register",
                    views: {
                        'login@login': {
                            templateUrl: '../static/template/register.tpl.html',
                            controller: 'registerCtr'
                        }
                    }
                }).state("login.forgotPwd", {
                    url: "/forgotPwd",
                    views: {
                        'login@login': {
                            templateUrl: '../static/template/forgotPwd.tpl.html',
                            controller: 'forgotPwdCtr'
                        }
                    }
                }).state("home", {
                    url: "/home",
                    resolve: {
                        allServers: ['resource', '$rootScope',
                            function (resource, $rootScope) {
                                return  resource.JsonPRequest(globalUrl + '/cheungssh/groupinfoall/').then(function (data) {
                                    return $.map(data.content, function (item) {
                                        item.type = 'modify';
                                        return item;
                                    });
                                });
                            }]
                    },
                    views: {
                        'main': {
                            templateUrl: '../static/template/home.tpl.html',
                            controller: 'homeCtr'
                        }
                    }
                }).state("home.serverList", {
                    url: '/:path',
                    views: {
                        'contentPanel': {
                            resolve: {
                                keyFileList: ['resource', '$rootScope',
                                    function (resource, $rootScope) {
                                        return resource.JsonPRequest(globalUrl + '/cheungssh/keyadmin/?show_type=list').then(function (data) {
                                            data.content[100] = '上传密钥';
                                            $rootScope.keyFileList = data.content;
                                            return data.content;
                                        });
                                    }]
                            },
                            templateUrl: '../static/template/serverList.tpl.html',
                            controller: 'serverListCtr'
                        }
                    }
                }).state("home.command", {
                    url: '/:path',
                    views: {
                        'contentPanel': {
                            templateUrl: '../static/template/command.tpl.html',
                            controller: 'commandCtr'
                        }
                    }
                }).state("home.transferLog", {
                    url: '/:path',
                    views: {
                        'contentPanel': {
                            templateUrl: '../static/template/transferLog.tpl.html',
                            controller: 'transferLogCtr'}
                    }
                }).state("home.fileUpload", {
                    url: '/:path',
                    views: {
                        'contentPanel': {
                            templateUrl: '../static/template/fileUpload.tpl.html',
                            controller: 'fileUploadCtr'}
                    }
                }).state("home.download", {
                    url: '/:path',
                    views: {
                        'contentPanel': {
                            templateUrl: '../static/template/download.tpl.html',
                            controller: 'downloadCtr'}
                    }
                }).state("home.keyfileMgr", {
                    url: '/:path',
                    views: {
                        'contentPanel': {
                            templateUrl: '../static/template/keyfileMgr.tpl.html',
                            controller: 'keyfileMgrCtr'}
                    }
                }).state("home.scheduleList", {
                    url: '/:path',
                    views: {
                        'contentPanel': {
                            templateUrl: '../static/template/scheduleList.tpl.html',
                            controller: 'scheduleListCtr'}
                    }
                }).state("home.script", {
                    url: '/:path',
                    views: {
                        'contentPanel': {
                            templateUrl: '../static/template/script.tpl.html',
                            controller: 'scriptCtr'}
                    }
                }).state("home.cmdHistory", {
                    url: '/:path',
                    views: {
                        'contentPanel': {
                            templateUrl: '../static/template/cmdHistory.tpl.html',
                            controller: 'cmdHisCtr'}
                    }
                }).state("home.visitHistory", {
                    url: '/:path',
                    views: {
                        'contentPanel': {
                            templateUrl: '../static/template/visitHistory.tpl.html',
                            controller: 'visitHisCtr'}
                    }
                });

            $urlRouterProvider.otherwise('login');
        }
    ]
)
    .controller('registerCtr', ['$scope', '$state', function ($scope, $state) {

    }])
    .controller('forgotPwdCtr', ['$scope', '$state', function ($scope, $state) {

    }])
    .factory('resource', ['$q', 'cfpLoadingBar', '$state', '$rootScope', function ($q, cfpLoadingBar, $state, $rootScope) {
        var ajaxCount = 0;
        return{
            JsonPRequest: function (url) {
                var defer = $q.defer();
                if (ajaxCount == 0) {
                    cfpLoadingBar.start();
                }
                ajaxCount++;
                $.jsonp({
                    url: url,
                    callbackParameter: "callback",
                    timeout: 5000,
                    error: function (xOptions, textStatus) { // 错误发生时，立即执行
                        defer.reject();
                        if (--ajaxCount == 0)
                            cfpLoadingBar.complete();
                    },
                    success: function (data) {
                        if (data.msgtype == 'login') {
                            $state.go("login");
                            $alert("请先登录");
                            defer.reject();
                        } else if (data.msgtype && data.msgtype.toLowerCase() == 'ok') {
                            defer.resolve(data);
                        } else {
                            $alertError(data.content ? data.content : "请求失败");
                            defer.reject(data);
                        }
                        if (--ajaxCount == 0)
                            cfpLoadingBar.complete();
                    }
                });
                return defer.promise;
            },
            cors: function (url, data) {
                var defer = $q.defer();
                if (ajaxCount == 0) {
                    cfpLoadingBar.start();
                }
                ajaxCount++;
                $.ajax({
                    type: "POST",
                    url: url,
                    data: data,
                    success: function (data) {
                        data = eval("(" + data + ")");
                        if (data.msgtype == 'login') {
                            $state.go("login");
                            $alert("请先登录");
                            defer.reject();
                        } else if (data.msgtype && data.msgtype.toLowerCase() == 'ok') {
                            defer.resolve(data);
                        } else {
                            $alertError (data.content);
                            defer.reject(data);
                        }

                        if (--ajaxCount == 0)
                            cfpLoadingBar.complete();
                    },
                    error: function () {
                        if (--ajaxCount == 0)
                            cfpLoadingBar.complete();
                        defer.reject();
                    },
                    complete: function (data) {
                        console.log(data.getAllResponseHeaders());
                    }
                });
                return defer.promise;
            }
        }
    }])
    .factory('utils', ['$q', function ($q) {
        return{
            removeFromArrayByKeyValue: function (array, key, value) {
                var tmp = [];
                var found = false;
                if (!angular.isArray(array)) return;
                for (var i = 0; i < array.length; i++) {
                    if (array[i][key] == value && !found) {
                        found = true;
                        continue;
                    }
                    tmp.push(array[i]);
                }
                return tmp;
            }
        }
    }])
    .factory('animate', ['$q', function ($q) {
        return{
            show: function (element) {
                element.addClass("ng-enter");
                element.addClass("ng-enter-active");
                element.css({display: "block"});
                setTimeout(function () {
                    element.removeClass("ng-enter ng-enter-active");
                    element.removeClass("ng-enter ng-enter-active");
                }, 300);
            },

            hide: function (element) {
                element.addClass("ng-leave");
                element.addClass("ng-leave-active");
                setTimeout(function () {
                    element.css({display: "none"});
                    element.removeClass("ng-leave ng-leave-active");
                }, 300);
            }
        }
    }])
    .provider('$waveEffect', function () {

        var requestAnimateFrame = function () {
            return (
                window.requestAnimationFrame ||
                window.mozRequestAnimationFrame ||
                window.oRequestAnimationFrame ||
                window.msRequestAnimationFrame ||
                function (callback) {
                    window.setTimeout(callback, 1000 / 60);
                }
                );
        }();

        this.$get = ["$timeout", function ($timeout) {
            function waveEffectFactory(element, waveEffectColor, waveEffectSpeed) {
                var canvas = {},
                    centerX = 0,
                    centerY = 0,
                    color = '#FFFFFF',
                    speed = 6,
                    context = {},
                    radius = 0,
                    press = function (event) {
                        element = event.toElement;
                        element.width = element.offsetWidth;
                        element.height = element.offsetHeight;
                        context.clearRect && context.clearRect(0, 0, element.clientWidth, element.clientHeight);
                        context = element.getContext('2d');
                        context.globalAlpha = 0.3
                        radius = 0;
                        centerX = event.offsetX;
                        centerY = event.offsetY;
                        draw();
                    },

                    draw = function () {
                        context.clearRect(0, 0, element.clientWidth, element.clientHeight);
                        context.beginPath();
                        context.arc(centerX, centerY, radius, 0, 2 * Math.PI, false);
                        context.fillStyle = color;
                        context.fill();
                        radius += speed;
                        if (radius < element.width) {
                            requestAnimateFrame(draw);
                        } else {
                            context.clearRect(0, 0, element.clientWidth, element.clientHeight);
                        }
                    };

                canvas = document.createElement('canvas');
                canvas.addEventListener('click', press, false);
                element[0].style.position = "relative";
                element[0].appendChild(canvas);
                canvas.style.width = '100%';
                canvas.style.height = '100%';
                canvas.style.position = 'absolute';
                canvas.style.top = '0px';
                canvas.style.left = '0px';
                waveEffectColor && (color = waveEffectColor);
                waveEffectSpeed && (speed = waveEffectSpeed);
            }

            return waveEffectFactory;

        }];
    })
    .directive('waveEffect', ['$waveEffect', function ($waveEffect) {
        return function (scope, element, attrs) {
            if (typeof attrs.waveEffectSpeed == "string") attrs.waveEffectSpeed = parseInt(attrs.waveEffectSpeed);
            $waveEffect(element, attrs.waveEffectColor, attrs.waveEffectSpeed);
        };
    }])
;

