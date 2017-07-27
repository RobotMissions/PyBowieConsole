angular.module('bowie', ['ngMaterial'])
.config(function($mdThemingProvider) {
  $mdThemingProvider.theme('default')
    .primaryPalette('blue')
    .accentPalette('orange');
})
.factory('ActionService', ['$http', '$interpolate', function($http, $interpolate) {
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
             }).then( function(response) {
                console.log(response);
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
.controller('bowieCtl', ['$scope', 'ActionService', function($scope, ActionService) {
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
}])
;
