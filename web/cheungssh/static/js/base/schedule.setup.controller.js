angular.module('cheungSSH').controller('scheduleSetupCtr',['$scope', '$stateParams', '$state', '$sce','$timeout','animate','resource','Upload','uiGridConstants','utils',
        function ($scope, $stateParams, $state, $sce,$timeout,animate,resource,Upload,uiGridConstants,utils) {
            if($scope.$parent.$parent.$parent.$parent.scheduleForm){
                $scope.scheduleForm = $scope.$parent.$parent.$parent.$parent.scheduleForm;
            }else{
                $scope.$parent.$parent.$parent.$parent.scheduleForm = $scope.scheduleForm ={
                    minute:{type:1,beginVal:1,endVal:2},
                    hour:{type:1,beginVal:1,endVal:2},
                    day:{type:1,beginVal:1,endVal:2},
                    month:{type:1,beginVal:1,endVal:2},
                    week:{type:1,beginVal:1,endVal:2}
                };

            }

            $scope.optionMinute = [
                {id:1,value:"每N分钟"},
                {id:2,value:"在第N分钟"},
                {id:3,value:"在N分钟范围"}
            ];

            $scope.optionHour = [
                {id:1,value:"每N小时"},
                {id:2,value:"在第N小时"},
                {id:3,value:"在N小时范围"}
            ];
            $scope.optionDay = [
                {id:1,value:"每N天"},
                {id:2,value:"在第N天"},
                {id:3,value:"在N天范围"}
            ];
            $scope.optionWeek = [
                {id:1,value:"每N周"},
                {id:2,value:"在第N周"},
                {id:3,value:"在N周范围"}
            ];
            $scope.optionMonth = [
                {id:1,value:"每N月"},
                {id:2,value:"在第N月"},
                {id:3,value:"在N月范围"}
            ];


            $scope.optionMinuteRangeBegin = [];
            $scope.optionMinuteRangeEnd = [];

            $scope.optionHourRangeBegin = [];
            $scope.optionHourRangeEnd = [];

            $scope.optionDayRangeBegin = [];
            $scope.optionDayRangeEnd = [];

            $scope.optionWeekRangeBegin = [];
            $scope.optionWeekRangeEnd = [];

            $scope.optionMonthRangeBegin = [];
            $scope.optionMonthRangeEnd = [];

            for(i = 0;i < 60; i++){
                var newObject = {id:i,value:i+"分钟"};
                $scope.optionMinuteRangeBegin.push(newObject);
                $scope.optionMinuteRangeEnd.push(newObject);
            }

            for(i = 1;i < 25; i++){
                var newObject = {id:i,value:i+"小时"};
                $scope.optionHourRangeBegin.push(newObject);
                $scope.optionHourRangeEnd.push(newObject);
            }

            for(i = 1;i < 31; i++){
                var newObject = {id:i,value:i+"周"};
                $scope.optionWeekRangeBegin.push(newObject);
                $scope.optionWeekRangeEnd.push(newObject);
            }

            for(i = 1;i < 32; i++){
                var newObject = {id:i,value:i+"天"};
                $scope.optionDayRangeBegin.push(newObject);
                $scope.optionDayRangeEnd.push(newObject);
            }

            for(i = 1;i < 13; i++){
                var newObject = {id:i,value:i+"月"};
                $scope.optionMonthRangeBegin.push(newObject);
                $scope.optionMonthRangeEnd.push(newObject);
            }


            $scope.hideMinuteRange = $scope.scheduleForm.minute.type == 3?true:false;
            $scope.hideHourRange = $scope.scheduleForm.hour.type == 3?true:false;
            $scope.hideDayRange = $scope.scheduleForm.day.type == 3?true:false;
            $scope.hideWeekRange = $scope.scheduleForm.week.type == 3?true:false;
            $scope.hideMonthRange = $scope.scheduleForm.month.type == 3?true:false;

            $scope.optionMinuteChange = function(item){
                if($scope.scheduleForm.minute.type == 3){
                    $scope.hideMinuteRange = true;
                }else{
                    $scope.hideMinuteRange = false;
                }
            };

            $scope.optionHourChange = function(item){
                if($scope.scheduleForm.hour.type == 3){
                    $scope.hideHourRange = true;
                }else{
                    $scope.hideHourRange = false;
                }
            };

            $scope.optionDayChange = function(item){
                if($scope.scheduleForm.day.type == 3){
                    $scope.hideDayRange = true;
                }else{
                    $scope.hideDayRange = false;
                }
            };
            $scope.optionWeekChange = function(item){
                if($scope.scheduleForm.week.type == 3){
                    $scope.hideWeekRange = true;
                }else{
                    $scope.hideWeekRange = false;
                }
            };
            $scope.optionMonthChange = function(item){
                if($scope.scheduleForm.month.type == 3){
                    $scope.hideMonthRange = true;
                }else{
                    $scope.hideMonthRange = false;
                }
            };
        }]
)