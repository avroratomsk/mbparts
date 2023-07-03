
var path = window.location.pathname



function loadCartData() {
  var cart_active = 'false';


  if ($('.cart').hasClass('cart--active')) {
    cart_active = 'true'
  } else {
    cart_active = 'false'
  }

  $('#cartData').load('/cart/get/ #cart_popup', function () {
    if (cart_active == 'true') {
      $(this).find('.cart').addClass('cart--active');
    }
  });
  $('#headerCart').load('/cart/get/ #cart_header', function () {
    if (cart_active == 'true') {
      $(this).find('.cart').addClass('cart--active');
    }
  });
}
loadCartData()



$(document).on('click', '.toggle-menu', function (e) {
  e.preventDefault();
  $(".menu-btn").toggleClass('menu-btn_active');
  $('.header__row').toggleClass('header__row--active')
  $('.header__dropdown').removeClass('header__dropdown--active')

})


$(document).on('click', '.header__cat', function (e) {
  e.preventDefault();
  $(".menu-btn").toggleClass('menu-btn_active');
})

$(document).on('click', '.content', function () {

  $(".menu-btn").removeClass('menu-btn_active');
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
$(document).on('click', '.header__link--drop', function (e) {
  e.preventDefault();
  $('.header__dropdown').removeClass('header__dropdown--active')
  $(this).next('.header__dropdown').toggleClass('header__dropdown--active')
})
$(document).on('click', '.content', function () {
  $('.header__dropdown').removeClass('header__dropdown--active')
})
$(document).on('mouseleave', '.header__dropdown', function () {
  $(this).removeClass('header__dropdown--active')
})


// Поиск

$(document).on('click', '.header__search', function (e) {
  e.preventDefault();
  $('.search').addClass('search--active')
})
$(document).on('click', '.search__closer', function (e) {
  e.preventDefault();
  $('.search').removeClass('search--active')
})

// Корзина

$(document).on('click', '.header__cart', function (e) {
  e.preventDefault()
  $('.cart').addClass('cart--active')
})
$(document).on('click', '.cart__close, .cart__closer', function (e) {
  e.preventDefault()
  $('.cart').removeClass('cart--active')
})


// Добавление в корзину product-list__form
$(function () {
  $(document).on('submit', '.product-list__form, .product-detail__form, .qtybutton', function (e) {
    var $form = $(this);
    $.ajax({
      type: $form.attr('method'),
      url: $form.attr('action'),
      data: $form.serialize()
    }).done(function () {
      $(".cart__inner").load(location.href + " .cart__refresh");
      $(".header__cart-wrap").load(location.href + " .header__cart");
      $(".cart-detail-wrap").load(location.href + " .cart-detail-wrap__refresh");


      $form.children('button').removeClass('btn--primary')
      $form.children('button').addClass('btn--success')
      $form.children('button').html('Добавлен')

      function explode() {

        $form.children('button').addClass('btn--primary')
        $form.children('button').removeClass('btn--success')
        $form.children('button').html('Еще')
      }
      setTimeout(explode, 1000);

      function uxplode() {
        $form.children('button').html('В корзину')
      }
      setTimeout(uxplode, 5000);

    }).fail(function () {
      console.log('fail');
    });
    e.preventDefault();
  });
});





//   Удаление из корзины
$(document).on('click', '.cart__remove, .product-remove a', function (e) {
  e.preventDefault();
  var url = $(this).attr('href')
  $.get(url, function () {
    $(".cart__inner").load(location.href + " .cart__refresh");
    $(".header__cart-wrap").load(location.href + " .header__cart");
    $(".cart-detail-wrap").load(location.href + " .cart-detail-wrap__refresh");

  });

  count = 0
  $('.cart__item').each(function (index) {
    count = index
  })
  if (count == 0) {
    function remove() {
      $('.cart').removeClass('cart--active')
    }
    setTimeout(remove, 1000);
  }
});

// Купон
$(function () {
  $(document).on('submit', '.cart-coupon', function (e) {
    var $form = $(this);
    $.ajax({
      type: $form.attr('method'),
      url: $form.attr('action'),
      data: $form.serialize()
    }).done(function () {

      $(".cart-detail-wrap").load(location.href + " .cart-detail-wrap__refresh");



    }).fail(function () {
      console.log('fail');
    });
    e.preventDefault();
  });
});

// Скрол хедера
$(window).scroll(function () {
  var height = $(window).scrollTop();
  /*Если сделали скролл на 100px задаём новый класс для header*/

  if (height > 450) {
    $('.header').addClass('header--fixed');

    if (path != '/') {
      $('.content').addClass('content--top');
    }



  } else {


    $('.header').removeClass('header--fixed');
    if (path != '/') {
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

$(document).on('click', '.sort__title', function () {
  $(this).next('.sort__options').show()

});

$(document).on('mouseleave', '.sort__options', function () {
  $('.sort__options').hide()

});

$(document).on('click', '.sort__option', function () {
  var getUrl = $(this).attr("data-url")

  function setLocation(curLoc) {
    try {
      history.pushState(null, null, curLoc);
      return;
    } catch (e) { }
    location.hash = '#' + curLoc;
  }

  setLocation(getUrl)

  function refresh() {
    $(".catalog__list").load(location.href + " .catalog__refresh");
    $(".catalog__sidebar").load(location.href + " .catalog__sidefresh");
  }
  setTimeout(refresh, 200);
});




// Фильтры
// !!! Какая то хуйня
$(document).on('keyup', '.filter__input', function () {
  // $(this).val($(this).val().replace(/[A-Za-zА-Яа-яЁё]/, ''))
  var filter = $(this).attr('data-filter')
  var key = $(this).attr('data-key')
  var getUrl = $(this).attr("data-get")

  if ($(this).val() == '') {
    var hrefUrl = '?' + key + '=' + filter + getUrl
  } else {
    var hrefUrl = '?' + key + '=' + $(this).val() + getUrl
  }
  function setLocation(curLoc) {
    try {
      history.pushState(null, null, curLoc);
      return;
    } catch (e) { }
    location.hash = '#' + curLoc;
  }

  setLocation(hrefUrl)

  function refresh() {
    $(".catalog__list").load(location.href + " .catalog__refresh");

    if ($(this).parent().parent().next('.filter__price-item') == true) {

      $(".ref-max").load(location.href + " .ref-max-ref");

    } else if ($(this).parent().parent().prev('.filter__price-item') == true) {
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
$(document).on('click', '.product-detail__nav-image', function () {
  var image = $(this).next('div').attr('data-image');
  $('.product-detail__image').attr('src', image)
  $('.product-detail__nav-image').removeClass('product-detail__nav-image--active')
  $(this).addClass('product-detail__nav-image--active')
});




// Замена опции при выборе

$(document).on('click', '.product-detail__option-value', function () {
  var image = $(this).attr('data-image');
  $('.product-detail__image').attr('src', image)

  $('.product-detail__option-value').removeClass('product-detail__option-value--active')
  $(this).addClass('product-detail__option-value--active')

  var oldPrice = parseFloat($('.product-detail__price').attr('data-price'))
  var newPrice = parseFloat($(this).attr('data-price'))
  var res = oldPrice + newPrice

  // console.log(res)
  $('.product-detail__price').html(String(res) + ',00₽')


  var newAction = $(this).attr('data-action')
  $('.product-detail__form').attr('action', newAction)
  $('.product-detail__option-value-reset').show()

});





// Слайдер !!! Дописать

jQuery(document).ready(function () {
  var count = 0
  var n = $(".rewiews__item").length;
  var cell = Math.floor(n / 2)

  // console.log(n%2)

  if (n % 2 == 0) {

    var counter = 0
    $(".rewiews__item").each(function () {
      counter += 1
      if (counter == 1) {
        console.log('!!!')

        var get_item = $(this).clone()

        $('.rewiews__grid').append(get_item)
      }

    });
  }

  $(".rewiews__item").each(function () {
    count += 1



    if (count <= cell) {

      $(this).addClass('rewiews__item--prev')
    }
    if (count > cell + 1) {
      $(this).addClass('rewiews__item--next')

    }
    if (count == cell + 1) {
      $(this).addClass('rewiews__item--active')
    }
  });


});


$(document).on('click', '.rewiews__item--next', function () {

  $('.rewiews__item').removeClass('rewiews__item--active')
  $(this).addClass('rewiews__item--active')

  var count = 0
  var n = $(".rewiews__item").length;
  var cell = Math.floor(n / 2)

  $('.rewiews__item').removeClass('rewiews__item--prev')
  $('.rewiews__item').removeClass('rewiews__item--next')

  $(".rewiews__item").each(function () {
    count += 1
    if (count == 1) {
      var html = $(this).clone()
      $('.rewiews__grid').append(html)
      $(this).remove()
    }

  });

  var count_w = 0
  $(".rewiews__item").each(function () {
    count_w += 1
    if (count_w <= cell) {
      $(this).addClass('rewiews__item--prev')
    }
    if (count_w > cell + 1) {
      $(this).addClass('rewiews__item--next')
    }

    // console.log(this)
  });

});



$(document).on('click', '.rewiews__item--prev', function () {

  $('.rewiews__item').removeClass('rewiews__item--active')
  $(this).addClass('rewiews__item--active')

  var count = 0
  var n = $(".rewiews__item").length;
  var cell = Math.floor(n / 2)

  $('.rewiews__item').removeClass('rewiews__item--prev')
  $('.rewiews__item').removeClass('rewiews__item--next')

  $(".rewiews__item").each(function () {
    count += 1
    if (count == n) {
      var html = $(this).clone()
      $('.rewiews__grid').prepend(html)
      $(this).remove()
    }

  });

  var count_w = 0
  $(".rewiews__item").each(function () {
    count_w += 1
    if (count_w <= cell) {
      $(this).addClass('rewiews__item--prev')
    }
    if (count_w > cell + 1) {
      $(this).addClass('rewiews__item--next')
    }

    // console.log(this)
  });

});





// Новости !!! Дописать


$(document).on('click', '.blog__item', function () {
  $('.blog__item').removeClass('blog__item--active')
  $(this).addClass('blog__item--active')
});






// Табы на главной
$(document).on('click', '.service__tab--first', function (e) {
  e.preventDefault();
  $('.service__tab').removeClass('service__tab--active')
  $(this).addClass('service__tab--active')

  $('.service__grid-serv').addClass('service__grid--active')
  $('.service__grid-cat').removeClass('service__grid--active')


});

$(document).on('click', '.service__tab--second', function (e) {
  e.preventDefault();
  $('.service__tab').removeClass('service__tab--active')
  $(this).addClass('service__tab--active')

  $('.service__grid-serv').removeClass('service__grid--active')
  $('.service__grid-cat').addClass('service__grid--active')

});

// Табы на главной


$(document).on('click', '.gallery__item', function (e) {
  e.preventDefault()

  $('.gallery-popup').show()
  $('.gallery-popup').css({
    'opacity': '100%',
    'z-index': '10000'
  })

});

$(document).on('click', '.gallery-popup__layout, .gallery-popup__closer', function (e) {
  e.preventDefault()

  $('.gallery-popup').hide()
  $('.gallery-popup').css({
    'opacity': '0',
    'z-index': '-1'
  })
});


$(document).on('click', '.gallery__item--home', function (e) {
  e.preventDefault()

  function getSliderSettings() {
    return {
      slidesToShow: 1,
      slidesToScroll: 1,
      arrows: false,
      fade: true,
      asNavFor: '.gallery-popup__nav'
    }
  }
  function getSliderSettingsNav() {
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
    url: '/gallery/',
    type: 'GET',
    success: function (data) {
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






$(document).on('click', '.for-search__btn', function (e) {
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
    supplier: supplier,
    price: price,
    quantity: quantity,
    date: data,
    csrfmiddlewaretoken: csrfToken
  }

  console.log(data)
  $.post("/cart/add_zakaz/", data)
    .done(function () {

      loadCartData();
      $(".cart-detail-wrap").load(location.href + " .cart-detail-wrap__refresh");

    });

})


$(document).on('click', '.zakaz__remove', function (e) {
  e.preventDefault();
  var csrfToken = $(this).attr('data-token')
  var id = $(this).attr('data-id')


  data = {
    id: id,
    csrfmiddlewaretoken: csrfToken
  }

  console.log(data)
  $.post("/cart/remove_zakaz/", data)
    .done(function () {

      loadCartData();
      $(".cart-detail-wrap").load(location.href + " .cart-detail-wrap__refresh");

    });

})

$(document).on('click', '.zakaz__minus', function (e) {
  e.preventDefault();
  var csrfToken = $(this).attr('data-token')
  var id = $(this).attr('data-id')


  data = {
    id: id,
    csrfmiddlewaretoken: csrfToken
  }

  console.log(data)
  $.post("/cart/minus_zakaz/", data)
    .done(function () {

      loadCartData();
      $(".cart-detail-wrap").load(location.href + " .cart-detail-wrap__refresh");

    });

})


$(document).on('click', '.zakaz__plus', function (e) {
  e.preventDefault();
  var csrfToken = $(this).attr('data-token')
  var id = $(this).attr('data-id')


  data = {
    id: id,
    csrfmiddlewaretoken: csrfToken
  }

  console.log(data)
  $.post("/cart/plus_zakaz/", data)
    .done(function () {

      loadCartData();
      $(".cart-detail-wrap").load(location.href + " .cart-detail-wrap__refresh");

    });

})





// .header__contacts-btn
$(document).on('click', '.show-popup', function (e) {
  e.preventDefault();
  $(".popup").toggleClass('popup--active');
})
$(document).on('click', '.popup__overlay, .popup__closer', function (e) {
  e.preventDefault();
  $(".popup").removeClass('popup--active');
})


function addFilter() {
  $(document).ready(function () {
    $('#brands').html('');
    // Создаем массив всех представленных брендов
    var brands = [];
    $('.brand-name').each(function () {
      var brand = $(this).text();
      if ($.inArray(brand, brands) === -1) {
        brands.push(brand);
      }
    });
    // Создаем чекбоксы для каждого бренда
    $.each(brands, function (index, value) {
      var checkbox = $('<input/>', {
        type: 'checkbox',
        value: value,
        click: function () {
          // При клике на чекбокс показываем/скрываем соответствующие бренды
          var selectedBrands = [];
          $('input:checked').each(function () {
            selectedBrands.push($(this).val());
          });

          if (selectedBrands.length > 0) {
            $('.for-search__item').hide();
            $.each(selectedBrands, function (index, brand) {
              $('.for-search__brand:contains("' + brand + '")').closest('.for-search__item').show();
            });
          } else {
            $('.for-search__item').show();
          }
        }
      });
      var label = $('<label/>', {
        text: value
      }).prepend(checkbox);

      $('#brands').append(label);
    });
    // Сортировка по цене
    $('#sort-price').click(function () {
      var items = $('.for-search__item').get();
      var sortDirection = $(this).data('sort-direction');
      $(this).toggleClass('active');
      items.sort(function (a, b) {
        var priceA = parseFloat($(a).find('.for-search__price').text());
        var priceB = parseFloat($(b).find('.for-search__price').text());

        if (sortDirection === 'asc') {
          return priceA - priceB;
        } else {
          return priceB - priceA;
        }
      });

      $.each(items, function (index, item) {
        $('#result').append(item);
      });

      // Переключение направления сортировки
      if (sortDirection === 'asc') {
        $(this).data('sort-direction', 'desc');
      } else {
        $(this).data('sort-direction', 'asc');
      }
    });
  });
}


$(document).on('click', '.open-filter, .filter__close', function (e) {
  e.preventDefault();
  $("#filter").toggleClass('active');

})




$(document).ready(function () {
  var query = $("#query").text(); // Получаем значение из элемента с id "query"
  var csrf = $("#query").attr('data-token');
  // Отправляем GET запрос на /cart/get/
  $.ajax({
    url: '/search_rossko/',
    type: 'GET',
    data: {
      q: query,
      csrfmiddlewaretoken: csrf
    },
    beforeSend: function () {
      // Перед отправкой запроса добавляем анимированный элемент загрузки
      $(".load").html('<div class="loader"></div>');
    },
    success: function (response) {
      var data = response


      $.each(data, function (index, item) {
        if (item.price != 0 && item.date != 0 && item.name != '' && item.name != null && item.name != 'null') {
          var html = `
                        <div class="for-search__item">
                            <div class="for-search__brand"><p class="for-search__hidden">Бренд: </p> <p class="brand-name">${item.brand}</p></div>
                            <div class="for-search__id" data-id="${item.id}"><p class="for-search__hidden">Артикул: </p> <p>${item.id}</p></div>
                            <div class="for-search__name"><p class="for-search__hidden">Наименование: </p> <p>${item.name}</p></div>
                            <div class="for-search__data"><p class="for-search__hidden">Срок поставки: </p> <p>${item.date}</p></div>
                            <div class="for-search__price">${item.price.toFixed(2)}₽</div>
                            <div class="for-search__cart">
                                <div class="for-search__btn"
                                    data-supplier="${item.supplier}"
                                    data-token="${csrf}"
                                    data-name="${item.name}"
                                    data-price="${item.price.toFixed(2)}"
                                    data-quantity="1"
                                    data-id="${item.id}"
                                    data-data="${item.date}">
                                    <svg width="26" height="26" viewBox="0 0 26 26" fill="none" xmlns="http://www.w3.org/2000/svg">
                                        <path fill-rule="evenodd" clip-rule="evenodd" d="M0.25 1.75C0.25 1.05964 0.809644 0.5 1.5 0.5H2.45492C3.87531 0.5 5.1738 1.30251 5.80902 2.57295L6.02254 3H22.1335C24.5325 3 26.3146 5.22156 25.7942 7.56349L24.4053 13.8135C24.024 15.5293 22.5022 16.75 20.7446 16.75H9.75543C7.99781 16.75 6.47601 15.5293 6.09473 13.8135L4.06315 4.67138L3.57295 3.69098C3.36121 3.2675 2.92838 3 2.45492 3H1.5C0.809644 3 0.25 2.44036 0.25 1.75ZM6.80827 5.5L8.5352 13.2712C8.66229 13.8431 9.16956 14.25 9.75543 14.25H20.7446C21.3304 14.25 21.8377 13.8431 21.9648 13.2712L23.3537 7.02116C23.5272 6.24052 22.9331 5.5 22.1335 5.5H6.80827ZM10.25 20.5C9.55964 20.5 9 21.0596 9 21.75C9 22.4404 9.55964 23 10.25 23C10.9404 23 11.5 22.4404 11.5 21.75C11.5 21.0596 10.9404 20.5 10.25 20.5ZM6.5 21.75C6.5 19.6789 8.17893 18 10.25 18C12.3211 18 14 19.6789 14 21.75C14 23.8211 12.3211 25.5 10.25 25.5C8.17893 25.5 6.5 23.8211 6.5 21.75ZM20.25 20.5C19.5596 20.5 19 21.0596 19 21.75C19 22.4404 19.5596 23 20.25 23C20.9404 23 21.5 22.4404 21.5 21.75C21.5 21.0596 20.9404 20.5 20.25 20.5ZM16.5 21.75C16.5 19.6789 18.1789 18 20.25 18C22.3211 18 24 19.6789 24 21.75C24 23.8211 22.3211 25.5 20.25 25.5C18.1789 25.5 16.5 23.8211 16.5 21.75Z" fill="black"></path>
                                    </svg>
                                </div>
                            </div>
                        </div>
                    `;

          $('#result').append(html);
        }
      });

    },
    error: function (xhr, status, error) {
      $("#result").html("Ошибка при выполнении запроса");
    },
    complete: function () {
      // По завершении запроса удаляем анимированный элемент загрузки
      $(".load").empty();
      addFilter();
      $('#result').attr('data-rossko', 'true');
    }
  });
});

var codeExecuted = false;
/*
$(window).scroll(function () {
  var windowHeight = $(window).height();
  var scrollTop = $(window).scrollTop();
  var elementOffset = $('#result').offset().top;
  var elementHeight = $('#result').outerHeight();
  var rossko = $('#result').attr('data-rossko');
  var distance = elementOffset - scrollTop;
  var bottomOffset = windowHeight - distance - elementHeight;

  if (bottomOffset >= 0 && !codeExecuted && rossko == 'true') {
    var query = $("#query").text(); // Получаем значение из элемента с id "query"
    var csrf = $("#query").attr('data-token');
    // Отправляем GET запрос на /cart/get/
    $.ajax({
      url: '/search_shate_m/',
      type: 'GET',
      data: {
        q: query,
        csrfmiddlewaretoken: csrf
      },
      beforeSend: function () {
        // Перед отправкой запроса добавляем анимированный элемент загрузки
        $(".load-shate").html('<div class="loader"></div>');
      },
      success: function (response) {
        var data = response


        $.each(data, function (index, item) {
          if (item.price != 0 && item.date != 0 && item.name != '' && item.name != null && item.name != 'null') {
            var html = `
                        <div class="for-search__item">
                            <div class="for-search__brand"><p class="for-search__hidden">Бренд: </p> <p class="brand-name">${item.brand}</p></div>
                            <div class="for-search__id"><p class="for-search__hidden">Артикул: </p> <p>${item.id}</p></div>
                            <div class="for-search__name"><p class="for-search__hidden">Наименование: </p> <p>${item.name}</p></div>
                            <div class="for-search__data"><p class="for-search__hidden">Срок поставки: </p> <p>${item.date}</p></div>
                            <div class="for-search__price">${item.price.toFixed(2)}₽</div>
                            <div class="for-search__cart">
                                <div class="for-search__btn"
                                    data-supplier="${item.supplier}"
                                    data-token="${csrf}"
                                    data-name="${item.name}"
                                    data-price="${item.price.toFixed(2)}"
                                    data-quantity="1"
                                    data-id="${item.id}"
                                    data-data="${item.date}">
                                    <svg width="26" height="26" viewBox="0 0 26 26" fill="none" xmlns="http://www.w3.org/2000/svg">
                                        <path fill-rule="evenodd" clip-rule="evenodd" d="M0.25 1.75C0.25 1.05964 0.809644 0.5 1.5 0.5H2.45492C3.87531 0.5 5.1738 1.30251 5.80902 2.57295L6.02254 3H22.1335C24.5325 3 26.3146 5.22156 25.7942 7.56349L24.4053 13.8135C24.024 15.5293 22.5022 16.75 20.7446 16.75H9.75543C7.99781 16.75 6.47601 15.5293 6.09473 13.8135L4.06315 4.67138L3.57295 3.69098C3.36121 3.2675 2.92838 3 2.45492 3H1.5C0.809644 3 0.25 2.44036 0.25 1.75ZM6.80827 5.5L8.5352 13.2712C8.66229 13.8431 9.16956 14.25 9.75543 14.25H20.7446C21.3304 14.25 21.8377 13.8431 21.9648 13.2712L23.3537 7.02116C23.5272 6.24052 22.9331 5.5 22.1335 5.5H6.80827ZM10.25 20.5C9.55964 20.5 9 21.0596 9 21.75C9 22.4404 9.55964 23 10.25 23C10.9404 23 11.5 22.4404 11.5 21.75C11.5 21.0596 10.9404 20.5 10.25 20.5ZM6.5 21.75C6.5 19.6789 8.17893 18 10.25 18C12.3211 18 14 19.6789 14 21.75C14 23.8211 12.3211 25.5 10.25 25.5C8.17893 25.5 6.5 23.8211 6.5 21.75ZM20.25 20.5C19.5596 20.5 19 21.0596 19 21.75C19 22.4404 19.5596 23 20.25 23C20.9404 23 21.5 22.4404 21.5 21.75C21.5 21.0596 20.9404 20.5 20.25 20.5ZM16.5 21.75C16.5 19.6789 18.1789 18 20.25 18C22.3211 18 24 19.6789 24 21.75C24 23.8211 22.3211 25.5 20.25 25.5C18.1789 25.5 16.5 23.8211 16.5 21.75Z" fill="black"></path>
                                    </svg>
                                </div>
                            </div>
                        </div>
                    `;

            $('#result').append(html);
          }
        });

        addFilter();
      },
      error: function (xhr, status, error) {
        // $("#result").append("Ошибка при выполнении запроса");
      },
      complete: function () {
        // По завершении запроса удаляем анимированный элемент загрузки
        $(".load-shate").empty();
        $('#result').attr('data-shate', 'true');
      }
    });

    // Устанавливаем флаг, чтобы код больше не выполнялся
    codeExecuted = true;
  }
});



var codeExecuted2 = false;

$(window).scroll(function () {
  var windowHeight = $(window).height();
  var scrollTop = $(window).scrollTop();
  var elementOffset = $('#result').offset().top;
  var elementHeight = $('#result').outerHeight();
  var rossko = $('#result').attr('data-shate');
  var distance = elementOffset - scrollTop;
  var bottomOffset = windowHeight - distance - elementHeight;

  if (bottomOffset >= 0 && !codeExecuted2 && rossko == 'true') {

    var query = $("#query").text();
    console.log(query)
    var csrf = $("#query").attr('data-token');
    // Отправляем GET запрос на /cart/get/
    $.ajax({
      url: '/search_favorit/',
      type: 'GET',
      data: {
        q: query,
        csrfmiddlewaretoken: csrf
      },
      beforeSend: function () {
        // Перед отправкой запроса добавляем анимированный элемент загрузки
        $(".load-favorit").html('<div class="loader"></div>');
      },
      success: function (response) {
        var data = response


        $.each(data, function (index, item) {
          if (item.price != 0 && item.date != 0 && item.name != '' && item.name != null && item.name != 'null') {
            var html = `
                        <div class="for-search__item">
                            <div class="for-search__brand"><p class="for-search__hidden">Бренд: </p> <p class="brand-name">${item.brand}</p></div>
                            <div class="for-search__id"><p class="for-search__hidden">Артикул: </p> <p>${item.id}</p></div>
                            <div class="for-search__name"><p class="for-search__hidden">Наименование: </p> <p>${item.name}</p></div>
                            <div class="for-search__data"><p class="for-search__hidden">Срок поставки: </p> <p>${item.date}</p></div>
                            <div class="for-search__price">${item.price.toFixed(2)}₽</div>
                            <div class="for-search__cart">
                                <div class="for-search__btn"
                                    data-supplier="${item.supplier}"
                                    data-token="${csrf}"
                                    data-name="${item.name}"
                                    data-price="${item.price.toFixed(2)}"
                                    data-quantity="1"
                                    data-id="${item.id}"
                                    data-data="${item.date}">
                                    <svg width="26" height="26" viewBox="0 0 26 26" fill="none" xmlns="http://www.w3.org/2000/svg">
                                        <path fill-rule="evenodd" clip-rule="evenodd" d="M0.25 1.75C0.25 1.05964 0.809644 0.5 1.5 0.5H2.45492C3.87531 0.5 5.1738 1.30251 5.80902 2.57295L6.02254 3H22.1335C24.5325 3 26.3146 5.22156 25.7942 7.56349L24.4053 13.8135C24.024 15.5293 22.5022 16.75 20.7446 16.75H9.75543C7.99781 16.75 6.47601 15.5293 6.09473 13.8135L4.06315 4.67138L3.57295 3.69098C3.36121 3.2675 2.92838 3 2.45492 3H1.5C0.809644 3 0.25 2.44036 0.25 1.75ZM6.80827 5.5L8.5352 13.2712C8.66229 13.8431 9.16956 14.25 9.75543 14.25H20.7446C21.3304 14.25 21.8377 13.8431 21.9648 13.2712L23.3537 7.02116C23.5272 6.24052 22.9331 5.5 22.1335 5.5H6.80827ZM10.25 20.5C9.55964 20.5 9 21.0596 9 21.75C9 22.4404 9.55964 23 10.25 23C10.9404 23 11.5 22.4404 11.5 21.75C11.5 21.0596 10.9404 20.5 10.25 20.5ZM6.5 21.75C6.5 19.6789 8.17893 18 10.25 18C12.3211 18 14 19.6789 14 21.75C14 23.8211 12.3211 25.5 10.25 25.5C8.17893 25.5 6.5 23.8211 6.5 21.75ZM20.25 20.5C19.5596 20.5 19 21.0596 19 21.75C19 22.4404 19.5596 23 20.25 23C20.9404 23 21.5 22.4404 21.5 21.75C21.5 21.0596 20.9404 20.5 20.25 20.5ZM16.5 21.75C16.5 19.6789 18.1789 18 20.25 18C22.3211 18 24 19.6789 24 21.75C24 23.8211 22.3211 25.5 20.25 25.5C18.1789 25.5 16.5 23.8211 16.5 21.75Z" fill="black"></path>
                                    </svg>
                                </div>
                            </div>
                        </div>
                    `;

            $('#result').append(html);
          }
        });

        addFilter();
      },
      error: function (xhr, status, error) {
        // $("#result").append("Ошибка при выполнении запроса");
      },
      complete: function () {
        // По завершении запроса удаляем анимированный элемент загрузки
        $(".load-favorit").empty();
        $('#result').attr('data-favorit', 'true');
      }
    });

    // Устанавливаем флаг, чтобы код больше не выполнялся
    codeExecuted2 = true;
  }
});

*/
$(document).on('focus', '#id_telephone, #id_phone', function (e) {
  $("#id_telephone").mask("+7 (999) 999 99-99");
  $("#id_phone").mask("+7 (999) 999 99-99");
})


$("#id_telephone, #id_phone").on("blur", function () {
  var last = $(this).val().substr($(this).val().indexOf("-") + 1);
  if (last.length == 3) {
    var move = $(this).val().substr($(this).val().indexOf("-") - 1, 1);
    var lastfour = move + last;
    var first = $(this).val().substr(0, 9);
    $(this).val(first + '-' + lastfour);
  }
});
