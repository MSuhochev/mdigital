(function ($) {
    "use strict";

    /*------------------------------------------------------------------
    [Table of contents]

    1. my owl function
    2. instafeed function
    3. text parallax init
    4. email patern
    5. content center function
    6. get and set logo
    7. equal height
    8. set width
    9. custom number function
    10. scroll view function
    11. select function
    12. case portfolio grid
    13. preloader
    14. preloader close button
    15. mega navigation menu init
    16. contact form init
    17. video popup init
    18. Side Offset cart menu open
    19. right click , ctrl+u and ctrl+shift+i disabled
    20. modal popup
    21. img default behavior off and dragable false
    22. subscribe form
    23. wow function init
    24. current page add class active on a
    25. banner slider
    26. tab swipe indicator
    27. testimonial slider 1
    28. testimonial slider 2
    29. testimonial slider 3
    30. testimonial slider 4
    31. gallery slider
    32. pie chart init
    33. number counter and skill bar animation
    34. waypoint int
    35. skill bar and number counter
    36. go to current section
    37. select init
    38. custom number init
    39. floating btn
    40. product slider and about slider
    41. scrollview init
    42. rate graph
    43. case study slideer
    44. rev slider init
    45. XpeedStudio Maps
    46. submit_question
    47. subscribe_question
    48. incoming_orders
    -------------------------------------------------------------------*/

    /*==========================================================
                    1. my owl function
    ======================================================================*/
    $.fn.myOwl = function (options) {

        var settings = $.extend({
            items: 1,
            dots: false,
            loop: true,
            mouseDrag: true,
            touchDrag: true,
            nav: false,
            autoplay: false,
            navText: ['', ''],
            margin: 0,
            stagePadding: 0,
            autoplayTimeout: 3000,
            autoplayHoverPause: true,
            autoplaySpeed: 3000,
            smartSpeed: 450,
            navRewind: false,
            responsive: {},
            animateOut: '',
            animateIn: '',
            center: '',
            merge: '',
            autoWidth: '',
        }, options);

        return this.owlCarousel({
            items: settings.items,
            loop: settings.loop,
            mouseDrag: settings.mouseDrag,
            touchDrag: settings.touchDrag,
            nav: settings.nav,
            navText: settings.navText,
            dots: settings.dots,
            margin: settings.margin,
            stagePadding: settings.stagePadding,
            autoplay: settings.autoplay,
            autoplayTimeout: settings.autoplayTimeout,
            autoplayHoverPause: settings.autoplayHoverPause,
            animateOut: settings.animateOut,
            animateIn: settings.animateIn,
            responsive: settings.responsive,
            navRewind: settings.navRewind,
            center: settings.center,
            merge: settings.merge,
            autoWidth: settings.autoWidth,
            autoplaySpeed: settings.autoplaySpeed,
            smartSpeed: settings.smartSpeed
        });
    };

    /*==========================================================
                    2. instafeed function
    ======================================================================*/
    $.fn.instaFeed = function (options) {
        var settings = $.extend({
            token: '',
            $this: $(this),
            photos: 0
        }, options);

        $.ajax({
            url: 'https://api.instagram.com/v1/users/self/media/recent',
            dataType: 'jsonp',
            type: 'GET',
            data: {access_token: settings.token, count: settings.photos},
            success: function (data) {
                for (let x in data.data) {
                    settings.$this.append('<li><a href="' + data.data[x].link + '" ><img src="' + data.data[x].images.standard_resolution.url + '"></a></li>');
                }
            },
            error: function (data) {
                console.log(data);
            }
        });
    }

    /*==========================================================
                    3. text parallax init
    ======================================================================*/
    function initparallax() {
        var a = {
            Android: function () {
                return navigator.userAgent.match(/Android/i);
            },
            BlackBerry: function () {
                return navigator.userAgent.match(/BlackBerry/i);
            },
            iOS: function () {
                return navigator.userAgent.match(/iPhone|iPad|iPod/i);
            },
            Opera: function () {
                return navigator.userAgent.match(/Opera Mini/i);
            },
            Windows: function () {
                return navigator.userAgent.match(/IEMobile/i);
            },
            any: function () {
                return a.Android() || a.BlackBerry() || a.iOS() || a.Opera() || a.Windows();
            }
        };
        var trueMobile = a.any();
        if (null == trueMobile) {
            var b = new Scrollax();
            b.reload();
            b.init();
        }
    }

    /*==========================================================
                    4. email patern
    ======================================================================*/
    function email_pattern(email) {
        var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
        return regex.test(email);
    }

    /*==========================================================
                    5. content center function
    ======================================================================*/
    let contentToCenter = () => {
        let header = $('.xs-header'),
            banner = $('.content-to-center .container');
        banner.css('marginTop', (header.outerHeight()));
    }

    /*==========================================================
                    6. get and set logo
    ======================================================================*/
    function setLogo() {
        let logo = $('.xs-logo').children(),
            navLogo = $('.nav-brand'),
            clone = logo.clone();
        if ($(window).width() <= 991) {
            if (navLogo.children().length === 0) {
                clone.appendTo(navLogo);
            }
        }
    }

    /*==========================================================
                    7. equal height
    ======================================================================*/
    function equalHeight() {
        let post = $('.single-blog-post-thumb'),
            subFrom = $('.newsletter-thumb-wraper');

        if ($(window).width() >= 991) {
            subFrom.css('height', post.outerHeight())
        } else {
            subFrom.css('height', 'auto')
        }
    }

    /*==========================================================
                    8. set width
    ======================================================================*/
    function setWidth() {
        let navwraper = $('.navSidebar-wraper'),
            child = navwraper.children();

        if (child.length > 1) {
            navwraper.css('width', (child.outerWidth(true) * child.length))
        } else {
            navwraper.css('width', '')
        }
    }

    /*==========================================================
                    9. custom number function
    ======================================================================*/
    $.fn.customNumber = function (options) {
        var settings = $.extend({
            plusIcon: '',
            minusIcon: ''
        }, options);

        this.append('<span class="add">' + settings.plusIcon + '</span>');
        this.append('<span class="sub">' + settings.minusIcon + '</span>');

        return this.each(function () {
            let spinner = $(this),
                input = spinner.find('input[type="number"]'),
                add = spinner.find('.add'),
                sub = spinner.find('.sub');

            input.parent().on('click', '.sub', function (event) {
                event.preventDefault();
                if (input.val() > parseInt(input.attr('min'), 10)) {
                    input.val(function (i, oldvalue) {
                        return --oldvalue;
                    })
                }
            });
            input.parent().on('click', '.add', function (event) {
                event.preventDefault();
                if (input.val() < parseInt(input.attr('max'), 10)) {
                    input.val(function (i, oldvalue) {
                        return ++oldvalue;
                    })
                }
            });
        });
    }

    /*==========================================================
                    10. scroll view function
    ======================================================================*/
    $.fn.scrollView = function () {
        return this.each(function () {
            $('html, body').animate({
                scrollTop: $(this).offset().top
            }, 1000);
        });
    }

    /*==========================================================
                    11. select function
    ======================================================================*/
    $.fn.mySelect = function (options) {
        let $this = $(this),
            numberOfOptions = $(this).children('option');

        $this.addClass('select-hidden');
        $this.wrap('<div class="select"></div>');
        $this.after('<div class="select-styled"></div>');

        let styledSelect = $this.next('.select-styled');
        styledSelect.text($this.children('option').eq(0).text());

        let list = $('<ul />', {
            'class': 'select-options'
        }).insertAfter(styledSelect);

        for (let i = 0; i < numberOfOptions.length; i++) {
            $('<li />', {
                text: $this.children('option').eq(i).text(),
                rel: $this.children('option').eq(i).val()
            }).appendTo(list);
        }

        let listItems = list.children('li');

        styledSelect.on('click', function (e) {
            e.stopPropagation();
            $('.select-styled.active').not(this).each(function () {
                $(this).removeClass('active').next('.select-options').fadeIn();
            });
            $(this).toggleClass('active').next('.select-options').toggle();
            $(this).parent().toggleClass('focus');
        });

        listItems.on('click', function (e) {
            e.stopPropagation();
            styledSelect.text($(this).text()).removeClass('active');
            $this.val($(this).attr('rel'));
            list.hide();
            if ($(this).parent().parent().hasClass('focus')) {
                $(this).parent().parent().removeClass('focus');
            }
        });

        $(document).on('click', function () {
            styledSelect.removeClass('active');
            list.hide();
        });
    }

    $.fn.myChart = function (options) {
        var settings = $.extend({
            barColor: '',
            scaleColor: 'transparent',
            trackColor: '#f9f9f9',
            lineCap: 'round',
            size: 160,
            lineWidth: 10,
        }, options);

        return this.easyPieChart({
            barColor: settings.barColor,
            scaleColor: settings.scaleColor,
            trackColor: settings.trackColor,
            lineCap: settings.lineCap,
            size: settings.size,
            lineWidth: settings.lineWidth
        });
    }

    function stickyHeader() {
        let mainheader = $('.nav-sticky'),
            height = mainheader.outerHeight(),
            scroll = $(document).scrollTop();
        $(window).on('load', function () {
            if ($(document).scrollTop() > height) {
                if (mainheader.hasClass('sticky-header')) {
                    mainheader.removeClass('sticky-header');
                } else {
                    mainheader.addClass('sticky-header');
                }
            }
        })
        $(window).on('scroll', function () {
            let scrolled = $(document).scrollTop(),
                header = $('.sticky-header');
            if (scrolled > scroll) {
                header.addClass('sticky');
            } else {
                header.removeClass('sticky');
            }
            if (scrolled === 0) {
                mainheader.removeClass('sticky-header');
            } else {
                mainheader.addClass('sticky-header');
            }
            scroll = $(document).scrollTop();
        });
    }

    $(window).on('load', function () {

        // parallax init
        initparallax();

        /* sticky header init */
        stickyHeader();

        /*=============================================================
                 12. case portfolio grid
        =========================================================================*/
        if ($('.cases-grid').length > 0) {
            var $container = $('.cases-grid'),
                colWidth = function () {
                    var w = $container.width(),
                        columnNum = 1,
                        columnWidth = 0;
                    if (w > 1200) {
                        columnNum = 3;
                    } else if (w > 900) {
                        columnNum = 3;
                    } else if (w > 600) {
                        columnNum = 3;
                    } else if (w > 450) {
                        columnNum = 2;
                    } else if (w > 385) {
                        columnNum = 1;
                    }
                    columnWidth = Math.floor(w / columnNum);
                    $container.find('.cases-grid-item').each(function () {
                        var $item = $(this),
                            multiplier_w = $item.attr('class').match(/cases-grid-item-w(\d)/),
                            multiplier_h = $item.attr('class').match(/cases-grid-item-h(\d)/),
                            width = multiplier_w ? columnWidth * multiplier_w[1] : columnWidth,
                            height = multiplier_h ? columnWidth * multiplier_h[1] * 0.4 - 12 : columnWidth * 0.5;
                        $item.css({
                            width: width
                            //height: height
                        });
                    });
                    return columnWidth;
                },
                isotope = function () {
                    $container.isotope({
                        resizable: false,
                        itemSelector: '.cases-grid-item',
                        masonry: {
                            columnWidth: colWidth(),
                            gutterWidth: 3
                        }
                    });
                };
            isotope();
            $(window).on('resize', isotope);
            var $optionSets = $('.filter-button-wraper .option-set'),
                $optionLinks = $optionSets.find('a');
            $optionLinks.on('click', function () {
                var $this = $(this);
                var $optionSet = $this.parents('.option-set');
                $optionSet.find('.selected').removeClass('selected');
                $this.addClass('selected');
                // make option object dynamically, i.e. { filter: '.my-filter-class' }
                var options = {},
                    key = $optionSet.attr('data-option-key'),
                    value = $this.attr('data-option-value');
                // parse 'false' as false boolean
                value = value === 'false' ? false : value;
                options[key] = value;
                if (key === 'layoutMode' && typeof changeLayoutMode === 'function') {
                    // changes in layout modes need extra logic
                    changeLayoutMode($this, options)
                } else {
                    // creativewise, apply new options
                    $container.isotope(options);
                }
                return false;
            });
        }

        /* content to center */
        contentToCenter();

        /* set logo */
        setLogo();

        // equal height
        equalHeight();

        // set width
        setWidth();

        /*==========================================================
                    13. preloader
        ======================================================================*/
        $('#preloader').addClass('loaded');


    }); // END load Function

    $(document).ready(function () {

        initparallax();

        /* content to center */
        contentToCenter();

        // equal height
        equalHeight();

        // set width
        setWidth();

        /* sticky header init */
        stickyHeader();

        /*==========================================================
                    14. preloader close button
        ======================================================================*/
        $('.preloader-btn').on('click', function (e) {
            e.preventDefault();
            $('#preloader').addClass('loaded');
        });

        /*==========================================================
                15. mega navigation menu init
        ======================================================================*/
        $(document).ready(function () {
            // Инициализация плагина
            if ($('.xs-menus').length > 0) {
                $('.xs-menus').xs_nav({
                    mobileBreakpoint: 992
                });
            }

            // Обработка кликов по ссылкам меню
            $('.single-page-menu li a').on('click', function (event) {
                event.preventDefault();

                var target = $(this.hash);
                target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');

                if (target.length) {
                    $('html, body').animate({
                        scrollTop: target.offset().top
                    }, 1000, function () {
                        // Этот код выполнится после завершения анимации прокрутки
                        var $panel = $('.nav-overlay-panel');
                        var $menuWrapper = $('.nav-menus-wrapper');

                        if ($menuWrapper.hasClass('nav-menus-wrapper-open')) {
                            $menuWrapper.removeClass('nav-menus-wrapper-open');
                        }

                        if ($panel.css('display') === 'block') {
                            $panel.css('display', 'none');
                        }

                        if ($('body').hasClass('no-scroll')) {
                            $('body').removeClass('no-scroll');
                        }
                    });
                }
            });
        });


        // $(document).ready(function () {
        //     // Инициализация плагина
        //     if ($('.xs-menus').length > 0) {
        //         $('.xs-menus').xs_nav({
        //             mobileBreakpoint: 992
        //         }, {
        //             passive: true
        //         });
        //     }
        //
        //     // Обработка кликов по ссылкам меню
        //     $('.single-page-menu li a').on('click', function (event) {
        //         event.preventDefault();
        //
        //         var target = $(this.hash);
        //         target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
        //
        //         if (target.length) {
        //             $('html, body').animate({
        //                 scrollTop: target.offset().top
        //             }, 1000);
        //         }
        //
        //         // Закрытие меню и панели
        //         var $panel = $('.nav-overlay-panel');
        //         var $menuWrapper = $('.nav-menus-wrapper');
        //
        //         if ($menuWrapper.hasClass('nav-menus-wrapper-open')) {
        //             $menuWrapper.removeClass('nav-menus-wrapper-open');
        //         }
        //
        //         if ($panel.css('display') === 'block') {
        //             $panel.css('display', 'none');
        //         }
        //
        //         if ($('body').hasClass('no-scroll')) {
        //             $('body').removeClass('no-scroll');
        //         }
        //     });
        // });

        // if ($('.xs-menus').length > 0) {
        // 	$('.xs-menus').xs_nav({
        // 		mobileBreakpoint: 992,
        // 	},
        // 	{
        // 		passive: true
        // 	});
        // }
        //
        // if ($('.single-page-menu li a').length > 0) {
        // 	$('.single-page-menu li a').on('click', function() {
        // 		if (location.pathname.replace(/^\//,'') == this.pathname.replace(/^\//,'')
        // 			|| location.hostname == this.hostname) {
        //
        // 			var target = $(this.hash);
        // 			target = target.length ? target : $('[name=' + this.hash.slice(1) +']');
        // 			   if (target.length) {
        // 				 $('html,body').animate({
        // 					 scrollTop: target.offset().top
        // 				}, 1000);
        // 				return false;
        // 			}
        // 		}
        // 	});
        // 	$('.single-page-menu li a').on('click', function () {
        // 		var panel = $('.nav-overlay-panel'),
        // 			menuWraper = $('.nav-menus-wrapper');
        //
        // 		if (menuWraper.hasClass('nav-menus-wrapper-open')) {
        // 			menuWraper.removeClass('nav-menus-wrapper-open')
        // 		}
        //
        // 		if (panel.css('display') === 'block') {
        // 			panel.css('display', 'none')
        // 		}
        // 		if ($('body').hasClass('no-scroll')) {
        // 			$('body').removeClass('no-scroll')
        // 		}
        // 	});
        // }

        /*==========================================================
                    16. contact form init
        ======================================================================*/

        $(document).on('submit', '#xs-contact-form', function (event) {
            event.preventDefault(); /* Act on the event */

            /* declare a variable */
            var xs_contact_name = $('#xs_contact_name'),
                xs_contact_email = $('#xs_contact_email'),
                xs_contact_phone = $('#xs_contact_phone'),
                xs_contact_subject = $('#xs_contact_subject'),
                x_contact_massage = $('#x_contact_massage'),
                xs_contact_submit = $('#xs_contact_submit'),
                xs_contact_error = false;

            /* remove success massage */
            $('.xpeedStudio_success_message').remove();

            /* xs_contact_name */
            if (xs_contact_name.val().trim() === '') {
                xs_contact_name.addClass('invaild');
                xs_contact_error = true;
                xs_contact_name.focus();
                return false;
            } else {
                xs_contact_name.removeClass('invaild');
            }

            /* xs_contact_email */
            if (xs_contact_email.val().trim() === '') {
                xs_contact_email.addClass('invaild');
                xs_contact_error = true;
                xs_contact_email.focus();
                return false;
            } else if (!email_pattern(xs_contact_email.val().toLowerCase())) {
                xs_contact_email.addClass('invaild');
                xs_contact_error = true;
                xs_contact_email.focus();
                return false;
            } else {
                xs_contact_email.removeClass('invaild');
            }

            /* xs_contact_phone */
            if (xs_contact_phone.val().trim() === '') {
                xs_contact_phone.addClass('invaild');
                xs_contact_error = true;
                xs_contact_phone.focus();
                return false;
            } else {
                xs_contact_phone.removeClass('invaild');
            }

            /* xs_contact_subject */
            if (xs_contact_subject.val().trim() === '') {
                xs_contact_subject.addClass('invaild');
                xs_contact_error = true;
                xs_contact_subject.focus();
                return false;
            } else {
                xs_contact_subject.removeClass('invaild');
            }

            /* x_contact_massage  */
            if (x_contact_massage.val().trim() === '') {
                x_contact_massage.addClass('invaild');
                xs_contact_error = true;
                x_contact_massage.focus();
                return false;
            } else {
                x_contact_massage.removeClass('invaild');
            }

            /* ajax request */
            if (xs_contact_error === false) {
                xs_contact_submit.before().hide().fadeIn();
                $.ajax({
                    type: "POST",
                    url: "assets/php/contact-form.php",
                    data: {
                        'xs_contact_name': xs_contact_name.val(),
                        'xs_contact_email': xs_contact_email.val(),
                        'xs_contact_phone': xs_contact_phone.val(),
                        'x_contact_massage': x_contact_massage.val(),
                        'xs_contact_subject': xs_contact_subject.val(),
                    },
                    success: function (result) {
                        xs_contact_submit.after('<p class="xpeedStudio_success_message">' + result + '</p>').hide().fadeIn();

                        setTimeout(() => {
                            $(".xpeedStudio_success_message").fadeOut(1000, function () {
                                $(this).remove();
                            });
                        }, 5000);

                        $('#xs-contact-form')[0].reset();
                    }
                });
            }
        });


        /*==========================================================
                17. video popup init
        ======================================================================*/
        if ($('.xs-video-popup').length > 0) {
            $('.xs-video-popup').magnificPopup({
                disableOn: 700,
                type: 'iframe',
                mainClass: 'mfp-fade',
                removalDelay: 160,
                preloader: false,
                fixedContentPos: false
            });
        }

        /*==========================================================
             18. Side Offset cart menu open
        ======================================================================*/
        if ($('.offset-side-bar').length > 0) {
            $('.offset-side-bar').on('click', function (e) {
                e.preventDefault();
                e.stopPropagation();
                $('.cart-group').addClass('isActive');
            });
        }
        if ($('.close-side-widget').length > 0) {
            $('.close-side-widget').on('click', function (e) {
                e.preventDefault();
                $('.cart-group').removeClass('isActive');
            });
        }
        if ($('.navSidebar-button').length > 0) {
            $('.navSidebar-button').on('click', function (e) {
                e.preventDefault();
                e.stopPropagation();
                $('.info-group').addClass('isActive');
            });
        }
        if ($('.close-side-widget').length > 0) {
            $('.close-side-widget').on('click', function (e) {
                e.preventDefault();
                $('.info-group').removeClass('isActive');
            });
        }
        $('body').on('click', function (e) {
            $('.info-group').removeClass('isActive');
            $('.cart-group').removeClass('isActive');
        });
        $('.xs-sidebar-widget').on('click', function (e) {
            e.stopPropagation();
        });


        /*=============================================================
                 19. right click , ctrl+u and ctrl+shift+i disabled
        =========================================================================*/
        // $('body').on('contextmenu', function (e) {
        // 	// alert('right click disabled');
        // 	e.preventDefault();
        // 	e.stopPropagation();
        // 	return false;
        // });
        // $(document).on('keydown', function(e) {
        // 	if (
        // 			(e.ctrlKey && (e.keyCode == 85)) ||
        // 			(e.ctrlKey && (e.shiftKey && e.keyCode == 73)) ||
        // 			(e.ctrlKey && (e.shiftKey && e.keyCode == 75))
        // 			) {
        // 		return false;
        // 	} else {
        // 		return true;
        // 	}
        // })

        /*=============================================================
                 20. modal popup
        =========================================================================*/
        if ($('.xs-modal-popup').length > 0) {
            $('.xs-modal-popup').magnificPopup({
                type: 'inline',
                fixedContentPos: false,
                fixedBgPos: true,
                overflowY: 'auto',
                closeBtnInside: false,
                callbacks: {
                    beforeOpen: function () {
                        this.st.mainClass = "my-mfp-slide-bottom xs-promo-popup";
                    }
                }
            });
        }

        /*=============================================================
                 21. img default behavior off and dragable false
        =========================================================================*/
        if ($('img').length > 0) {
            $('img').each(function () {
                $(this).attr('draggable', 'false');
                $(this).on('mousedown', function (event) {
                    if (event.preventDefault) {
                        event.preventDefault()
                    }
                })
            });
        }

        /*=============================================================
                 22. subscribe form
        =========================================================================*/
        if ($('.subscribe-form').length > 0) {
            $('.subscribe-form').ajaxChimp({
                url: 'https://facebook.us8.list-manage.com/subscribe/post?u=85f515a08b87483d03fee7755&amp;id=66389dc38b'
            });
        }

        /*=============================================================
                 23. wow function init
        =========================================================================*/
        $(function () {
            var wow = new WOW({
                boxClass: 'wow',
                animateClass: 'animated',
                offset: 0,
                mobile: false,
                live: true,
                scrollContainer: null,
            });
            wow.init();
        });

        /*=============================================================
                 24. current page add class active on a
        =========================================================================*/
        let url = window.location.pathname,
            activePage = url.substr(url.lastIndexOf('/') + 1);
        $('.xs-menus .nav-menu li a').each(function (e, i) {
            var currentPage = this.href.substr(this.href.lastIndexOf('/') + 1);
            if (activePage == currentPage) {
                $([i]).removeClass("active");
                if ($([i]).parents().closest('.nav-submenu').parent('li')) {
                    $([i]).parents().closest('.nav-submenu').parent('li').removeClass('active')
                }
                $([i]).parent().removeClass('active');
            }
        });

        /*=============================================================
                 25. banner slider
        =========================================================================*/
        if ($('.banner-slider').length > 0) {
            $('.banner-slider').myOwl({
                animateOut: 'fadeOut',
                animateIn: 'fadeIn'
            });
        }

        /*=============================================================
                    26. tab swipe indicator
        =========================================================================*/
        if ($('.tab-swipe').length > 0) {
            $('.tab-swipe').append('<li class="indicator"></li>');
            if ($('.tab-swipe li a').hasClass('active')) {
                let cLeft = $('.tab-swipe li a.active').position().left + 'px',
                    cWidth = $('.tab-swipe li a.active').css('width');
                $('.indicator').css({
                    left: cLeft,
                    width: cWidth
                })
            }
            $('.tab-swipe li a').on('click', function () {
                $('.tab-swipe li a').removeClass('isActive');
                $(this).addClass('isActive');
                let cLeft = $('.tab-swipe li a.isActive').position().left + 'px',
                    cWidth = $('.tab-swipe li a.isActive').css('width');
                $('.indicator').css({
                    left: cLeft,
                    width: cWidth
                })
            });
        }

        /*=============================================================
                 27. testimonial slider 1
        =========================================================================*/
        if (($('#sync1') && $('#sync2')).length > 0) {
            let sync1 = $("#sync1");
            let sync2 = $("#sync2");
            let slidesPerPage = 3; //globaly define number of elements per page
            let syncedSecondary = true;

            sync1.owlCarousel({
                items: 1,
                slideSpeed: 2000,
                nav: false,
                autoplay: true,
                dots: true,
                loop: true,
                responsiveRefreshRate: 200,
            }).on('changed.owl.carousel', syncPosition);

            sync2
                .on('initialized.owl.carousel', function () {
                    sync2.find(".owl-item").eq(0).addClass("current");
                })
                .owlCarousel({
                    items: slidesPerPage,
                    dots: true,
                    nav: false,
                    autoplay: true,
                    smartSpeed: 200,
                    slideSpeed: 500,
                    slideBy: slidesPerPage, //alternatively you can slide by 1, this way the active slide will stick to the first item in the second carousel
                    responsiveRefreshRate: 100,
                    responsive: {
                        0: {
                            items: 1
                        },
                        768: {
                            items: 2
                        },
                        1024: {
                            items: slidesPerPage
                        }
                    }
                }).on('changed.owl.carousel', syncPosition2);

            function syncPosition(el) {
                //if you set loop to false, you have to restore this next line
                //let current = el.item.index;

                //if you disable loop you have to comment this block
                let count = el.item.count - 1;
                let current = Math.round(el.item.index - (el.item.count / 2) - .5);

                if (current < 0) {
                    current = count;
                }
                if (current > count) {
                    current = 0;
                }

                //end block

                sync2
                    .find(".owl-item")
                    .removeClass("current")
                    .eq(current)
                    .addClass("current");
                let onscreen = sync2.find('.owl-item.active').length - 1;
                let start = sync2.find('.owl-item.active').first().index();
                let end = sync2.find('.owl-item.active').last().index();

                if (current > end) {
                    sync2.data('owl.carousel').to(current, 100, true);
                }
                if (current < start) {
                    sync2.data('owl.carousel').to(current - onscreen, 100, true);
                }
            }

            function syncPosition2(el) {
                if (syncedSecondary) {
                    let number = el.item.index;
                    sync1.data('owl.carousel').to(number, 100, true);
                }
            }

            sync2.on("click", ".owl-item", function (e) {
                e.preventDefault();
                let number = $(this).index();
                sync1.data('owl.carousel').to(number, 300, true);
            });
        }

        /*=============================================================
                 28. testimonial slider 2
        =========================================================================*/
        if (($('#sync3') && $('#sync4')).length > 0) {
            let sync3 = $("#sync3");
            let sync4 = $("#sync4");
            let slidesPerPage = 3; //globaly define number of elements per page
            let syncedSecondary = true;

            sync3.owlCarousel({
                items: 1,
                slideSpeed: 2000,
                nav: false,
                autoplay: true,
                dots: true,
                loop: true,
                responsiveRefreshRate: 200,
            }).on('changed.owl.carousel', syncPosition);

            sync4
                .on('initialized.owl.carousel', function () {
                    sync4.find(".owl-item").eq(0).addClass("current");
                })
                .owlCarousel({
                    items: slidesPerPage,
                    dots: true,
                    nav: false,
                    smartSpeed: 200,
                    autoplay: true,
                    slideSpeed: 500,
                    slideBy: slidesPerPage, //alternatively you can slide by 1, this way the active slide will stick to the first item in the second carousel
                    responsiveRefreshRate: 100,
                    responsive: {
                        0: {
                            items: 1
                        },
                        768: {
                            items: 2
                        },
                        1024: {
                            items: slidesPerPage
                        }
                    }
                }).on('changed.owl.carousel', syncPosition2);

            function syncPosition(el) {
                //if you set loop to false, you have to restore this next line
                //let current = el.item.index;

                //if you disable loop you have to comment this block
                let count = el.item.count - 1;
                let current = Math.round(el.item.index - (el.item.count / 2) - .5);

                if (current < 0) {
                    current = count;
                }
                if (current > count) {
                    current = 0;
                }

                //end block

                sync4
                    .find(".owl-item")
                    .removeClass("current")
                    .eq(current)
                    .addClass("current");
                let onscreen = sync4.find('.owl-item.active').length - 1;
                let start = sync4.find('.owl-item.active').first().index();
                let end = sync4.find('.owl-item.active').last().index();

                if (current > end) {
                    sync4.data('owl.carousel').to(current, 100, true);
                }
                if (current < start) {
                    sync4.data('owl.carousel').to(current - onscreen, 100, true);
                }
            }

            function syncPosition2(el) {
                if (syncedSecondary) {
                    let number = el.item.index;
                    sync3.data('owl.carousel').to(number, 100, true);
                }
            }

            sync4.on("click", ".owl-item", function (e) {
                e.preventDefault();
                let number = $(this).index();
                sync3.data('owl.carousel').to(number, 300, true);
            });
        }

        /*=============================================================
                 29. testimonial slider 3
        =========================================================================*/
        if (($('#sync5') && $('#sync6')).length > 0) {
            let sync5 = $("#sync5");
            let sync6 = $("#sync6");
            let slidesPerPage = 3; //globaly define number of elements per page
            let syncedSecondary = true;

            sync5.owlCarousel({
                items: 1,
                slideSpeed: 2000,
                nav: false,
                autoplay: true,
                dots: true,
                loop: true,
                responsiveRefreshRate: 200,
            }).on('changed.owl.carousel', syncPosition);

            sync6
                .on('initialized.owl.carousel', function () {
                    sync6.find(".owl-item").eq(0).addClass("current");
                })
                .owlCarousel({
                    items: slidesPerPage,
                    dots: true,
                    nav: false,
                    smartSpeed: 200,
                    autoplay: true,
                    slideSpeed: 500,
                    slideBy: slidesPerPage, //alternatively you can slide by 1, this way the active slide will stick to the first item in the second carousel
                    responsiveRefreshRate: 100,
                    responsive: {
                        0: {
                            items: 1
                        },
                        768: {
                            items: 2
                        },
                        1024: {
                            items: slidesPerPage
                        }
                    }
                }).on('changed.owl.carousel', syncPosition2);

            function syncPosition(el) {
                //if you set loop to false, you have to restore this next line
                //var current = el.item.index;

                //if you disable loop you have to comment this block
                let count = el.item.count - 1;
                let current = Math.round(el.item.index - (el.item.count / 2) - .5);

                if (current < 0) {
                    current = count;
                }
                if (current > count) {
                    current = 0;
                }

                //end block

                sync6
                    .find(".owl-item")
                    .removeClass("current")
                    .eq(current)
                    .addClass("current");
                let onscreen = sync6.find('.owl-item.active').length - 1;
                let start = sync6.find('.owl-item.active').first().index();
                let end = sync6.find('.owl-item.active').last().index();

                if (current > end) {
                    sync6.data('owl.carousel').to(current, 100, true);
                }
                if (current < start) {
                    sync6.data('owl.carousel').to(current - onscreen, 100, true);
                }
            }

            function syncPosition2(el) {
                if (syncedSecondary) {
                    let number = el.item.index;
                    sync5.data('owl.carousel').to(number, 100, true);
                }
            }

            sync6.on("click", ".owl-item", function (e) {
                e.preventDefault();
                let number = $(this).index();
                sync5.data('owl.carousel').to(number, 300, true);
            });
        }

        /*=============================================================
                 30. testimonial slider 4
        =========================================================================*/
        if ($('.testimonial-slider').length > 0) {
            $('.testimonial-slider').myOwl({
                dots: true
            });
        }

        /*=============================================================
                 31. gallery slider
        =========================================================================*/
        if ($('.gallery-slider').length > 0) {
            $('.gallery-slider').myOwl({
                nav: true,
                navText: ['<i class="icon icon-left-arrows"></i>', '<i class="icon icon-right-arrow"></i>']
            });
        }

        /*=============================================================
                 32. pie chart init
        =========================================================================*/
        var barColors = ['#50e2c2', '#ffac42', '#9013fd'];
        var chart = $('.chart');

        function chartInit() {
            for (let i = 0; i < $('.single-piechart').length; i++) {
                $(chart[i]).myChart({
                    barColor: barColors[i]
                })
            }
        }

        chart.each(function () {
            var value = $(this).attr('data-percent');
            $(this).find('.chart-content').append('<span class="chart-value">' + value + '%</span>');
        })
        var chartValue = $('.chart-value');
        for (let i = 0; i < barColors.length; i++) {
            $(chartValue[i]).css('color', barColors[i]);
        }

        /*==========================================================
                33. number counter and skill bar animation
        =======================================================================*/
        var number_percentage = $(".number-percentage");

        function animateProgressBar() {
            number_percentage.each(function () {
                $(this).animateNumbers($(this).attr("data-value"), true, parseInt($(this).attr("data-animation-duration"), 10));
            });
        }

        /*=============================================================
                 34. waypoint int
        =========================================================================*/
        if ($('.waypoint-tigger').length > 0) {
            var waypoint = new Waypoint({
                element: document.getElementsByClassName('waypoint-tigger'),
                handler: function (direction) {
                    animateProgressBar();
                    chartInit();
                },
                offset: '50%'
            });
        }

        /*==========================================================
                35. skill bar and number counter
        =======================================================================*/
        $.fn.animateNumbers = function (stop, commas, duration, ease) {
            return this.each(function () {
                var $this = $(this);
                var start = parseInt($this.text().replace(/,/g, ""), 10);
                commas = (commas === undefined) ? true : commas;
                $({
                    value: start
                }).animate({
                    value: stop
                }, {
                    duration: duration == undefined ? 500 : duration,
                    easing: ease == undefined ? "swing" : ease,
                    step: function () {
                        $this.text(Math.floor(this.value));
                        if (commas) {
                            $this.text($this.text().replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,"));
                        }
                    },
                    complete: function () {
                        if (parseInt($this.text(), 10) !== stop) {
                            $this.text(stop);
                            if (commas) {
                                $this.text($this.text().replace(/(\d)(?=(\d\d\d)+(?!\d))/g, "$1,"));
                            }
                        }
                    }
                });
            });
        };

        /*=============================================================
                 36. go to current section
        =========================================================================*/
        $('body').on('click', '.next-step[href^="#"]', function (event) {
            event.preventDefault();
            var target = $(this).attr('href');
            if ($(target).length > 0) {
                $('html, body').animate({
                    scrollTop: $(target).offset().top
                }, 1000);
            } else {
                console.warn('Element ' + target + ' does not exist');
            }
        });

        /*=============================================================
                 37. select init
        =========================================================================*/
        if ($('.xs-select').length > 0) {
            $('.xs-select').mySelect();
        }

        /*=============================================================
                 38. custom number init
        =========================================================================*/
        if ($('.custom_number').length > 0) {
            $('.custom_number').customNumber({
                plusIcon: '<i class="icon icon-up-arrow2"></i>',
                minusIcon: '<i class="icon icon-down-arrow2"></i>'
            });
        }

        /*=============================================================
                 39. floating btn
        =========================================================================*/
        if ($(".btn-floating").length > 0) {
            var content = $('.floating-icons-list');

            content.addClass('hidden');

            $('.btn-floating').each(function () {
                $(this).on('click', function (e) {
                    e.preventDefault();

                    $(this).next().toggleClass("open");
                    $(this).next().toggleClass("hidden");

                    if ($(this).hasClass('active')) {
                        $(this).removeClass('active');
                    } else {
                        $(this).addClass('active');
                    }
                });
            });
        }

        /*=============================================================
                 40. product slider and about slider
        =========================================================================*/
        if ($('.product-slider, .about-slider').length > 0) {
            $('.product-slider, .about-slider').myOwl({
                dots: true
            })
        }

        /*=============================================================
                 41. scrollview init
        =========================================================================*/
        $('.comment-reply-link').on('click', function (event) {
            event.preventDefault();
            $('#comment-form').scrollView();
        });

        /*=============================================================
                 42. rate graph
        =========================================================================*/
        if ($('.rate-graph').length > 0) {
            $('.rate-graph').each(function () {
                if ($(this).find('.rate-graph-bar').attr('data-percent') <= 100) {
                    $(this).find('.rate-graph-bar').css({
                        width: $(this).find('.rate-graph-bar').attr('data-percent') + '%',
                    });
                } else {
                    $(this).find('.rate-graph-bar').css({
                        width: 100 + '%',
                    });
                }
            });
        }

        /*=============================================================
                 43. case study slideer
        =========================================================================*/
        if ($('.case-study-slider').length > 0) {
            $('.case-study-slider').myOwl({
                items: 3,
                dots: true,
                margin: 30,
                stagePadding: 15,
                responsive: {
                    0: {
                        items: 1
                    },
                    768: {
                        items: 2
                    },
                    1024: {
                        items: 3
                    }
                }
            });
        }

        /*=============================================================
                 44. rev slider init
        =========================================================================*/
        if ($('#rev_slider_6_1').length > 0) {
            var revapi6,
                tpj;
            (function () {
                if (!/loaded|interactive|complete/.test(document.readyState)) document.addEventListener("DOMContentLoaded", onLoad); else onLoad();

                function onLoad() {
                    if (tpj === undefined) {
                        tpj = jQuery;
                        if ("off" == "on") tpj.noConflict();
                    }
                    if (tpj("#rev_slider_6_1").revolution == undefined) {
                        revslider_showDoubleJqueryError("#rev_slider_6_1");
                    } else {
                        revapi6 = tpj("#rev_slider_6_1").show().revolution({
                            sliderType: "standard",
                            jsFileLocation: "",
                            sliderLayout: "fullwidth",
                            dottedOverlay: "none",
                            delay: 9000,
                            navigation: {
                                keyboardNavigation: "off",
                                keyboard_direction: "horizontal",
                                mouseScrollNavigation: "off",
                                mouseScrollReverse: "default",
                                onHoverStop: "off",
                                arrows: {
                                    style: "gyges",
                                    enable: true,
                                    hide_onmobile: false,
                                    hide_onleave: false,
                                    tmp: '',
                                    left: {
                                        h_align: "left",
                                        v_align: "center",
                                        h_offset: 20,
                                        v_offset: 0
                                    },
                                    right: {
                                        h_align: "right",
                                        v_align: "center",
                                        h_offset: 20,
                                        v_offset: 0
                                    }
                                }
                            },
                            responsiveLevels: [1240, 1024, 778, 480],
                            visibilityLevels: [1240, 1024, 778, 480],
                            gridwidth: [1240, 1024, 778, 480],
                            gridheight: [868, 768, 960, 720],
                            lazyType: "none",
                            minHeight: "850",
                            parallax: {
                                type: "mouse",
                                origo: "enterpoint",
                                speed: 400,
                                speedbg: 0,
                                speedls: 0,
                                levels: [5, 10, 15, 20, 25, 30, 35, 40, 45, 46, 47, 48, 49, 50, 51, 55],
                            },
                            shadow: 0,
                            spinner: "spinner0",
                            stopLoop: "off",
                            stopAfterLoops: -1,
                            stopAtSlide: -1,
                            shuffle: "off",
                            autoHeight: "off",
                            disableProgressBar: "on",
                            hideThumbsOnMobile: "off",
                            hideSliderAtLimit: 0,
                            hideCaptionAtLimit: 0,
                            hideAllCaptionAtLilmit: 0,
                            debugMode: false,
                            fallbacks: {
                                simplifyAll: "off",
                                nextSlideOnWindowFocus: "off",
                                disableFocusListener: false,
                            }
                        });
                    }
                    ; /* END OF revapi call */
                }; /* END OF ON LOAD FUNCTION */
            }()); /* END OF WRAPPING FUNCTION */
        }

    }); // end ready function

    $(window).on('scroll', function () {
        if ($('.working-process-anim').length > 0) {
            var scrollTop = $(window).scrollTop(),
                elementOffset = $('.working-process-anim').offset().top,
                elementHeight = $('.working-process-anim').outerHeight(true);
            if (!(elementOffset < screenTop)) {
                $('.working-process-anim').removeClass('current-section');
            }
            if (elementOffset <= (scrollTop + 150)) {
                $('.working-process-anim').addClass('current-section');
                if (!((elementHeight + elementOffset) > (scrollTop + 200))) {
                    $('.working-process-anim').removeClass('current-section');
                }
            }
        }
    }); // END Scroll Function

    $(window).on('resize', function () {

        /* content to center */
        contentToCenter();

        /* set logo */
        setLogo();

        // equal height
        equalHeight();

        // set width
        setWidth();
    }); // End Resize

    /*==========================================================
                45. XpeedStudio Maps
    ======================================================================*/
    if ($('.map').length > 0) {
        ymaps.ready(init);

        function init() {
            var mapOptions = {
                center: [46.680868, 38.279200], // Координаты адреса
                zoom: 12 // Масштаб карты
            };

            var maps = document.getElementsByClassName('map');
            for (var i = 0; i < maps.length; i++) {
                var map = new ymaps.Map(maps[i], mapOptions);

                var placemark = new ymaps.Placemark(
                    [46.680868, 38.279200],
                    {
                        iconCaption: 'MDigital', // Название метки
                        balloonContent: '353680 г.Ейск, Россия, Мичурина ул., 16/1, Этаж 2'
                    },
                    {
                        preset: 'islands#blueDotIconWithCaption', // Стиль метки
                        iconCaptionMaxWidth: '200' // Максимальная ширина названия метки
                    }
                );

                map.geoObjects.add(placemark);
            }
        }
    }

})(jQuery);

/*==========================================================
			46. submit_question(contact-form, xs-contact-form)
======================================================================*/
$(document).ready(function () {
    $('.contact-form').on('submit', function (event) {
        event.preventDefault(); // Предотвращаем отправку формы по умолчанию
        // Получаем значения полей формы
        var email = $('#email').val();
        var message = $('#message').val();

        // Проверяем, заполнены ли поля
        if (email.trim() === '' || message.trim() === '') {
            // Если одно из полей пустое, показываем сообщение об ошибке
            $('#question-message').text('Пожалуйста, заполните все поля.').addClass('error-message response-message');
            hideMessageAfterDelay('#question-message'); // Скрываем сообщение через время по умолчанию
            return; // Прерываем выполнение функции
        }

        var formData = $(this).serialize(); // Получаем данные формы

        $.ajax({
            url: $(this).attr('action'),
            type: $(this).attr('method'),
            data: formData,
            dataType: 'json',
            success: function (data) {
                // Вставляем ответ на страницу
                $('#question-message').text(data.message).addClass('success-message response-message');
                hideMessageAfterDelay('#question-message'); // Скрываем сообщение через время по умолчанию
                $('.contact-form')[0].reset();
            },
            error: function (xhr, status, error) {
                console.error('Ошибка:', error);
                $('#question-message').text('Произошла ошибка при отправке вопроса.');
                hideMessageAfterDelay('#question-message'); // Скрываем сообщение через время по умолчанию
            }
        });
    });
});

$(document).ready(function () {
    $('.xs-contact-form').on('submit', function (event) {
        event.preventDefault(); // Предотвращаем отправку формы по умолчанию
        // Получаем значения полей формы
        var name = $('#name').val();
        var email = $('#email').val();
        var phone = $('#phone').val();
        var subject = $('#subject').val();
        var message = $('#message').val();

        // Проверяем, заполнены ли поля
        if (name.trim() === '' || email.trim() === '' || message.trim() === '') {
            // Если одно из полей пустое, показываем сообщение об ошибке
            $('#xs-form-message').text('Пожалуйста, заполните все поля.').addClass('error-message response-message');
            hideMessageAfterDelay('#xs-form-message'); // Скрываем сообщение через время по умолчанию
            return; // Прерываем выполнение функции
        }

        // Проверяем формат телефона
        var phoneRegex = /^\+?7?\d{9,15}$/;
        if (!phoneRegex.test(phone)) {
            // Если формат телефона некорректен, показываем сообщение об ошибке
            $('#xs-form-message').text('Пожалуйста, введите корректный номер телефона.').addClass('error-message response-message');
            hideMessageAfterDelay('#xs-form-message'); // Скрываем сообщение через время по умолчанию
            return; // Прерываем выполнение функции
        }

        var formData = $(this).serialize(); // Получаем данные формы

        $.ajax({
            url: $(this).attr('action'),
            type: $(this).attr('method'),
            data: formData,
            dataType: 'json',
            success: function (data) {
                // Вставляем ответ на страницу
                $('#xs-form-message').text(data.message).addClass('success-message response-message');
                hideMessageAfterDelay('#xs-form-message'); // Скрываем сообщение через время по умолчанию
                $('.xs-contact-form')[0].reset();
            },
            error: function (xhr, status, error) {
                console.error('Ошибка:', error);
                $('#xs-form-message').text('Произошла ошибка при отправке формы.');
                hideMessageAfterDelay('#xs-form-message'); // Скрываем сообщение через время по умолчанию
            }
        });
    });
});

/*==========================================================
			47. subscribe_question
======================================================================*/
$(document).ready(function () {
    $('#subscribe-form').submit(function (e) {
        e.preventDefault();

        var form = $(this); // Сохраняем ссылку на форму
        var url = form.data('url'); // Получаем URL из атрибута data-url

        $.ajax({
            type: 'POST',
            url: url,
            data: form.serialize(),
            success: function (response) {
                // Очищаем форму
                form.trigger('reset');

                // Обновляем содержимое поля вывода сообщений пользователю
                $('#subscribe-message').text(response.message).addClass('success-message response-message');
                hideMessageAfterDelay('#subscribe-message'); // Скрываем сообщение через время по умолчанию
            },
            error: function (response) {
                // Обновляем содержимое поля вывода сообщений пользователю в случае ошибки
                $('#subscribe-message').text("Произошла ошибка при отправке формы подписки.");
                hideMessageAfterDelay('#subscribe-message'); // Скрываем сообщение через время по умолчанию
            }
        });
    });
});
/*==========================================================
			48. incoming_orders
======================================================================*/
$(document).ready(function () {
    $('.xs-inline-form').on('submit', function (event) {
        event.preventDefault(); // Предотвращаем отправку формы по умолчанию
        // Получаем значения полей формы
        var site = $('#website').val();
        var email = $('#emails').val();

        // Проверяем, заполнены ли поля
        if (site.trim() === '' || email.trim() === '') {
            // Если одно из полей пустое, показываем сообщение об ошибке
            $('#orders-message').text('Пожалуйста, заполните все поля.').addClass('error-message response-message');
            hideMessageAfterDelay('#orders-message'); // Скрываем сообщение через время по умолчанию
            return; // Прерываем выполнение функции
        }

        var formData = $(this).serialize(); // Получаем данные формы

        $.ajax({
            url: $(this).attr('action'),
            type: $(this).attr('method'),
            data: formData,
            dataType: 'json',
            success: function (data) {
                // Вставляем ответ на страницу
                $('#orders-message').text(data.message).addClass('success-message response-message');
                hideMessageAfterDelay('#orders-message'); // Скрываем сообщение через время по умолчанию
                $('.xs-inline-form')[0].reset(); // Очищаем форму
            },
            error: function (xhr, status, error) {
                console.error('Ошибка:', error);
                $('#orders-message').text('Произошла ошибка при отправке запроса.');
                hideMessageAfterDelay('#orders-message'); // Скрываем сообщение через время по умолчанию
            }
        });
    });
});


// Функция для скрытия сообщения после задержки
function hideMessageAfterDelay(selector, delay = 5000) {
    setTimeout(function () {
        $(selector).text('').removeClass('error-message success-message response-message');
    }, delay);
}


// Подтягиваем описание направлений в мобильной версии для services
document.addEventListener('DOMContentLoaded', function () {
    var tabs = document.querySelectorAll('.nav-link');

    // Функция для удаления анимации в мобильной версии
    function removeAnimationOnMobile() {
        if (window.innerWidth < 768) {
            document.querySelectorAll('.tab-pane').forEach(function (pane) {
                pane.classList.remove('fadeInRight');
            });
        }
    }

    // Удаляем анимацию сразу при загрузке страницы в мобильной версии
    removeAnimationOnMobile();

    tabs.forEach(function (tab) {
        tab.addEventListener('click', function (event) {
            if (window.innerWidth < 768) { // Проверка ширины экрана
                // Отключить вертикальную прокрутку
                document.body.style.overflowY = 'hidden';

                // Удаляем анимацию при каждом клике на вкладку в мобильной версии
                removeAnimationOnMobile();

                // Задержка для завершения переключения вкладки
                setTimeout(function () {
                    var targetPaneId = tab.getAttribute('href');
                    var targetElement = document.querySelector(targetPaneId + ' .single-service-preview');

                    if (targetElement) {
                        targetElement.scrollIntoView({behavior: 'smooth', block: 'start'});
                    }

                    // Включить вертикальную прокрутку после завершения анимации
                    setTimeout(function () {
                        document.body.style.overflowY = 'auto';
                    }, 100); // Увеличьте время, если нужно больше для завершения анимации
                }, 300);
            }
        });
    });
});

document.addEventListener('DOMContentLoaded', function () {
    var backToTopButton = document.getElementById('back-to-top');

    window.onscroll = function () {
        if (document.body.scrollTop > 100 || document.documentElement.scrollTop > 100) {
            backToTopButton.style.display = 'block';
        } else {
            backToTopButton.style.display = 'none';
        }
    };

    backToTopButton.onclick = function () {
        window.scrollTo({top: 0, behavior: 'smooth'});
    };
});

document.addEventListener("DOMContentLoaded", function () {
    // Находим чекбокс согласия с политикой конфиденциальности
    var checkbox = document.querySelector("input[name='agree_to_privacy_policy']");

    // Назначаем идентификатор, если чекбокс найден
    if (checkbox) {
        checkbox.setAttribute("id", "agree_to_privacy_policy_checkbox");
    }
});

/* Управление модальным окном консультации */
document.addEventListener('DOMContentLoaded', function () {
    var modal = document.getElementById("consultation-modal");
    var btn = document.getElementById("open-consultation-modal");
    var anotherBtn = document.getElementById("open-another-consultation-modal");
    var span = document.getElementById("close-consultation-modal");
    var form = document.getElementById("consultation-form");
    var mobileMenu = document.querySelector(".nav-menus-wrapper");
    var menuToggleBtn = document.querySelector(".menu-toggle-btn");

    function openModal() {
        if (modal) {
            modal.style.display = "block";
        }

        if (window.innerWidth <= 768 && mobileMenu && mobileMenu.style.display !== "none") {
            mobileMenu.style.display = "none";
            mobileMenu.setAttribute('data-hidden-by-modal', 'true');

            if (menuToggleBtn && mobileMenu.classList.contains('open')) {
                menuToggleBtn.click();
            }
        }
    }

    function closeModal() {
        if (modal) {
            modal.style.display = "none";
        }

        if (window.innerWidth <= 768 && mobileMenu && mobileMenu.getAttribute('data-hidden-by-modal') === 'true') {
            mobileMenu.style.display = "block";
            mobileMenu.removeAttribute('data-hidden-by-modal');
        }
    }

    if (btn) {
        btn.onclick = openModal;
    }

    if (anotherBtn) {
        anotherBtn.onclick = openModal;
    }

    if (span) {
        span.onclick = closeModal;
    }

    window.onclick = function (event) {
        if (event.target === modal) {
            closeModal();
        }
    }

    if (form) {
        form.addEventListener('submit', function (event) {
            event.preventDefault();

            var formData = new FormData(form);

            fetch(form.action, {
                method: form.method,
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    var successMessage = document.createElement('p');
                    successMessage.textContent = 'Спасибо! Мы свяжемся с вами в ближайшее время.';
                    successMessage.style.color = 'green';

                    form.reset();
                    form.innerHTML = '';
                    form.appendChild(successMessage);

                    setTimeout(closeModal, 2000);
                } else {
                    var errorMessage = document.createElement('p');
                    errorMessage.textContent = 'Ошибка: ' + JSON.stringify(data.errors);
                    errorMessage.style.color = 'red';
                    form.appendChild(errorMessage);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    }
});

/* End управления модальным окном консультации */

/*FAQ js start*/
document.addEventListener("DOMContentLoaded", function () {
    const toggles = document.querySelectorAll(".faq-toggle");

    toggles.forEach(toggle => {
        toggle.addEventListener("click", function () {
            const answer = this.closest(".faq-item").querySelector(".faq-answer");
            const icon = this.querySelector(".plus-icon");

            if (answer.style.display === "block") {
                answer.style.display = "none";
                icon.textContent = "+";
            } else {
                answer.style.display = "block";
                icon.textContent = "−";
            }
        });
    });
});
/*FAQ js end*/

/*Cost TG bots START */
document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('costCalculationForm');
    form.addEventListener('submit', function (event) {
        event.preventDefault();

        const formData = new FormData(form);
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        const url = form.getAttribute('data-url');

        fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
            },
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const successMessage = document.getElementById('successMessage');
                    successMessage.querySelector('p').innerText = data.message;
                    successMessage.style.display = 'block';
                    form.style.display = 'none';
                } else {
                    alert(data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Произошла ошибка при отправке формы.');
            });
    });
});
/*Cost TG bots END */

/*Swipe func START*/
$(function () {
    const $carousel = $('#carouselExampleControls'); // Сохраняем jQuery объект в переменную
    let resizeTimer; // Явное объявление переменной
    let maxHeight; // Явное объявление переменной для высоты

    // Инициализация карусели
    $carousel.carousel();

    // Функция для установки высоты карусели
    function setCarouselHeight() {
        if (resizeTimer) {
            clearTimeout(resizeTimer);
        }
        resizeTimer = setTimeout(function () {
            maxHeight = 0; // Инициализация maxHeight с использованием let
            $('.carousel-item').each(function () {
                const $this = $(this); // Сохранение $(this) в переменную
                const itemHeight = $this.outerHeight();
                if (itemHeight > maxHeight) {
                    maxHeight = itemHeight;
                }
            });
            $('.carousel-inner').height(maxHeight);
        }, 100);
    }

    // Установка высоты при загрузке и изменении слайдов
    setCarouselHeight();
    $carousel.on('slid.bs.carousel', setCarouselHeight);

    // Инициализация свайпов для карусели
    $carousel.swipe({
        swipeLeft: function () {
            $carousel.carousel('next');
        },
        swipeRight: function () {
            $carousel.carousel('prev');
        },
        allowPageScroll: "vertical"
    });

    // Обработчик кликов по кнопкам управления
    function handleCarouselControl(event) {
        event.preventDefault();
        const $target = $(event.target);
        if ($target.hasClass('carousel-control-prev')) {
            $carousel.carousel('prev');
        } else if ($target.hasClass('carousel-control-next')) {
            $carousel.carousel('next');
        }
    }

    // Инициализация кнопок управления
    $('.carousel-control-prev, .carousel-control-next, .carousel-indicators li').on('click', handleCarouselControl);
});
/*Swipe func END*/

/* SendResumeForm Start */
$(document).ready(function() {
    $('.open-form').on('click', function(event) {
        event.preventDefault();
        $('#resumeModal').modal('show'); // Открытие модального окна
    });

    $('#resume-form').on('submit', function(event) {
        event.preventDefault(); // Предотвращает стандартную отправку формы
        var formData = new FormData(this); // Собирает данные формы

        $.ajax({
            url: $(this).data('url'), // Используем URL из атрибута data-url
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                $('#form-message').text(response.message).show();
                $('#resume-form')[0].reset(); // Очищает форму
                $('#resumeModal').modal('hide'); // Закрывает модальное окно после успешной отправки
            },
            error: function(xhr) {
                var errors = xhr.responseJSON.errors;
                var errorMessages = '';
                for (var key in errors) {
                    errorMessages += errors[key].join('<br>') + '<br>';
                }
                $('#form-message').html(errorMessages).show();
            }
        });
    });
});

/* SendResumeForm END */
