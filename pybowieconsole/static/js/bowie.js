angular.module('bowie', ['ngMaterial', 'angular-joystick'])
.config(function($mdThemingProvider) {
  $mdThemingProvider.theme('default')
    .primaryPalette('blue')
    .accentPalette('orange');
})
.factory('ActionService', ['$http', function($http) {
    $http.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
    return {
        performAction: function(action, cmd1, key1, val1, cmd2, key2, val2) {
            return $http({
                method: 'POST',
                url: 'bowieaction',
                data: {
                    action: action,
                    cmd1: cmd1,
                    key1: key1,
                    val1: val1,
                    cmd2: cmd2,
                    key2: key2,
                    val2: val2
                }
             }).then(function(response) {
                console.log(response);
             });
        }
    };
}])
.factory('SensorService', ['$http', function($http) {
    return {
        getSensorPackets: function() {
            return $http({
                method: 'GET',
                url: 'bowiesensors',
             }).then(function(response) {
                console.log(response.data.data);
                response.data.data.forEach(function(elem) {
                  var area = $('#sensors');
                  area.val(area.val() + '\n' + elem);
                });
             });
        }
    };
}])
.directive('lightswitch', [function() {
    return {
        template: '<md-switch ng-model="value" ng-click="clicked()"><ng-transclude></md-switch>',
        restrict: 'A',
        transclude: true,
        controller: ['$scope', 'ActionService', function($scope, ActionService) {
            $scope.value = false;
            $scope.clicked = function() {
                console.log("light on = "+$scope.value);
                ActionService.performAction('#', 'Q', '1', ($scope.value)?'255':'0', 'Q', '2', ($scope.value)?'255':'0');
            };
        }]
    };
}])
.controller('bowieCtl', ['$scope', '$timeout', 'ActionService', 'SensorService', function($scope, $timeout, ActionService, SensorService) {
    var sendTime = new Date().getTime();
    $scope.coords = {x: 0, y: 0};
    $scope.joystickMove = function() {
        var now = new Date().getTime();
        //if ((now - sendTime) < 100) {
        //    return;
        //}
        sendTime = now;
        console.log("stick position: "+$scope.coords.x+","+$scope.coords.y);
        // clamp values
        var x_adj = $scope.coords.x > 0? Math.min($scope.coords.x, 40) :  Math.max($scope.coords.x, -40);
        var y_adj = $scope.coords.y > 0? Math.min($scope.coords.y, 40) :  Math.max($scope.coords.y, -40);
        // scale values
        var x_adj = -(x_adj / 40.0);
        var y_adj = (y_adj / 40.0);
        console.log("adj : "+x_adj+","+y_adj);
        var l_speed = (y_adj) * 255;
        var r_speed = (y_adj) * 255;
        console.log("sd1 : "+l_speed+","+r_speed);
        l_speed = Math.max(Math.min((y_adj + x_adj) * 255, 255), -255);
        r_speed = Math.max(Math.min((y_adj + -x_adj) * 255, 255), -255);
        console.log("sd2 : "+l_speed+","+r_speed);
        var l_dir = l_speed < 0 ? '0' : '1';
        var r_dir = r_speed < 0 ? '0' : '1';
        console.log("dir : "+l_dir+","+r_dir);
        l_speed = Math.abs(l_speed);
        r_speed = Math.abs(r_speed);
        ActionService.performAction('#', 'L', l_dir, Math.abs(l_speed), 'R', r_dir, Math.abs(r_speed));
    };
    $scope.redClicked = function() {
        ActionService.performAction('#', 'P', '1', '1', 'P', '0', '0');
    };
    $scope.greenClicked = function() {
        ActionService.performAction('#', 'G', '1', '1', 'G', '0', '0');
    };
    $scope.yellowClicked = function() {
        ActionService.performAction('#', 'Y', '1', '1', 'Y', '0', '0');
    };
    $scope.blueClicked = function() {
        ActionService.performAction('#', 'B', '1', '1', 'B', '0', '0');
    };
    $scope.whiteClicked = function() {
        ActionService.performAction('#', 'W', '1', '1', 'W', '0', '0');
    };
    $scope.blackClicked = function() {
        ActionService.performAction('#', 'N', '1', '1', 'N', '0', '0');
    };
    $scope.getSensorData = function() {
        SensorService.getSensorPackets();
        $timeout(function() { $scope.getSensorData(); }, 4000);
    };
    $scope.getSensorData();
}])
;
