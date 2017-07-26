angular.module('bowie', [])
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
        template: '<input type="checkbox" ng-model="value", ng-click="clicked()"/>',
        restrict: 'A',
        controller: ['$scope', 'ActionService', function($scope, ActionService) {
            $scope.value = false;
            $scope.clicked = function() {
                console.log("light on = "+$scope.value);
                ActionService.performAction('#', 'Q', '1', ($scope.value)?'255':'0', 'Q', '2', ($scope.value)?'255':'0');
            };
        }]
    };
}])
;
