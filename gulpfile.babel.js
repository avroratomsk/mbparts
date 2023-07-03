"use strict";

import gulp from "gulp";

const requireDir = require("require-dir"),
  paths = {
    views: {
      src: [
        "./#src/templates/theme/mb/**/*.html",
        "./#src/templates/theme/mb/pages/*.html"
      ],
      dist: "./main/core/theme/mb/views/",
      watch: [
        "./#src/templates/theme/mb/**/*.html",
        "./#src/templates/theme/mb/pages/*.html"
      ]
    },

    styles: {
      src: "./#src/scss/theme/default/style.{scss,sass}",
      dist: "./main/core/theme/default/css/",
      watch: [
        "./#src/scss/theme/default/**/*.{scss,sass}",
        "./#src/scss/theme/global/**/*.{scss,sass}"
      ]
    },
    scripts: {
      src: "./#src/js/theme/default/app.js",
      dist: "./main/core/theme/default/js/",
      watch: [
        "./#src/js/theme/default/**/*.js",
        "./#src/js/theme/default/**/*.js"
      ]
    },
    images: {
      src: [
        "./#src/images/theme/default/**/*.{jpg,jpeg,png,gif,tiff,svg}",
        "!./#src/images/theme/default/fav/*.{jpg,jpeg,png,gif,tiff}"
      ],
      dist: "./main/core/theme/default/images/",
      watch: "./#src/images/theme/default/**/*.{jpg,jpeg,png,gif,svg,tiff}"
    },
    sprites: {
      src: "./#src/images/theme/default/sprites/*.svg",
      dist: "./main/core/theme/default/images/sprites/",
      watch: "./#src/images/theme/default/sprites/*.svg"
    },
    fonts: {
      src: "./#src/fonts/theme/default/**/*.{woff,woff2,ttf}",
      dist: "./main/core/theme/default/fonts/",
      watch: "./#src/fonts/theme/default/**/*.{woff,woff2,ttf}"
    },
    favicons: {
      src: "./#src/img/theme/default/fav/*.{jpg,jpeg,png,gif}",
      dist: "./main/core/img/fav/",
    },
    gzip: {
      src: "./#src/.htaccess",
      dist: "./main/core/"
    },

    // mb
    mbviews: {
      src: [
        "./#src/templates/theme/mb/**/*.html",
        "./#src/templates/theme/mb/pages/*.html"
      ],
      dist: "./main/core/theme/mb/views/",
      watch: [
        "./#src/templates/theme/mb/**/*.html",
        "./#src/templates/theme/mb/pages/*.html"
      ]
    },
    mbstyles: {
      src: "./#src/scss/theme/mb/style.{scss,sass}",
      dist: "./main/core/theme/mb/css/",
      watch: [
        "./#src/scss/theme/mb/**/*.{scss,sass}",
        "./#src/scss/theme/global/**/*.{scss,sass}"
      ]
    },
    mbscripts: {
      src: "./#src/js/theme/mb/app.js",
      dist: "./main/core/theme/mb/js/",
      watch: [
        "./#src/js/theme/mb/**/*.js",
        "./#src/js/theme/mb/**/*.js"
      ]
    },
    mbimages: {
      src: [
        "./#src/images/theme/mb/**/*.{jpg,jpeg,png,gif,tiff,svg}",
        "!./#src/images/theme/mb/fav/*.{jpg,jpeg,png,gif,tiff}"
      ],
      dist: "./main/core/theme/mb/images/",
      watch: "./#src/images/theme/mb/**/*.{jpg,jpeg,png,gif,svg,tiff}"
    },
    mbsprites: {
      src: "./#src/images/theme/mb/sprites/*.svg",
      dist: "./main/core/theme/mb/images/sprites/",
      watch: "./#src/images/theme/mb/sprites/*.svg"
    },
    mbfonts: {
      src: "./#src/fonts/theme/mb/**/*.{woff,woff2,ttf}",
      dist: "./main/core/theme/mb/fonts/",
      watch: "./#src/fonts/theme/mb/**/*.{woff,woff2,ttf}"
    },
    mbfavicons: {
      src: "./#src/img/theme/mb/fav/*.{jpg,jpeg,png,gif}",
      dist: "./main/core/img/fav/",
    },
    mbgzip: {
      src: "./#src/.htaccess",
      dist: "./main/core/"
    },


    // Global
    global_views: {
      src: [
        "./#src/templates/theme/global/**/*.html",
        "./#src/templates/theme/global/pages/*.html"
      ],
      dist: "./main/core/theme/default/views/global/",
      watch: [
        "./#src/templates/theme/global/**/*.html",
        "./#src/templates/theme/global/pages/*.html"
      ]
    },
    global_scripts: {
      src: "./#src/js/theme/global/global.js",
      dist: "./main/core/theme/default/js/",
      watch: [
        "./#src/js/theme/global/**/*.js",
        "./#src/js/theme/global/**/*.js"
      ]
    },
    global_mb_views: {
      src: [
        "./#src/templates/theme/global/**/*.html",
        "./#src/templates/theme/global/pages/*.html"
      ],
      dist: "./main/core/theme/mb/views/global/",
      watch: [
        "./#src/templates/theme/global/**/*.html",
        "./#src/templates/theme/global/pages/*.html"
      ]
    },
    global_mb_scripts: {
      src: "./#src/js/theme/global/global.js",
      dist: "./main/core/theme/mb/js/",
      watch: [
        "./#src/js/theme/global/**/*.js",
        "./#src/js/theme/global/**/*.js"
      ]
    },

    // admin
    adminviews: {
      src: [
        "./#src/templates/admin/**/*.html",
        "./#src/templates/admin/pages/*.html"
      ],
      dist: "./main/core/admin/views/",
      watch: [
        "./#src/templates/admin/**/*.html",
        "./#src/templates/admin/pages/*.html"
      ]
    },
    adminstyles: {
      src: "./#src/scss/admin/style.{scss,sass}",
      dist: "./main/core/admin/css/",
      watch: [
        "./#src/scss/admin/**/*.{scss,sass}",
        "./#src/scss/admin/**/*.{scss,sass}"
      ]
    },
    adminscripts: {
      src: "./#src/js/admin/app.js",
      dist: "./main/core/admin/js/",
      watch: [
        "./#src/js/admin/**/*.js",
        "./#src/js/admin/**/*.js"
      ]
    },
    adminimages: {
      src: [
        "./#src/images/admin/**/*.{jpg,jpeg,png,gif,tiff,svg}",
        "!./#src/images/admin/fav/*.{jpg,jpeg,png,gif,tiff}"
      ],
      dist: "./main/core/admin/images/",
      watch: "./#src/images/admin/**/*.{jpg,jpeg,png,gif,svg,tiff}"
    },
    adminsprites: {
      src: "./#src/images/admin/sprites/*.svg",
      dist: "./main/core/admin/images/sprites/",
      watch: "./#src/images/admin/sprites/*.svg"
    },
    adminfonts: {
      src: "./#src/fonts/admin/**/*.{woff,woff2,ttf}",
      dist: "./main/core/admin/fonts/",
      watch: "./#src/fonts/admin/**/*.{woff,woff2,ttf}"
    },
    adminfavicons: {
      src: "./#src/img/admin/fav/*.{jpg,jpeg,png,gif}",
      dist: "./main/core/img/fav/",
    }
  };

requireDir("./gulp-tasks/");

export { paths };

export const development = gulp.series("clean", "adminclean",
  gulp.parallel([
    "global_views",
    "global_scripts",
    "global_mb_views",
    "global_mb_scripts",
    "views",
    "styles",
    "scripts",
    "images",
    "webp",
    "sprites",
    "fonts",
    "favicons",
    "mbviews",
    "mbstyles",
    "mbscripts",
    "mbimages",
    "mbwebp",
    "mbsprites",
    "mbfonts",
    "mbfavicons",
    "adminviews",
    "adminstyles",
    "adminscripts",
    "adminimages",
    "adminwebp",
    "adminsprites",
    "adminfonts",
    "adminfavicons"

  ]),
  gulp.parallel("serve"));

export const prod = gulp.series("clean", "adminclean",
  gulp.parallel([
    "global_views",
    "global_scripts",
    "global_mb_views",
    "global_mb_scripts",
    "views",
    "styles",
    "scripts",
    "images",
    "webp",
    "sprites",
    "fonts",
    "favicons",
    "gzip",
    "mbviews",
    "mbstyles",
    "mbscripts",
    "mbimages",
    "mbwebp",
    "mbsprites",
    "mbfonts",
    "mbfavicons",
    "adminviews",
    "adminstyles",
    "adminscripts",
    "adminimages",
    "adminwebp",
    "adminsprites",
    "adminfonts",
    "adminfavicons",
  ]));

export default development;