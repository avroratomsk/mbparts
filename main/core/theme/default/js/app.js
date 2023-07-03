
var path = window.location.pathname



$(document).ready(function() {
   

    function doSomething() {
        $(document).on('click','.glob-nav li a',function(e){
            e.preventDefault();
            console.log('!!!')
            dataLast = $(this).attr('data-last')
            url = $(this).attr('href')
        
            $(this).next('.glob-nav__child').show()
        
            if (dataLast == 'last') {
                
                window.location.href = url;
            }
        
            
        
        })
    }

    if ($(window).width() <= 992) {
        doSomething();
      }
 
    $(window).resize(function() {
      if ($(window).width() <= 992) {
        doSomething();
      }
    });
  });




$(document).on('click','.header__bottom-cat',function(e){

    e.preventDefault();
})

$(document).on('click','.toggle-menu',function(e){
    e.preventDefault();
    $(".menu-btn").toggleClass('menu-btn_active');
    $(".catalog__sidebar").toggleClass('catalog__sidebar--active');
   
   
   
})


$(document).on('click','.glob-nav__closer',function(e){
    e.preventDefault();
   
   
    $(".navbar__wrap").load(location.href + " .navbar");
   
})



$(document).on('click','.header__cat',function(e){
    e.preventDefault();
    $(".menu-btn").toggleClass('menu-btn_active');
})

$(document).on('click','.content',function(){
    
   
    $('.header__row').removeClass('header__row--active')
})

jQuery(document).ready(function ($) {
    var url = document.location.href;
    $.each($(".header__link"), function () {
        if (this.href == url) {
        $(this).addClass('header__link--active');
        }
    });
});

jQuery(document).ready(function ($) {
    var url = document.location.href;
    $.each($(".catalog__link"), function () {
        if (this.href == url) {
        $(this).addClass('catalog__link--active');
        }
    });
});

jQuery(document).ready(function ($) {
    var url = document.location.href;
    $.each($(".account__top-link"), function () {
        if (this.href == url) {
        $(this).addClass('account__top-link--active');
        }
    });
});

jQuery(document).ready(function ($) {
    var url = document.location.href;
    $.each($(".blog-list__sidebar-item"), function () {
        if (this.href == url) {
        $(this).addClass('blog-list__sidebar-item--active');
        }
    });
});



// Навигация
$(document).on('click','.header__link--drop',function(e){
    e.preventDefault();
    $('.header__dropdown').removeClass('header__dropdown--active')
    $(this).next('.header__dropdown').toggleClass('header__dropdown--active')
})
$(document).on('click','.content',function(){
    $('.header__dropdown').removeClass('header__dropdown--active')
})
$(document).on('mouseleave','.header__dropdown',function(){
    $(this).removeClass('header__dropdown--active')
})


// Поиск

$(document).on('click','.header__search',function(e){
    e.preventDefault();
    $('.search').addClass('search--active')
})
$(document).on('click','.search__closer',function(e){
    e.preventDefault();
    $('.search').removeClass('search--active')
})

// Корзина

$(document).on('click','.header__cart',function(e){
    e.preventDefault()
    $('.cart').addClass('cart--active')
})
$(document).on('click','.cart__close, .cart__closer',function(e){
    e.preventDefault()
    $('.cart').removeClass('cart--active')
})


// Добавление в корзину product-list__form
$(function() {
    $(document).on('submit','.product-list__form, .product-detail__form, .qtybutton',function(e){
      var $form = $(this);
      $.ajax({
        type: $form.attr('method'),
        url: $form.attr('action'),
        data: $form.serialize()
      }).done(function() {
        $(".cart__inner").load(location.href + " .cart__refresh");
        $(".header__cart-wrap").load(location.href + " .header__cart");
        $(".cart-detail-wrap").load(location.href + " .cart-detail-wrap__refresh");
        

        $form.children('button').removeClass('btn--primary')
        $form.children('button').addClass('btn--success')
        
        
        
        
      }).fail(function() {
        console.log('fail');
      });
      e.preventDefault();
    });
});





//   Удаление из корзины
$(document).on('click','.cart__remove, .product-remove a',function(e){
    e.preventDefault();
    var url = $(this).attr('href')
    $.get(url, function() {
        $(".cart__inner").load(location.href + " .cart__refresh");
        $(".header__cart-wrap").load(location.href + " .header__cart");
        $(".cart-detail-wrap").load(location.href + " .cart-detail-wrap__refresh");
        
    });

    count = 0
    $('.cart__item').each(function(index){
        count = index
    })
    if (count==0) {
        function remove(){
            $('.cart').removeClass('cart--active')
        }
        setTimeout(remove, 1000);
    }
});

// Купон
$(function() {
    $(document).on('submit','.cart-coupon',function(e){
      var $form = $(this);
      $.ajax({
        type: $form.attr('method'),
        url: $form.attr('action'),
        data: $form.serialize()
      }).done(function() {
        
        $(".cart-detail-wrap").load(location.href + " .cart-detail-wrap__refresh");
        

        
      }).fail(function() {
        console.log('fail');
      });
      e.preventDefault();
    });
});

// Скрол хедера
$(window).scroll(function() {
    var height = $(window).scrollTop();
    /*Если сделали скролл на 100px задаём новый класс для header*/
    
    if(height > 450){
        $('.header').addClass('header--fixed');
        $('.header__cart-wrap').addClass('header__cart-wrap--fixed');

        if(path != '/') {
            $('.content').addClass('content--top');
        }
        

        
    } else{
        

        $('.header').removeClass('header--fixed');
        $('.header__cart-wrap').removeClass('header__cart-wrap--fixed');
        if(path != '/') {
            $('.content').removeClass('content--top');
        }
       
    }
});


// jQuery(document).ready(function($) {
//     var url=document.location.href;
//     $.each($(".header__link"),function(){
//         if(this.href==url){
//             $(this).addClass('header__link--active');
//         }
//     });
// });



// Сортировка

$(document).on('click','.sort__title',function(){
    $(this).next('.sort__options').show()
    
});

$(document).on('mouseleave','.sort__options',function(){
    $('.sort__options').hide()
    
});

$(document).on('click','.sort__option',function(){
    var getUrl = $(this).attr("data-url")

    function setLocation(curLoc){
        try {
          history.pushState(null, null, curLoc);
          return;
        } catch(e) {}
        location.hash = '#' + curLoc;
    }

    setLocation(getUrl)

    function refresh(){
        $(".catalog__list").load(location.href + " .catalog__refresh");
        $(".catalog__sidebar").load(location.href + " .catalog__sidefresh");
    }
    setTimeout(refresh, 200);
});




// Фильтры
// !!! Какая то хуйня
$(document).on('keyup','.filter__input',function(){
    // $(this).val($(this).val().replace(/[A-Za-zА-Яа-яЁё]/, ''))
    var filter = $(this).attr('data-filter')
    var key = $(this).attr('data-key')
    var getUrl = $(this).attr("data-get")

    if ($(this).val() == '') {
        var hrefUrl = '?' + key + '=' + filter + getUrl
    } else {
        var hrefUrl = '?' + key + '=' + $(this).val() + getUrl
    }
    function setLocation(curLoc){
        try {
          history.pushState(null, null, curLoc);
          return;
        } catch(e) {}
        location.hash = '#' + curLoc;
    }
    
    setLocation(hrefUrl)

    function refresh(){
        $(".catalog__list").load(location.href + " .catalog__refresh");
        
        if($(this).parent().parent().next('.filter__price-item') == true ) {

            $(".ref-max").load(location.href + " .ref-max-ref");
            
        } else if ($(this).parent().parent().prev('.filter__price-item') == true ) {
            $(".ref-min").load(location.href + " .ref-min-ref");
        }

    }

    setTimeout(refresh, 200);

    $(this).focus()
    
    

});



// счетчик

function calculate() {
	let inpt = document.querySelector('.product-detail__count-inp')
	let plus = document.querySelector('.product-detail__plus')
	let minus = document.querySelector('.product-detail__minus')
	if (plus) {
		plus.addEventListener('click', function () {
			inpt.value++
		})
	}
	if (minus) {
		minus.addEventListener('click', function () {
			inpt.value--
			if (inpt.value < 2) {
				inpt.value = 1
			}
		})
	}
}
calculate()



// Замена картинки
// .product-detail__nav-image
$(document).on('click','.product-detail__nav-image',function(){
    var image = $(this).next('div').attr('data-image');
    $('.product-detail__image').attr('src', image)
    $('.product-detail__nav-image').removeClass('product-detail__nav-image--active')
    $(this).addClass('product-detail__nav-image--active')
});




// Замена опции при выборе

$(document).on('click','.product-detail__option-value',function(){
    var image = $(this).attr('data-image');
    $('.product-detail__image').attr('src', image)

    $('.product-detail__option-value').removeClass('product-detail__option-value--active')
    $(this).addClass('product-detail__option-value--active')

    var oldPrice = parseFloat($('.product-detail__price').attr('data-price'))
    var newPrice = parseFloat($(this).attr('data-price'))
    var res = oldPrice + newPrice

    // console.log(res)
    $('.product-detail__price').html(String(res)+',00₽')

    
    var newAction = $(this).attr('data-action')
    $('.product-detail__form').attr('action', newAction)
    $('.product-detail__option-value-reset').show()
    
});





// Слайдер !!! Дописать

jQuery(document).ready(function () {
    var count = 0
    var n = $( ".rewiews__item" ).length;
    var cell = Math.floor(n/2)

    // console.log(n%2)

    if(n%2 == 0) {
        
        var counter = 0
        $(".rewiews__item").each(function() {
            counter += 1
            if (counter==1) {
                console.log('!!!')

                var get_item = $(this).clone()

                $('.rewiews__grid').append(get_item)
            }

        });
    }

    $(".rewiews__item").each(function() {
        count += 1

        

        if(count <= cell ){

            $(this).addClass('rewiews__item--prev')
        }
        if(count > cell + 1 ){
            $(this).addClass('rewiews__item--next')
            
        }
        if(count == cell +1 ){
            $(this).addClass('rewiews__item--active')
        } 
    });


});


$(document).on('click','.rewiews__item--next',function(){
   
    $('.rewiews__item').removeClass('rewiews__item--active')
    $(this).addClass('rewiews__item--active')

    var count = 0
    var n = $( ".rewiews__item" ).length;
    var cell = Math.floor(n/2)

    $('.rewiews__item').removeClass('rewiews__item--prev')
    $('.rewiews__item').removeClass('rewiews__item--next')

    $(".rewiews__item").each(function() {
        count += 1
        if(count==1) {
            var html = $(this).clone()
            $('.rewiews__grid').append(html)
            $(this).remove()
        }
        
    });

    var count_w = 0
    $(".rewiews__item").each(function() {
        count_w += 1
        if(count_w <= cell ){
            $(this).addClass('rewiews__item--prev')
        }
        if(count_w > cell + 1 ){
            $(this).addClass('rewiews__item--next')
        }

        // console.log(this)
    });
    
});



$(document).on('click','.rewiews__item--prev',function(){
   
    $('.rewiews__item').removeClass('rewiews__item--active')
    $(this).addClass('rewiews__item--active')

    var count = 0
    var n = $( ".rewiews__item" ).length;
    var cell = Math.floor(n/2)

    $('.rewiews__item').removeClass('rewiews__item--prev')
    $('.rewiews__item').removeClass('rewiews__item--next')

    $(".rewiews__item").each(function() {
        count += 1
        if(count==n) {
            var html = $(this).clone()
            $('.rewiews__grid').prepend(html)
            $(this).remove()
        }
        
    });

    var count_w = 0
    $(".rewiews__item").each(function() {
        count_w += 1
        if(count_w <= cell ){
            $(this).addClass('rewiews__item--prev')
        }
        if(count_w > cell + 1 ){
            $(this).addClass('rewiews__item--next')
        }

        // console.log(this)
    });
    
});





// Новости !!! Дописать


$(document).on('click','.blog__item',function(){
    $('.blog__item').removeClass('blog__item--active')
    $(this).addClass('blog__item--active')
});






// Табы на главной
$(document).on('click','.service__tab--first',function(e){
    e.preventDefault();
    $('.service__tab').removeClass('service__tab--active')
    $(this).addClass('service__tab--active')
    
    $('.service__grid-serv').addClass('service__grid--active')
    $('.service__grid-cat').removeClass('service__grid--active')


});

$(document).on('click','.service__tab--second',function(e){
    e.preventDefault();
    $('.service__tab').removeClass('service__tab--active')
    $(this).addClass('service__tab--active')

    $('.service__grid-serv').removeClass('service__grid--active')
    $('.service__grid-cat').addClass('service__grid--active')

});

// Табы на главной


$(document).on('click','.gallery__item',function(e){
    e.preventDefault()

    $('.gallery-popup').show()
    $('.gallery-popup').css({
        'opacity':'100%',
        'z-index': '10000'
    })

});

$(document).on('click','.gallery-popup__layout, .gallery-popup__closer',function(e){
    e.preventDefault()

    $('.gallery-popup').hide()
    $('.gallery-popup').css({
        'opacity':'0',
        'z-index': '-1'
    })
});


$(document).on('click','.gallery__item--home',function(e){
    e.preventDefault()

    function getSliderSettings(){
        return {
            slidesToShow: 1,
            slidesToScroll: 1,
            arrows: false,
            fade: true,
            asNavFor: '.gallery-popup__nav'
        }
    }
    function getSliderSettingsNav(){
        return {
            slidesToShow: 6,
            slidesToScroll: 1,
            asNavFor: '.gallery-popup__inner',
            dots: false,
            // centerMode: true,
            focusOnSelect: true,
            prevArrow: '<button id="prev" type="button" class="btn btn-juliet"><img src="/core/theme/default/images/icons/prev.svg"></button>',
            nextArrow: '<button id="next" type="button" class="btn btn-juliet"><img src="/core/theme/default/images/icons/next.svg"></button>',

        }
    }
    $.ajax({
        url:'/gallery/',
        type:'GET',
        success: function(data){
            $('.gallery-popup').html($(data).find('.gallery-popup').html());

            
            $('.gallery-popup__inner').slick(getSliderSettings()); /* Initialize the slick again */
            $('.gallery-popup__nav').slick(getSliderSettingsNav()); /* Initialize the slick again */
        }
    });
});





$('.gallery-popup__inner').slick({
    slidesToShow: 1,
    slidesToScroll: 1,
    arrows: false,
    fade: true,
    asNavFor: '.gallery-popup__nav'
  });
  $('.gallery-popup__nav').slick({
    slidesToShow: 6,
    slidesToScroll: 1,
    asNavFor: '.gallery-popup__inner',
    dots: false,
    // centerMode: true,
    focusOnSelect: true,
    prevArrow: '<button id="prev" type="button" class="btn btn-juliet"><img src="/core/theme/default/images/icons/prev.svg"></button>',
    nextArrow: '<button id="next" type="button" class="btn btn-juliet"><img src="/core/theme/default/images/icons/next.svg"></button>',


    responsive: [
        {
          breakpoint: 577,
          settings: {
            slidesToShow: 4,
            slidesToScroll: 1,
            infinite: true,
            dots: true
          }
        },
        {
          breakpoint: 600,
          settings: {
            slidesToShow: 2,
            slidesToScroll: 2
          }
        },
        {
          breakpoint: 480,
          settings: {
            slidesToShow: 1,
            slidesToScroll: 1
          }
        }
        // You can unslick at a given breakpoint now by adding:
        // settings: "unslick"
        // instead of a settings object
      ]
  });





  $('.product-list--slider').slick({
    slidesToShow: 4,
    slidesToScroll: 1,
    arrows: true,
    responsive: [
        {
          breakpoint: 1199,
          settings: {
            slidesToShow: 3,
            slidesToScroll: 1,
            infinite: true,
            dots: true
          }
        },
        {
            breakpoint: 768,
            settings: {
              slidesToShow: 2,
              slidesToScroll: 1,
              infinite: true,
              dots: true
            }
        },
        {
            breakpoint: 480,
            settings: {
              slidesToShow: 1,
              slidesToScroll: 1,
              infinite: true,
              dots: true
            }
          }
      ]
    
  });





 $(document).ready(function() {
    
    var max_filter = $('#max_filter').attr('data-filter')

    var data_max = $('.data-max').attr('data-max')

    var max_link = $('#max_filter').text()
    

    var min_filter = $('#min_filter').attr('data-filter')
    var data_min = $('.data-min').attr('data-min')

    

    var min_link = $('#min_filter').text()
    

    $( ".polzunok-5" ).mouseup(function() {

        $(this).mouseleave(function(){
            var get_min = $('.polzunok-input-5-left').val()
            var get_max = $('.polzunok-input-5-right').val()
    
            var min_url = '?price_min=' + get_min
            var max_url = '&price_max=' + get_max + max_link
            var result = min_url + max_url
    
            var url = document.location.pathname + result
    
            console.log(url)

            location.href = url;

        })
        
        


    });

    var filter_max = $('#max_filter').attr('data-filter')
    
    if(data_max != max_filter) {
        max_filter = data_max
    }
    if(data_min != min_filter) {
        min_filter = data_min
    }
    $(".polzunok-5").slider({
        min: 0,
        max: filter_max,
        values: [min_filter, max_filter],
        range: true,
        animate: "fast",
        slide : function(event, ui) {    
            $(".polzunok-input-5-left").val(ui.values[ 0 ]);   
            $(".polzunok-input-5-right").val(ui.values[ 1 ]);  
        }    
    });
    $(".polzunok-input-5-left").val($(".polzunok-5").slider("values", 0));
    $(".polzunok-input-5-right").val($(".polzunok-5").slider("values", 1));
    $(".polzunok-container-5 input").change(function() {
        var input_left = $(".polzunok-input-5-left").val().replace(/[^0-9]/g, ''),    
        opt_left = $(".polzunok-5").slider("option", "min"),
        where_right = $(".polzunok-5").slider("values", 1),
        input_right = $(".polzunok-input-5-right").val().replace(/[^0-9]/g, ''),    
        opt_right = $(".polzunok-5").slider("option", "max"),
        where_left = $(".polzunok-5").slider("values", 0); 
        if (input_left > where_right) { 
            input_left = where_right; 
        }
        if (input_left < opt_left) {
            input_left = opt_left; 
        }
        if (input_left == "") {
        input_left = 0;    
        }        
        if (input_right < where_left) { 
            input_right = where_left; 
        }
        if (input_right > opt_right) {
            input_right = opt_right; 
        }
        if (input_right == "") {
        input_right = 0;    
        }    
        $(".polzunok-input-5-left").val(input_left); 
        $(".polzunok-input-5-right").val(input_right); 

        


        if (input_left != where_left) {
            $(".polzunok-5").slider("values", 0, input_left);
            
        }
        if (input_right != where_right) {
            $(".polzunok-5").slider("values", 1, input_right);
        }
    });
});

$(document).ready(function() {
    // получить текущий URL
    var url = window.location.href;
    // получить значение параметра masla_filter из URL
    var masla_filter = getParameterByName('masla_filter', url);
    // разбить строку на массив с помощью запятой
    var masla_filter_arr = masla_filter ? masla_filter.split(',') : [];
  
    // перебрать все чекбоксы и установить их состояние в зависимости от наличия их значения в массиве
    $('.maslo-filter input[type="checkbox"]').each(function() {
      if ($.inArray($(this).val(), masla_filter_arr) !== -1) {
        $(this).prop('checked', true);
      } else {
        $(this).prop('checked', false);
      }
    });
  
    // обработка события изменения состояния чекбокса
    $('.maslo-filter input[type="checkbox"]').on('change', function() {
      // получить текущий URL
      var url = window.location.href;
      // получить значение параметра masla_filter из URL
      var masla_filter = getParameterByName('masla_filter', url);
      // разбить строку на массив с помощью запятой
      var masla_filter_arr = masla_filter ? masla_filter.split(',') : [];
  
      // добавить или удалить значение чекбокса в зависимости от его состояния
      if ($(this).prop('checked')) {
        masla_filter_arr.push($(this).val());
      } else {
        var index = masla_filter_arr.indexOf($(this).val());
        if (index !== -1) {
          masla_filter_arr.splice(index, 1);
        }
      }
  
      // объединить массив в строку с помощью запятой
      var new_masla_filter = masla_filter_arr.join(',');
  
      // заменить параметр masla_filter в URL
      var new_url = replaceQueryStringParameter(url, 'masla_filter', new_masla_filter);
  
      // перенаправить на новый URL
      window.location.href = new_url;
    });
  });


$(document).ready(function() {
    // получить текущий URL
    var url = window.location.href;
    // получить значение параметра masla_filter из URL
    var masla_filter = getParameterByName('man_filter', url);
    // разбить строку на массив с помощью запятой
    var masla_filter_arr = masla_filter ? masla_filter.split(',') : [];
  
    // перебрать все чекбоксы и установить их состояние в зависимости от наличия их значения в массиве
    $('.man-filter input[type="checkbox"]').each(function() {
      if ($.inArray($(this).val(), masla_filter_arr) !== -1) {
        $(this).prop('checked', true);
      } else {
        $(this).prop('checked', false);
      }
    });
  
    // обработка события изменения состояния чекбокса
    $('.man-filter input[type="checkbox"]').on('change', function() {
      // получить текущий URL
      var url = window.location.href;
      // получить значение параметра masla_filter из URL
      var masla_filter = getParameterByName('man_filter', url);
      // разбить строку на массив с помощью запятой
      var masla_filter_arr = masla_filter ? masla_filter.split(',') : [];
  
      // добавить или удалить значение чекбокса в зависимости от его состояния
      if ($(this).prop('checked')) {
        masla_filter_arr.push($(this).val());
      } else {
        var index = masla_filter_arr.indexOf($(this).val());
        if (index !== -1) {
          masla_filter_arr.splice(index, 1);
        }
      }
  
      // объединить массив в строку с помощью запятой
      var new_masla_filter = masla_filter_arr.join(',');
  
      // заменить параметр masla_filter в URL
      var new_url = replaceQueryStringParameter(url, 'man_filter', new_masla_filter);
  
      // перенаправить на новый URL
      window.location.href = new_url;
    });
  });

$(document).ready(function() {
    // получить текущий URL
    var url = window.location.href;
    // получить значение параметра masla_filter из URL
    var masla_filter = getParameterByName('volume_filter', url);
    // разбить строку на массив с помощью запятой
    var masla_filter_arr = masla_filter ? masla_filter.split(',') : [];
  
    // перебрать все чекбоксы и установить их состояние в зависимости от наличия их значения в массиве
    $('.volume-filter input[type="checkbox"]').each(function() {
      if ($.inArray($(this).val(), masla_filter_arr) !== -1) {
        $(this).prop('checked', true);
      } else {
        $(this).prop('checked', false);
      }
    });
  
    // обработка события изменения состояния чекбокса
    $('.volume-filter input[type="checkbox"]').on('change', function() {
      // получить текущий URL
      var url = window.location.href;
      // получить значение параметра masla_filter из URL
      var masla_filter = getParameterByName('volume_filter', url);
      // разбить строку на массив с помощью запятой
      var masla_filter_arr = masla_filter ? masla_filter.split(',') : [];
  
      // добавить или удалить значение чекбокса в зависимости от его состояния
      if ($(this).prop('checked')) {
        masla_filter_arr.push($(this).val());
      } else {
        var index = masla_filter_arr.indexOf($(this).val());
        if (index !== -1) {
          masla_filter_arr.splice(index, 1);
        }
      }
  
      // объединить массив в строку с помощью запятой
      var new_masla_filter = masla_filter_arr.join(',');
  
      // заменить параметр masla_filter в URL
      var new_url = replaceQueryStringParameter(url, 'volume_filter', new_masla_filter);
  
      // перенаправить на новый URL
      window.location.href = new_url;
    });
  });
  
  // функция получения значения параметра из URL
  function getParameterByName(name, url) {
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, '\\$&');
    var regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)'),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, ' '));
  }
  
// функция замены параметра в URL
function replaceQueryStringParameter(url, key, value) {
    if (!url) url = window.location.href;
    var re = new RegExp("([?&])" + key + "=.*?(&|#|$)(.*)", "gi"),
        hash;
  
    if (re.test(url)) {
        if (typeof value !== 'undefined' && value !== null)
            return url.replace(re, '$1' + key + "=" + value + '$2$3');
        else {
            hash = url.split('#');
            url = hash[0].replace(re, '$1$3').replace(/(&|\?)$/, '');
            if (typeof hash[1] !== 'undefined' && hash[1] !== null)
                url += '#' + hash[1];
            return url;
        }
    } else {
        if (typeof value !== 'undefined' && value !== null) {
            var separator = url.indexOf('?') !== -1 ? '&' : '?';
            return url + separator + key + '=' + value;
        } else {
            return url;
        }
    }
  }
  



$(document).on('focus', '#id_telephone, #id_phone' ,function(e){
    $("#id_telephone").mask("+7 (999) 999 99-99");
    $("#id_phone").mask("+7 (999) 999 99-99");
})


$("#id_telephone, #id_phone").on("blur", function() {
    var last = $(this).val().substr( $(this).val().indexOf("-") + 1 );
    if( last.length == 3 ) {
        var move = $(this).val().substr( $(this).val().indexOf("-") - 1, 1 );
        var lastfour = move + last;
        var first = $(this).val().substr( 0, 9 );
        $(this).val( first + '-' + lastfour );
    }
});





$(document).on('click','.for-search__btn',function(e){
    e.preventDefault();

    var count = parseInt($('.header__cart-coutn').text());
    $('.header__cart-coutn').text(count + 1);


    var csrfToken = $(this).attr('data-token')
    var id = $(this).attr('data-id')
    var name = $(this).attr('data-name')
    var supplier = $(this).attr('data-supplier')
    var price = $(this).attr('data-price')
    var quantity = $(this).attr('data-quantity')
    var data = $(this).attr('data-data')
    
    data = {
        id: id, 
        name: name, 
        supplier:supplier,
        price:price,
        quantity:quantity,
        date: data,
        csrfmiddlewaretoken: csrfToken
    }

    console.log(data)
    $.post( "/cart/add_zakaz/", data)
        .done(function( ) {
        
            $(".cart__inner").load(location.href + " .cart__refresh");
        
            $(".cart__order-create-wrapper").load(location.href + " .cart__order-create-wrapper-inner");
            $(".header__cart-wrap").load(location.href + " .header__cart");
            $(".cart__deliv-method-wrap").load(location.href + " .cart__deliv-method");
            $(".cart-detail-wrap").load(location.href + " .cart-detail-wrap__refresh");

        });
    
})


$(document).on('click','.zakaz__remove',function(e){
    e.preventDefault();
    var csrfToken = $(this).attr('data-token')
    var id = $(this).attr('data-id')
  
    
    data = {
        id: id, 
        csrfmiddlewaretoken: csrfToken
    }

    console.log(data)
    $.post( "/cart/remove_zakaz/", data)
        .done(function( ) {
        
            $(".cart__inner").load(location.href + " .cart__refresh");
        
            $(".cart__order-create-wrapper").load(location.href + " .cart__order-create-wrapper-inner");
            $(".header__cart-wrap").load(location.href + " .header__cart");
            $(".cart__deliv-method-wrap").load(location.href + " .cart__deliv-method");
            $(".cart-detail-wrap").load(location.href + " .cart-detail-wrap__refresh");

        });
    
})

$(document).on('click','.zakaz__minus',function(e){
    e.preventDefault();
    var csrfToken = $(this).attr('data-token')
    var id = $(this).attr('data-id')
  
    
    data = {
        id: id, 
        csrfmiddlewaretoken: csrfToken
    }

    console.log(data)
    $.post( "/cart/minus_zakaz/", data)
        .done(function( ) {
        
            $(".cart__inner").load(location.href + " .cart__refresh");
        
            $(".cart__order-create-wrapper").load(location.href + " .cart__order-create-wrapper-inner");
            $(".header__cart-wrap").load(location.href + " .header__cart");
            $(".cart__deliv-method-wrap").load(location.href + " .cart__deliv-method");
            $(".cart-detail-wrap").load(location.href + " .cart-detail-wrap__refresh");

        });
    
})


$(document).on('click','.zakaz__plus',function(e){
    e.preventDefault();
    var csrfToken = $(this).attr('data-token')
    var id = $(this).attr('data-id')
  
    
    data = {
        id: id, 
        csrfmiddlewaretoken: csrfToken
    }

    console.log(data)
    $.post( "/cart/plus_zakaz/", data)
        .done(function( ) {
        
            $(".cart__inner").load(location.href + " .cart__refresh");
        
            $(".cart__order-create-wrapper").load(location.href + " .cart__order-create-wrapper-inner");
            $(".header__cart-wrap").load(location.href + " .header__cart");
            $(".cart__deliv-method-wrap").load(location.href + " .cart__deliv-method");
            $(".cart-detail-wrap").load(location.href + " .cart-detail-wrap__refresh");

        });
    
})

$(document).ready(function() {
    var sortedPrice = false;
    var sortedDate = false;
    var sortAsc = true;
    
    $('#sort-btn-price').click(function() {
      sortedDate = false;
      $(this).toggleClass('active');
      var items = $('.for-search__item').toArray();
      items.sort(function(a, b) {
        var priceA = parseFloat($(a).find('.for-search__price').text().replace('₽', ''));
        var priceB = parseFloat($(b).find('.for-search__price').text().replace('₽', ''));
        return sortAsc ? priceA - priceB : priceB - priceA;
      });
      if (!sortedPrice) {
        $('.for-search__item').remove();
        $('.for-search').append(items);
        sortedPrice = true;
      } else {
        $('.for-search__item').remove();
        $('.for-search').append(items.reverse());
        sortAsc = !sortAsc;
      }
    });
    
    $('#sort-btn-date').click(function() {
      sortedPrice = false;
      $(this).toggleClass('active');
      var items = $('.for-search__item').toArray();
      items.sort(function(a, b) {
        var dateA = parseInt($(a).find('.for-search__data').text());
        var dateB = parseInt($(b).find('.for-search__data').text());
        return sortAsc ? dateA - dateB : dateB - dateA;
      });
      if (!sortedDate) {
        $('.for-search__item').remove();
        $('.for-search').append(items);
        sortedDate = true;
      } else {
        $('.for-search__item').remove();
        $('.for-search').append(items.reverse());
        sortAsc = !sortAsc;
      }
    });
  });
  
  