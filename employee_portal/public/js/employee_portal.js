
$(function () {
  const currentPath = window.location.pathname.replace(/\/+$/, '');
  document.querySelectorAll('.sidebar-nav li a').forEach(link => {
    if (link.getAttribute('href').replace(/\/+$/, '') === currentPath) {
      link.parentElement.classList.add('active');
    }
  });
});
$(document).ready(function () {
  $("#menu-toggle").click(function (e) {
    e.preventDefault();
    $("#wrapper").toggleClass("menuDisplayed");
    let icon = $(this).find("span");
    if ($("#wrapper").hasClass("menuDisplayed")) {
      icon.text("menu_open");
    } else {
      icon.text("menu");
    }
  });

  $(document).on("click", ".module-link", function (e) {
    console.log("Click");
    $('.sidebar-nav li').removeClass('active');
    $(this).parent().addClass('active');
  });


  function loadModule(url) {
    console.log(url)
    $('#dynamic-content').fadeOut(150, function () {
      $.ajax({
        url: url,
        method: 'GET',
        success: function (response) {
          let newContent = $(response).find('#dynamic-content').html();

          $('#dynamic-content').html(newContent).fadeIn(150);

          $(response).find('link[rel="stylesheet"]').each(function () {
            let href = $(this).attr('href');
            if (!$(`link[href="${href}"]`).length) {
              $('<link>', { rel: 'stylesheet', href: href }).appendTo('head');
            }
          });

          let scripts = $(response).find('script[src]').map(function () {
            return $(this).attr('src');
          }).get();

          // TODO: QUITAR ESTO

          loadScriptsSequentially(scripts, function () {
            $(response).find('script:not([src])').each(function () {
              $.globalEval(this.textContent || this.innerText);
            });
          });

          history.pushState(null, '', url);
          attachModuleEvents();
        },
        error: function (xhr, status, error) {
          console.error("Error al cargar el contenido: ", error);
          $('#dynamic-content').fadeIn(150);
        }
      });
    });
  }

  function attachModuleEvents() {
    $('.module-link').off('click').on('click', function (event) {
      event.preventDefault();
      let url = $(this).data('url');
      loadModule(url);
    });
  }

  attachModuleEvents();
});
