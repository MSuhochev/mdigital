document.addEventListener("DOMContentLoaded", function() {
    const cookieConsent = document.querySelector("#cookie-consent");
    const acceptBtn = document.querySelector("#accept-cookies");

    if (!getCookie("cookie_consent")) {
        cookieConsent.style.display = "block";
    } else {
        loadScripts(); // Загружаем скрипты, если куки уже установлены
    }

    acceptBtn.addEventListener("click", function(event) {
        event.preventDefault();

        fetch('/cookie-consent/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({})
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                cookieConsent.style.display = "none";
                document.cookie = "cookie_consent=yes; max-age=" + (365*24*60*60) + "; path=/";
                document.body.style.overflow = '';
                loadScripts(); // Загружаем скрипты после согласия
            }
        });
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function loadScripts() {
        // Загружаем Google Analytics
        // const gaScript = document.createElement('script');
        // gaScript.async = true;
        // gaScript.src = "https://www.googletagmanager.com/gtag/js?id=YOUR_GOOGLE_ANALYTICS_ID";
        // document.head.appendChild(gaScript);
        //
        // gaScript.onload = function() {
        //     window.dataLayer = window.dataLayer || [];
        //     function gtag(){dataLayer.push(arguments);}
        //     gtag('js', new Date());
        //     gtag('config', 'YOUR_GOOGLE_ANALYTICS_ID');
        // };

        // Загружаем Яндекс.Метрику
        const ymScript = document.createElement('script');
        ymScript.type = "text/javascript";
        ymScript.src = "https://mc.yandex.ru/metrika/tag.js";
        document.head.appendChild(ymScript);

        ymScript.onload = function() {
            ym(97577619, "init", {
                clickmap: true,
                trackLinks: true,
                accurateTrackBounce: true,
                webvisor: true
            });
        };
    }
});
