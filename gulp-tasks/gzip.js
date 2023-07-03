"use strict";

import { paths } from "../gulpfile.babel";
import gulp from "gulp";
import debug from "gulp-debug";

gulp.task("gzip", () => {
    return gulp.src(paths.gzip.src)
        .pipe(gulp.dest(paths.gzip.dist))
        .pipe(debug({
            "title": "GZIP config"
        }));
});

gulp.task("mbgzip", () => {
    return gulp.src(paths.mbgzip.src)
        .pipe(gulp.dest(paths.mbgzip.dist))
        .pipe(debug({
            "title": "GZIP config"
        }));
});