"use strict";

var app = angular.module('PublicationShop');

app.controller('ListItemsController', function ($scope, PublicationsService) {


    PublicationsService.getAllPublications().then(function (response) {
        $scope.products = response.data;
    });

});
