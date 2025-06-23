////////////////////////////////
// Setup
////////////////////////////////

// Gulp and package
const {src, dest, parallel, series, watch} = require('gulp');
const pjson = require('./package.json');

// Plugins
const autoprefixer = require('autoprefixer');
const browserSync = require('browser-sync').create();
const concat = require('gulp-concat');
const tildeImporter = require('node-sass-tilde-importer');
const cssnano = require('cssnano');
const imagemin = require('gulp-imagemin');
const pixrem = require('pixrem');
const plumber = require('gulp-plumber');
const postcss = require('gulp-postcss');
const reload = browserSync.reload;
const rename = require('gulp-rename');
const sass = require('gulp-sass')(require('sass'));
const spawn = require('child_process').spawn;
const uglify = require('gulp-uglify-es').default;
const npmdist = require("gulp-npm-dist");

// Relative paths function
function pathsConfig(appName) {
    this.app = `./${pjson.name}`;
    const vendorsRoot = 'node_modules';

    return {
        vendorsJs: [
            `${vendorsRoot}/@popperjs/core/dist/umd/popper.js`,
            `${vendorsRoot}/bootstrap/dist/js/bootstrap.js`,
            `${vendorsRoot}/simplebar/dist/simplebar.js`,
            `${vendorsRoot}/gumshoejs/dist/gumshoe.polyfills.js`,
            `${vendorsRoot}/apexcharts/dist/apexcharts.min.js`,
            `${vendorsRoot}/prismjs/prism.js`,
            `${vendorsRoot}/prismjs/plugins/normalize-whitespace/prism-normalize-whitespace.js`,
            `${vendorsRoot}/toastify-js/src/toastify.js`,
            `${vendorsRoot}/dragula/dist/dragula.js`,
            `${vendorsRoot}/iconify-icon/dist/iconify-icon.js`,
            `${vendorsRoot}/clipboard/dist/clipboard.min.js`,
            `${vendorsRoot}/moment/moment.js`,
            `${vendorsRoot}/flatpickr/dist/flatpickr.js`,
            `${vendorsRoot}/swiper/swiper-bundle.min.js`,
            `${vendorsRoot}/rater-js/index.js`,
            `${vendorsRoot}/sweetalert2/dist/sweetalert2.min.js`,
            `${vendorsRoot}/inputmask/dist/inputmask.min.js`,
            `${vendorsRoot}/choices.js/public/assets/scripts/choices.min.js`,
            `${vendorsRoot}/nouislider/dist/nouislider.min.js`,
            `${vendorsRoot}/multi.js/dist/multi.min.js`,
            `${vendorsRoot}/quill/dist/quill.js`,
            `${vendorsRoot}/wnumb/wNumb.min.js`,
            `${vendorsRoot}/vanilla-wizard/dist/js/wizard.min.js`,
        ],
        vendorsCSS: [
            `${vendorsRoot}/dropzone/dist/min/dropzone.min.css`,
            `${vendorsRoot}/flatpickr/dist/flatpickr.css`,
            `${vendorsRoot}/swiper/swiper-bundle.min.css`,
            `${vendorsRoot}/sweetalert2/dist/sweetalert2.min.css`,
            `${vendorsRoot}/choices.js/public/assets/styles/choices.min.css`,
            `${vendorsRoot}/nouislider/dist/nouislider.min.css`,
            `${vendorsRoot}/multi.js/dist/multi.min.css`,
            `${vendorsRoot}/quill/dist/quill.core.css`,
            `${vendorsRoot}/quill/dist/quill.bubble.css`,
            `${vendorsRoot}/quill/dist/quill.snow.css`,
        ],
        app: this.app,
        templates: `${this.app}/templates`,
        css: `${this.app}/static/css`,
        scss: `${this.app}/static/scss`,
        fonts: `${this.app}/static/fonts`,
        images: `${this.app}/static/images`,
        js: `${this.app}/static/js`,
    };
}

const paths = pathsConfig();

////////////////////////////////
// Tasks
////////////////////////////////

// Styles autoprefixing and minification
const processCss = [
    autoprefixer(), // adds vendor prefixes
    pixrem(), // add fallbacks for rem units
];

const minifyCss = [
    cssnano({preset: 'default'}), // minify result
];

function styles() {
    return src([`${paths.scss}/app.scss`, `${paths.scss}/icons.scss`])
        .pipe(
            sass({
                importer: tildeImporter,
                includePaths: [paths.scss],
            }).on('error', sass.logError),
        )
        .pipe(plumber()) // Checks for errors
        .pipe(postcss(processCss))
        .pipe(dest(paths.css))
        .pipe(rename({suffix: '.min'}))
        .pipe(postcss(minifyCss)) // Minifies the result
        .pipe(dest(paths.css));
}

// Javascript minification
function scripts() {
    return src([`${paths.js}/app.js`, `${paths.js}/config.js`, `${paths.js}/layout.js`])
        .pipe(plumber()) // Checks for errors
        .pipe(uglify()) // Minifies the js
        .pipe(rename({suffix: '.min'}))
        .pipe(dest(paths.js));
}

// Vendor Javascript minification
function vendorScripts() {
    return src(paths.vendorsJs, {sourcemaps: true})
        .pipe(concat('vendors.js'))
        .pipe(dest(paths.js))
        .pipe(plumber()) // Checks for errors
        .pipe(uglify()) // Minifies the js
        .pipe(rename({suffix: '.min'}))
        .pipe(dest(paths.js, {sourcemaps: '.'}));
}

// Vendor CSS minification
function vendorStyles() {
    return src(paths.vendorsCSS, {sourcemaps: true})
        .pipe(concat('vendors.css'))
        .pipe(plumber()) // Checks for errors
        .pipe(postcss(processCss))
        .pipe(dest(paths.css))
        .pipe(rename({suffix: '.min'}))
        .pipe(postcss(minifyCss)) // Minifies the result
        .pipe(dest(paths.css));
}

// Whole Plugins
const plugins = function () {
    const out = paths.app + "/static/vendor/";
    return src(npmdist(), {base: "./node_modules"})
        .pipe(rename(function (path) {
            path.dirname = path.dirname.replace(/\/dist/, '').replace(/\\dist/, '');
        }))
        .pipe(dest(out));
};

// Watch
function watchPaths() {
    watch(`${paths.scss}/*.scss`, styles);
    watch(`${paths.templates}/**/*.html`).on('change', reload);
    watch([`${paths.js}/*.js`, `!${paths.js}/*.min.js`], scripts).on(
        'change',
        reload,
    );
}

// Generate all assets
const build = parallel(styles, scripts, vendorScripts, vendorStyles, plugins);

// Set up dev environment
const dev = parallel(watchPaths);

exports.default = series(build, dev);
exports['build'] = build;
exports['dev'] = dev;
