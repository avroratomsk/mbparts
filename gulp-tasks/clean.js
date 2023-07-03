"use strict";

import gulp from "gulp";
import del from "del";

gulp.task("clean", () => {
    return del([
        "./main/core/theme/default/css",
        "./main/core/theme/default/fonts",
        "./main/core/theme/default/images",
        "./main/core/theme/default/views",
        "./main/core/theme/default/js",
        "./main/core/theme/mb/css",
        "./main/core/theme/mb/fonts",
        "./main/core/theme/mb/images",
        "./main/core/theme/mb/views",
        "./main/core/theme/mb/js",
    ]);
});

gulp.task("adminclean", () => {
    return del(["./main/core/admin/*"]);
});