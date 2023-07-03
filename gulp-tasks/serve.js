"use strict";

import { paths } from "../gulpfile.babel";
import gulp from "gulp";
import browsersync from "browser-sync";

gulp.task("serve", () => {
  browsersync.init({
    notify: false,
    port: 3000,
    proxy: '127.0.0.1:8000'
  });

  gulp.watch(paths.views.watch, gulp.parallel("views"));

  gulp.watch(paths.global_views.watch, gulp.parallel("global_views"));

  gulp.watch(paths.global_scripts.watch, gulp.parallel("global_scripts"));

  gulp.watch(paths.global_mb_views.watch, gulp.parallel("global_mb_views"));
  gulp.watch(paths.global_mb_scripts.watch, gulp.parallel("global_mb_scripts"));

  gulp.watch(paths.styles.watch, gulp.parallel("styles"));
  gulp.watch(paths.scripts.watch, gulp.parallel("scripts"));
  gulp.watch(paths.sprites.watch, gulp.parallel("sprites"));
  gulp.watch(paths.images.watch, gulp.parallel("images"));
  gulp.watch(paths.fonts.watch, gulp.parallel("fonts"));

  gulp.watch(paths.mbviews.watch, gulp.parallel("mbviews"));
  gulp.watch(paths.mbstyles.watch, gulp.parallel("mbstyles"));
  gulp.watch(paths.mbscripts.watch, gulp.parallel("mbscripts"));
  gulp.watch(paths.mbsprites.watch, gulp.parallel("mbsprites"));
  gulp.watch(paths.mbimages.watch, gulp.parallel("mbimages"));
  gulp.watch(paths.mbfonts.watch, gulp.parallel("mbfonts"));


  gulp.watch(paths.adminviews.watch, gulp.parallel("adminviews"));
  gulp.watch(paths.adminstyles.watch, gulp.parallel("adminstyles"));
  gulp.watch(paths.adminscripts.watch, gulp.parallel("adminscripts"));
  gulp.watch(paths.adminsprites.watch, gulp.parallel("adminsprites"));
  gulp.watch(paths.adminimages.watch, gulp.parallel("adminimages"));
  gulp.watch(paths.adminfonts.watch, gulp.parallel("adminfonts"));
});