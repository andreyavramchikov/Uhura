"use strict";


var app = angular.module('PublicationShop');


app.service('PublicationsService', function ($http) {

    this.getAllPublications = function(){
        return $http.get('/api/publications/')
    };
});