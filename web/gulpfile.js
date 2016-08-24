var gulp          = require('gulp');
var browserSync   = require('browser-sync').create();
var sass          = require('gulp-sass');
var minifyCss     = require('gulp-minify-css');
var rename        = require('gulp-rename');
var twig          = require('gulp-twig');
var prettify      = require('gulp-prettify');
var concat        = require('gulp-concat');
var uglify        = require('gulp-uglify');
var data          = require('gulp-data');
var fs            = require('fs');
var path          = require('path');
var jsoncombine   = require("gulp-jsoncombine");

/**
 * Support Functions and Data
 */

/**
 * Gets data from global JSON file.
 */

function getGlobalJsonData(file) {
  return getFile('src/data/global.json');
}

/**
 * Gets data from JSON, depending on file path
 */
function getJsonData(file) {
  return getFile('src/data/' + path.basename(file.path) + '.json');
}

/**
 * Gets data from a filepath
 */
function getFile(path) {
  return JSON.parse(fs.readFileSync(path));
}

/**
 * Server, Gulp-specific Functions
 */

// Static Server + watching scss/html files
gulp.task('serve', ['preview'], function() {

  browserSync.init({
    server: "./app",
  });

  gulp.watch("src/data/global/*.json", ['global_json']);
  gulp.watch("src/scss/**/*.scss", ['sass']);
  gulp.watch("src/js/**/*.js", ['js']);
  gulp.watch(["src/html/**/*.html", "src/data/*.json"], ['html']).on('change', browserSync.reload);
});

gulp.task('preview', ['js',
  'sass',
  'html']);

// Compile sass into minified CSS & auto-inject into browsers
gulp.task('sass', function() {
  return gulp.src("src/scss/*.scss")
    .pipe(sass())
    .pipe(minifyCss({compatibility: 'ie8', keepBreaks: false}))
    .pipe(rename({suffix: '.min' }))
    .pipe(gulp.dest("app/css"))
    .pipe(browserSync.stream());
});

// Compile Twig templates to HTML
gulp.task('html', function() {
  return gulp.src('src/html/*.html')
    .pipe(data(getGlobalJsonData))
    .pipe(data(getJsonData))
    .pipe(twig())
    .pipe(prettify({indent_size: 2}))
    .pipe(gulp.dest('app'));
});

// Compile into minified JS & auto-inject into browsers
gulp.task('js', function() {
  return gulp.src("src/js/**/*.js")
    .pipe(concat('script.min.js'))
    .pipe(uglify())
    .pipe(gulp.dest("app/js"))
    .pipe(browserSync.stream());
});

// Combine all global JSON files into one.
gulp.task('global_json', function() {
  return gulp.src('src/data/global/*.json')
    .pipe(jsoncombine("global.json", function(data){
      return new Buffer(JSON.stringify(data));
    }))
    .pipe(gulp.dest('src/data'));
})

gulp.task('default', ['serve']);
