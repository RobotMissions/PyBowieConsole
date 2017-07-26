
module.exports = function(grunt) {

  // Project configuration.
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),
        bowercopy: {
            options: {
                // Bower components folder will be removed afterwards
                clean: true
            },
            angular: {
                options: {
                    destPrefix: 'pybowieconsole/js'
                },
                files: {
                    'angular.js': 'angular/angular.js',
                    'angular.min.js': 'angular/angular.min.js'
                }
            },
        },
        jshint: {
            options: {
                reporter: require('jshint-stylish')
            },
            all: [
                'Gruntfile.js',
                'pybowieconsole/js/*.js'
            ]
        },
        clean: {
            backup: ["eucaconsole.backup"],
            minified: ["eucaconsole/static/js/minified"]
        },
        watch: {
            scripts: {
                files: ['eucaconsole/static/js/**/*.js'],
                tasks: ['karma:ci', 'jshint'],
                options: {
                    spawn: false
                }
            },
            sass: {
                files: ['eucaconsole/static/sass/**/*.scss'],
                tasks: ['compass'],
                options: {
                    spawn: false
                }
            }
        }
    });

    // Load the plugins
    grunt.loadNpmTasks('grunt-contrib-clean');
    grunt.loadNpmTasks('grunt-contrib-jshint');
    grunt.loadNpmTasks('grunt-contrib-watch');

    // Default task(s).
    grunt.registerTask('default', ['watch']);
};
